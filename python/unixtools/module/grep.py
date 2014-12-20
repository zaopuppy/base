#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zaopuppy'


import sys
import re
import time
import getopt


try:
    import readline
except ImportError as e:
    print("warn: cant find readline")


if sys.version_info.major != 3:
    print("python 3.x needed")
    quit(-1)

def usage():
    print("""
    <grep> <pattern> files
    """)


IGNORE_CASE = False

def get_line(file_list, max_len=4096):
    if len(file_list) <= 0:
        while True:
            yield input()
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

    for o, a, in optlist:
        if o == "-i":
            global IGNORE_CASE
            IGNORE_CASE = True

    pattern = args[0]
    file_list = args[1:]

    if IGNORE_CASE:
        prog = re.compile(pattern.lower())
    else:
        prog = re.compile(pattern)

    for line in get_line(file_list):
        if IGNORE_CASE:
            if prog.search(line.lower()):
                print(line, end='')
        else:
            if prog.search(line):
                print(line, end='')


if __name__ == "__main__":
    main()

