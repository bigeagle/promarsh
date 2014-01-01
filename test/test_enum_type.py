#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import unittest
from promarsh.base_type import PackError
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.array_type import Array, PrefixArray
from promarsh.struct_type import Struct
from promarsh.enum_type import Enum
from promarsh.container import Container
from promarsh.context import context


class TestEnumField(unittest.TestCase):

    def test_enum_deserialization(self):
        opcode = Enum[UInt8b](
            ("OP1", 0xf1),
            ("OP2", 0xf2),
            ("OP3", 0x03),
        )
        buf = "\xf1\xf2\x03"
        o, buf = opcode.deserialize_from(buf)
        self.assertEqual(o, "OP1")
        o, buf = opcode.deserialize_from(buf)
        self.assertEqual(o, "OP2")
        o, buf = opcode.deserialize_from(buf)
        self.assertEqual(o, "OP3")

    def test_enum_serialization(self):
        opcode = Enum[UInt8b](
            ("OP1", 0xf1),
            ("OP2", 0xf2),
            ("OP3", 0x03),
        )
        self.assertEqual(opcode.serialize("OP1"), "\xf1")
        self.assertEqual(opcode.serialize("OP3"), "\x03")
        self.assertRaises(PackError, opcode.serialize, "NOT")

if __name__ == "__main__":
    unittest.main()
# vim: ts=4 sw=4 sts=4 expandtab
