# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: web_amazon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='web_amazon.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x10web_amazon.proto\"\x1d\n\tOrderInfo\x12\x10\n\x08order_id\x18\x03 \x02(\x03\"F\n\x12\x43ustomerUpdateDest\x12\x0e\n\x06\x64\x65st_x\x18\x01 \x02(\x05\x12\x0e\n\x06\x64\x65st_y\x18\x02 \x02(\x05\x12\x10\n\x08order_id\x18\x03 \x02(\x03\"\x1f\n\x0b\x43\x61ncelOrder\x12\x10\n\x08order_id\x18\x01 \x02(\x03\"m\n\tWACommand\x12\x1a\n\x06\x63reate\x18\x01 \x03(\x0b\x32\n.OrderInfo\x12&\n\tchangeDst\x18\x02 \x03(\x0b\x32\x13.CustomerUpdateDest\x12\x1c\n\x06\x63\x61ncel\x18\x03 \x03(\x0b\x32\x0c.CancelOrder')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ORDERINFO = _descriptor.Descriptor(
  name='OrderInfo',
  full_name='OrderInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order_id', full_name='OrderInfo.order_id', index=0,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=49,
)


_CUSTOMERUPDATEDEST = _descriptor.Descriptor(
  name='CustomerUpdateDest',
  full_name='CustomerUpdateDest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dest_x', full_name='CustomerUpdateDest.dest_x', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dest_y', full_name='CustomerUpdateDest.dest_y', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='order_id', full_name='CustomerUpdateDest.order_id', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=121,
)


_CANCELORDER = _descriptor.Descriptor(
  name='CancelOrder',
  full_name='CancelOrder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='order_id', full_name='CancelOrder.order_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=154,
)


_WACOMMAND = _descriptor.Descriptor(
  name='WACommand',
  full_name='WACommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='create', full_name='WACommand.create', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='changeDst', full_name='WACommand.changeDst', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cancel', full_name='WACommand.cancel', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=156,
  serialized_end=265,
)

_WACOMMAND.fields_by_name['create'].message_type = _ORDERINFO
_WACOMMAND.fields_by_name['changeDst'].message_type = _CUSTOMERUPDATEDEST
_WACOMMAND.fields_by_name['cancel'].message_type = _CANCELORDER
DESCRIPTOR.message_types_by_name['OrderInfo'] = _ORDERINFO
DESCRIPTOR.message_types_by_name['CustomerUpdateDest'] = _CUSTOMERUPDATEDEST
DESCRIPTOR.message_types_by_name['CancelOrder'] = _CANCELORDER
DESCRIPTOR.message_types_by_name['WACommand'] = _WACOMMAND

OrderInfo = _reflection.GeneratedProtocolMessageType('OrderInfo', (_message.Message,), dict(
  DESCRIPTOR = _ORDERINFO,
  __module__ = 'web_amazon_pb2'
  # @@protoc_insertion_point(class_scope:OrderInfo)
  ))
_sym_db.RegisterMessage(OrderInfo)

CustomerUpdateDest = _reflection.GeneratedProtocolMessageType('CustomerUpdateDest', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERUPDATEDEST,
  __module__ = 'web_amazon_pb2'
  # @@protoc_insertion_point(class_scope:CustomerUpdateDest)
  ))
_sym_db.RegisterMessage(CustomerUpdateDest)

CancelOrder = _reflection.GeneratedProtocolMessageType('CancelOrder', (_message.Message,), dict(
  DESCRIPTOR = _CANCELORDER,
  __module__ = 'web_amazon_pb2'
  # @@protoc_insertion_point(class_scope:CancelOrder)
  ))
_sym_db.RegisterMessage(CancelOrder)

WACommand = _reflection.GeneratedProtocolMessageType('WACommand', (_message.Message,), dict(
  DESCRIPTOR = _WACOMMAND,
  __module__ = 'web_amazon_pb2'
  # @@protoc_insertion_point(class_scope:WACommand)
  ))
_sym_db.RegisterMessage(WACommand)


# @@protoc_insertion_point(module_scope)