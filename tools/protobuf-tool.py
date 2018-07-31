# created at 2018.07.27 by opendev-choi
# Protobuf의 decode, encode를 편하게 할 수 있는 툴입니다.

import re
import struct

import google
import protocol_pb2

import statics

if __name__ == '__main__':
    pdu: protocol_pb2.server_status = protocol_pb2.server_status()

    print(statics.protobuf_tool_intro)
    mode = input('E - encode \nD - decode \nMode: ')
    if mode.upper() == 'E':
        # Encode Mode
        pdu.mac = input('mac : ')
        pdu.ip = input('ip : ')
        pdu.hostname = input('hostname : ')
        pdu.cpu_rate = input('cpu_rate : ')
        pdu.memory_rate = float(input('memory_rate : '))
        print('GPB serialize 결과입니다.')
        print(pdu.SerializeToString())

    elif mode.upper() == 'D':
        # Decode Mode
        byte_input = input('Python Byte : ')
        # 앞의 b' 와 뒤의 ' 분리 후 Bytearray로 변환한다
        # TODO b'deadbeaf' 와 같은 문자열을 Byte로 변환한다
        try:
            pdu.ParseFromString(byte_input.encode())
        except google.protobuf.message.DecodeError:
            print('Parse 오류입니다! 스트링을 다시 확인해주세요!')
        else:
            print(pdu)
    else:
        print('잘못된 입력입니다.\n프로그램을 종료합니다.')
