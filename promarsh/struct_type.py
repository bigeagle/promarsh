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

    @property
    def length(self):
        try:
            return sum([f.length for _, f in self._fields])
        except:
            return None

    def name(self):
        return self._name or "struct-%d" % (id(self))


__all__ = ['Struct']
# vim: ts=4 sw=4 sts=4 expandtab
