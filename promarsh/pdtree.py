#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Packet Description Tree

A multi-layered structure to describe packet layout,

Author: Justin Wong <justin.w.xd@gmail.com>
"""
import six
from .base_type import FieldType, MetaFieldType
from .struct_type import Struct
from .context import context
from .container import Packet


# def PDHeader(object):
#     __slots__ = ('_struct', 'type_field', )
#
#     def __init__(self, *args, type_field=None):
#         self._struct=Struct(*args)
#         self.type_field = type_field

class Map(object):

    __slots__ = ('_typefunc', "_dict", )

    def __init__(self, typefunc, **_dict):
        if not callable(typefunc):
            raise Exception("A callable function to determine payload type from context is needed")

        for k, v in six.iteritems(_dict):
            if not isinstance(v, (FieldType, PDT, MetaFieldType, )):
                raise TypeError("'{0}' should be a `FieldType` or `PDT`".format(k))

        self._typefunc = typefunc
        self._dict = _dict

    def __getitem__(self, key):
        return self._dict[key]

    def get(self, *args, **kwargs):
        return self._dict.get(*args, **kwargs)

    def get_type(self):
        key = self._typefunc(context)
        return self._dict[key]


class PDT(object):

    __slots__ = ('header', 'payload_map', 'payload')

    def __init__(self, header, _payload):
        if isinstance(header, (tuple, list)):
            self.header = Struct(*header)
        elif isinstance(header, (FieldType, MetaFieldType)):
            self.header = header
        else:
            raise TypeError("header field should be a `FieldType` instance")

        if isinstance(_payload, (tuple, list)):
            self.payload = Struct(*header)
            self.payload_map = None
        elif isinstance(_payload, (FieldType, PDT, MetaFieldType, )):
            self.payload = _payload
            self.payload_map = None
        elif isinstance(_payload, Map):
            self.payload = None
            self.payload_map = _payload
        else:
            raise TypeError("payload field should be `FieldType`, `PDT` or `Map`")

    def deserialize_from(self, buf, **kwargs):

        with context():
            header, buf = self.header.deserialize_from(buf, _with_ctx=False)
            payload_type = self.payload or self.payload_map.get_type()
            context.set('_header', header)
            payload, buf = payload_type.deserialize_from(buf, _with_ctx=True)

        return Packet(header=header, payload=payload), buf


__all__ = ['Map', "PDT"]

# vim: ts=4 sw=4 sts=4 expandtab
