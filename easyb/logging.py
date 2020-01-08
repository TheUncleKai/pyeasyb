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


import os
import colorama
import sys
import traceback
from datetime import datetime
from typing import TextIO


def _create_scheme(style="", fore="", back=""):
    scheme = ""

    text_style = None
    text_fore = None
    text_back = None

    if style != "":
        text_style = getattr(colorama.Style, style)

    if fore != "":
        text_fore = getattr(colorama.Fore, fore)

    if back != "":
        text_back = getattr(colorama.Back, back)

    if text_style is not None:
        scheme += text_style

    if text_fore is not None:
        scheme += text_fore

    if text_back is not None:
        scheme += text_back
    return scheme


def _write_stdout(content, raw=False):
    sys.stdout.write(content)
    if raw is True:
        return
    sys.stdout.write("\n")
    return


def _write_stderr(content, raw=False):
    sys.stderr.write(content)
    if raw is True:
        return
    sys.stderr.write("\n")
    return


class Log(object):

    def __init__(self):
        colorama.init()

        self.app_name = ""
        self.fill_number: int = 15
        self.level: int = 0

        self.name_logging: str = ""
        self.name_serial: str = ""

        # noinspection PyTypeChecker
        self.file_logging: TextIO = None

        # noinspection PyTypeChecker
        self.file_serial: TextIO = None
        return

    def __del__(self):
        if self.file_logging is not None:
            self.file_logging.close()

        if self.file_serial is not None:
            self.file_serial.close()
        return

    def open(self, **kwargs) -> bool:
        item = kwargs.get("name", None)
        if item is not None:
            self.app_name = item

        item = kwargs.get("number", None)
        if item is not None:
            self.fill_number = item

        item = kwargs.get("level", None)
        if item is not None:
            self.level = item

        item = kwargs.get("logging", None)
        if item is not None:
            self.name_logging = item

        item = kwargs.get("serial", None)
        if item is not None:
            self.name_serial = item

        if (self.name_logging != "") and (self.file_logging is None):
            file_path = os.path.abspath(os.path.normpath(self.name_logging))
            self.file_logging = open(file_path, "a")

        if (self.name_serial != "") and (self.file_serial is None):
            file_path = os.path.abspath(os.path.normpath(self.name_serial))
            self.file_serial = open(file_path, "a")
        return True

    def _write_logging(self, content: str, raw=False):
        if self.file_logging is None:
            return

        self._write_file(self.file_logging, content, raw)
        return

    def _write_serial(self, content: str, raw=False):
        if self.file_serial is None:
            return

        self._write_file(self.file_serial, content, raw)
        return

    @staticmethod
    def _write_file(file: TextIO, content: str, raw=False):
        if file is None:
            return

        file.write(content)
        if raw is True:
            return
        file.write("\n")
        return

    @staticmethod
    def raw(content: str):
        _write_stdout(content)
        return

    def _log_short(self, scheme: str, level: str, text: str):
        name = ""

        if self.app_name != "":
            name = self.app_name.ljust(self.fill_number)

        level = level.ljust(self.fill_number)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content_stdout = "{0:s}{1:s} {2:s}{3:s}{4:s}| {5:s}".format(colorama.Style.RESET_ALL, name, scheme, level,
                                                                    colorama.Style.RESET_ALL, text)

        content_text = "{0:s}: {1:s} - {2:s}".format(timestamp, level, text)

        _write_stdout(content_stdout)
        self._write_logging(content_text)
        return

    def _log_long(self, scheme: str, level: str, tag: str, text: str):
        name = ""

        if self.app_name != "":
            name = self.app_name.ljust(self.fill_number)

        tag = tag.ljust(self.fill_number)
        level = level.ljust(self.fill_number)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content_stdout = "{0:s}{1:s} {2:s}{3:s}{4:s}| {5:s}".format(colorama.Style.RESET_ALL, name, scheme, tag,
                                                                    colorama.Style.RESET_ALL, text)
        content_text = "{0:s}: {1:s}{2:s} - {3:s}".format(timestamp, level, tag, text)

        _write_stdout(content_stdout)
        self._write_logging(content_text)
        return

    def inform(self, tag, text):

        scheme = _create_scheme("BRIGHT", "GREEN")
        self._log_long(scheme, "INFORM", tag, text)
        return

    def debug1(self, tag, text):

        if self.level < 1:
            return

        scheme = _create_scheme("BRIGHT", "CYAN")
        self._log_long(scheme, "DEBUG1", tag, text)
        return

    def debug2(self, tag, text):

        if self.level < 2:
            return

        scheme = _create_scheme("BRIGHT", "MAGENTA")
        self._log_long(scheme, "DEBUG2", tag, text)
        return

    def debug3(self, tag, text):

        if self.level < 3:
            return

        scheme = _create_scheme("BRIGHT", "BLACK")
        self._log_long(scheme, "DEBUG3", tag, text)
        return

    def warn(self, tag, text):
        scheme = _create_scheme("BRIGHT", "MAGENTA")
        self._log_long(scheme, "WARN", tag, text)
        return

    def error(self, text):
        scheme = _create_scheme("BRIGHT", "RED")
        self._log_short(scheme, "ERROR", text)
        return

    def log_traceback(self):
        ttype, value, tb = sys.exc_info()
        self.error("Uncaught exception")
        self.error("Type:  " + str(ttype))
        self.error("Value: " + str(value))

        lines = traceback.format_tb(tb)
        for line in lines:
            _write_stderr(line, True)
            self._write_logging(line, True)
        return

    def exception(self, e):
        scheme = _create_scheme("BRIGHT", "RED")
        text = str(e)

        self._log_short(scheme, "EXCEPTION", text)
        return
