from __future__ import annotations

import re
from abc import abstractmethod

from y2022.d7.filesystem import FilesystemNode


class Cmd:
    cmd_re: re.Pattern

    @classmethod
    def parse_cmd(cls, command_string: str) -> Cmd:
        m = cls.cmd_re.match(command_string)
        if not m:
            raise ValueError(f"Command {command_string} is not a {cls}")
        cmd = cls.create_cmd(matches=m)
        return cmd

    @abstractmethod
    def create_cmd(cls, matches: list) -> Cmd:
        pass

    @abstractmethod
    def parse_output(self, lines: list[str]) -> Cmd:
        pass

    @abstractmethod
    def exec(self, node: FilesystemNode) -> FilesystemNode:
        pass


class cdCmd(Cmd):
    cmd_re = re.compile("\$ cd (\w+|\.\.|\.)")

    def __init__(self, dir_name: str):
        self.dir_name = dir_name

    @classmethod
    def create_cmd(cls, matches: re.Match):
        return cls(dir_name=matches[1])

    def parse_output(self, lines: list[str] = None):
        return self

    def exec(self, node: FilesystemNode) -> FilesystemNode:
        if self.dir_name == ".":
            return node
        if self.dir_name == "..":
            return node.parent
        new_node = FilesystemNode(parent=node)
        node.children[self.dir_name] = new_node
        return new_node


class lsCmd(Cmd):
    cmd_re = re.compile("\$ ls")
    output_re = re.compile("")

    def __init__(self) -> None:
        self.output = {}

    @classmethod
    def create_cmd(cls, matches: re.Match):
        return cls()

    def parse_output(self, lines: list[str]):
        # dir e
        # 29116 f
        dir_re = re.compile("^dir (\w+)")
        file_re = re.compile("^(\d+) ([\w\.]+)")
        for line in lines:
            m_dir = dir_re.match(line)
            m_file = file_re.match(line)
            if m_dir:
                self.output[m_dir[1]] = None
            elif m_file:
                self.output[m_file[2]] = int(m_file[1])
            else:
                break
        return self

    def exec(self, node: FilesystemNode) -> FilesystemNode:
        for name, size in self.output.items():
            new_node = FilesystemNode(parent=node, size=size)
            node.children[name] = new_node
        return node
