import unittest
from promarsh.integer_type import (
    UInt8b, UInt8l, SInt8b, SInt8l,
    UInt16b, UInt16l, SInt16b, SInt16l,
    UInt32b, UInt32l, SInt32b, SInt32l,
)
from promarsh.helpers import list_to_bytestring


class TestIntegerFields(unittest.TestCase):

    def test_integer_deserialization(self):
        v, r = UInt8b.unpack_from(list_to_bytestring([35]))
        self.assertEqual(v, 35)
        self.assertEqual(r, '')

        v, r = UInt8l.unpack_from(list_to_bytestring([35]))
        self.assertEqual(v, 35)
        self.assertEqual(r, '')

        v, r = SInt8b.unpack_from('\xdd')
        self.assertEqual(v, -35)
        self.assertEqual(r, '')

        v, r = SInt8l.unpack_from('\xdd')
        self.assertEqual(v, -35)
        self.assertEqual(r, '')

        v, r = UInt16b.unpack_from('\x02\x17')
        self.assertEqual(v, 535)
        self.assertEqual(r, '')

        v, r = UInt16l.unpack_from('\x17\x02')
        self.assertEqual(v, 535)
        self.assertEqual(r, '')

        v, r = SInt16b.unpack_from('\xf2\x17')
        self.assertEqual(v, -3561)
        self.assertEqual(r, '')

        v, r = SInt16l.unpack_from('\x17\xf2')
        self.assertEqual(v, -3561)
        self.assertEqual(r, '')

        v, r = UInt32b.unpack_from('\xf1\x09\x17\x12')
        self.assertEqual(v, 4043904786)
        self.assertEqual(r, '')

        v, r = UInt32l.unpack_from('\x12\x17\x09\xf1')
        self.assertEqual(v, 4043904786)
        self.assertEqual(r, '')

        v, r = SInt32b.unpack_from('\xf1\x09\x17\x12')
        self.assertEqual(v, -251062510)
        self.assertEqual(r, '')

        v, r = SInt32l.unpack_from('\x12\x17\x09\xf1')
        self.assertEqual(v, -251062510)
        self.assertEqual(r, '')


if __name__ == "__main__":
    unittest.main()
