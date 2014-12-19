#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zaopuppy'


import sys
import re
import time
import getopt


if sys.version_info.major != 3:
    print("python 3.x needed")
    quit(-1)

try:
    import readline
except ImportError as e:
    pass

try:
    if not readline:
        import pyreadline as readline
except ImportError as e:
    pass

if not readline:
    print("pyreadline is not found, bash-like key binding is not available.")


def usage():
    print("""
    <grep> <pattern> files
    """)


def get_line(file_list, max_len=4096):
    if len(file_list) <= 0:
        # _io.TextIOWrapper'
        read_line = readline.Readline()
        while True:
            yield read_line.readline()
    else:
        for f in file_list:
            with open(f, "rb") as fp:
                # _io.BufferedReader
                for line in iter(lambda: fp.readline(max_len), b''):
                    # TODO: encoding
                    yield line.decode()


def main():
    optlist, args = getopt.getopt(sys.argv[1:], "i", "ignore-case=")

    if len(args) <= 0:
        usage()
        return 1

    pattern = args[0]
    file_list = args[1:]

    prog = re.compile(pattern)

    for line in get_line(file_list):
        if prog.search(line):
            print(line, end='')


if __name__ == "__main__":
    main()

