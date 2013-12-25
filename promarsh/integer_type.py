#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Integer Types

Author: Justin Wong <justin.w.xd@gmail.com>
"""

import struct
from .base_type import FieldType


class BaseInteger(FieldType):
    """
    Base Class for integer types

    Attrs:
        fmt: same as parent
        length: integer length in bytes
    """

    @classmethod
    def _pack(cls, value):
        """
        Non-user API
        """
        return struct.pack(cls.fmt, value)

    @classmethod
    def _unpack_from(cls, buf):
        """
        Non-user API
        """
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
