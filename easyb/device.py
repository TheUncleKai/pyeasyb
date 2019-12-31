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

from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, SerialException, SerialTimeoutException







class Control(object):

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

    def setup(self, baudrate: int = 4800, timeout: int = 3, write_timeout: int = 2) -> bool:
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
                               bytesize=EIGHTBITS,
                               parity=PARITY_NONE,
                               stopbits=STOPBITS_ONE,
                               timeout=timeout,
                               xonxoff=0,
                               rtscts=0,
                               dsrdtr=0,
                               interCharTimeout=None,
                               writeTimeout=write_timeout)
        except SerialException as e:
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
        except SerialTimeoutException as e:
            easyb.log.error("Timeout during opening of serial port!")
            easyb.log.exception(e)
            return False
        except SerialException as e:
            easyb.log.error("Problem during opening of serial port!")
            easyb.log.exception(e)
            return False
        return True

    def send(self, address: int, command: int) -> bool:
        return True
