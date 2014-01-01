#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Integer Types

Author: Justin Wong <justin.w.xd@gmail.com>
"""

import struct
from .base_type import FieldType, MetaFieldType


class BaseInteger(FieldType):
    """
    Base Class for integer types

    Attrs:
        _fmt: same as parent
        _length: integer length in bytes
    """

    @classmethod
    def _pack(cls, value):
        """
        Non-user API
        """
        return struct.pack(cls._fmt, value)

    @classmethod
    def _unpack_from(cls, buf):
        """
        Non-user API
        """
        value = struct.unpack_from(cls._fmt, buf)[0]
        return value, buf[cls.length:]


class UInt8b(BaseInteger):
    """ Unsigned 8-bit integer in big endian"""
    _fmt = ">B"
    _length = 1


class UInt8l(BaseInteger):
    """ Signed 8-bit integer in little endian"""
    _fmt = "<B"
    _length = 1


class SInt8b(BaseInteger):
    """ Signed 8-bit integer in big endian"""
    _fmt = ">b"
    _length = 1


class SInt8l(BaseInteger):
    """ Signed 8-bit integer in little endian"""
    _fmt = "<b"
    _length = 1


class UInt16b(BaseInteger):
    """ Unsigned 16-bit integer in big endian"""
    _fmt = ">H"
    _length = 2


class UInt16l(BaseInteger):
    """ Signed 16-bit integer in little endian"""
    _fmt = "<H"
    _length = 2


class SInt16b(BaseInteger):
    """ Signed 16-bit integer in big endian"""
    _fmt = ">h"
    _length = 2


class SInt16l(BaseInteger):
    """ Signed 16-bit integer in little endian"""
    _fmt = "<h"
    _length = 2


class UInt32b(BaseInteger):
    """ Unsigned 32-bit integer in big endian"""
    _fmt = ">I"
    _length = 4


class UInt32l(BaseInteger):
    """ Signed 32-bit integer in little endian"""
    _fmt = "<I"
    _length = 4


class SInt32b(BaseInteger):
    """ Signed 32-bit integer in big endian"""
    _fmt = ">i"
    _length = 4


class SInt32l(BaseInteger):
    """ Signed 32-bit integer in little endian"""
    _fmt = "<i"
    _length = 4


__all__ = [
    "UInt8b", "UInt8l", "SInt8b", "SInt8l",
    "UInt16b", "UInt16l", "SInt16b", "SInt16l",
    "UInt32b", "UInt32l", "SInt32b", "SInt32l",
]
# vim: ts=4 sw=4 sts=4 expandtab
