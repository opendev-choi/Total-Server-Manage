# created at 2018.07.31 by opendev-choi
# agent 역할을 하는 프로그램입니다.
# 최초 실행 및 주기별로 Elasticsearch 에 접속하여 설정 정보를 받아갑니다.
# CPU, Mem, disk 등을 수집합니다.

import sys
import time
import logging
import netifaces
import configparser
from logging.handlers import RotatingFileHandler

import psutil
import elasticsearch

import statics
import protocol_pb2


def cpu_perf():
    return psutil.cpu_percent(interval=1, percpu=True)


def mem_perf():
    return psutil.virtual_memory(), psutil.swap_memory()


def disk_perf():
    disk_uasge: map = {}
    for mount in psutil.disk_partitions():
        disk_uasge[mount] = psutil.disk_usage(mount)

    return disk_uasge


def boottime_perf():
    return psutil.boot_time()


def mac_perf():
    for interface in netifaces.interfaces():
        if 'lo' == interface or 'local' in interface:
            continue
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK]['addr']
    return ''


def get_elasticsearch_config(es_ip: str):
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

def perf(ip_addr):
    perf_pdu = protocol_pb2.server_status()
    perf_pdu.ip = ip_addr
    # TODO add hostname
    # perf_pdu.hostname
    for cpu_rate in cpu_perf():
        perf_pdu.cpu_idle_rate.append(cpu_rate)
    perf_pdu.memory_rate
    disk_part, disk_usage = disk_perf()
    for directory in disk_part:
        perf_pdu.disk[directory] = disk_usage[directory]


if __name__ == '__main__':
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
    # config: configparser.ConfigParser
    config = configparser.ConfigParser()
    config.read(statics.config_file_name)
    try:
        es_ip: str = config.get(statics.config_elastic_section_name, "address")
    except configparser.Error:
        logger.error('Get elasticsearch ip fail from config [es-config.conf] run initialize.py or setting conf file')
        sys.exit(-1)

    # 최초 시작시에만 E/S 를 통해서 config 가져와야 할것 같음
    # TODO config 에 의존하지 않고 데이터를 가져올 방법이 있을까?
    logger.info(f'Elasticsearch IP setted {es_ip}')

    es_config: dict = {}
    while 'agent_kafka_ip' not in es_config:
        es_config = get_elasticsearch_config(es_ip)

        logger.debug(f'elasticsearch config setted {es_config}')
        if 'agent_kafka_ip' not in es_config.keys():
            logger.error(f'elasticsearch config not setted! please set {es_ip}/config/doc/agent_kafka_ip')
            time.sleep(60)

    # TODO kafka 를 이용해서 register 하는 로직 추가
    
    # TODO kafka 를 이용해서 register 결과물 받는 로직 추가
    print()
