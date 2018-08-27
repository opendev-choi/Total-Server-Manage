# created at 2018.07.31 by opendev-choi
# agent 역할을 하는 프로그램입니다.
# 최초 실행 및 주기별로 Elasticsearch 에 접속하여 설정 정보를 받아갑니다.
# CPU, Mem, disk 등을 수집합니다.

import sys
import time
import socket
import logging
import datetime
import netifaces
import configparser
from logging.handlers import RotatingFileHandler

import kafka
import psutil
import elasticsearch

from include import statics
from include import protocol_pb2
from include import exceptions


class Performance:
    @staticmethod
    def cpu_perf() -> list:
        try:
            return psutil.cpu_percent(interval=1, percpu=True)
        except psutil.Error as e:
            raise exceptions.PerfFailException(f'cpu_perf fail cause {e!s}')

    @staticmethod
    def mem_perf() -> psutil._psplatform.svmem:
        try:
            return psutil.virtual_memory()
        except psutil.Error as e:
            raise exceptions.PerfFailException(f'mem_perf fail cause {e!s}')

    @staticmethod
    def disk_perf() -> list:
        try:
            disk_list: list = []
            for mount in psutil.disk_partitions():
                disk = protocol_pb2.server_status.disk()
                disk.disk_mount = mount.mountpoint

                disk.disk_total = psutil.disk_usage(disk.disk_mount).total
                disk.disk_use = psutil.disk_usage(disk.disk_mount).used
                disk_list.append(disk)

            return disk_list
        except psutil.Error as e:
            raise exceptions.PerfFailException(f'disk_perf fail cause {e!s}')

    @staticmethod
    def boottime_perf() -> float:
        try:
            return psutil.boot_time()
        except psutil.Error as e:
            raise exceptions.PerfFailException(f'boottime_perf fail cause {e!s}')

    @staticmethod
    def mac_perf() -> str:
        for interface in netifaces.interfaces():
            if 'lo' == interface or 'local' in interface:
                continue
            return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        raise exceptions.PerfFailException(
            f'Perf fail at get mac address, cannot find interface without \'lo\' or \'local\' in interface name,'
            f'interface list[{netifaces.interfaces()}]')


def get_elasticsearch_config(es_ip: str) -> dict:
    es = elasticsearch.Elasticsearch(es_ip)
    query: map = {
        "query": {
            "terms": {"_id": ["agent_kafka_ip", "agent_term"]}
        }
    }

    return_config = {}
    try:
        res = es.search(index="config", body=query)
    except elasticsearch.exceptions.NotFoundError:
        del es
        return {}

    logger.info(f"get elasticsearch config {res['hits']['total']} hits:")
    for config_val in res['hits']['hits']:
        return_config[config_val['_id']] = config_val['_source']['config_val']

    del es
    return return_config


def kafka_produce(kafka_ip) -> None:
    producer: kafka.KafkaProducer = kafka.KafkaProducer(bootstrap_servers=kafka_ip)
    while True:
        produce_protobuf, topic = yield
        future = producer.send(topic, produce_protobuf)

        try:
            record_metadata = future.get(timeout=10)
            logger.debug(record_metadata)
        except kafka.KafkaError as kafka_e:
            logger.error(f'Produce Fail! cause {kafka_e}')


