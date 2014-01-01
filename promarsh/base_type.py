#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Base Field Type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from .context import context


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


class BaseFieldType(object):
    """
    Base class for field types

    Attrs:
        fmt: format string for `struct` module
        length: field length in bytes
    """
    __metaclass__ = MetaFieldType

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


class FieldType(BaseFieldType):
    """
    Base class for field types

    Attrs:
        fmt: format string for `struct` module
        length: field length in bytes

        _before_pack: function to execute before serializing
        _afeter_unpack: function to execute after serializing
    """

    def __init__(self, before_pack=None, after_unpack=None, *args, **kwargs):
        self._before_pack = before_pack
        self._after_unpack = after_unpack
        # make class and instance both able to call serialize and
        # deserialize_from method
        self.serialize = self.__serialize
        self.deserialize_from = self.__deserialize_from
        super(BaseFieldType, self).__init__(*args, **kwargs)

    @classmethod
    def serialize(cls, value, _before_pack=None):
        """Serialize packet to byte string

        Returns:
            pack: binary byte string
        """
        if callable(_before_pack):
            _before_pack(context, value)

        return cls._pack(value)

    @classmethod
    def deserialize_from(cls, buf, _after_unpack=None):
        """unpack value from buffer

        Args:
            buf: a byte string contains binary data

        Returns:
            instance: integer value unpacked from buf
            rest: rest binary data in the buf
        """
        value, buf = cls._unpack_from(buf)

        if callable(_after_unpack):
            _after_unpack(context, value)

        return value, buf

    def __serialize(self, value):
        if callable(self._before_pack):
            self._before_pack(context, value)

        return self._pack(value)

    def __deserialize_from(self, buf):
        value, buf = self._unpack_from(buf)

        if callable(self._after_unpack):
            self._after_unpack(context, value)

        return value, buf

    @classmethod
    def get_length(cls):
        return cls._length

    @classmethod
    def name(cls):
        return cls.__name__

# vim: ts=4 sw=4 sts=4 expandtab
