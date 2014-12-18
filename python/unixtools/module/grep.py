#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zaopuppy'


import sys
import re
import time


def usage():
    print("""
    <grep> <pattern> files
    """)


def get_line(file_list, max_len=4096):
    if len(file_list) <= 0:
        # _io.TextIOWrapper'
        for line in iter(lambda: sys.stdin.readline(max_len), b''):
            yield line
    else:
        for f in file_list:
            with open(f, "rb") as fp:
                # _io.BufferedReader
                for line in iter(lambda: fp.readline(max_len), b''):
                    # TODO: encoding
                    yield line.decode()


def main():
    if len(sys.argv) <= 1:
        usage()
        return 1

    pattern = sys.argv[1]
    file_list = sys.argv[2:]

    prog = re.compile(pattern)

    for line in get_line(file_list):
        if prog.search(line):
            print(line, end='')


if __name__ == "__main__":
    main()

