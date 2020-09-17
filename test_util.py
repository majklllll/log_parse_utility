#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A suite of tests for util.py utility example. """
import subprocess

import pytest

PYTHON_INTERPRETER = "venv/Scripts/python"
EXEC_STRING = PYTHON_INTERPRETER + " util.py test_sample.log"

# list of pairs Tuple(arguments, expected lines from test_sample file)
expected_behaviour = [
    ("-f 4", list(range(1, 5))),
    ("--first 4", list(range(1, 5))),
    ("-l 6", list(range(10, 16))),
    ("--timestamps", list(range(1, 16))),
    ("--ipv4", list(range(1, 8)) + [10, 11, 12, 14, 15]),
    ("--ipv6", [8, 9, 13]),
    ("--ipv4 --last 50", list(range(1, 8)) + [10, 11, 12, 14, 15]),
    ("--last 50 --first 20", list(range(1, 16))),
    ("--last 10 --first 10", list(range(6, 11))),
    ("--ipv4 --ipv6", []),
    ("--ipv4 66.249.73.135 ", [7, 11, 12]),
    ("--ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7335", [9, 13]),
    ("--ipv6 2001:0db8:85a3:0000:0000:8a2e:0370:7334", [8]),
    ("--timestamps 21:05:19", [5]),
    ("--timestamps 21:05:20", []),
    ("--ipv4 66.249.73.135 --timestamps 21:05:18", [11]),

]

unpassable_arguments = [
    "-f -455",
    "-l lalala",
    "--timestamps 9.rijen",
    "--ipv4 7.7.7.7.77.7",
    "--ipv6 ipevesest",

]


def execute_test_with_params(params):
    return subprocess.check_output("{} {}".format(EXEC_STRING, params), universal_newlines=True)


def check_line_numbers(lines: list, expected_numbers: list):
    assert len(lines) == len(expected_numbers)
    for index, expected_number in enumerate(expected_numbers):
        assert lines[index].endswith(str(expected_number))


class TestUtilConsole:

    def test_run_help(self):
        help_message = execute_test_with_params("-h")
        assert "positional arguments" in help_message
        assert "optional arguments:" in help_message
        assert "usage: util.py [-h] [-f FIRST] [-l LAST] [-t [TIMESTAMPS]] [-i [IPV4]]" in help_message

    @pytest.mark.parametrize("arguments,expected_numbers", expected_behaviour)
    def test_good_arguments_should_pass(self, arguments, expected_numbers):
        output = execute_test_with_params("{}".format(arguments))
        output_lines = output.strip().split("\n") if output.strip() != "" else []
        check_line_numbers(lines=output_lines, expected_numbers=expected_numbers)

    @pytest.mark.parametrize("arguments", unpassable_arguments)
    def test_bad_arguments_should_fail(self, arguments):
        with pytest.raises(subprocess.CalledProcessError):
            result = execute_test_with_params(arguments)
            assert result == ''
