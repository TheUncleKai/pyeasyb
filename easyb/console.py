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

import sys
import easyb
import easyb.devices
from optparse import OptionParser, OptionGroup

from easyb.device import Device
from easyb.devices import list_devices, get_device

__all__ = [
    "Console"
]


class Console(object):

    options = None

    @property
    def parser(self) -> OptionParser:
        return self._parser

    @property
    def device(self) -> Device:
        return self._device

    def __init__(self):

        usage = "usage: %prog [options] arg1 arg2"

        parser = OptionParser(usage=usage)
        parser.add_option("-v", "--verbose", help="run verbose level [0..3]", metavar="1", type="int",
                          default=0)
        parser.add_option("-r", "--read", help="read values continuously", action="store_true", default=False)
        parser.add_option("-l", "--list", help="list device and commands", action="store_true", default=False)
        parser.add_option("-i", "--interval", help="interval between measurements for read mode (in seconds)",
                          metavar="2.0", type="float", default=2.0)

        device = OptionGroup(parser, "Device Options", "Set device type, command or address to use.")
        device.add_option("-d", "--device", help="use device", type="string", default="")
        device.add_option("-c", "--command", help="run command", metavar="0", type="int", default=None)

        parser.add_option_group(device)

        serial = OptionGroup(parser, "Serial Options", "Set serial port options.")
        serial.add_option("-p", "--port", help="serial port", metavar="/dev/ttyUSB0", type="string", default="")
        serial.add_option("-b", "--baudrate", help="serial port baudrate", metavar="4800", type="int", default=4800)
        serial.add_option("-t", "--timeout", help="serial port timeout (in seconds)", metavar="6", type="int",
                          default=6)
        serial.add_option("-w", "--writetimeout", help="serial port write timeout", metavar="2", type="int", default=2)

        parser.add_option_group(serial)

        self._parser = parser

        self._device = None
        return

    def _check_params(self) -> bool:
        if self.options.list is True:
            return True

        if self.options.device == "":
            easyb.log.error("No device given!")
            return False

        if (self.options.command is None) and (self.options.read is False):
            easyb.log.error("No command given!")
            return False

        if self.options.port == "":
            easyb.log.error("Serial port is missing!")
            return False

        return True

    def prepare(self) -> bool:
        """Start and prepare the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """

        (options, args) = self.parser.parse_args()

        if options is None:
            easyb.log.error("Unable to parse options!")
            return False

        self.options = options
        easyb.log.level = options.verbose

        version = "python {0:d}.{1:d}.{2:d}.{3:s}".format(sys.version_info.major, sys.version_info.minor,
                                                          sys.version_info.micro, sys.version_info.releaselevel)

        easyb.log.inform(easyb.__name__, sys.platform)
        easyb.log.inform(easyb.__name__, version)

        check = self._check_params()
        if check is False:
            return False

        if self.options.list is True:
            list_devices()
            return True

        c = get_device(self.options.device)

        # noinspection PyCallingNonCallable
        self._device = c(address=1, port=self.options.port, baudrate=self.options.baudrate,
                         timeout=self.options.timeout, write_timeout=self.options.writetimeout)
        if self.device is None:
            easyb.log.error("Device {0:s} is unknown!".format(options.device))
            return False

        if self.options.command not in self.device.command_list:
            easyb.log.error("Command number is unknown: {0:d}".format(self.options.command))
            return False

        self.device.setup()
        self.device.port = self.options.port

        check = self.device.connect()
        if check is False:
            return False

        if self.options.read is True:
            check = self.device.prepare()
            if check is False:
                return False

        return True

    def run(self) -> bool:
        """Run the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """
        if self.options.list is True:
            return True

        easyb.log.inform("Port", self.options.port)
        easyb.log.inform("Device", self.options.device)

        command = self.device.get_command(self.options.command)

        easyb.log.inform("Command", "{0:d}: {1:s}".format(command.number, command.name))
        return True

    def close(self) -> bool:
        """Run the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """
        if self.options.list is True:
            return True

        return True
