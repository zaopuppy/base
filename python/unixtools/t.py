#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import plyplus
import subprocess
import threading
import time
import io


def func1(pipe_in, pipe_out):
    time.sleep(2)
    pipe_out.write("Just a test\r\n")
    pipe_out.flush()
    pipe_out.close()


def func2(pipe_in, pipe_out):
    for line in iter(lambda: pipe_in.readline(1024), ''):
        print(line)


def test_pipe():
    p1 = subprocess.Popen(
        ["C:\\Windows\\system32\\cmd.exe",
         "/c",
         "dir"],
        stdin=None, stdout=subprocess.PIPE, stderr=None)
    p2 = subprocess.Popen(
        ["D:\\Python34\python.exe",
         "D:\\source\\base\\python\\unixtools\\module\\grep.py",
         "0"],
        stdin=p1.stdout, stdout=None, stderr=None)
    p1.stdout.close()
    p2.communicate()
    # p2cread, p2cwrite = os.pipe()
    # pipe_in = io.TextIOWrapper(io.open(p2cread, "rb"))
    # pipe_out = io.TextIOWrapper(io.open(p2cwrite, "wb"))
    # thread1 = threading.Thread(target=func1, daemon=False, args=(pipe_in, pipe_out))
    # thread2 = threading.Thread(target=func2, daemon=False, args=(pipe_in, pipe_out))
    # thread1.start()
    # thread2.start()


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


def test_plyplus():
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


def main():
    test_pipe()


if __name__ == "__main__":
    main()



# end