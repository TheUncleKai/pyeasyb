import unittest

from easyb.definitions import Length
from easyb.bit import debug_data
from easyb.message.stream import Stream

__all__ = [
    "TestStream"
]


# noinspection DuplicatedCode
class TestStream(unittest.TestCase):
    """Testing class for message coding and decoding module."""

    def setUp(self):
        """set up test.
        """
        return

    def tearDown(self):
        """tear down test.
        """
        return

    def test_stream(self):
        stream = Stream(Length.Byte3)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 0)
        return

    def test_expand_data(self):
        stream = Stream(Length.Byte3)
        stream.expand_data(3)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 3)
        return

    def test_set_data_1(self):
        data1 = [0, 0, 0, 0, 0, 0]
        data2 = bytes(data1)
        data3 = debug_data(data2)

        stream = Stream(Length.Byte6)

        check = stream.set_data(data1)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 6)
        self.assertTrue(check)

        self.assertIs(stream.length, Length.Byte6)
        self.assertEqual(stream.data, data1)
        self.assertEqual(stream.bytes, data2)
        self.assertEqual(repr(stream), data3)
        self.assertEqual(str(stream), data3)
        return

    def test_set_data_2(self):
        data1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        data2 = bytes(data1)
        data3 = debug_data(data2)

        stream = Stream(Length.Variable)

        check = stream.set_data(data1)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 12)
        self.assertTrue(check)

        self.assertIs(stream.length, Length.Variable)
        self.assertEqual(stream.data, data1)
        self.assertEqual(stream.bytes, data2)
        self.assertEqual(repr(stream), data3)
        self.assertEqual(str(stream), data3)
        return

    def test_set_data_3(self):
        data1 = [0, 0, 0, 0, 0, 0]

        stream = Stream(Length.Byte3)
        stream.expand_data(3)

        check = stream.set_data(data1)

        self.assertFalse(check)
        return

    def test_append_1(self):
        stream = Stream(Length.Byte3)

        check = stream.append(bytes([0xfe, 0x0d, 0x1e]))
        self.assertTrue(check)
        return

    def test_append_2(self):
        stream = Stream(Length.Byte3)

        check = stream.append(bytes([0xfe, 0x0d]))
        self.assertFalse(check)
        return

    def test_append_3(self):
        stream = Stream(Length.Byte3)

        check = stream.append(bytes([0xfc, 0x0d, 0x1e]))
        self.assertFalse(check)
        return

    def test_append_4(self):
        stream = Stream(Length.Byte3)

        check = stream.append(bytes([]))
        self.assertFalse(check)
        return

    def test_verify_length_1(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        stream = Stream(Length.Byte9)
        stream.data = data

        check = stream.verify_length()
        self.assertTrue(check)
        return

    def test_verify_length_2(self):
        data = []

        stream = Stream(Length.Byte9)
        stream.data = data

        check = stream.verify_length()
        self.assertFalse(check)
        return

    def test_verify_length_3(self):
        data = [0xfe, 0x0d]

        stream = Stream(Length.Byte9)
        stream.data = data

        check = stream.verify_length()
        self.assertFalse(check)
        return

    def test_verify_length_4(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        stream = Stream(Length.Byte3)
        stream.data = data

        check = stream.verify_length()
        self.assertFalse(check)
        return

    def test_verify_length_5(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        stream = Stream(Length.Byte6)
        stream.data = data

        check = stream.verify_length()
        self.assertFalse(check)
        return

    def test_verify_length_6(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84]

        stream = Stream(Length.Byte9)
        stream.data = data

        check = stream.verify_length()
        self.assertFalse(check)
        return

    def test_encode_1(self):
        data = [0x1, 0x0d, 0, 0x8d, 0xff, 0, 0x8d, 0xff, 0]
        data_check = [254, 13, 30, 114, 255, 132, 114, 255, 132]

        stream = Stream(Length.Byte9)
        stream.set_data(data)

        check = stream.encode()
        self.assertTrue(check)
        self.assertEqual(stream.data, data_check)
        return

    def test_encode_2(self):
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        stream = Stream(Length.Byte9)
        stream.set_data(data)

        check = stream.encode()
        self.assertFalse(check)
        return

    def test_encode_3(self):
        stream = Stream(Length.Byte9)

        check = stream.encode()
        self.assertFalse(check)
        return

    def test_decode_1(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84, 0x00, 0xfc, 0x05]

        stream = Stream(Length.Byte9)
        check = stream.decode(bytes(data))
        self.assertTrue(check)
        return

    def test_decode_2(self):
        data = []

        stream = Stream(Length.Byte9)
        check = stream.decode(bytes(data))
        self.assertFalse(check)
        return

    def test_decode_3(self):
        data = [0xfe, 0x0d, 0x1e, 0x72, 0xff, 0x84, 0x00, 0xfc]

        stream = Stream(Length.Byte9)
        check = stream.decode(bytes(data))
        self.assertFalse(check)
        return
