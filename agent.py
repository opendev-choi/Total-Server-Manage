# created at 2018.07.31 by opendev-choi
# agent 역할을 하는 프로그램입니다.
# 최초 실행 및 주기별로 Elasticsearch 에 접속하여 설정 정보를 받아갑니다.
# CPU, Mem, disk 등을 수집합니다.

import sys
import logging
import configparser
from logging.handlers import RotatingFileHandler

import elasticsearch

import statics


def get_elasticsearch_config(es_ip: str):
    es = elasticsearch.Elasticsearch(es_ip)
    query: map = {
        "query": {
            "terms": {"_id": ["agent_kafka_ip", "agent_term"]}
        }
    }
    while True:
        return_config = {}
        res = es.search(index="config", body=query)
        logger.info(f"get elasticsearch config {res['hits']['total']} hits:")
        for config_val in res['hits']['hits']:
            return_config[config_val['_id']] = config_val['_source']['config_val']

        yield return_config


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

    logger.info(f'Elasticsearch IP setted {es_ip}')
    global es_config
    es_config = get_elasticsearch_config(es_ip)

    logger.debug(f'elasticsearch config setted {next(es_config)}')

