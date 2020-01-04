import unittest

import easyb.command
import easyb.message.stream

from easyb.definitions import Length
from easyb.bit import debug_data


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

    def test_stream_1(self):
        data1 = [0, 0, 0]
        data2 = bytes(data1)
        data3 = debug_data(data2)

        stream = easyb.message.stream.Stream(Length.Byte3)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 3)
        self.assertIs(stream.length, Length.Byte3)
        self.assertEqual(stream.data, data1)
        self.assertEqual(stream.bytes, data2)
        self.assertEqual(repr(stream), data3)
        self.assertEqual(str(stream), data3)
        return

    def test_stream_2(self):
        data1 = [0, 0, 0, 0, 0, 0]
        data2 = bytes(data1)
        data3 = debug_data(data2)

        stream = easyb.message.stream.Stream(Length.Byte6)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 6)
        self.assertIs(stream.length, Length.Byte6)
        self.assertEqual(stream.data, data1)
        self.assertEqual(stream.bytes, data2)
        self.assertEqual(repr(stream), data3)
        self.assertEqual(str(stream), data3)
        return

    def test_stream_3(self):
        data1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        data2 = bytes(data1)
        data3 = debug_data(data2)

        stream = easyb.message.stream.Stream(Length.Byte9)

        self.assertIsNotNone(stream)
        self.assertEqual(stream.len, 9)
        self.assertIs(stream.length, Length.Byte9)
        self.assertEqual(stream.data, data1)
        self.assertEqual(stream.bytes, data2)
        self.assertEqual(repr(stream), data3)
        self.assertEqual(str(stream), data3)
        return

    def test_encode_1(self):
        data = [1, 0, 0]

        stream = easyb.message.stream.Stream(Length.Byte3)
        check1 = stream.set_data(data)
        check2 = stream.encode()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertEqual(stream.data, [0xfe, 0, 0x3d])
        return

    def test_encode_2(self):
        data = [0x3, 0xf2, 0x0, 0xca, 0x0, 0x0]

        stream = easyb.message.stream.Stream(Length.Byte6)
        check1 = stream.set_data(data)
        check2 = stream.encode()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertEqual(stream.data, [0xfc, 0xf2, 0xc7, 0x35, 0x0, 0x47])
        return

    def test_encode_3(self):
        data = [0x3, 0xf2, 0x0, 0xca, 0x0]

        stream = easyb.message.stream.Stream(Length.Byte6)
        check1 = stream.set_data(data)
        check2 = stream.encode()

        self.assertFalse(check1)
        self.assertFalse(check2)
        self.assertEqual(stream.data, [0, 0, 0, 0, 0, 0])
        return

    def test_decode_1(self):
        header = [0xfe, 0x05, 0x26]

        stream = easyb.message.stream.Stream(Length.Byte3)

        check1 = stream.decode(bytes(header))
        check2 = stream.verify_length()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertEqual(stream.data, header)
        return

    def test_decode_2(self):
        header = []

        stream = easyb.message.stream.Stream(Length.Byte3)

        check1 = stream.decode(bytes(header))

        self.assertFalse(check1)
        return

    def test_decode_3(self):
        header = [0xfe, 0x05]

        stream = easyb.message.stream.Stream(Length.Byte3)

        check1 = stream.decode(bytes(header))

        self.assertFalse(check1)
        return

    def test_decode_4(self):
        header = [0xfe, 0x05, 0x27]

        stream = easyb.message.stream.Stream(Length.Byte3)

        check1 = stream.decode(bytes(header))

        self.assertFalse(check1)
        return

    def test_set_data_1(self):
        header = [0xfe, 0x05, 0x26]
        data = [0x71, 0x00, 0x48, 0xe3, 0x54, 0x28]
        all_data = [0xfe, 0x05, 0x26, 0x71, 0x00, 0x48, 0xe3, 0x54, 0x28]

        stream = easyb.message.stream.Stream(Length.Byte3)

        check1 = stream.decode(bytes(header))
        check2 = stream.verify_length()

        self.assertTrue(check1)
        self.assertTrue(check2)
        self.assertEqual(stream.data, header)

        stream.append(bytes(data))
        stream.length = Length.Byte9

        check3 = stream.verify_length()
        check4 = stream.verify_crc()

        self.assertTrue(check3)
        self.assertTrue(check4)
        self.assertEqual(stream.data, all_data)
        return

    def test_verify_length_1(self):
        stream = easyb.message.stream.Stream(Length.Byte3)

        stream.data[0] = 1
        stream.data[1] = 0
        stream.data[2] = 0

        check1 = stream.verify_length()

        self.assertTrue(check1)
        return

    def test_verify_length_2(self):
        stream = easyb.message.stream.Stream(Length.Byte3)

        stream.data[0] = 1
        stream.data[1] = 0
        stream.data[2] = 0

        stream.data.append(0)

        check1 = stream.verify_length()

        self.assertFalse(check1)
        return

    def test_verify_length_3(self):
        stream = easyb.message.stream.Stream(Length.Byte3)

        stream._data = []

        check1 = stream.verify_length()

        self.assertFalse(check1)
        return

    def test_verify_length_4(self):
        stream = easyb.message.stream.Stream(Length.Byte3)

        stream.data[0] = 1
        stream.data[1] = 0
        stream.data[2] = 0

        stream.data.append(1)
        stream.data.append(0)
        stream.data.append(0)

        check1 = stream.verify_length()

        self.assertFalse(check1)
        return

    def test_verify_length_5(self):
        stream = easyb.message.stream.Stream(Length.Byte6)

        stream.data[0] = 1
        stream.data[1] = 0
        stream.data[2] = 0
        stream.data[3] = 1
        stream.data[4] = 0
        stream.data[5] = 0

        stream.data.append(1)
        stream.data.append(0)
        stream.data.append(0)

        check1 = stream.verify_length()

        self.assertFalse(check1)
        return

    def test_verify_length_6(self):
        stream = easyb.message.stream.Stream(Length.Byte9)

        stream.data[0] = 1
        stream.data[1] = 0
        stream.data[2] = 0
        stream.data[3] = 1
        stream.data[4] = 0
        stream.data[5] = 0
        stream.data[6] = 1
        stream.data[7] = 0
        stream.data[8] = 0

        stream.data.append(1)
        stream.data.append(0)
        stream.data.append(0)

        check1 = stream.verify_length()

        self.assertFalse(check1)
        return
