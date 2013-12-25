#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Integer Types

Author: Justin Wong <justin.w.xd@gmail.com>
"""

import struct
from .base_type import BaseFieldType
from .context import context


class BaseInteger(BaseFieldType):
    """
    Base Class for integer types

    Attrs:
        fmt: same as parent
        value: integer value
    """

    def __init__(self, value=None, before_pack=None, after_unpack=None):
        self.value = value
        self._before_pack = before_pack
        self._after_unpack = after_unpack

    def serialize(self):
        """Serialize packet to byte string

        Returns:
            pack: binary byte string

        Raises:
            ValueError: raise if value is `None`

        """
        if self.value is None:
            raise ValueError("Field value not set")

        if callable(self._before_pack):
            self._before_pack(context, self.value)

        return self.pack(self.value)

    def deserialize_from(self, buf):
        """unpack value from buffer

        Args:
            buf: a byte string contains binary data

        Returns:
            instance: integer value unpacked from buf
            rest: rest binary data in the buf
        """
        value, buf = self.unpack_from(buf)
        self.value = value

        if callable(self._after_unpack):
            self._after_unpack(context, value)

        return self, buf

    @classmethod
    def pack(cls, value):
        return struct.pack(cls.fmt, value)

    @classmethod
    def unpack_from(cls, buf):
        value = struct.unpack_from(cls.fmt, buf)[0]
        return value, buf[cls.length:]


class UInt8b(BaseInteger):
    """ Unsigned 8-bit integer in big endian"""
    fmt = ">B"
    length = 1


class UInt8l(BaseInteger):
    """ Signed 8-bit integer in little endian"""
    fmt = "<B"
    length = 1


class SInt8b(BaseInteger):
    """ Signed 8-bit integer in big endian"""
    fmt = ">b"
    length = 1


class SInt8l(BaseInteger):
    """ Signed 8-bit integer in little endian"""
    fmt = "<b"
    length = 1


class UInt16b(BaseInteger):
    """ Unsigned 16-bit integer in big endian"""
    fmt = ">H"
    length = 2


class UInt16l(BaseInteger):
    """ Signed 16-bit integer in little endian"""
    fmt = "<H"
    length = 2


class SInt16b(BaseInteger):
    """ Signed 16-bit integer in big endian"""
    fmt = ">h"
    length = 2


class SInt16l(BaseInteger):
    """ Signed 16-bit integer in little endian"""
    fmt = "<h"
    length = 2


class UInt32b(BaseInteger):
    """ Unsigned 32-bit integer in big endian"""
    fmt = ">I"
    length = 4


class UInt32l(BaseInteger):
    """ Signed 32-bit integer in little endian"""
    fmt = "<I"
    length = 4


class SInt32b(BaseInteger):
    """ Signed 32-bit integer in big endian"""
    fmt = ">i"
    length = 4


class SInt32l(BaseInteger):
    """ Signed 32-bit integer in little endian"""
    fmt = "<i"
    length = 4


__all__ = [
    "UInt8b", "UInt8l", "SInt8b", "SInt8l",
    "UInt16b", "UInt16l", "SInt16b", "SInt16l",
    "UInt32b", "UInt32l", "SInt32b", "SInt32l",
]
# vim: ts=4 sw=4 sts=4 expandtab
