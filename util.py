#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This is a command line utility for dynamic filtering of log files by given regex patterns. """
import argparse
import fileinput
import re
from ipaddress import IPv4Address, IPv6Address

from termcolor import colored

PATTERNS_FILE = 'patterns.txt'


class LogUtility:
    patterns = {}

    @classmethod
    def _load_patterns(cls, file=PATTERNS_FILE):
        with open(file=file, mode='r', encoding='utf8') as f:
            for line in f.readlines():
                name, pattern = cls._parse_pattern(line)
                cls.patterns[name] = pattern

    @classmethod
    def _parse_pattern(cls, line: str):
        match = re.search(pattern=r"(\w+)\s(.+)", string=line)
        if not match or not match.group(1) or not match.group(2):
            raise RuntimeError("Unable to parse valid pattern from following line content ({}).".format(line))
        return match.group(1), match.group(2)

    @classmethod
    def run(cls, arguments: dict):
        """
        Runs parse utility with arguments given,
        :param arguments: dictionary mapping used arguments and their values
        :return: (marked) lines
        """
        cls._load_patterns()
        lines = list(fileinput.input(files=arguments['file']))
        filtered_arguments = {k: v for k, v in arguments.items() if k not in ['file', 'first', 'last']}
        for regex_name, value in filtered_arguments.items():
            regex_name = regex_name.upper()
            if regex_name not in cls.patterns:
                raise RuntimeError("Undefined regex name ({})".format(regex_name))
            regex = re.compile(pattern=r"({})".format(cls.patterns[regex_name]))
            if value is True:
                lines = [line for line in lines if regex.search(string=line)]
                lines = [regex.sub(string=line, repl=colored("\\1", color="blue")) for line in lines]
            elif value is None:
                continue
            else:
                lines = [line for line in lines if str(value) in line]
                lines = [line.replace(str(value), colored(str(value), color="red")) for line in lines]

        lines_final = cls._apply_list_boundaries(lines, first=arguments['first'], last=arguments['last'])
        cls._print_lines(lines_final)
        return lines_final

    @classmethod
    def _apply_list_boundaries(cls, lines: list, first: int, last: int):
        len_lines = len(lines)
        start = 0
        end = len_lines
        if first:
            end = min(first, len_lines)
        if last:
            start = max(0, len_lines - last)
        return lines[start:end]

    @classmethod
    def _print_lines(cls, lines: list):
        for line in lines:
            print(line, end="")


def timestamp_argument(x: str):
    if not re.search(pattern=r"\d\d:\d\d:\d\d", string=x):
        raise RuntimeError("Timestamp in wrong format")
    return x


def positive_int_argument(x: str):
    if int(x) < 0:
        raise RuntimeError("Negative argument instead of positive integer.")
    return int(x) if int(x) >= 0 else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File name of entry log file", nargs=1)
    parser.add_argument("-f", "--first", type=positive_int_argument, help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=positive_int_argument, help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", type=timestamp_argument,
                        help="Print lines that contain a timestamp in HH:MM:SS format",
                        required=False, nargs='?', const=True)
    parser.add_argument("-i", "--ipv4", help="Print lines that contain an IPv4 address, matching IPs are highlighted",
                        type=lambda x: x if IPv4Address(x) else None, required=False, nargs='?', const=True)
    parser.add_argument("-I", "--ipv6",
                        help="Print lines that contain IPv6 address (standard notation), matching IPs are highlighted",
                        type=lambda x: x if IPv6Address(x) else None, required=False, nargs='?', const=True)

    args = vars(parser.parse_args())
    LogUtility.run(args)
