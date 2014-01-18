#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import six
from types import NoneType
from .base_type import FieldType
from .container import Container, Flags
from .context import context, Bind


class BitField(object):
    _bitlen = 0
    _mask = 0
    _name = ""

    def __init__(self, before_pack=None, after_unpack=None, bind_value=None):
        self._before_pack = before_pack
        self._after_unpack = after_unpack
        if not isinstance(bind_value, (Bind, NoneType)):
            if isinstance(bind_value, tuple):
                self._bind_value = Bind(*bind_value)
            elif isinstance(bind_value, dict):
                self._bind_value = Bind(**bind_value)
            else:
                self._bind_value = Bind(bind_value)
        else:
            self._bind_value = bind_value
        # make class and instance both able to call serialize and
        # deserialize_from method
        self.bit_pack = self.__instance_bit_pack
        self.bit_unpack = self.__instance_bit_unpack

    def _bit_pack(cls, value):
        NotImplemented

    def _bit_unpack(cls, bits):
        NotImplemented

    @classmethod
    def bit_pack(cls, value):
        return cls._bit_pack(value)

    @classmethod
    def bit_unpack(cls, bits):
        return cls._bit_unpack(bits)

    def __instance_bit_pack(self, value):
        if callable(self._before_pack):
            self._before_pack(context, value)

        if callable(self._bind_value):
            value = self._bind_value(context, value)

        return self._bit_pack(value)

    def __instance_bit_unpack(self, bits):
        value = self._bit_unpack(bits)

        if callable(self._after_unpack):
            self._after_unpack(context, value)

        if callable(self._bind_value):
            self._bind_value(context, value, is_setter=True)

        return value

    @classmethod
    def name(cls):
        return cls._name

    def __rlshift__(cls, name):
        return (name, cls)

    def __rdiv__(cls, x):
        return (x, cls)


class BaseBitInt(BitField):
    pass


class _BitPadding(BitField):

    @classmethod
    def _bit_pack(cls, value):
        return 0

    @classmethod
    def _bit_unpack(cls, num):
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
    def _bit_pack(cls, value):
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
    def _bit_unpack(cls, num):
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
    def _bit_pack(cls, value):
        if value not in (0, 1, True, False):
            raise ValueError("BitFlag value should be whether True or False")
        return True if value else False

    @classmethod
    def _bit_unpack(cls, num):
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
        FieldType.__init__(self, **kwargs)
        BitField.__init__(self, **kwargs)

    def _pack(self, container, **kwargs):
        _byte = self.bit_pack(container)

        # transform the merged bit-fields to a big-endian bytes array
        _bytes = []
        for i in xrange(self._length):
            _bytes.append(chr(_byte & 0xFF))
            _byte >>= 8
        _bytes.reverse()

        return ''.join(_bytes)

    def _unpack_from(self, buf, **kwargs):
        _buf = buf[:self._length]
        rest = buf[self._length:]

        # transform buf to a big-endian unsigned integer
        num = 0
        for b in _buf:
            num = (num << 8) + ord(b)

        container = self.bit_unpack(num)
        return container, rest

    def _bit_pack(self, container):
        """
        Packup a container to a number
        """
        _byte = 0
        for fname, offset, ftype in self._fields:
            if not isinstance(ftype, MetaBitPadding):
                v = getattr(container, fname, 0)
                _byte += ftype.bit_pack(v) << offset

        return _byte

    def _bit_unpack(self, num):
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


class BitFlagStruct(BitStruct):
    """
    BitStruct containing only BitFlag fields
    """

    def __init__(self, *flags, **kwargs):
        fields = [flag << BitFlag
                  if isinstance(flag, six.string_types) else flag
                  for flag in flags]

        super(BitFlagStruct, self).__init__(*fields, **kwargs)

    def _bit_unpack(self, num):
        flags = Flags()
        for fname, offset, ftype in self._fields:
            _b = num >> offset
            if not isinstance(ftype, MetaBitPadding):
                flags.set_field(fname, ftype.bit_unpack(_b))

        return flags


__all__ = ['UBitIntb', "BitFlag", "BitPadding", 'BitStruct', 'BitFlagStruct', "EmbeddedBitStruct"]
# vim: ts=4 sw=4 sts=4 expandtab
