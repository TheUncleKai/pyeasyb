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
