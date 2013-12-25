#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Base Field Type

Author: Justin Wong <justin.w.xd@gmail.com>
"""


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
        pass

    def serialize(self, value):
        raise NotImplemented

    def deserialize_from(cls, buf):
        raise NotImplemented

    def _pack(cls, value):
        raise NotImplemented

    def _unpack_from(cls, buf):
        raise NotImplemented

# vim: ts=4 sw=4 sts=4 expandtab