def kafka_consume(kafka_ip, mac_address) -> None:
    consumer: kafka.KafkaConsumer = kafka.KafkaConsumer('to_agent',
                                                        bootstrap_servers=kafka_ip,
                                                        consumer_timeout_ms=10000)
    while True:
        for message in consumer:
            logger.debug("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))
            if mac_address.encode() in message.value:
                yield message.value.replace(mac_address.encode(), b'')
        yield None


def perf() -> protocol_pb2.server_status:
    perf_pdu = protocol_pb2.server_status()
    perf_pdu.agent_id = agent_id
    # get address data
    perf_pdu.ip = socket.gethostbyname(socket.gethostname())
    perf_pdu.hostname = socket.gethostname()

    # cpu/mem perf
    for cpu_rate in Performance.cpu_perf():
        perf_pdu.cpu_idle_rate.append(cpu_rate)
    memory = Performance.mem_perf()
    perf_pdu.memory_total = memory.total
    perf_pdu.memory_use = memory.used

    # disk
    disk_usage = Performance.disk_perf()
    for disk_list in disk_usage:
        disk = perf_pdu.disk_list.add()
        disk.disk_mount = disk_list.disk_mount
        disk.disk_total = disk_list.disk_total
        disk.disk_use = disk_list.disk_use

    return perf_pdu


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
    file_handler = RotatingFileHandler('agent.log', maxBytes=1048576, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # E/S 에서 가져온 기본 설정
    logger.info("agent start")

    global config
    config = configparser.ConfigParser()
    config.read(statics.config_file_name)


def initialize():
    try:
        es_ip: str = config.get(statics.config_elastic_section_name, "address")
    except configparser.Error:
        logger.error('Get elasticsearch ip fail from config [es-config.conf] run initialize.py or setting conf file')
        sys.exit(-1)
    # 최초 시작시에만 E/S 를 통해서 config 가져와야 할것 같음
    # TODO config 에 의존하지 않고 데이터를 가져올 방법이 있을까?
    logger.info(f'Elasticsearch IP setted {es_ip}')

    global es_config
    es_config = {}
    while 'agent_kafka_ip' not in es_config:
        es_config = get_elasticsearch_config(es_ip)

        logger.debug(f'elasticsearch config setted {es_config}')
        if 'agent_kafka_ip' not in es_config.keys():
            logger.error(f'elasticsearch config not setted! please set {es_ip}/config/doc/agent_kafka_ip')
            time.sleep(60)

    register_protobuf: protocol_pb2.agent_register = protocol_pb2.agent_register()
    register_protobuf.mac = Performance.mac_perf()

    global kafka_pro
    kafka_pro = kafka_produce(es_config['agent_kafka_ip'])
    next(kafka_pro)
    kafka_pro.send([b'REG' + register_protobuf.SerializeToString(), 'from_agent'])
    global kafka_con
    kafka_con = kafka_consume(es_config['agent_kafka_ip'], register_protobuf.mac)
    registration_data = None
    while not registration_data:
        registration_data = next(kafka_con)

    logger.info('register finished!')
    agent_data = protocol_pb2.agent_register_reply()
    agent_data.ParseFromString(registration_data)
    global agent_id
    agent_id = agent_data.agent_id
    logger.info(f'initialize end! agent no {agent_id}')


if __name__ == '__main__':
    default_setting()
    initialize()

    agent_term: int = 60
    if 'agent_term' in es_config.keys():
        agent_term = int(es_config['agent_term'])

    now_time = datetime.datetime.now()
    # 수집이 일정하게 되지 않게 하기 위해서 agent_id 를 term으로 나눠
    # term에 균등하게 나누어서 수집
    time_elapse_sec = now_time.hour * 60 * 60 + now_time.minute * 60 + now_time.second

    logger.info(f'collect wait until {agent_term - (time_elapse_sec % agent_term) + (agent_id % agent_term)} second')
    standard_time = now_time + \
                    datetime.timedelta(seconds=agent_term - (time_elapse_sec % agent_term))

    time.sleep(agent_term - (time_elapse_sec % agent_term) + (agent_id % agent_term))

    while True:
        time_s = datetime.datetime.now()
        perf_data = perf()
        perf_data.collection_time = standard_time.strftime('%Y%m%d%H%M%S')
        kafka_pro.send([perf_data.SerializeToString(), 'agent_data'])
        elapse_sec = (datetime.datetime.now() - time_s).total_seconds()
        logger.info(f'{perf_data.collection_time} collection end! server data collect elapse {elapse_sec:.2f} seconds')
        time.sleep(agent_term - elapse_sec)

        standard_time += datetime.timedelta(seconds=agent_term)
