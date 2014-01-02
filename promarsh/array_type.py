#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Array type

Author: Justin Wong <justin.w.xd@gmail.com>
"""

from operator import add
from .base_type import FieldType, UnpackError, MetaFieldType
from .integer_type import BaseInteger
from .context import context


class BaseArray(FieldType):
    """
    Array

    Attrs:
        T: Element type
        _count: element counts
        _length: field length in bytes
    """

    T = None
    _count = None
    _length = None

    @classmethod
    def _pack(cls, value):
        return reduce(add, [cls.T._pack(v) for v in value])

    @classmethod
    def _unpack_from(cls, buf):
        lst = []
        count = cls.count()
        if count is not None:
            for _ in xrange(cls.count()):
                v, buf = cls.T._unpack_from(buf)
                lst.append(v)
        else:
            l = cls.length
            field_buf = buf[:l]
            buf = buf[l:]
            while len(field_buf) > 0:
                v, field_buf = cls.T._unpack_from(field_buf)
                lst.append(v)

        return lst, buf

    @classmethod
    def count(cls):
        """
        infer element count from context
        """

        if isinstance(cls._count, int):
            return cls._count
        else:
            if isinstance(cls.T.length, int):
                return cls.length / cls.T.length
            else:
                return None

    @classmethod
    def get_length(cls):
        if isinstance(cls._length, int):
            return cls._length
        elif isinstance(cls._count, int):
            return cls._count * cls.T.length
        else:
            if callable(cls._length):
                return cls._length(context)
            else:
                try:
                    return context.buf_size - context.prev_size - context.rest_size
                except:
                    raise UnpackError("Error inferring packet length from context")


class MetaArray(MetaFieldType):
    """
    metaclass to support `Array[T:count:length]` syntax
    """

    __array_classes = {}

    @classmethod
    def __getitem__(self, _slice):
        if isinstance(_slice, (MetaFieldType, FieldType)):
            T, count, length = _slice, None, None
        elif isinstance(_slice, slice):
            T, count, length = _slice.start, _slice.stop, _slice.step
        return self._gen_array(T, count, length)

    @classmethod
    def _gen_array(cls, T, count=None, length=None):

        if isinstance(count, int):
            N = count
        else:
            if isinstance(length, int):
                N = count / T.length
            else:
                if callable(length):
                    length = staticmethod(length)
                    N = "ctx_{}".format(id(length))
                else:
                    N = "any"

        name = "Array_{}_{}".format(T.name(), N)
        if name not in cls.__array_classes:
            cls.__array_classes[name] = MetaFieldType(
                name, (BaseArray, ), dict(T=T, _count=count, _length=length))
        return cls.__array_classes[name]


class Array(object):
    __metaclass__ = MetaArray


# ----- prefix array -----------

class BasePrefixArray(FieldType):
    """
    Array with a length prefix
    """

    PT = None
    T = None

    @classmethod
    def _pack(cls, value):
        return cls.PT.pack(len(value)*cls.T.length) \
            + reduce(add, [cls.T.pack(v) for v in value])

    @classmethod
    def _unpack_from(cls, buf):
        l, buf = cls.PT._unpack_from(buf)
        lst = []
        for _ in xrange(l/cls.T.length):
            v, buf = cls.T._unpack_from(buf)
            lst.append(v)

        return lst, buf

    @classmethod
    def get_length(cls):
        return None


class MetaPrefixArray(MetaFieldType):
    """
    metaclass to support `PrefixArray[PT:T]` syntax
    """

    __prefix_array_classes = {}

    @classmethod
    def __getitem__(self, _slice):
        if not isinstance(_slice, slice):
            raise SyntaxError("PrefixArray[PT:T]")

        PT, T = _slice.start, _slice.stop
        return self._gen_prefix_array(PT, T)

    @classmethod
    def _gen_prefix_array(cls, PT, T):
        if not issubclass(PT, BaseInteger):
            raise TypeError("PT should be a Integer class")
        if not isinstance(T, (FieldType, MetaFieldType)):
            raise TypeError("T should be a FieldType class")

        name = "PrefixArray_{}_{}".format(PT.name(), T.name())
        if name not in cls.__prefix_array_classes:
            cls.__prefix_array_classes[name] = MetaFieldType(
                name, (BasePrefixArray, ), dict(PT=PT, T=T))
        return cls.__prefix_array_classes[name]


class PrefixArray(object):
    __metaclass__ = MetaPrefixArray

__all__ = ["Array", "PrefixArray"]

# vim: ts=4 sw=4 sts=4 expandtab
