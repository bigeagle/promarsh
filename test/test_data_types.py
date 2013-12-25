import unittest
from promarsh.integers import (
    UInt8b, UInt8l, SInt8b, SInt8l,
    UInt16b, UInt16l, SInt16b, SInt16l,
    UInt32b, UInt32l, SInt32b, SInt32l,
)
from promarsh.helpers import list_to_bytestring


class TestFieldDeserialization(unittest.TestCase):

    def test_integers(self):
        f = UInt8b()
        v, r = f.deserialize_from(list_to_bytestring([35]))
        self.assertEqual(v, 35)
        self.assertEqual(r, '')

        f = UInt8l()
        v, r = f.deserialize_from(list_to_bytestring([35]))
        self.assertEqual(v, 35)
        self.assertEqual(r, '')

        f = SInt8b()
        v, r = f.deserialize_from('\xdd')
        self.assertEqual(v, -35)
        self.assertEqual(r, '')

        f = SInt8l()
        v, r = f.deserialize_from('\xdd')
        self.assertEqual(v, -35)
        self.assertEqual(r, '')

        f = UInt16b()
        v, r = f.deserialize_from('\x02\x17')
        self.assertEqual(v, 535)
        self.assertEqual(r, '')

        f = UInt16l()
        v, r = f.deserialize_from('\x17\x02')
        self.assertEqual(v, 535)
        self.assertEqual(r, '')

        f = SInt16b()
        v, r = f.deserialize_from('\xf2\x17')
        self.assertEqual(v, -3561)
        self.assertEqual(r, '')

        f = SInt16l()
        v, r = f.deserialize_from('\x17\xf2')
        self.assertEqual(v, -3561)
        self.assertEqual(r, '')

        f = UInt32b()
        v, r = f.deserialize_from('\xf1\x09\x17\x12')
        self.assertEqual(v, 4043904786)
        self.assertEqual(r, '')

        f = UInt32l()
        v, r = f.deserialize_from('\x12\x17\x09\xf1')
        self.assertEqual(v, 4043904786)
        self.assertEqual(r, '')

        f = SInt32b()
        v, r = f.deserialize_from('\xf1\x09\x17\x12')
        self.assertEqual(v, -251062510)
        self.assertEqual(r, '')

        f = SInt32l()
        v, r = f.deserialize_from('\x12\x17\x09\xf1')
        self.assertEqual(v, -251062510)
        self.assertEqual(r, '')


if __name__ == "__main__":
    unittest.main()
