import sys
import time
import json
import logging
import datetime
import configparser
from logging.handlers import TimedRotatingFileHandler

import kafka
import elasticsearch
import google.protobuf.json_format

import statics
import protocol_pb2


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
    global es

    es = elasticsearch.Elasticsearch(es_ip)
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
    kafka_con = kafka_consume(es_config['agent_kafka_ip'])


def kafka_consume(kafka_ip):
    consumer: kafka.KafkaConsumer = kafka.KafkaConsumer('agent_data',
                                                        bootstrap_servers=kafka_ip)
    for message in consumer:
        yield message.value


def put_elasticsearch():
    while True:
        server_resource = yield
        res = es.index(index="agent_collect",
                       doc_type='doc',
                       id=f'{server_resource["collectionTime"]}_{server_resource["agentId"]}',
                       body=json_data)

        res = es.index(index="agent_last_status",
                       doc_type='doc',
                       id=server_resource["agentId"],
                       body=json_data)


if __name__ == '__main__':
    default_setting()
    initialize()
    connect_kafka()

    elastic_insert = put_elasticsearch()
    next(elastic_insert)

    while True:
        server_data = next(kafka_con)
        server_data_gpb = protocol_pb2.server_status()
        server_data_gpb.ParseFromString(server_data)
        json_string = google.protobuf.json_format.MessageToJson(server_data_gpb, True)

        json_data = json.loads(json_string)
        json_data["date"] = datetime.datetime.now()
        temp_cpu_rate = []
        for cpu_rate in json_data['cpuIdleRate']:
            temp_cpu_rate.append(round(cpu_rate, 3))
        json_data['cpuIdleRate'] = temp_cpu_rate
        print(json_data)

        elastic_insert.send(json_data)
