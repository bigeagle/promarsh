#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Base Field Type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

import six
from types import NoneType
from .context import context, Bind


class UnpackError(Exception):
    pass


class PackError(Exception):
    pass


class _ClassProperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, cls, owner):
        return getattr(cls, self.getter)()


class MetaFieldType(type):
    length = _ClassProperty('get_length')

    def __rlshift__(cls, x):
        return (x, cls)

    def __rdiv__(cls, x):
        return (x, cls)

    def __len__(cls):
        return cls.length


@six.add_metaclass(MetaFieldType)
class BaseFieldType(object):
    """
    Base class for field types

    Attrs:
        fmt: format string for `struct` module
        length: field length in bytes
    """

    _fmt = None
    _length = None

    def __init__(self, *args, **kwargs):
        super(BaseFieldType, self).__init__(*args, **kwargs)

    def serialize(self, value):
        raise NotImplemented

    def deserialize_from(self, buf):
        raise NotImplemented

    def _pack(cls, value):
        raise NotImplemented

    def _unpack_from(cls, buf):
        raise NotImplemented

    def name(cls):
        raise NotImplemented


field_options = ['before_pack', 'after_unpack', 'bind_value']


class FieldType(BaseFieldType):
    """
    Base class for field types

    Attrs:
        fmt: format string for `struct` module
        length: field length in bytes

        _before_pack: function to execute before serializing
        _afeter_unpack: function to execute after serializing
        _bind_value: a Bind instance which save value to context after unpack
                    and get value from context before packing
    """

    def __init__(self, before_pack=None, after_unpack=None, bind_value=None, *args, **kwargs):
        self._before_pack = before_pack
        self._after_unpack = after_unpack
        if not isinstance(bind_value, (Bind, NoneType)):
            if isinstance(bind_value, tuple):
                self._bind_value = Bind(*bind_value)
            elif isinstance(bind_value, dict):
                self._bind_value = Bind(**bind_value)
            else:
                self._bind_value = Bind(bind_value)
        else:
            self._bind_value = bind_value
        # make class and instance both able to call serialize and
        # deserialize_from method
        self.serialize = self.__serialize
        self.deserialize_from = self.__deserialize_from
        super(FieldType, self).__init__(*args, **kwargs)

    @classmethod
    def serialize(cls, value, _before_pack=None, _bind_value=None, **kwargs):
        """Serialize packet to byte string

        Returns:
            pack: binary byte string
        """
        if callable(_before_pack):
            _ret = _before_pack(context, value)
            if _ret is not None:
                value = _ret

        if callable(_bind_value):
            value = _bind_value(context, value)

        return cls._pack(value, **kwargs)

    @classmethod
    def deserialize_from(cls, buf, _after_unpack=None, _bind_value=None, **kwargs):
        """unpack value from buffer

        Args:
            buf: a byte string contains binary data

        Returns:
            instance: integer value unpacked from buf
            rest: rest binary data in the buf
        """
        value, buf = cls._unpack_from(buf, **kwargs)

        if callable(_after_unpack):
            _after_unpack(context, value)

        if callable(_bind_value):
            _bind_value(context, value, is_setter=True)

        return value, buf

    def __serialize(self, value, **kwargs):
        if callable(self._before_pack):
            self._before_pack(context, value)

        if callable(self._bind_value):
            value = self._bind_value(context, value)

        return self._pack(value, **kwargs)

    def __deserialize_from(self, buf, **kwargs):
        value, buf = self._unpack_from(buf, **kwargs)

        if callable(self._after_unpack):
            self._after_unpack(context, value)

        if callable(self._bind_value):
            self._bind_value(context, value, is_setter=True)

        return value, buf

    @classmethod
    def get_length(cls):
        return cls._length

    @classmethod
    def name(cls):
        return cls.__name__

    def __rlshift__(self, x):
        return (x, self)

    def __rdiv__(self, x):
        return (x, self)

# vim: ts=4 sw=4 sts=4 expandtab
