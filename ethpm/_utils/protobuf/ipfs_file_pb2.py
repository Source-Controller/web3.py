# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ipfs_file.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fipfs_file.proto\"\xc1\x01\n\x04\x44\x61ta\x12\x1c\n\x04Type\x18\x01 \x01(\x0e\x32\x0e.Data.DataType\x12\x11\n\x04\x44\x61ta\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x12\x15\n\x08\x66ilesize\x18\x03 \x01(\x04H\x01\x88\x01\x01\x12\x12\n\nblocksizes\x18\x04 \x03(\x04\"G\n\x08\x44\x61taType\x12\x07\n\x03Raw\x10\x00\x12\r\n\tDirectory\x10\x01\x12\x08\n\x04\x46ile\x10\x02\x12\x0c\n\x08Metadata\x10\x03\x12\x0b\n\x07Symlink\x10\x04\x42\x07\n\x05_DataB\x0b\n\t_filesize\"^\n\x06PBLink\x12\x11\n\x04Hash\x18\x01 \x01(\x0cH\x00\x88\x01\x01\x12\x11\n\x04Name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05Tsize\x18\x03 \x01(\x04H\x02\x88\x01\x01\x42\x07\n\x05_HashB\x07\n\x05_NameB\x08\n\x06_Tsize\"<\n\x06PBNode\x12\x16\n\x05Links\x18\x02 \x03(\x0b\x32\x07.PBLink\x12\x11\n\x04\x44\x61ta\x18\x01 \x01(\x0cH\x00\x88\x01\x01\x42\x07\n\x05_Datab\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ipfs_file_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DATA._serialized_start=20
  _DATA._serialized_end=213
  _DATA_DATATYPE._serialized_start=120
  _DATA_DATATYPE._serialized_end=191
  _PBLINK._serialized_start=215
  _PBLINK._serialized_end=309
  _PBNODE._serialized_start=311
  _PBNODE._serialized_end=371
# @@protoc_insertion_point(module_scope)
