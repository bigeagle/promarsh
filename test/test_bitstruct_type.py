#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.array_type import Array, PrefixArray
from promarsh.bitstruct_type import BitStruct, UBitIntb, BitPadding
from promarsh.container import Container
from promarsh.context import context


class TestBitStructField(unittest.TestCase):

    def test_bit_integers(self):
        u1 = UBitIntb[13]
        self.assertEqual(u1.bit_unpack((0x01<<8)+(0x02)), 258)
        self.assertEqual(u1.bit_unpack((0xE1<<8)+(0x02)), 258)

    def test_bitstruct_deserialization(self):
        bs = BitStruct(
            'f1' << UBitIntb[4],
            'f2' << UBitIntb[3],
            'f3' << UBitIntb[1],
        )
        buf = '\xdb'
        v, _ = bs.deserialize_from(buf)
        self.assertEqual(v.f1, 13)
        self.assertEqual(v.f2, 5)
        self.assertEqual(v.f3, 1)

        bs = BitStruct(
            'flags' << BitStruct(
                BitPadding[1],
                ('DF', 1),
                ('MF', 1)
            ),
            ('offset', 13),
        )
        buf = '\x61\x02'

        v, _ = bs.deserialize_from(buf)

        self.assertEqual(v.flags.DF, 1)
        self.assertEqual(v.flags.MF, 1)
        self.assertEqual(v.offset, 258)

    def test_bitstruct_serialization(self):
        bs = BitStruct(
            ('f1', 4),
            ('f2', 3),
            ('f3', 1),
        )
        c = Container(f1=13, f2=5, f3=1)
        self.assertEqual(bs.serialize(c), '\xdb')

        bs = BitStruct(
            ('flags', BitStruct(
                ('R', 1),
                ('DF', 1),
                ('MF', 1))),
            ('offset', 13),
        )
        c = Container(flags=Container(R=0, DF=1, MF=1), offset=259)
        self.assertEqual(bs.serialize(c), '\x61\x03')


if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
