import sys
import time
import logging
import datetime
import configparser
from logging.handlers import TimedRotatingFileHandler

import kafka
import elasticsearch

from ..include import statics
from ..include import protocol_pb2


def kafka_produce(kafka_ip):
    producer: kafka.KafkaProducer = kafka.KafkaProducer(bootstrap_servers=kafka_ip)
    while True:
        produce_protobuf = yield
        future = producer.send('to_agent', produce_protobuf)

        try:
            record_metadata = future.get(timeout=10)
            logger.debug(record_metadata)
        except kafka.KafkaError as kafka_e:
            logger.error(f'Produce Fail! cause {kafka_e}')


def kafka_consume(kafka_ip):
    consumer: kafka.KafkaConsumer = kafka.KafkaConsumer('from_agent',
                                                        bootstrap_servers=kafka_ip)
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
        if message.value[:3] == b'REG':
            yield message.value[3:]


def default_setting():
    # Logging 세팅
    global logger
    # logger: logging.Logger
    logger = logging.getLogger("Servermanage")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 화면 + 파일 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 1MB 씩 최대 10개 파일 보관
    file_handler = TimedRotatingFileHandler('register_server.log', when='midnight')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # E/S 에서 가져온 기본 설정
    logger.info("agent start")

    global config
    # config: configparser.ConfigParser
    config = configparser.ConfigParser()
    config.read(statics.config_file_name)


def get_last_seq():
    try:
        res = es.get(index="config", doc_type='doc', id='last_seq')
        return res['_source']['config_val']
    except elasticsearch.exceptions.NotFoundError:
        return 0


def check_register(mac):
    try:
        res = es.get(index="agent_list", doc_type='doc', id=mac)
        return res['_source']['agent_id']
    except elasticsearch.exceptions.NotFoundError:
        return False


def register_agent(mac, seq):
    doc = {
        'agent_id': seq,
        'timestamp': datetime.datetime.now(),
    }
    res = es.index(index="agent_list", doc_type='doc', id=mac, body=doc)
    if res['result'] not in ['created, updated']:
        logger.error('elasticsearch agent_list create/update fail')

    doc = {
        'config_val': seq
    }
    res = es.index(index="config", doc_type='doc', id='last_seq', body=doc)
    if res['result'] not in ['created, updated']:
        logger.error('elasticsearch sequence update create/update fail')


def get_elasticsearch_config():
    query: dict = {
        "query": {
            "terms": {"_id": ["agent_kafka_ip", "agent_term"]}
        }
    }

    return_config = {}
    try:
        res = es.search(index="config", body=query)
    except elasticsearch.exceptions.NotFoundError:
        return {}

    logger.info(f"get elasticsearch config {res['hits']['total']} hits:")
    for config_val in res['hits']['hits']:
        return_config[config_val['_id']] = config_val['_source']['config_val']

    return return_config


def initialize():
    try:
        es_ip: str = config.get(statics.config_elastic_section_name, "address")
    except configparser.Error:
        logger.error('Get elasticsearch ip fail from config [es-config.conf] run initialize.py or setting conf file')
        sys.exit(-1)
    # 최초 시작시에만 E/S 를 통해서 config 가져와야 할것 같음
    # TODO config 에 의존하지 않고 데이터를 가져올 방법이 있을까?
    logger.info(f'Elasticsearch IP setted {es_ip}')

    global es_seq
    global es

    es = elasticsearch.Elasticsearch(es_ip)
    es_seq = get_last_seq()

    global es_config
    es_config = {}
    while 'agent_kafka_ip' not in es_config:
        es_config = get_elasticsearch_config()

        logger.debug(f'elasticsearch config setted {es_config}')
        if 'agent_kafka_ip' not in es_config.keys():
            logger.error(f'elasticsearch config not setted! please set {es_ip}/config/doc/agent_kafka_ip')
            time.sleep(60)


def connect_kafka():
    global kafka_con
    global kafka_pro
    kafka_con = kafka_consume(es_config['agent_kafka_ip'])
    kafka_pro = kafka_produce(es_config['agent_kafka_ip'])
    next(kafka_pro)


if __name__ == "__main__":
    default_setting()
    initialize()
    connect_kafka()

    while True:
        reg_data = next(kafka_con)
        reg_pdu = protocol_pb2.agent_register()
        reg_pdu.ParseFromString(reg_data)

        echo_pdu = protocol_pb2.agent_register_reply()
        # 이미 해당 agent 가 등록되었는지 확인
        is_exist = check_register(reg_pdu.mac)
        if is_exist is False:
            # 등록 안되어있으면 새로 등록 후 SEQ ++
            es_seq += 1
            register_agent(reg_pdu.mac, es_seq)
            echo_pdu.agent_id = es_seq
        else:
            # 등록 되어있으면 해당 agent_no 전송
            echo_pdu.agent_id = is_exist
        logger.info(f'agent_id {echo_pdu.agent_id} is register at {datetime.datetime.now()}')
        time.sleep(0.5)
        kafka_pro.send(reg_pdu.mac.encode() + echo_pdu.SerializeToString())
