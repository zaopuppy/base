#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import re

import plyplus


if __name__ == "__main__":
    # re.match('.*(?<!\\)b', 'cccbbbbbbbbbbbbb')
    parser = plyplus.Grammar(open("bash.g"))
    ast = parser.parse('D:\ls.exe > 1.txt|ls')
    print(ast)

