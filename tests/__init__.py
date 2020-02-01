#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

from typing import List

import easyb

from easyb.data.base import Type
from easyb.command import Command
from easyb.device import Device
from easyb.message import Message
from easyb.bit import Value
from easyb.definitions import Error

__all__ = [
    "bit",
    "console",
    "device",
    "gmh3710",
    "message",
    "stream",

    "TestDevice",
    "TestException",
    "TestSerial",
    "TestOptions"
]


class TestDevice(Device):

    def __init__(self, **kwargs):
        Device.__init__(self, name="TEST-DEVICE", wait_time=0.1, address=1, **kwargs)

        self.value: float = 0.0

        # noinspection PyTypeChecker
        self.message: Message = None

        # noinspection PyTypeChecker
        self.error: Error = None

        self.data.add_column("value", "Temperature", Type.float)
        self.data.add_column("error", "Error", Type.string)
        return

    def init_commands(self):

        command = Command(name="Messwert lesen", code=0, func_call=self.read_messwert)
        self.add_command(command)
        return

    def read_messwert(self, message: Message) -> bool:
        self.message = message

        if self.message.stream is None:
            return False

        data = message.stream.data
        bitio = Value(data=data)

        check = bitio.decode32()

        if check is False:
            easyb.log.warn(self.name, "Error: {0:s}".format(bitio.error.text))
        else:
            debug = "{0:.2f}".format(bitio.value)
            easyb.log.inform(self.name, debug)

        self.error = bitio.error
        self.value = bitio.value
        return True

    def prepare(self) -> bool:
        return True

    def run(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        data = message.stream.data
        bitio = Value(data=data)

        check = bitio.decode32()
        row = self.create_row()

        if check is False:
            easyb.log.warn(self.name, "Error: {0:s}".format(bitio.error.text))
            row.value = 0.0
            row.error = bitio.error.text
        else:
            row.value = bitio.value
            row.error = ""
            debug = "{0:06d} {1:s}: {2:.2f}".format(self.interval_counter, row.datetime.strftime("%H:%M:%S"), row.value)
            easyb.log.inform(self.name, debug)
        return True

    def close(self) -> bool:
        length = len(self.data.rows)

        if length == 0:
            return False

        return True


class TestException(object):

    def __init__(self, number: int, exception: Exception):
        self.run: int = number

        # noinspection PyTypeChecker
        self.exception: Exception = exception
        return


class TestSerial(object):

    def __init__(self, **kwargs):
        self.is_open = False

        self.read_run: int = 0
        self.read_data: List[List[int]] = []

        self.write_run: int = 0
        self.write_data: List[List[int]] = []

        # noinspection PyTypeChecker
        self.read_exception: TestException = None

        # noinspection PyTypeChecker
        self.write_exception: TestException = None
        return

    def open(self):
        self.is_open = True
        return

    def write(self, data: bytes):
        if self.write_exception is not None:
            if self.write_exception.run == self.write_run:
                raise self.write_exception.exception

        run_list = []
        for item in data:
            run_list.append(int(item))
        self.write_data.append(run_list)
        self.write_run += 1
        return

    # noinspection PyUnusedLocal
    def read(self, count: int = 0) -> bytes:
        if self.read_exception is not None:
            if self.read_exception.run == self.read_run:
                raise self.read_exception.exception

        data = self.read_data[self.read_run]
        result = bytes(data)
        self.read_run += 1
        return result


class TestOptions(object):

    def __init__(self):
        self.verbose = 2
        self.read = False
        self.list = False
        self.interval = 2.0

        self.device = ""
        self.command = 0

        self.port = ""
        self.baudrate = 4800
        self.timeout = 2
        self.writetimeout = 2

        self.output = "none"
        self.filename = "measurement"
        return

    def test_1(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 2
        return

    def test_2(self):
        self.port = "TEST"

    def test_3(self):
        self.port = "TEST"
        self.device = "GMH"

    def test_4(self):
        self.port = "TEST"
        self.device = "GMH 3710"
        self.command = None

    def test_5(self):
        self.port = "TEST"
        self.device = "GMH 3710"
        self.command = 22

    def test_6(self):
        self.list = True

    def test_7(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = ""
        self.verbose = 2

    def test_8(self):
        self.device = "GMH 3710"
        self.command = 0
        self.port = "TEST"
        self.verbose = 2
        self.read = True
