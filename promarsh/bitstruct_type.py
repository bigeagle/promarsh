#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import struct
from .base_type import FieldType
from .container import Container


class BaseBitInt(object):
    _bitlen = 0
    _mask = 0

    @classmethod
    def pack(cls, value):
        raise NotImplemented

    @classmethod
    def unpack(cls, bits):
        raise NotImplemented


class MetaBitInt(type):
    __types = {}
    _name = ""
    _base_class = BaseBitInt

    def __getitem__(self, bitlen):
        name = "{0}_{1}".format(self._name, bitlen)
        if name not in self.__types:
            self.__types[name] = type(
                name, (self._base_class, ),
                dict(_bitlen=bitlen, _mask=(2**bitlen-1)))

        return self.__types[name]


class _UBitIntb(BaseBitInt):
    @classmethod
    def pack(cls, value):
        # v = value & cls._mask
        # blen = cls._bitlen
        # _bytes = []
        # while blen > 0:
        #     _bytes.append(v & 0b11111111)
        #     blen -= 8
        #     v >>= 8
        # _bytes.reverse()
        # num = 0
        # for i in _bytes:
        #     num = (num << 8) + i
        # return num
        if value < 0:
            raise ValueError("UBitIntb value should be larger than 0")
        return value

    @classmethod
    def unpack(cls, num):
        """
        Args:
            num: a logically big-endian int
        """
        # value = 0
        # num &= cls._mask
        # i = 0
        # blen = cls._bitlen

        # while blen > 0:
        #     offset = i * 8
        #     value += (num & 0b11111111) << offset
        #     blen -=8
        #     num >>= 8
        #     i += 1

        # return value
        return num & cls._mask


class MetaUBitIntb(MetaBitInt):
    _name = "UIntb"
    _base_class = _UBitIntb


class UBitIntb(BaseBitInt):
    """ Unsigned Integer, big endian"""
    __metaclass__ = MetaUBitIntb


class BitStruct(FieldType):

    def __init__(self, *fields, **kwargs):
        """
        Args:
            *fields: list of (fname, ftype), ftype should be a BitInt class, if int is given, UBitIntb type is assumed
        """

        blen = 0
        for fname, ftype in fields:
            if isinstance(ftype, int):
                ftype = UBitIntb[ftype]
            blen += ftype._bitlen
        self._length = (blen + 8 - 1) // 8  # length in bytes
        _offset = self._length * 8

        self._fields = []
        for fname, ftype in fields:
            if isinstance(ftype, int):
                ftype = UBitIntb[ftype]
            _offset -= ftype._bitlen
            self._fields.append((fname, _offset, ftype))

        self._name = kwargs.pop('name', None)
        super(BitStruct, self).__init__(**kwargs)

    def _pack(self, container):
        _byte = 0
        for fname, offset, ftype in self._fields:
            v = getattr(container, fname, 0)
            _byte += ftype.pack(v) << offset

        # transform the merged bit-fields to a big-endian bytes array
        _bytes = []
        for i in xrange(self._length):
            _bytes.append(chr(_byte & 0xFF))
            _byte >>= 8
        _bytes.reverse()

        return ''.join(_bytes)

    def _unpack_from(self, buf):
        _buf = buf[:self._length]
        rest = buf[self._length:]

        # transform buf to a big-endian unsigned integer
        num = 0
        for b in _buf:
            num = (num << 8) + ord(b)

        container = Container()
        for fname, offset, ftype in self._fields:
            _b = num >> offset
            container.set_field(fname, ftype.unpack(_b))

        return container, rest

    @property
    def length(self):
        return self._length

    def name(self):
        return self._name or "bitstruct-%d" (id(self))


def EmbeddedBitStruct(*args, **kwargs):
    return ("", BitStruct(*args, **kwargs))

__all__ = ['UBitIntb', 'BitStruct', "EmbeddedBitStruct"]
# vim: ts=4 sw=4 sts=4 expandtab
