#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Array type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from operator import add
from .base_type import BaseFieldType, UnpackError
from .integer_type import BaseInteger
from .context import context


class Array(BaseFieldType):
    """
    Array

    Attrs:
        fmt: same as parent
        value: tuple value
    """
    fmt = None

    def __init__(self, T, count=None, length=None,
                 before_pack=None, after_unpack=None):
        """
        Args:
            T: type of elements
            value: field value
        Raises:
            TypeError: raise if T is not a valid class Name
        """
        if not issubclass(T, BaseFieldType):
            raise TypeError("T should be a FieldType class")
        self.T = T
        self._count = count
        self._length = length
        self._before_pack = before_pack
        self._after_unpack = after_unpack

    def serialize(self, value):
        if callable(self._before_pack):
            self._before_pack(context, self.value)

        return self._pack(value)

    def deserialize_from(self, buf):
        lst, buf = self._unpack_from(buf)

        if callable(self._after_unpack):
            self._after_unpack(context, lst)

        return lst, buf

    def _pack(self, value):
        return reduce(add, [self.T._pack(v) for v in value])

    def _unpack_from(self, buf):
        lst = []
        for _ in xrange(self.count):
            v, buf = self.T._unpack_from(buf)
            lst.append(v)

        return lst, buf

    @property
    def count(self):
        """
        infer element count from context
        """

        if isinstance(self._count, int):
            return self._count
        else:
            return self.length / self.T.length

    @property
    def length(self):
        if isinstance(self._length, int):
            return self._length
        else:
            if callable(self._length):
                return self._length(context)
            else:
                try:
                    return context.buf_size - context.prev_size - context.rest_size
                except:
                    raise UnpackError("Error inferring packet length from context")


class PrefixArray(Array):
    """
    Array with a length prefix
    """
    def __init__(self, PT, T, before_pack=None, after_unpack=None):
        if not issubclass(T, BaseFieldType):
            raise TypeError("T should be a FieldType class")
        if not issubclass(PT, BaseInteger):
            raise TypeError("PT should be a Integer class")
        self.PT = PT
        self.T = T
        self._before_pack = before_pack
        self._after_unpack = after_unpack

    def _pack(self, value):
        return self.PT.pack(len(value)*self.T.length) \
            + reduce(add, [self.T.pack(v) for v in value])

    def _unpack_from(self, buf):
        l, buf = self.PT._unpack_from(buf)
        lst = []
        for _ in xrange(l/self.T.length):
            v, buf = self.T._unpack_from(buf)
            lst.append(v)

        return lst, buf

    @property
    def count(self):
        return None

    @property
    def length(self):
        return None

__all__ = ["Array", "PrefixArray"]
# vim: ts=4 sw=4 sts=4 expandtab
