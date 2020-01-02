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
from optparse import OptionParser

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

        self._parser = OptionParser("usage: %prog [options]")
        self._parser.add_option("-d", "--device", help="use device", metavar="DEVICE", type="string", default="")
        self._parser.add_option("-c", "--command", help="run command", metavar="COMMAND", type="int", default=None)
        self._parser.add_option("-p", "--port", help="serial port", metavar="PORT", type="string", default="")
        self._parser.add_option("-v", "--verbose", help="run verbose level [0..3]", metavar="VERBOSE", type="int",
                                default=0)

        self._parser.add_option("-r", "--read", help="read values continuously", action="store_true", default=False)
        self._parser.add_option("-l", "--list", help="list device and commands", action="store_true", default=False)

        self._device = None
        self._command = None
        self._port = ""
        self._read = False
        self._list = False
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

        self._device = get_device(self.options.device)
        if self.device is None:
            easyb.log.error("Device {0:s} is unknown!".format(options.device))
            return False

        if self.options.command not in self.device.command_list:
            easyb.log.error("Command number is unknown: {0:d}".format(self.options.command))
            return False

        self.device.


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
