import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from io import TextIOWrapper

import numpy as np
import pandas as pd

from tools.tools import get_input_dir

move_re = re.compile("move (\d+) from (\d+) to (\d+)")
# [T] [G] [T] [R] [B] [P] [B] [G] [G]
#     [A] [B]             [C]

StateRow = dict[int, str]


@dataclass
class Add:
    x: int


def instructions(f: TextIOWrapper):
    for line in f:
        try:
            x = line[4:-1]
        except IndexError:
            x = ""
        yield 0
        if x:
            yield int(x)


def signal_strength(signal: int, cycle: int):
    return signal * cycle


def solve_part_1():
    input_dir = get_input_dir(fname=__file__)
    xs = [1]
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for delta_x in instructions(f=f):
            xs.append(xs[-1] + delta_x)

    print(len(xs))

    cycles = [20, 60, 100, 140, 180, 220]

    print(sum(signal_strength(signal=xs[c - 1], cycle=c) for c in cycles))
    xs = np.array(xs[:-1])
    with open(file=("out.txt"), mode="w") as f:
        for crt_row in np.array_split(xs, 6):
            idxs = np.array(range(40))
            row = (idxs - 1 <= crt_row) & (crt_row <= idxs + 1)
            print("".join(["#" if x else "." for x in row]), file=f)


def solve():
    solve_part_1()


if __name__ == "__main__":
    solve()
