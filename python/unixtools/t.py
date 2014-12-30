#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import re

import plyplus

import subprocess


def test_pipe():
    p1 = subprocess.Popen(
        ["C:\\Windows\\system32\\cmd.exe",
         "/c",
         "dir"],
        stdin=None, stdout=subprocess.PIPE, stderr=None)
    p2 = subprocess.Popen(
        ["D:\\Python34\python.exe",
         "D:\\source\\base\\python\\unixtools\\module\\grep.py",
         "."],
        stdin=p1.stdout, stdout=None, stderr=None)
    p1.stdout.close()
    p2.communicate()


def transfer_dbl_quo_string(s):
    result = ""
    escaping = False
    for idx, c in enumerate(s):
        if not escaping:
            if c == '\\':
                escaping = True
            else:
                result += c
        else:
            escaping = False
            if c == '\\':
                result += '\\'
            elif c == 'n':
                result += '\n'
            elif c == 'r':
                result += '\r'
            elif c == 't':
                result += '\t'
            elif c == '"':
                result += '"'
            elif c == "'":
                result += "'"
            else:
                # bad escaping character, ignore escape character
                result += '\\'
                result += c
    return result


def transfer_quo_string(s):
    return transfer_dbl_quo_string(s)


def transfer_string(s):
    if s.startswith('"'):
        return transfer_dbl_quo_string(s[1:-1])
    elif s.startswith("'"):
        return transfer_quo_string(s[1:-1])
    else:
        return s


def extract_cmd_args(cmd):
    if cmd.head != "cmd":
        return []
    return [transfer_string(x.tail[0]) for x in cmd.tail]


def extract_cmd_list(ast):
    if ast.head != "start":
        return []
    return [extract_cmd_args(c) for c in ast.tail]


def main():
    parser = plyplus.Grammar(open("bash.g"))
    # ast = parser.parse('C:\\Windows\\system32\\cmd.exe /c dir|D:\\Python34\python.exe D:\\source\\base\\python\\unixtools\\module\\grep.py . haha')
    ast = parser.parse('/bin/ls "/"|/usr/bin/grep "l"')
    print(ast)
    cmd_list = extract_cmd_list(ast);
    print(cmd_list)
    if len(cmd_list) <= 0:
        return
    process_list = []
    last_out = None
    for cmd in cmd_list[0:-1]:
        p = subprocess.Popen(cmd, stdin=last_out, stdout=subprocess.PIPE)
        process_list.append(p)
        last_out = p.stdout
    process_list.append(subprocess.Popen(cmd_list[-1], stdin=last_out))
    for p in process_list[0:-1]:
        p.stdout.close()
    process_list[-1].communicate()


if __name__ == "__main__":
    main()



# end
