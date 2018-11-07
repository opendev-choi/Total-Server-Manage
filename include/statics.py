import os

headlines: str = """
##############################################################
#     ___________        _________            _____          #
#     \\__    ___/       /   _____/           /     \\         #
#       |    |  ______  \\_____  \\   ______  /  \\ /  \\        #
#       |    | /_____/  /        \\ /_____/ /    Y    \\       #
#       |____|         /_______  /         \\____|__  /       #
#                              \\/                  \\/        #
##############################################################
Initialize Program...
"""

if 'nt' == os.name.lower():
    config_file_name: str = "etc\\es-config.conf"
else:
    config_file_name: str = "etc/es-config.conf"

default_config: str = """
[elasticsearch]
address = server.elasticsearch
"""

config_elastic_section_name: str = "elasticsearch"

protobuf_tool_intro: str = """
Protobuf Tool 입니다.
사용법은 두가지이며, Encode와 Decode 기능입니다.

Encode 시에는 해당하는 정보를 입력하면 Python Byte 형식의 메세지를 출력하게 됩니다.
Decode 시에는 b'lorem ipsum' 식의 정보를 입력하면 데이터를 출력합니다.
"""