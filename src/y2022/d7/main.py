from __future__ import annotations

import functools
import itertools
from cmd import Cmd
from io import TextIOWrapper

from tools.tools import get_input_dir
from y2022.d7.commands import cdCmd, lsCmd
from y2022.d7.filesystem import FilesystemNode

cmds: list[Cmd] = [cdCmd, lsCmd]


def choose_command(command_string: str):
    for cmd_cls in cmds:
        try:
            return cmd_cls.parse_cmd(command_string=command_string)
        except ValueError:
            continue
    raise ValueError(f"Command not found {command_string}")


def command_parser(f: TextIOWrapper):
    cur_cmd = None
    cur_output = []
    for line in f:
        if not line.startswith("$"):
            cur_output.append(line)
            continue
        if cur_cmd is not None:
            cur_cmd.parse_output(cur_output)
            yield cur_cmd
        cur_output = []
        cur_cmd = choose_command(command_string=line)

    yield cur_cmd.parse_output(cur_output)


def find_nodes_max_size(
    node: FilesystemNode, max_size: int
) -> list[FilesystemNode]:
    nodes = []
    for child_node in node.children.values():
        nodes.extend(find_nodes_max_size(node=child_node, max_size=max_size))
    if node.size <= max_size and node.children:
        nodes.append(node)
    return nodes


def find_nodes_min_size(
    node: FilesystemNode, min_size: int
) -> list[FilesystemNode]:
    nodes = []
    for child_node in node.children.values():
        nodes.extend(find_nodes_min_size(node=child_node, min_size=min_size))
    if node.size >= min_size and node.children:
        nodes.append(node)
    return nodes


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        root = FilesystemNode(parent=None)
        new_node = root
        # ignore first line
        f.readline()
        for cmd in command_parser(f=f):
            new_node = cmd.exec(node=new_node)

    small_dirs = find_nodes_max_size(root, max_size=100000)
    small_dirs_size = sum(node.size for node in small_dirs)
    print(small_dirs_size)

    free_size = 70000000 - root.size
    free_size_needed = 30000000

    min_size_to_free = free_size_needed - free_size
    small_dirs = find_nodes_min_size(root, min_size=min_size_to_free)
    small_dirs = sorted(small_dirs, key=lambda node: node.size)
    candidate = next(
        itertools.dropwhile(
            lambda node: node.size < min_size_to_free, small_dirs
        )
    )
    print(candidate.size)


if __name__ == "__main__":
    solve()
