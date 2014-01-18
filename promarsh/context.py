#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
Context aware local variable

Author:  Jonathan Gardner
"""

import threading


class Dynamic(object):

    def __init__(self, threadlocal):
        self._threadlocal = threadlocal
        self._threadlocal.dynamic_frame = None

    def __call__(self, **vars):
        return DynamicFrame(self._threadlocal, vars)

    def __getattr__(self, name):
        if not self._threadlocal.dynamic_frame:
            raise NameError("name %r is not defined" % name)

        return getattr(self._threadlocal.dynamic_frame, name)


class DynamicFrame(object):

    def __init__(self, threadlocal, vars):
        self._threadlocal = threadlocal
        self._vars = vars

        self._parent = self._threadlocal.dynamic_frame
        self._threadlocal.dynamic_frame = self
        self._ = self._parent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._threadlocal.dynamic_frame = self._parent

    def __getattr__(self, name):
        try:
            return self._vars[name]
        except KeyError:
            if self._parent:
                return getattr(self._parent, name)
            else:
                raise NameError("name %r is not defined" % name)

    def __setattr__(self, name, value):
        if name in ('_parent', '_vars', '_threadlocal'):
            return object.__setattr__(self, name, value)

        self._vars[name] = value

    def __delattr__(self, name):
        try:
            del self._vars[name]
        except KeyError:
            raise NameError("name %r is not defined" % name)

    def _force_set(self, name, value):
        try:
            setattr(self, name, value)
        except:
            pass

    def set(self, name, value):
        return setattr(self, name, value)

    def clear(self, *attrs):
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
        return None

context = Dynamic(threading.local())


class Bind(object):
    """
    NOTICE: Not Fully Implemented
    """
    def __init__(self, getter, setter=None):
        self.getter = getter
        self.setter = setter

    def __call__(self, ctx, value, is_setter=False):
        if is_setter:
            if self.setter is None:
                return value
            if callable(self.setter):
                return self.setter(ctx, value)
            else:
                return ctx.set(self.setter, value)
        else:
            if callable(self.getter):
                return self.getter(ctx, value)
            else:
                return getattr(ctx, self.getter)


__all__ = ["context", "Bind"]
# vim: ts=4 sw=4 sts=4 expandtab
