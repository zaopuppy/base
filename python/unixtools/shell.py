#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["Shell"]


import io
import os
import os.path
import subprocess
import sys
import threading
import plyplus


try:
    import readline
except ImportError:
    readline = None
    print("warn: cant find readline")


if sys.version_info.major != 3:
    print("python 3.x needed")
    quit(-1)


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


class Command:
    """
    pass
    """

    PIPE = -1

    def __init__(self, shell, args, stdin=None, stdout=None, stderr=None):
        self.shell = shell
        self.args = args

        if stdin == Command.PIPE:
            p2cread, p2cwrite = os.pipe()
            self.stdin_read = io.TextIOWrapper(io.open(p2cread, "rb", -1))
            self.stdin = io.TextIOWrapper(io.open(p2cwrite, "wb", -1))
        elif stdin is None:
            self.stdin_read, self.stdin = sys.stdin, None
        else:
            self.stdin_read, self.stdin = stdin, None

        if stdout == Command.PIPE:
            c2pread, c2pwrite = os.pipe()
            self.stdout = io.TextIOWrapper(io.open(c2pread, "rb", -1))
            self.stdout_write = io.TextIOWrapper(io.open(c2pwrite, "wb", -1))
        elif stdout is None:
            self.stdout, self.stdout_write = None, sys.stdout
        else:
            self.stdout, self.stdout_write = None, stdout

        if stderr == Command.PIPE:
            errread, errwrite = os.pipe()
            self.stderr = io.TextIOWrapper(io.open(errread, "rb", -1))
            self.stderr_write = io.TextIOWrapper(io.open(errwrite, "wb", -1))
        elif stderr is None:
            self.stderr, self.stderr_write = None, sys.stderr
        else:
            self.stderr, self.stderr_write = None, stderr

        self.thread = threading.Thread(target=self.thread_run, daemon=True)
        self.thread.start()

    def thread_run(self):
        self.execute()
        if self.stdin_read is not None and self.stdin_read is not sys.stdin:
            self.stdin_read.close()
        if self.stdout_write is not None and self.stdout_write is not sys.stdout:
            self.stdout_write.close()
        if self.stderr_write is not None and self.stderr_write is not sys.stderr:
            self.stderr_write.close()

    def execute(self):
        self.print("NotImplementedError")

    def communicate(self):
        self.thread.join()
        for f in filter(lambda x: x is not None,
                        (self.stdin, self.stdout, self.stderr)):
            f.close()

    def print(self, msg, end='\n', flush=False):
        if not isinstance(msg, str):
            msg = str(msg)
        self.stdout_write.write(msg + end)
        if flush:
            self.stdout_write.flush()

    def input(self, prompt=''):
        self.stdout_write.write(prompt)
        self.stdout_write.flush()
        return self.stdin_read.readline(2048)


class Echo(Command):
    def execute(self):
        self.print(" ".join(self.args[1:]))


class Cd(Command):
    def execute(self):
        os.chdir(self.args[1])
        self.shell.cwd = self.args[1]


class Ls(Command):
    def execute(self):
        for f in os.listdir(self.shell.cwd):
            self.print(f)


class Pwd(Command):
    def execute(self):
        self.print(self.shell.cwd)


class Exit(Command):
    def execute(self):
        self.shell.is_running = False


class Help(Command):
    def execute(self):
        if len(self.args) > 1:
            match = self.args[1]
        else:
            match = None
        for k, v in self.shell.cmd_map.items():
            if match is not None:
                # FIXME: may cause performance issue if there are too many execute files in paths
                cmd_list = tuple(filter(lambda x: match in x, v))
                if len(cmd_list) > 0:
                    self.print('[' + k + ']')
                    for f in cmd_list:
                        print(f)
                    print()
            else:
                self.print('[' + k + ']')
                for i in v:
                    print(i)
                print()


class Test(Command):
    def execute(self):
        line = self.input('test> ')
        self.print("your input: " + line)


