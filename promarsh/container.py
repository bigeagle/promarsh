#!/usr/bin/env python2
# -*- coding:utf-8 -*-


class Container(object):
    """
    struct value
    """

    def __init__(self, **kwargs):
        self._fields = []
        for k, v in kwargs.iteritems():
            self.set_field(k, v)

    def set_field(self, name, value):
        self._fields.append(name)
        setattr(self, name, value)
        return self

    def get_field(self, name):
        return getattr(self, name)

    def _items(self):
        return [(name, getattr(self, name)) for name in self._fields]

    def _iteritems(self):
        for name in self.__fields:
            yield (name, getattr(self, name))

    def __str__(self):
        return '{' + ', '.join(
            ["{0}:{1}".format(k, getattr(self, k)) for k in self._fields]) + "}"


class Flags(Container):

    def set_flag(self, name):
        self.set_field(name, True)

    def unset_flag(self, name):
        self.set_field(name, False)

    def __str__(self):
        return '{' + ', '.join([k for k in self._fields if getattr(self, k) is True])+ '}'


class Packet(Container):

    def __str__(self):
        return "{0} | {1}".format(self.header, self.payload)


__all__ = ['Container', 'Packet', 'Flags']
# vim: ts=4 sw=4 sts=4 expandtab
