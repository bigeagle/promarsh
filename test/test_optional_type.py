#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh import Struct, UInt8b, BitStruct, BitFlag, BitPadding, Optional, Container


class TestOptionalField(unittest.TestCase):

    def setUp(self):
        self.MyStruct1 = Struct(
            "f1" << UInt8b,
            "flags" << BitStruct(
                BitPadding[7],
                "OPT" << BitFlag(bind_value=lambda ctx, v: ctx.options is not None),
            ),
            "options" << Optional[
                Struct(
                    "o1" << UInt8b,
                    "o2" << UInt8b
                )
            ](lambda ctx: ctx.flags.OPT),
        )

    def test_optional_field_deserialization(self):

        buf = "\x06\x02\x17\x01"
        s, _ = self.MyStruct1.deserialize_from(buf)
        self.assertEqual(s.flags.OPT, False)
        self.assertEqual(s.options, None)

        buf = "\x06\x01\x17\x01"
        s, _ = self.MyStruct1.deserialize_from(buf)
        self.assertEqual(s.flags.OPT, True)
        self.assertEqual(s.options.o1, 0x17)
        self.assertEqual(s.options.o2, 0x01)

    def test_optional_field_serialization(self):
        packet = Container(
            f1=0x5,
            flags=Container(),
            options=Container(o1=0x12, o2=0x34)
        )

        _bytes = self.MyStruct1.serialize(packet)
        self.assertEqual(_bytes, '\x05\x01\x12\x34')

        packet = Container(
            f1=0x5,
            flags=Container(),
            options=None
        )

        _bytes = self.MyStruct1.serialize(packet)
        self.assertEqual(_bytes, '\x05\x00')


if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
