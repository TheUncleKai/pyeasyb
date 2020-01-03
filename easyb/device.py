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

import time
import abc
import easyb
import serial

from serial import Serial
from typing import List, Union

from easyb.bit import debug_data
from easyb.message import Message
from easyb.command import Command
from easyb.definitions import Length

from abc import ABCMeta


class Device(metaclass=ABCMeta):

    port = ""
    baudrate = 0
    timeout = 2
    write_timeout = 2
    address = 0
    wait_time = 0.0
    counter = 0

    def __init__(self, **kwargs):
        self._name = ""

        item = kwargs.get("name", "")
        if item is not None:
            self._name = item

        item = kwargs.get("port", "")
        if item is not None:
            self.port = item

        item = kwargs.get("address", 0)
        if item is not None:
            self.address = item

        item = kwargs.get("wait_time", 0.1)
        if item is not None:
            self.wait_time = item

        item = kwargs.get("baudrate", 4800)
        if item is not None:
            self.baudrate = item

        item = kwargs.get("timeout", 2)
        if item is not None:
            self.timeout = item

        item = kwargs.get("write_timeout", 2)
        if item is not None:
            self.write_timeout = item

        self._commands = []
        self._command_list = []
        self._serial = None

        self.init_commands()
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def serial(self) -> Serial:
        return self._serial

    @property
    def commands(self) -> List[Command]:
        return self._commands

    @property
    def command_list(self) -> List[int]:
        return self._command_list

    def get_command(self, number: int) -> Union[None, Command]:
        command = None

        for item in self.commands:
            if item.number == number:
                command = item

        if command is None:
            easyb.log.error("Command number is unknown: " + str(number))

        return command

    def setup(self):
        # baudrate: int = 4800, timeout: int = 6, write_timeout: int = 2

        ser = Serial(baudrate=self.baudrate,
                     bytesize=serial.EIGHTBITS,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     timeout=self.timeout,
                     xonxoff=0,
                     rtscts=0,
                     dsrdtr=0,
                     interCharTimeout=None,
                     writeTimeout=self.write_timeout)
        self._serial = ser
        return

    def connect(self) -> bool:
        """Open serial connection

        :return: True if successfull, otherwise false
        :rtype: bool
        """

        if self.port == "":
            easyb.log.error("Port is missing/not configured!")
            return False

        if self.serial is None:
            easyb.log.error("Serial port is not set up!")
            return False

        easyb.log.debug1(self.name, "Port:          {0:s}".format(self.port))
        easyb.log.debug1(self.name, "Baudrate:      {0:d}".format(self.baudrate))
        easyb.log.debug1(self.name, "Address:       {0:d}".format(self.address))
        easyb.log.debug1(self.name, "Timeout:       {0:d}".format(self.timeout))
        easyb.log.debug1(self.name, "Write timeout: {0:d}".format(self.write_timeout))

        self.serial.port = self.port

        try:
            self.serial.open()
        except serial.SerialException as e:
            easyb.log.error("Problem during opening of serial port!")
            easyb.log.exception(e)
            return False

        easyb.log.inform(self.name, "Establish connection to {0:s}".format(self.port))
        return True

    def disconnect(self):
        """Close serial connection
        """

        if self.serial is None:
            easyb.log.error("Serial port is not set up!")
            return

        if self.serial.is_open is False:
            easyb.log.warn(self.name, "Connection to {0:s} is already closed!".format(self.port))
            return

        self.serial.close()
        easyb.log.inform(self.name, "Disconnect from {0:s}".format(self.port))
        return

    def send(self, message: Message) -> bool:

        stream = message.encode()

        if message.success is False:
            return False

        debug = debug_data(stream)

        debug2 = "Address " + str(message.address) + ", Code: " + str(message.code)
        debug2 += ", " + message.priority.name
        debug2 += ", " + message.length.name
        debug2 += ", " + message.direction.name

        easyb.log.debug2("SERIAL", debug2)
        easyb.log.debug1("SERIAL", "Write: " + debug)

        try:
            self.serial.write(stream)
        except serial.SerialException as e:
            easyb.log.error("Problem during write to serial port!")
            easyb.log.exception(e)
            return False

        return True

    def read_unit_timeout(self) -> bytes:
        result = []

        while True:
            check = False
            try:
                _in = self.serial.read()

                for item in _in:
                    check = True
                    value = int(item)
                    result.append(value)

            except serial.SerialException as e:
                easyb.log.error("Problem during reading of message body!")
                easyb.log.exception(e)
                break

            if check is False:
                break

        res = bytes(result)
        return res

    def receive(self) -> Union[None, Message]:
        try:
            header = self.serial.read(3)
        except serial.SerialException as e:
            easyb.log.error("Problem during reading of message header!")
            easyb.log.exception(e)
            return None

        debug = debug_data(header)
        easyb.log.debug1("SERIAL", "Header: {0:s}".format(debug))

        message = Message()
        message.decode(header)

        if message.code == 5:
            easyb.log.warn(self.name, "Command not supported!")
            return None

        if message.success is False:
            return None

        message.info()

        number = 0

        if message.length is Length.Byte6:
            number = 3

        if message.length is Length.Byte9:
            number = 6

        if message.length is Length.Variable:
            number = -1

        if number == 0:
            message.info()
            easyb.log.warn(self.name, "Message body has no size!")
            message.data = header
            return message

        if number == -1:
            message.info()
            easyb.log.warn(self.name, "Message body is variable!")
            data = self.read_unit_timeout()
        else:
            try:
                data = self.serial.read(number)
            except serial.SerialException as e:
                easyb.log.error("Problem during reading of message body!")
                easyb.log.exception(e)
                return None

        debug = debug_data(data)
        easyb.log.debug1("SERIAL", "{0:s}: {1:s}".format(message.length.name, debug))
        message.data = data
        return message

    def execute(self, command: Command) -> Union[None, Message]:
        message = Message()
        message.command(command)

        check = self.send(message)
        if check is False:
            return None

        time.sleep(self.wait_time)

        data = self.receive()
        if data is None:
            return None

        if data.success is False:
            return None

        return data

    def run_command(self, number: int) -> bool:
        command = self.get_command(number)

        if command is None:
            return False

        easyb.log.inform(self.name, "Run {0:d}: {1:s}".format(command.number, command.name))

        message = self.execute(command)
        if message is None:
            return False

        check = command.call(message)
        return check

    def default_command(self, message: Message):
        if message.length is Length.Byte6:
            message.value_16()

        if message.length is Length.Byte9:
            message.value_32()

        if message.value is None:
            easyb.log.warn(self.name, "No value!")
            return False

        easyb.log.inform(self.name, str(message.value))
        return True

    def list_commands(self):
        for command in self.commands:
            easyb.log.inform(self.name, "Command {0:d}: {1:s}".format(command.number, command.name))
        return

    def add_command(self, command: Command):
        command.number = self.counter
        command.address = self.address
        self.commands.append(command)
        self.command_list.append(command.number)
        self.counter += 1
        return

    @abc.abstractmethod
    def init_commands(self):
        return

    @abc.abstractmethod
    def prepare(self) -> bool:
        return True

    @abc.abstractmethod
    def run(self) -> bool:
        return True

    @abc.abstractmethod
    def close(self) -> bool:
        return True
