#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import six
from .base_type import FieldType, PackError, MetaFieldType, field_options
from .bitstruct_type import BitField, MetaBitField


class BaseEnum(FieldType, BitField):

    T = None

    def __init__(self, *enum, **kwargs):
        _options = {}
        for k in field_options:
            _options[k] = kwargs.pop(k, None)

        enums = list(enum) + kwargs.items()

        self._map = dict([(v, k) for k, v in enums])
        self._rmap = dict(enums)

        super(BaseEnum, self).__init__(**_options)

    def _pack(self, value):
        try:
            v = self._rmap[value]
        except:
            raise PackError("%s is not valid enum" % value)
        return self.T.serialize(v)

    def _unpack_from(self, buf):
        v, rest = self.T.deserialize_from(buf)
        return self._map.get(v, v), rest

    def _bit_pack(self, value):
        try:
            v = self._rmap[value]
        except:
            raise PackError("%s is not valid enum" % value)
        return self.T.bit_pack(v)

    def _bit_unpack(self, value):
        v = self.T.bit_unpack(value)
        return self._map.get(v, v)

    @classmethod
    def get_length(cls):
        return cls.T.length


class MetaEnum(MetaFieldType):
    """
    metaclass to support `Enum[T]` syntax
    """

    __enum_classes = {}

    @classmethod
    def __getitem__(self, T):
        if not isinstance(T, (MetaFieldType, MetaBitField)):
            raise SyntaxError("Enum[T]")

        return self._gen_enum(T)

    @classmethod
    def _gen_enum(cls, T):
        if not isinstance(T, (MetaFieldType, MetaBitField)):
            raise TypeError("T should be a FieldType class")

        name = "Enum_{}".format(T.name())
        if name not in cls.__enum_classes:
            cls.__enum_classes[name] = MetaFieldType(
                name, (BaseEnum, ), dict(T=T))
        return cls.__enum_classes[name]


@six.add_metaclass(MetaEnum)
class Enum(object):
    pass

__all__ = ['Enum']
# vim: ts=4 sw=4 sts=4 expandtab
