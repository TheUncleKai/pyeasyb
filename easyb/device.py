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

import easyb
import serial

from serial import Serial
from typing import List

from easyb.message import Message
from easyb.definitions import Length


class Device(object):

    def __init__(self, port: str):
        """Control constructor

        :param port: serial port
        :type port: str
        """
        self._ser = None
        self._port = port
        return

    @property
    def port(self) -> str:
        return self._port

    @property
    def ser(self) -> Serial:
        return self._ser

    def setup(self, baudrate: int = 4800, timeout: int = 6, write_timeout: int = 2) -> bool:
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

        try:
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
        except serial.SerialException as e:
            easyb.log.exception(e)

        return True

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
        except serial.SerialTimeoutException as e:
            easyb.log.error("Timeout during opening of serial port!")
            easyb.log.exception(e)
            return False
        except serial.SerialException as e:
            easyb.log.error("Problem during opening of serial port!")
            easyb.log.exception(e)
            return False
        return True

    def send(self, message: Message) -> bool:

        data = ""
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
