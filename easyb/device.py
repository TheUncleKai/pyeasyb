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

from easyb.message import Message
from easyb.command import Command
from easyb.definitions import Length

from abc import ABCMeta


class Device(metaclass=ABCMeta):

    def __init__(self, name: str, wait_time: float = 0.01):
        """Control constructor

        :param name: device name
        :type name: str
        """
        self._name = name
        self._ser = None
        self._port = ""
        self._wait_time = wait_time
        self._commands = []

        self.init_commands()
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def ser(self) -> Serial:
        return self._ser

    @property
    def port(self) -> str:
        return self._port

    @port.setter
    def port(self, port: str):
        self._port = port
        return

    @property
    def wait_time(self) -> float:
        return self._wait_time

    @property
    def commands(self) -> List[Command]:
        return self._commands

    def get_command(self, number: int) -> Union[None, Command]:
        command = None

        for item in self.commands:
            if item.number == number:
                command = item

        if command is None:
            easyb.log.error("Command number is unknown: " +  str(number))

        return command

    def setup(self, baudrate: int = 4800, timeout: int = 6, write_timeout: int = 2):
        """Setup control module

        :param baudrate: baudrate of serial connection
        :type baudrate: int

        :param timeout: serial port timeout
        :type timeout: int

        :param write_timeout: serial port write timeout
        :type write_timeout: int

        :return: True if successfull, otherwise false
        :rtype: bool
        """

        self._ser = Serial(baudrate=baudrate,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           timeout=timeout,
                           xonxoff=0,
                           rtscts=0,
                           dsrdtr=0,
                           interCharTimeout=None,
                           writeTimeout=write_timeout)
        return

    def open(self) -> bool:
        """Open serial connection

        :return: True if successfull, otherwise false
        :rtype: bool
        """

        if self._port == "":
            easyb.log.error("Port is missing/not configured!")
            return False

        self.ser.port = self._port

        try:
            self.ser.open()
        except serial.SerialException as e:
            easyb.log.error("Problem during opening of serial port!")
            easyb.log.exception(e)
            return False
        return True

    def send(self, message: Message) -> bool:

        debug = ""
        stream = message.encode()

        if message.success is False:
            return False

        for item in stream:
            if debug == "":
                debug = "0x{:02x}".format(item)
            else:
                debug = debug + " 0x{:02x}".format(item)

        debug2 = "Address " + str(message.address) + ", Code: " + str(message.code)
        debug2 += ", " + message.priority.name
        debug2 += ", " + message.length.name
        debug2 += ", " + message.direction.name

        easyb.log.debug2("SERIAL", debug2)
        easyb.log.debug1("SERIAL", "Write: " + debug)
        count = self.ser.write(stream)
        if count != len(stream):
            return False
        return True

    def receive(self) -> Message:
        header = self.ser.read(3)
        message = Message()
        message.decode(header)

        data = None

        if message.length is Length.Byte6:
            data = self.ser.read(3)

        if message.length is Length.Byte9:
            data = self.ser.read(6)

        if data is not None:
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
        if data.success is False:
            return None

        return data

    def run(self, number: int) -> bool:
        command = self.get_command(number)

        if command is None:
            return False

        check = command.call()
        return check

    @abc.abstractmethod
    def init_commands(self):
        return
