#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.array_type import Array, PrefixArray
from promarsh.struct_type import Struct
from promarsh.bitstruct_type import EmbeddedBitStruct
from promarsh.container import Container
from promarsh.context import context


class TestStructField(unittest.TestCase):

    def test_struct_deserialization(self):
        MyStruct1 = Struct(
            "f1" << UInt16b,
            'f2' << Array[UInt16b:3],
            'f3' << Struct(
                'ff1' << UInt8b,
            ),
            '' << Struct(
                'ff2' << UInt8b,
            ),
            EmbeddedBitStruct(
                ('R', 1),
                ('ff3', 7),
            ),
        )
        buf = "\x00\x06\x02\x17\x00l\x00c\x09\x10\x05"
        s, _ = MyStruct1.deserialize_from(buf)
        self.assertEqual(s.f1, 6)
        self.assertEqual(s.f2, [535, 108, 99])
        self.assertEqual(s.f3.ff1, 9)
        self.assertEqual(s.ff2, 16)
        self.assertEqual(s.ff3, 5)

    def test_struct_serialization(self):
        MyStruct1 = Struct(
            'f1' << UInt16b,
            'f2' << Array[UInt16b:3],
        )
        container = Container(f1=6, f2=[535, 108, 99])
        self.assertEqual(MyStruct1.serialize(container), "\x00\x06\x02\x17\x00l\x00c")

    def test_struct_array_deserialization(self):
        MyStruct1 = Struct(
            'f1' << UInt16b,
            'f2' << Array[UInt16b:3],
        )
        ArrStruct = Array[MyStruct1:2]

        buf = "\x00\x06\x02\x17\x00l\x00c\x00\x06\x02\x17\x00l\x00c"
        a, _ = ArrStruct.deserialize_from(buf)
        self.assertEqual(a[0].f1, 6)
        self.assertEqual(a[1].f2, [535, 108, 99])

    def test_struct_array_serialization(self):
        MyStruct1 = Struct(
            'f1' << UInt16b,
            'f2' << Array[UInt16b:3],
        )
        ArrStruct = Array[MyStruct1:2]
        c1 = Container(f1=6, f2=[535, 108, 99])
        c2 = Container(f1=7, f2=[535, 108, 100])

        self.assertEqual(
            ArrStruct.serialize([c1, c2]),
            "\x00\x06\x02\x17\x00l\x00c\x00\x07\x02\x17\x00l\x00d"
        )


if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
