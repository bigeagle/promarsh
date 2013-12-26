#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from .base_type import FieldType, PackError
from .helpers import serialize, deserialize_from


class Enum(FieldType):

    def __init__(self, T, *enums, **kwargs):
        self.T = T
        self._map = dict(enums)
        self._rmap = dict([(v, k) for k, v in enums])
        super(Enum, self).__init__(**kwargs)

    def _pack(self, value):
        try:
            v = self._rmap[value]
        except:
            raise PackError("%s is not valid enum" % value)
        return serialize(self.T, v)

    def _unpack_from(self, buf):
        v, rest = deserialize_from(self.T, buf)
        return self._map.get(v, v), rest


# vim: ts=4 sw=4 sts=4 expandtab
