#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.enum_type import Enum
from promarsh.bitstruct_type import *
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
            'f2' << Enum[UBitIntb[3]](
                E1=5,
                E2=3,
            ),
            'f3' << UBitIntb[1],
        )
        buf = '\xdb'
        v, _ = bs.deserialize_from(buf)
        self.assertEqual(v.f1, 13)
        self.assertEqual(v.f2, 'E1')
        self.assertEqual(v.f3, 1)

        bs = BitStruct(
            'flags' << BitStruct(
                BitPadding[1],
                'DF' << BitFlag,
                'MF' << BitFlag,
            ),
            ('offset', 13),
        )
        buf = '\x41\x02'

        v, _ = bs.deserialize_from(buf)

        self.assertEqual(v.flags.DF, True)
        self.assertEqual(v.flags.MF, False)
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
            'flags' << BitStruct(
                BitPadding[1],
                'DF' << BitFlag,
                'MF' << BitFlag,
            ),
            ('offset', 13),
        )
        c = Container(flags=Container(DF=True, MF=False), offset=259)
        self.assertEqual(bs.serialize(c), '\x41\x03')


if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
