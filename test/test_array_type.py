import unittest
from promarsh.integer_type import UInt16b, UInt8b
from promarsh.array_type import Array, PrefixArray
from promarsh.context import context


class TestArrayField(unittest.TestCase):

    def test_array_deserialization(self):

        ArrayUInt16b3 = Array(UInt16b, count=3)
        arr, _ = ArrayUInt16b3.deserialize_from("\x02\x17\x00l\x00c")
        self.assertEqual(arr.value, [535, 108, 99])

        with context() as ctx:
            LenField = UInt16b(after_unpack=lambda ctx, v: ctx.set('arr_length', v))
            ArrField = Array(UInt16b, length=lambda ctx: ctx.arr_length)

            buf = "\x00\x06\x02\x17\x00l\x00c\x00\x00"
            l, buf = LenField.deserialize_from(buf)
            arr, _ = ArrField.deserialize_from(buf)
            self.assertEqual(arr.value, [535, 108, 99])

        with context() as ctx:
            ctx.buf_size = 10

            A = Array(UInt16b)
            buf = "\x00\x00\x02\x17\x00l\x00c\x00\x00"
            x, buf = UInt16b.unpack_from(buf)
            self.assertEqual(x, 0)
            ctx.prev_size = 2
            ctx.rest_size = 2
            arr, _ = A.deserialize_from(buf)
            self.assertEqual(arr.value, [535, 108, 99])

        arr, rest = PrefixArray(UInt8b, UInt16b).deserialize_from("\x06\x02\x17\x00l\x00c\x00\x00")
        self.assertEqual(arr.value, [535, 108, 99])
        self.assertEqual(rest, "\x00\x00")

    def test_array_serailization(self):
        ArrayUInt16b3 = Array(UInt16b, count=3, value=[535, 108, 99])
        buf = ArrayUInt16b3.serialize()
        self.assertEqual(buf, "\x02\x17\x00l\x00c")


if __name__ == "__main__":
    unittest.main()
