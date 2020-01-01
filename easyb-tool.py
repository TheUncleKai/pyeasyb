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
from typing import Union
from optparse import OptionParser

from easyb.device import Device
from easyb.devices import list_devices, get_device


class Main(object):

    options = None
    parser = OptionParser("usage: %prog [options]")

    def __init__(self):

        self.parser.add_option("-d", "--device", help="use device", metavar="DEVICE", type="string", default="")
        self.parser.add_option("-c", "--command", help="run command", metavar="COMMAND", type="int", default=None)
        self.parser.add_option("-p", "--port", help="serial port", metavar="PORT", type="string", default="")
        self.parser.add_option("-v", "--verbose", help="run verbose level [0..3]", metavar="VERBOSE", type="int",
                               default=0)

        self.parser.add_option("-r", "--read", help="read values continuously", action="store_true", default=False)
        self._device = None
        self._command = None
        self._port = ""
        return

    @property
    def device(self) -> Device:
        return self._device

    @property
    def command(self) -> Union[None, int]:
        return self._command

    @property
    def port(self) -> str:
        return self._port

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

        if options.port == "":
            easyb.log.error("Serial port is missing!")
            return False

        self._port = options.port

        if options.device == "":
            easyb.log.error("No device given!")
            list_devices()
            return False

        self._device = get_device(options.device)

        if self.device is None:
            easyb.log.error("Device {0:s} is unknown!".format(options.device))
            return False

        if options.command is None:
            easyb.log.error("No command given!")
            self.device.list_commands()
            return False

        command = options.command

        if command not in self.device.command_list:
            easyb.log.error("Command number is unknown: {0:d}".format(command))
            return False

        self._command = command
        return True

    def run(self) -> bool:
        """Run the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """
        easyb.log.inform("Port", self.port)
        easyb.log.inform("Device", self.device.name)

        command = self.device.get_command(self.command)

        easyb.log.inform("Command", "{0:d}: {1:s}".format(command.number, command.name))
        return True

    def close(self) -> bool:
        """Run the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """
        return True


if __name__ == '__main__':

    main = Main()

    if main.prepare() is False:
        sys.exit(1)

    if main.run() is False:
        sys.exit(1)

    if main.close() is False:
        sys.exit(1)

    sys.exit(0)
