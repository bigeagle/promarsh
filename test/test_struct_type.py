#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.array_type import Array, PrefixArray
from promarsh.struct_type import Struct
from promarsh.container import Container
from promarsh.context import context


class TestArrayField(unittest.TestCase):

    def test_struct_deserialization(self):
        MyStruct1 = Struct(
            ('f1', UInt16b),
            ('f2', Array(UInt16b, count=3)),
            ('f3', Struct(
                ('ff1', UInt8b),
            )),
        )
        buf = "\x00\x06\x02\x17\x00l\x00c\x09"
        s, _ = MyStruct1.deserialize_from(buf)
        self.assertEqual(s.f1, 6)
        self.assertEqual(s.f2, [535, 108, 99])
        self.assertEqual(s.f3.ff1, 9)

    def test_struct_serialization(self):
        MyStruct1 = Struct(
            ('f1', UInt16b),
            ('f2', Array(UInt16b, count=3)),
        )
        container = Container(f1=6, f2=[535, 108, 99])
        self.assertEqual(MyStruct1.serialize(container), "\x00\x06\x02\x17\x00l\x00c")

if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
