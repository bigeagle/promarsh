#!/usr/bin/env python2
# -*- coding:utf-8 -*-


class Container(object):
    """
    struct value
    """

    def __init__(self, **kwargs):
        self.__fields = []
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def set_field(self, name, value):
        self.__fields.append(name)
        setattr(self, name, value)

    def get_field(self, name):
        return getattr(self, name)

    def __str__(self):
        return ','.join(
            ["{0}:{1}".format(k, getattr(self, k)) for k in self.__fields])

# vim: ts=4 sw=4 sts=4 expandtab
