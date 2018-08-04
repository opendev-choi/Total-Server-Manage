# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Total-Server-Manage/protocol.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Total-Server-Manage/protocol.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\"Total-Server-Manage/protocol.proto\"\xea\x01\n\rserver_status\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\x05\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x10\n\x08hostname\x18\x03 \x01(\t\x12\x15\n\rcpu_idle_rate\x18\x04 \x03(\x02\x12\x14\n\x0cmemory_total\x18\x05 \x01(\x02\x12\x12\n\nmemory_use\x18\x06 \x01(\x02\x12&\n\tdisk_list\x18\x07 \x03(\x0b\x32\x13.server_status.disk\x1a@\n\x04\x64isk\x12\x12\n\ndisk_mount\x18\x01 \x01(\t\x12\x12\n\ndisk_total\x18\x02 \x01(\x04\x12\x10\n\x08\x64isk_use\x18\x03 \x01(\x04\"\x1d\n\x0e\x61gent_register\x12\x0b\n\x03mac\x18\x01 \x01(\t\"(\n\x14\x61gent_register_reply\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\x05\x62\x06proto3')
)




_SERVER_STATUS_DISK = _descriptor.Descriptor(
  name='disk',
  full_name='server_status.disk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='disk_mount', full_name='server_status.disk.disk_mount', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_total', full_name='server_status.disk.disk_total', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_use', full_name='server_status.disk.disk_use', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=209,
  serialized_end=273,
)

_SERVER_STATUS = _descriptor.Descriptor(
  name='server_status',
  full_name='server_status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='server_status.agent_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip', full_name='server_status.ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hostname', full_name='server_status.hostname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpu_idle_rate', full_name='server_status.cpu_idle_rate', index=3,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory_total', full_name='server_status.memory_total', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory_use', full_name='server_status.memory_use', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_list', full_name='server_status.disk_list', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SERVER_STATUS_DISK, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=273,
)


_AGENT_REGISTER = _descriptor.Descriptor(
  name='agent_register',
  full_name='agent_register',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mac', full_name='agent_register.mac', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=275,
  serialized_end=304,
)


_AGENT_REGISTER_REPLY = _descriptor.Descriptor(
  name='agent_register_reply',
  full_name='agent_register_reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='agent_register_reply.agent_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=306,
  serialized_end=346,
)

_SERVER_STATUS_DISK.containing_type = _SERVER_STATUS
_SERVER_STATUS.fields_by_name['disk_list'].message_type = _SERVER_STATUS_DISK
DESCRIPTOR.message_types_by_name['server_status'] = _SERVER_STATUS
DESCRIPTOR.message_types_by_name['agent_register'] = _AGENT_REGISTER
DESCRIPTOR.message_types_by_name['agent_register_reply'] = _AGENT_REGISTER_REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

server_status = _reflection.GeneratedProtocolMessageType('server_status', (_message.Message,), dict(

  disk = _reflection.GeneratedProtocolMessageType('disk', (_message.Message,), dict(
    DESCRIPTOR = _SERVER_STATUS_DISK,
    __module__ = 'Total_Server_Manage.protocol_pb2'
    # @@protoc_insertion_point(class_scope:server_status.disk)
    ))
  ,
  DESCRIPTOR = _SERVER_STATUS,
  __module__ = 'Total_Server_Manage.protocol_pb2'
  # @@protoc_insertion_point(class_scope:server_status)
  ))
_sym_db.RegisterMessage(server_status)
_sym_db.RegisterMessage(server_status.disk)

agent_register = _reflection.GeneratedProtocolMessageType('agent_register', (_message.Message,), dict(
  DESCRIPTOR = _AGENT_REGISTER,
  __module__ = 'Total_Server_Manage.protocol_pb2'
  # @@protoc_insertion_point(class_scope:agent_register)
  ))
_sym_db.RegisterMessage(agent_register)

agent_register_reply = _reflection.GeneratedProtocolMessageType('agent_register_reply', (_message.Message,), dict(
  DESCRIPTOR = _AGENT_REGISTER_REPLY,
  __module__ = 'Total_Server_Manage.protocol_pb2'
  # @@protoc_insertion_point(class_scope:agent_register_reply)
  ))
_sym_db.RegisterMessage(agent_register_reply)


# @@protoc_insertion_point(module_scope)
