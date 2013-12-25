#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Base Field Type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from .context import context


class UnpackError(Exception):
    pass


class BaseFieldType(object):
    """
    Base class for field types

    Attrs:
        fmt: format string for `struct` module
        length: field length in bytes
    """

    fmt = None
    length = None

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
        super(BaseFieldType, self).__init__(*args, **kwargs)

    def serialize(self, value):
        """Serialize packet to byte string

        Returns:
            pack: binary byte string
        """
        if callable(self._before_pack):
            self._before_pack(context, value)

        return self._pack(value)

    def deserialize_from(self, buf):
        """unpack value from buffer

        Args:
            buf: a byte string contains binary data

        Returns:
            instance: integer value unpacked from buf
            rest: rest binary data in the buf
        """
        value, buf = self._unpack_from(buf)

        if callable(self._after_unpack):
            self._after_unpack(context, value)

        return value, buf

# vim: ts=4 sw=4 sts=4 expandtab
