#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from .base_type import FieldType, PackError, MetaFieldType


class BaseEnum(FieldType):

    T = None

    def __init__(self, *enums, **kwargs):
        self._map = dict([(v, k) for k, v in enums])
        self._rmap = dict(enums)
        super(BaseEnum, self).__init__(**kwargs)

    def _pack(self, value):
        try:
            v = self._rmap[value]
        except:
            raise PackError("%s is not valid enum" % value)
        return self.T.serialize(v)

    def _unpack_from(self, buf):
        v, rest = self.T.deserialize_from(buf)
        return self._map.get(v, v), rest

    @classmethod
    def get_length(cls):
        return cls.T.length


class MetaEnum(MetaFieldType):
    """
    metaclass to support `Enum[T]` syntax
    """

    __enum_classes = {}

    def __getitem__(self, T):
        if not isinstance(T, MetaFieldType):
            raise SyntaxError("Enum[T]")

        return self._gen_enum(T)

    @classmethod
    def _gen_enum(cls, T):
        if not isinstance(T, MetaFieldType):
            raise TypeError("T should be a FieldType class")

        name = "Enum_{}".format(T.name())
        if name not in cls.__enum_classes:
            cls.__enum_classes[name] = MetaFieldType(
                name, (BaseEnum, ), dict(T=T))
        return cls.__enum_classes[name]


class Enum(object):
    __metaclass__ = MetaEnum

__all__ = ['Enum']
# vim: ts=4 sw=4 sts=4 expandtab
