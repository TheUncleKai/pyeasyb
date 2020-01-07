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
from easyb.bit import decode_u32
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
    "TestSerial"
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

        error, value = decode_u32(data[3], data[4], data[6], data[7])

        if error is not None:
            easyb.log.warn(self.name, "Error: {0:s}".format(error.text))
        else:
            debug = "{0:.2f}".format(value)
            easyb.log.inform(self.name, debug)

        self.error = error
        self.value = value
        return True

    def prepare(self) -> bool:
        return True

    def run(self) -> bool:
        command = self.get_command(0)

        message = self.execute(command)
        if message is None:
            return False

        data = message.stream.data
        error, value = decode_u32(data[3], data[4], data[6], data[7])

        row = self.create_row()

        if error is not None:
            easyb.log.warn(self.name, "Error: {0:s}".format(error.text))
            row.value = 0.0
            row.error = error.text
        else:
            row.value = value
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

    def __init__(self):
        self.read_run: int = 0
        self.read_data: List[List[int]] = []

        self.write_run: int = 0
        self.write_data: List[List[int]] = []

        # noinspection PyTypeChecker
        self.read_exception: TestException = None

        # noinspection PyTypeChecker
        self.write_exception: TestException = None
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
