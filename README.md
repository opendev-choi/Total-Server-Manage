# Total-Server-Manage
Total Server Management Project with ElasticSearch, Kafka

흔히 솔루션 회사에서 SMS 라고 부르는 솔루션을 Kafka, Elasticsearch 를 사용하여
CPU, Memory, I/O 등을 최소화 하고, Scale Out 구조의 프로그램을 만드는 프로젝트입니다!

현재 설정값은 Elasticsearch 를 사용하여 보관하며,
파일로 저장하는 값은 Elasticsearch 의 서버 주소 하나입니다.

최초 설치시에는 파일의 소유자를 실행할 유저로 해주시고,
initalize.py 로 실행해주세요

web 화면은 현재 개발중에 있으며, 실제로 사용 가능한 서비스가 목표입니다.


---------------------------------------

사용 라이브러리 및 버전

Python3.7.0

```
Python3.7.0

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

사용중입니다.