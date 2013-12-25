#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from operator import add
from .base_type import FieldType
from .container import Container
from .helpers import serialize, deserialize_from


class Struct(FieldType):

    def __init__(self, *fields, **kwargs):
        for name, ftype in fields:
            if not (isinstance(ftype, FieldType) or issubclass(ftype, FieldType)):
                raise TypeError("(%s, %s) is not valid field" % (name, ftype))

        self._fields = fields
        super(Struct, self).__init__(**kwargs)

    def _pack(self, container):

        return reduce(add, [serialize(ftype, container.get_field(name))
                            for name, ftype in self._fields])

    def _unpack_from(self, buf):
        container = Container()
        for name, ftype in self._fields:
            value, buf = deserialize_from(ftype, buf)
            container.set_field(name, value)

        return container, buf



# vim: ts=4 sw=4 sts=4 expandtab
