#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["Shell"]


import os
import os.path
import subprocess
import sys
import plyplus


try:
    import readline
except ImportError as e:
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


# TODO: support pipeline
# TODO: support script
# TODO: alias
class Shell:
    """
    """
    LINE_BUF_SIZE = 2048

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
                for cmd in cmd_list[0:-1]:
                    # p = subprocess.Popen(cmd, stdin=last_out, stdout=subprocess.PIPE)
                    p = self.create_subprocess(cmd, stdin=last_out, stdout=subprocess.PIPE)
                    process_list.append(p)
                    last_out = p.stdout
                process_list.append(subprocess.Popen(cmd_list[-1], stdin=last_out))

                # run them
                for p in process_list[0:-1]:
                    p.stdout.close()
                process_list[-1].communicate()
            except KeyboardInterrupt as e:
                print()
                continue
            except Exception as e:
                print(e)
                continue
            args = line.strip().split()
            if len(args) > 0:
                self.errno = self.process_command(args[0], args[1:])
            else:
                self.errno = 0

    @staticmethod
    def execute(exe, args):
        try:
            return subprocess.Popen([exe,] + args).communicate()
        except Exception as e:
            print("exception while execute: [{}]".format(exe))
        except KeyboardInterrupt as e:
            print("keyboard interrupt while execute: [{}]".format(exe))

    def execute_python(self, script, args):
        return self.execute(
            "D:\\Python34\python.exe",
            [script, ] + args
        )

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

    def process_command(self, cmd, args):
        # try built-in command first
        handler_name = "command_" + cmd
        if hasattr(self, handler_name):
            return getattr(self, handler_name)(cmd, args)

        # find in paths
        cmd_path = self.find_cmd_in_paths(cmd)
        if not cmd_path:
            print("[{}]: not such command or file".format(cmd))
            return -1

        if cmd_path.endswith(".py"):
            return self.execute_python(cmd_path, args)
        else:
            return self.execute(cmd_path, args)

    def replace_variable(self, s):
        """ TODO: a very simple but usable implementation"""
        if s == "$?":
            if not self.errno:
                self.errno = 0
            return str(self.errno)
        else:
            return s

    def command_echo(self, cmd, args):
        print(" ".join(map(self.replace_variable, args)))

    def command_cd(self, cmd, args):
        if not args or len(args) != 1:
            print("no enough arguments")
            return -1

        new_path = os.path.join(self.cwd, args[0])
        os.chdir(new_path)
        self.cwd = os.getcwd()

    def command_ls(self, cmd, args):
        print(os.listdir(self.cwd))

    def command_dir(self, cmd, args):
        return self.command_ls(cmd, args)

    def command_pwd(self, cmd, args):
        print(self.cwd)

    def command_exit(self, cmd, args):
        self.is_running = False

    def command_help(self, cmd, args):
        print(self.cmd_map)

    @staticmethod
    def create_subprocess(args, stdin=None, stdout=None, stderr=None):
        return subprocess.Popen(args, stdin, stdout, stderr)


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


