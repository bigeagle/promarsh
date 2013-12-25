#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Array type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from operator import add
from .base_type import BaseFieldType, UnpackError
from .context import context


class Array(BaseFieldType):
    """
    Array

    Attrs:
        fmt: same as parent
        value: tuple value
    """
    fmt = None

    def __init__(self, T, count=None, length=None, value=None,
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
        self.value = value
        self._count = count
        self._length = length
        self._before_pack = before_pack
        self._after_unpack = after_unpack

    def serialize(self):
        if self.value is None:
            raise ValueError("Field value not set")

        if callable(self._before_pack):
            self._before_pack(context, self.value)

        return reduce(add, [self.T.pack(v) for v in self.value])

    def deserialize_from(self, buf):
        lst = []
        for _ in xrange(self.count):
            v, buf = self.T.unpack_from(buf)
            lst.append(v)
        self.value = lst

        if callable(self._after_unpack):
            self._after_unpack(context, self.value)

        return self, buf

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


__all__ = ["Array"]
# vim: ts=4 sw=4 sts=4 expandtab
