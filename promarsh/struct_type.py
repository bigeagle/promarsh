#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from .base_type import FieldType
from .container import Container
from .context import context


class Struct(FieldType):

    def __init__(self, *fields, **kwargs):
        for fname, ftype in fields:
            if not (isinstance(ftype, FieldType) or issubclass(ftype, FieldType)):
                raise TypeError("(%s, %s) is not valid field" % (fname, ftype))

        self._fields = fields
        self._name = kwargs.pop('name', None)
        super(Struct, self).__init__(**kwargs)

    def __pack(self, container, **kwargs):
        _bytes = ""
        for name, ftype in self._fields[::-1]:
            value = container.get_field(name)
            context.set(name, value)
            _bytes = ftype.serialize(value, **kwargs) + _bytes
        return _bytes

    def _pack(self, container, _with_ctx=True):
        if _with_ctx:
            with context():
                return self.__pack(container, _with_ctx=True)
        else:
            return self.__pack(container)

    def __unpack_from(self, buf, **kwargs):
        container = Container()

        for name, ftype in self._fields:
            value, buf = ftype.deserialize_from(buf, **kwargs)
            if len(name) > 0:
                container.set_field(name, value)
                context.set(name, value)
            elif isinstance(value, Container):  # Embedded struct
                for k, v in value._items():
                    container.set_field(k, v)
                    context.set(k, v)

        return container, buf

    def _unpack_from(self, buf, _with_ctx=True):
        if _with_ctx:
            with context():
                return self.__unpack_from(buf, _with_ctx=True)
        else:
            return self.__unpack_from(buf)

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
