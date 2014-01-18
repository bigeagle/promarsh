#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import six
from .base_type import FieldType, MetaFieldType
from .context import context


class _Optional(FieldType):
    T = None

    def __init__(self, rely_on=None, **kwargs):
        if not callable(rely_on):
            raise TypeError("`rely_on` should be callable")

        self._rely_on = rely_on
        super(_Optional, self).__init__(**kwargs)

    def _pack(self, value, **kwargs):
        return self.T.serialize(value) if value is not None else ""

    def _unpack_from(self, buf, **kwargs):
        return self.T.deserialize_from(buf) if self._rely_on(context) else (None, buf)

    @classmethod
    def get_length(cls):
        return cls.T.length


class MetaOptional(MetaFieldType):
    """
    metaclass to support `Optional[T]` syntax
    """

    __types = {}

    @classmethod
    def __getitem__(self, T):
        return self.__call__(T)

    @classmethod
    def __call__(self, T):
        if not isinstance(T, (MetaFieldType, FieldType)):
            raise SyntaxError("Optional[T]")

        return self._gen_enum(T)

    @classmethod
    def _gen_enum(cls, T):
        if not isinstance(T, (MetaFieldType, FieldType)):
            raise TypeError("T should be a FieldType class")

        name = "Optional_{}".format(T.name())
        if name not in cls.__types:
            cls.__types[name] = MetaFieldType(
                name, (_Optional, ), dict(T=T))
        return cls.__types[name]


@six.add_metaclass(MetaOptional)
class Optional(object):
    pass

__all__ = ['Optional']

# vim: ts=4 sw=4 sts=4 expandtab