# TODO: support pipeline
# TODO: support script
# TODO: alias
class Shell:
    """
    """
    LINE_BUF_SIZE = 2048

    if sys.platform == "win32":
        PYTHON_PATH = "D:\\Python34\\python.exe"
    else:
        PYTHON_PATH = "/usr/local/bin/python3"

    def __init__(self, cwd=None, ps1="$ ", ps2=".. ", path=[]):
        if not cwd:
            self.cwd = os.getcwd()
        else:
            self.cwd = cwd
        self.ps1 = ps1
        self.ps2 = ps2
        self.is_running = False
        self.paths = path
        # use RB-Tree instead of normal map, we need auto-complete
        # TODO: self.cmd_map = [] -> "path" -> [ "cmd.exe", "fde.dll" ]
        self.cmd_map = {}
        self.errno = 0
        self.parser = plyplus.Grammar(open("bash.g"))
        self.load_script_in_path(self.paths)
        self.builtin = {
            'echo': Echo,
            'cd': Cd,
            'ls': Ls,
            'dir': Ls,
            'pwd': Pwd,
            'exit': Exit,
            'help': Help,
            'test': Test,
        }

    def load_script_in_path(self, paths):
        for p in paths:
            self.cmd_map[p] = []
            for f in os.listdir(p):
                self.cmd_map[p].append(f)
                # file_name = os.path.basename(f)
                # self.cmd_map[file_name] = os.path.join(p, f)

    def run(self):
        # interactive mode
        self.is_running = True
        while self.is_running:
            try:
                line = input(self.ps1)

                if not line:
                    continue

                line = line.strip()

                if len(line) == 0:
                    continue

                # parse input
                ast = self.parser.parse(line)

                # get command list from input
                cmd_list = extract_cmd_list(ast)
                print(cmd_list)
                if len(cmd_list) <= 0:
                    print()
                    continue

                # create sub-processes
                process_list = []
                last_out = None
                for args in cmd_list[0:-1]:
                    p = self.create_subprocess(args, stdin=last_out, stdout=subprocess.PIPE)
                    process_list.append(p)
                    last_out = p.stdout
                process_list.append(self.create_subprocess(cmd_list[-1], stdin=last_out))

                process_list[-1].communicate()
            except KeyboardInterrupt:
                print("^C")
                continue
            except plyplus.TokenizeError as tokenizeError:
                print(tokenizeError)
                continue

    def find_cmd_in_paths(self, cmd):
        if os.path.isabs(cmd):
            try:
                os.stat(cmd)
                return cmd
            except FileNotFoundError as e:
                return None

        for path, cmd_list in self.cmd_map.items():
            if cmd in cmd_list:
                return os.path.join(path, cmd)
            elif cmd + ".py" in cmd_list:
                return os.path.join(path, cmd + ".py")
            elif cmd + ".exe" in cmd_list:
                return os.path.join(path, cmd + ".exe")
            else:
                pass
        return None

    def replace_variable(self, s):
        """ TODO: a very simple but usable implementation"""
        if s == "$?":
            if not self.errno:
                self.errno = 0
            return str(self.errno)
        else:
            return s

    def is_builtin(self, cmd):
        return cmd in self.builtin.keys()

    def create_subprocess(self, args, stdin=None, stdout=None, stderr=None):
        cmd = args[0]
        if self.is_builtin(cmd):
            cmd_type = self.builtin.get(cmd)
            return cmd_type(self, args, stdin=stdin, stdout=stdout, stderr=stderr)
        else:
            full_path = self.find_cmd_in_paths(cmd)
            if not full_path:
                raise Exception("Not such command or file")
            if full_path.endswith(".py"):
                return subprocess.Popen(
                    [self.PYTHON_PATH, full_path] + args[1:], stdin=stdin, stdout=stdout, stderr=stderr)
            else:
                return subprocess.Popen(
                    [full_path, ] + args[1:], stdin=stdin, stdout=stdout, stderr=stderr)


def main():
    path = os.path.pathsep.join((os.getenv("PATH"), os.path.join(os.getcwd(), "module")))
    sh = Shell(
        path=path.split(os.path.pathsep)
    )
    if len(sys.argv) <= 1:
        sh.run()
    else:
        # execute script
        raise Exception("Not implemented")


if __name__ == "__main__":
    main()
    # print("TEST")
    # cmd = Echo(None, ["echo", "haha", "Good"])
    # cmd.communicate()
    # cmd = Command(None, None)
    # cmd.communicate()


