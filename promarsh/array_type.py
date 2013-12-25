#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Array type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from operator import add
from .base_type import FieldType, UnpackError
from .integer_type import BaseInteger
from .context import context


class Array(FieldType):
    """
    Array

    Attrs:
        fmt: same as parent
        count: element counts
        length: field length in bytes
    """

    def __init__(self, T, count=None, length=None, *args, **kwargs):
        """
        Args:
            T: type of elements
            value: field value
        Raises:
            TypeError: raise if T is not a valid class Name
        """
        if not issubclass(T, FieldType):
            raise TypeError("T should be a FieldType class")
        self.T = T
        self._count = count
        self._length = length
        super(Array, self).__init__(*args, **kwargs)

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


class PrefixArray(FieldType):
    """
    Array with a length prefix
    """
    def __init__(self, PT, T, *args, **kwargs):
        if not issubclass(T, FieldType):
            raise TypeError("T should be a FieldType class")
        if not issubclass(PT, BaseInteger):
            raise TypeError("PT should be a Integer class")
        self.PT = PT
        self.T = T
        super(PrefixArray, self).__init__(*args, **kwargs)

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

__all__ = ["Array", "PrefixArray"]
# vim: ts=4 sw=4 sts=4 expandtab
