#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from .base_type import FieldType, MetaFieldType


def list_to_bytestring(lst):
    """convert a list of int8 to bytestring

    Args:
        lst: a list with int values ranges from 0 to 255

    Raises:
        ValueError: raise if int value is not in range(256)
        TypeError: raise if lst does not contain int
    """

    return ''.join(map(chr, lst))


def serialize(ftype, value):
    if isinstance(ftype, FieldType):
        return ftype.serialize(value)
    elif issubclass(ftype, FieldType):
        return ftype._pack(value)
    else:
        raise TypeError("%s is not valid type" % (ftype))


def deserialize_from(ftype, buf):
    if isinstance(ftype, FieldType):
        return ftype.deserialize_from(buf)
    elif isinstance(ftype, MetaFieldType):
        return ftype._unpack_from(buf)
    else:
        raise TypeError("%s is not valid type" % (ftype))

# vim: ts=4 sw=4 sts=4 expandtab
