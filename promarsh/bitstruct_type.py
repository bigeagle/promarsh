#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from .base_type import FieldType
from .container import Container


class BitField(object):
    _bitlen = 0
    _mask = 0
    _name = ""

    @classmethod
    def bit_pack(cls, value):
        raise NotImplemented

    @classmethod
    def bit_unpack(cls, bits):
        raise NotImplemented

    @classmethod
    def name(cls):
        return cls._name


class BaseBitInt(BitField):
    pass


class _BitPadding(BitField):

    @classmethod
    def bit_pack(cls, value):
        return 0

    @classmethod
    def bit_unpack(cls, num):
        return 0


class MetaBitField(type):
    __types = {}
    _name = ""
    _base_class = BitField

    @classmethod
    def __getitem__(self, bitlen):
        name = "{0}_{1}".format(self._name, bitlen)
        if name not in self.__types:
            self.__types[name] = MetaBitField(
                name, (self._base_class, ),
                dict(_bitlen=bitlen, _mask=(2**bitlen-1), _name=name))

        return self.__types[name]

    def __rlshift__(cls, name):
        return (name, cls)

    def __rdiv__(cls, x):
        return (x, cls)


class _UBitIntb(BaseBitInt):
    @classmethod
    def bit_pack(cls, value):
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
    def bit_unpack(cls, num):
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


class MetaUBitIntb(MetaBitField):
    _name = "UIntb"
    _base_class = _UBitIntb


class UBitIntb(BaseBitInt):
    """ Unsigned Integer, big endian"""
    __metaclass__ = MetaUBitIntb


class BitFlag(BaseBitInt):
    _bitlen = 1
    _mask = 1
    __metaclass__ = MetaBitField

    @classmethod
    def bit_pack(cls, value):
        if value not in (0, 1, True, False):
            raise ValueError("BitFlag value should be whether True or False")
        return True if value else False

    @classmethod
    def bit_unpack(cls, num):
        """
        Args:
            num: a logically big-endian int
        """
        return True if (num & cls._mask) else False


class MetaBitPadding(MetaBitField):
    __types = {}
    _name = "BitPadding"
    _base_class = _BitPadding

    def __getitem__(self, bitlen):
        name = "{0}_{1}".format(self._name, bitlen)
        if name not in self.__types:
            self.__types[name] = MetaBitPadding(
                name, (self._base_class, ),
                dict(_bitlen=bitlen, _mask=(2**bitlen-1)))

        return ("", self.__types[name])

        return self.__call__(bitlen)


class BitPadding(BitField):
    __metaclass__ = MetaBitPadding


class BitStruct(FieldType, BitField):

    def __init__(self, *fields, **kwargs):
        """
        Args:
            *fields: list of (fname, ftype), ftype should be a BitInt class, if int is given, UBitIntb type is assumed
        """

        self._bitlen = 0
        for fname, ftype in fields:
            if isinstance(ftype, int):
                ftype = UBitIntb[ftype]
            self._bitlen += ftype._bitlen

        self._mask = 2 ** self._bitlen - 1
        self._length = (self._bitlen + 8 - 1) // 8  # length in bytes
        _offset = self._bitlen

        self._fields = []
        for fname, ftype in fields:
            if isinstance(ftype, int):
                ftype = UBitIntb[ftype]
            _offset -= ftype._bitlen
            self._fields.append((fname, _offset, ftype))

        self._name = kwargs.pop('name', None)
        super(BitStruct, self).__init__(**kwargs)

    def _pack(self, container):
        _byte = self.bit_pack(container)

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

        container = self.bit_unpack(num)
        return container, rest

    def bit_pack(self, container):
        """
        Packup a container to a number
        """
        _byte = 0
        for fname, offset, ftype in self._fields:
            if not isinstance(ftype, MetaBitPadding):
                v = getattr(container, fname, 0)
                _byte += ftype.bit_pack(v) << offset

        return _byte

    def bit_unpack(self, num):
        """
        Unpack from an unsigned integer
        """
        container = Container()
        for fname, offset, ftype in self._fields:
            _b = num >> offset
            if not isinstance(ftype, MetaBitPadding):
                container.set_field(fname, ftype.bit_unpack(_b))

        return container

    @property
    def length(self):
        return self._length

    def name(self):
        return self._name or "bitstruct-%d" (id(self))


def EmbeddedBitStruct(*args, **kwargs):
    return ("", BitStruct(*args, **kwargs))


__all__ = ['UBitIntb', "BitFlag", "BitPadding", 'BitStruct', "EmbeddedBitStruct"]
# vim: ts=4 sw=4 sts=4 expandtab
