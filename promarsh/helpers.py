#!/usr/bin/env python2
# -*- coding:utf-8 -*-


def list_to_bytestring(lst):
    """convert a list of int8 to bytestring

    Args:
        lst: a list with int values ranges from 0 to 255

    Raises:
        ValueError: raise if int value is not in range(256)
        TypeError: raise if lst does not contain int
    """

    return ''.join(map(chr, lst))


# vim: ts=4 sw=4 sts=4 expandtab
