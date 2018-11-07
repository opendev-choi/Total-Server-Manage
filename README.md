# Total-Server-Manage
> Scale out Elasticsearch 성능 수집기


Metricbeat 와 같은 Cpu, Memory 등 서버 데이터 Elasticsearch 수집기를 Scale Out 구조로 만드는 프로젝트입니다.


## 설치 방법

리눅스 / 윈도우:

```sh
Elasticsearch 및 Kafka 사전설치 필요

1. initialize 실행
- E/S IP 및 Kafka IP 설정
```


## 사용 예제
Release 는 pyinstaller 를 통하여 Exe 로 묶어서 배포중입니다.

Server/Agent 둘 다 initialize 파일을 통하여 초기화가 가능하며, 초기화 이후에는 실행만 시켜주시면 됩니다.

Server - register_server, collect_server 실행

Agent - agent 실행

데이터는 Elasticsearch 의 다음과 같은 인덱스에 들어가 있습니다.

config - 상세 설정 정보 저장
agent_list - 에이전트 리스트 저장
agent_last_status - 에이전트의 최신 정보가 들어가 있습니다.
```json
{  
   "_index":"agent_last_status",
   "_type":"doc",
   "_id":"2",
   "_version":3,
   "_score":1,
   "_source":{  
      "agentId":2,
      "ip":"192.168.244.1",
      "hostname":"DESKTOP-I7B6FFM",
      "cpuIdleRate":[  
         31.9,
         18.8,
         12.5,
         6.2
      ],
      "memoryTotal":17096474624,
      "memoryUse":8369500160,
      "diskList":[  
         {  
            "diskMount":"C:\\", 
            "diskTotal":"239011000320",
            "diskUse":"213363695616"
         },
         {  
            "diskMount":"D:\\", 
            "diskTotal":"1000068870144",
            "diskUse":"674538033152"
         }
      ],
      "collectionTime":"20181107132300",
      "date":"2018-11-07T13:23:03.084560"
   }
}
```
agent_collect - 에이전트의 수집 데이터가 들어가 있습니다.
```json
{  
   "_index":"agent_collect",
   "_type":"doc",
   "_id":"20181107132200_2",
   "_version":1,
   "_score":1,
   "_source":{  
      "agentId":2,
      "ip":"192.168.244.1",
      "hostname":"DESKTOP-I7B6FFM",
      "cpuIdleRate":[  
         23.1,
         12.5,
         12.5,
         18.8
      ],
      "memoryTotal":17096474624,
      "memoryUse":8305950720,
      "diskList":[  
         {  
            "diskMount":"C:\\", 
            "diskTotal":"239011000320",
            "diskUse":"213363994624"
         },
         {  
            "diskMount":"D:\\", 
            "diskTotal":"1000068870144",
            "diskUse":"674538033152"
         }
      ],
      "collectionTime":"20181107132200",
      "date":"2018-11-07T13:22:03.090672"
   }
}
```


## 개발 환경 설정
Python3.6.5 버전을 사용하여 개발하였으며, 사용된 프레임워크는 다음과 같습니다.

```
Package       Version
------------- -------
elasticsearch 6.3.1
kafka-python  1.4.3
netifaces     0.10.7
pip           18.0
protobuf      3.6.0
psutil        5.4.7
setuptools    40.2.0
six           1.11.0
urllib3       1.23
```

## 업데이트 내역

* 0.1.0
    * 첫 출시
    * initialize 파일 kafka 설정 추가
* 0.0.1
    * 최초 프로젝트 생성

## 정보
Choi JongHyeok - opendev.choi@gmail.com

[https://github.com/opendev-choi](https://github.com/opendev-choi)
