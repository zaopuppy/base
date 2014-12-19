#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ["Shell"]


import os
import os.path
import subprocess
import sys

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

    def init(self):
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
        read_line = readline.Readline()
        while self.is_running:
            try:
                if not read_line:
                    line = input(self.ps1)
                else:
                    line = read_line.readline(self.ps1)
            except KeyboardInterrupt as e:
                print()
                continue
            args = line.strip().split()
            if len(args) > 0:
                self.errno = self.process_command(args[0], args[1:])
            else:
                self.errno = 0

    def execute(self, exe, args):
        try:
            return subprocess.Popen([exe,] + args).wait()
        except Exception as e:
            print("exception while execute: [{}]".format(exe))
        except KeyboardInterrupt as e:
            print("keyboard interrupt while execute: [{}]".format(exe))

    def execute_python(self, script, args):
        return self.execute(
            "D:\\Python34\python.exe",
            [script,] + args
        )

    def find_cmd_in_paths(self, cmd):
        for path, cmds in self.cmd_map.items():
            if cmd in cmds:
                return os.path.join(path, cmd)
            elif cmd + ".py" in cmds:
                return os.path.join(path, cmd + ".py")
            elif cmd + ".exe" in cmds:
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

def main():
    # sh = Shell(path=["c:\\Windows\\System32\\"])
    sh = Shell(
        path=[os.path.join(os.getcwd(), "module")]
    )
    sh.init()
    if len(sys.argv) <= 1:
        sh.run()
    else:
        # execute script
        raise Exception("Not implemented")


if __name__ == "__main__":
    main()


