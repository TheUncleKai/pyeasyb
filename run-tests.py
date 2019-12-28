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

import coverage

cov = coverage.Coverage()

import easyb
from typing import List
from optparse import OptionParser

from easyb.utils import check_dict, openjson

import os
import sys
import unittest
import warnings
import time

from unittest.signals import registerResult
import unittest.result as result


class Module(object):

    id = ""
    path = ""
    classname = ""
    tests = []

    def load(self, data: dict) -> bool:

        check = check_dict(data, ["id", "path", "classname", "tests"])
        if check is False:
            easyb.log.error("Module config not complete!")
            return False

        self.id = data["id"]
        self.path = data["path"]
        self.classname = data["classname"]
        self.tests = data["tests"]
        return True


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')  # text-mode streams translate to \r\n if needed


class TextTestResult(result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        super(TextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions
        self.current_test = ""
        return

    @staticmethod
    def _get_description(test):
        desc = str(test)
        # doc_first_line = test.shortDescription()
        # if self.descriptions and doc_first_line:
        #     return '\n'.join((str(test), doc_first_line))
        # else:
        #     return str(test)
        return desc

    def startTest(self, test):
        super(TextTestResult, self).startTest(test)
        self.current_test = self._get_description(test)
        return

    def addSuccess(self, test):
        super(TextTestResult, self).addSuccess(test)
        easyb.log.inform("OK", self.current_test)
        return

    def addError(self, test, err):
        super(TextTestResult, self).addError(test, err)
        easyb.log.warn("ERROR", self.current_test)
        return

    def addFailure(self, test, err):
        super(TextTestResult, self).addFailure(test, err)
        easyb.log.warn("FAIL", self.current_test)
        return

    def addSkip(self, test, reason):
        super(TextTestResult, self).addSkip(test, reason)
        content = "skipped {0!r}".format(reason)
        easyb.log.warn(self.current_test, content)
        return

    def addExpectedFailure(self, test, err):
        super(TextTestResult, self).addExpectedFailure(test, err)
        easyb.log.warn(self.current_test, "expected failure")
        return

    def addUnexpectedSuccess(self, test):
        super(TextTestResult, self).addUnexpectedSuccess(test)
        easyb.log.warn(self.current_test, "unexpected success")
        return

    # noinspection PyPep8Naming
    def printErrors(self):
        self._print_error_list('ERROR', self.errors)
        self._print_error_list('FAIL', self.failures)
        return

    def _print_error_list(self, flavour, errors):
        for test, err in errors:
            easyb.log.error(flavour)
            easyb.log.raw(self.separator1 + "\n")
            easyb.log.raw(self._get_description(test) + "\n")
            easyb.log.raw(self.separator2 + "\n")
            easyb.log.raw("%s" % err)
        return


class TextTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = TextTestResult

    def __init__(self, name="", stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warning=None,
                 *, tb_locals=False):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        if stream is None:
            stream = sys.stderr
        self.name = name
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.warnings = warning
        if resultclass is not None:
            self.resultclass = resultclass

    def _make_result(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        """Run the given test case or test suite.

        :param test: test suite.
        :type test: unittest.TestSuite

        :return: test result.
        :rtype: TextTestResult
        """
        test_result = self._make_result()
        registerResult(test_result)
        test_result.failfast = self.failfast
        test_result.buffer = self.buffer
        test_result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module', category=DeprecationWarning,
                                            message='Please use assert\w+ instead.')
            start_time = time.time()
            start_test_run = getattr(test_result, 'startTestRun', None)
            if start_test_run is not None:
                start_test_run()
            try:
                test(test_result)
            finally:
                stop_test_run = getattr(test_result, 'stopTestRun', None)
                if stop_test_run is not None:
                    stop_test_run()
            stop_time = time.time()
        time_taken = stop_time - start_time
        test_result.printErrors()
        # if hasattr(result, 'separator2'):
        #     self.stream.writeln(result.separator2)
        run = test_result.testsRun

        logline = "Ran %d test%s in %.3fs" % (run, run != 1 and "s" or "", time_taken)
        easyb.log.inform("RUNNER", logline)

        expected_fails = unexpected_successes = skipped = 0
        try:
            results = map(len, (test_result.expectedFailures,
                                test_result.unexpectedSuccesses,
                                test_result.skipped))
        except AttributeError:
            pass
        else:
            expected_fails, unexpected_successes, skipped = results

        infos = []
        if not test_result.wasSuccessful():
            failed, errored = len(test_result.failures), len(test_result.errors)
            if failed:
                easyb.log.warn("FAILURES", str(failed))
            if errored:
                easyb.log.warn("ERRORS", str(errored))
        else:
            easyb.log.inform("RUNNER", "OK")

        if skipped:
            infos.append("skipped=%d" % skipped)

        if expected_fails:
            infos.append("expected failures=%d" % expected_fails)

        if unexpected_successes:
            infos.append("unexpected successes=%d" % unexpected_successes)

        if infos:
            logline = " (%s)" % (", ".join(infos),)
            easyb.log.raw(logline)
        return test_result


class TestTask(object):

    options = None
    parser = OptionParser("usage: %prog [options]")

    def __init__(self):
        """The constructor.
        """

        self.parser.add_option("-c", "--config", help="run profile", metavar="PROFILE", type="string",
                               default="tests.json")
        self.parser.add_option("-m", "--module", help="run class", metavar="CLASS", type="string", default="")
        self.parser.add_option("-t", "--test", help="run test", metavar="TEST", type="string", default="")

        self._suite = None
        """test suite"""

        self._modules = []
        """stores test config."""
        return

    @property
    def suite(self) -> unittest.TestSuite:
        return self._suite

    @property
    def modules(self) -> List[Module]:
        return self._modules

    def _load_config(self, filename: str) -> bool:
        """Parse config file.

        :param filename: filename of config file.
        :type filename: str

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """

        if os.path.exists(filename) is False:
            easyb.log.error("File not found: " + filename)
            return False

        data = openjson(filename)

        check = check_dict(data, ["modules"])

        if check is False:
            easyb.log.error("Config is invalid!")
            return False

        for item in data["modules"]:
            module = Module()

            check = module.load(item)
            if check is False:
                continue

            if self.options.module != "":
                if module.id == self.options.module:
                    self._modules.append(module)
            else:
                self._modules.append(module)

        if len(self.modules) == 0:
            easyb.log.error("No tests configured!")
            return False

        easyb.log.inform("TESTS", "Number of modules: " + str(len(self._modules)))
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

        filename = os.path.abspath(os.path.normpath(self.options.config))

        check = self._load_config(filename)
        if check is False:
            return False

        self._suite = unittest.TestSuite()
        count = 0

        for module in self.modules:
            easyb.log.inform("RUN", module.id)

            fromlist = [module.classname]
            m = __import__(module.path, globals(), locals(), fromlist)
            c = getattr(m, module.classname)
            for item in module.tests:

                if self.options.test != "":
                    if self.options.test == item:
                        self.suite.addTest(c(item))
                        count += 1
                else:
                    self.suite.addTest(c(item))
                    count += 1

        if count == 0:
            easyb.log.error("No tests to run!")
            return False
        easyb.log.inform("TESTS", "Tests to run: " + str(count))
        return True

    def run(self) -> bool:
        """Run the test task.

        :returns: True if successfull, otherwise False.
        :rtype: bool
        """
        runner = TextTestRunner(verbosity=2)

        runner.run(self.suite)
        return True


if __name__ == '__main__':

    cov.start()

    main = TestTask()

    if main.prepare() is False:
        sys.exit(1)

    if main.run() is False:
        sys.exit(1)

    cov.stop()
    cov.save()

    cov.html_report()

    sys.exit(0)
