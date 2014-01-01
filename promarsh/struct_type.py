#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from operator import add
from .base_type import FieldType
from .container import Container


class Struct(FieldType):

    def __init__(self, *fields, **kwargs):
        for fname, ftype in fields:
            if not (isinstance(ftype, FieldType) or issubclass(ftype, FieldType)):
                raise TypeError("(%s, %s) is not valid field" % (fname, ftype))

        self._fields = fields
        self._name = kwargs.pop('name', None)
        super(Struct, self).__init__(**kwargs)

    def _pack(self, container):

        return reduce(add, [ftype.serialize(container.get_field(name))
                            for name, ftype in self._fields])

    def _unpack_from(self, buf):
        container = Container()
        for name, ftype in self._fields:
            value, buf = ftype.deserialize_from(buf)
            container.set_field(name, value)

        return container, buf

    @classmethod
    def get_length(cls):
        try:
            return sum([f.length for _, f in cls._fields])
        except:
            return None

    def name(self):
        return self._name or "struct-%d" % (id(self))


class BitStruct(FieldType):

    __mask = {
        1: 0b00000001,
        2: 0b00000011,
        3: 0b00000111,
        4: 0b00001111,
        5: 0b00011111,
        6: 0b00111111,
        7: 0b01111111
    }

    def __init__(self, *fields, **kwargs):

        _offset = 8
        self._fields = []
        for fname, flen in fields:
            _offset -= flen
            self._fields.append((fname, _offset, flen))

        self._name = kwargs.pop('name', None)
        super(BitStruct, self).__init__(**kwargs)

    def _pack(self, container):
        _byte = 0
        for fname, offset, flen in self._fields:
            v = getattr(container, fname, 0)
            _byte |= ((v & self.__mask[flen]) << offset)
        return chr(_byte)

    def _unpack_from(self, buf):
        _byte = ord(buf[0])
        rest = buf[1:]

        container = Container()
        for fname, offset, flen in self._fields:
            v = (_byte >> offset) & self.__mask[flen]
            container.set_field(fname, v)
        return container, rest

    @classmethod
    def get_length(cls):
        return 1

    def name(self):
        return self._name or "bitstruct-%d" (id(self))

# vim: ts=4 sw=4 sts=4 expandtab
