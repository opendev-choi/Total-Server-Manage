# created at 2018.07.26 by opendev-choi
# Program That Initialize Program ...
# Total-Server-Manage 프로그램을 초기화 시켜주는 프로그램입니다.
# 만약 이 프로그램을 통하여 설정하지 않았다면 기본 설정으로 됩니다.
# 기본적으론 ElasticSearch 주소만 파일에 저장하며
# 기타 정보들은 ElasticSearch 에 저장하게 됩니다.

import os
import sys
import configparser

import statics

if __name__ == '__main__':
    print(statics.headlines)

    # Check File Exist
    while os.path.exists(statics.config_file_name) is False:
        user_select: str
        # if non-exist Create File or Close Program
        user_select = input('Config file not found... create new file? : ')
        if user_select in ['y', 'Y']:
            try:
                with open(statics.config_file_name, 'w') as file:
                    print(file)
                    file.writelines(statics.default_config)
            except PermissionError as pe:
                print(f'Config file create fail! cause {pe.args}')
                print('Close initialize program... check create dile')
                sys.exit(-1)

        if user_select in ['n', 'N']:
            sys.exit(0)

        else:
            continue

    # Read Config File & print Now Setting
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(statics.config_file_name)

    exist_es_section: bool = True
    es_server_address: str
    try:
        print('Start Elasticsearch settings ...\n')
        print(f'Now Elasticsearch server address is {config.get(statics.config_elastic_section_name, "address")}\n')
    except configparser.NoSectionError:
        print(f'There are no section \'{statics.config_elastic_section_name}\'')
        exist_es_section = False

    es_server_address = input('If need change Elasticsearch server address enter server address name\n'
                              'or you not need change Elaticsearch Setting just enter\n'
                              'E/S server Address : ')

    if es_server_address:
        if exist_es_section is False:
            config.add_section(statics.config_elastic_section_name)

        config.set(statics.config_elastic_section_name, 'address', es_server_address)
        try:
            with open(statics.config_file_name, 'w') as file:
                config.write(file)
        except PermissionError as pe:
            print(f'PermissionError at write file cause {pe.args}')
        print('config file changed! end program')
    else:
        print('nothing change settings... end program')
