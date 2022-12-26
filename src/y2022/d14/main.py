from __future__ import annotations

import dataclasses as dc
import itertools
import re
from collections import defaultdict
from io import TextIOWrapper
from typing import Optional

import numpy as np
import numpy.typing as npt

from tools.tools import get_input_dir

Pos = tuple[int, int]

m = np.full(shape=(1000, 1000), fill_value=True)


def get_rock_paths(f: TextIOWrapper):
    for line in f:
        coords = line.strip().split(sep=" -> ")
        ret = []
        for coord in coords:
            x, y = coord.strip().split(",")
            ret.append((int(x), int(y)))
        yield ret


class SandGrainOutOfBounds(Exception):
    pass


def apply_gravity(pos: Pos):
    try:
        delta_y = np.argwhere(m[pos[0], pos[1] :] == False)[0][0] - 1
        pos = (pos[0], pos[1] + max(delta_y, 0))
        return pos
    except IndexError:
        raise SandGrainOutOfBounds()


def slide_left(pos: Pos):
    new_pos = pos[0] - 1, pos[1] + 1
    if m[new_pos] == True:
        return new_pos
    return None


def slide_right(pos: Pos):
    new_pos = pos[0] + 1, pos[1] + 1
    if m[new_pos] == True:
        return new_pos
    return None


def update_sand_grain(pos: Pos):
    while True:
        pos = apply_gravity(pos=pos)
        left_path = slide_left(pos=pos)
        if left_path is not None:
            pos = left_path
            continue

        right_path = slide_right(pos=pos)
        if right_path is not None:
            pos = right_path
            continue

        # grain is still
        return pos


def create_path(path: list[tuple[int, int]]):
    for A, B in zip(path[:-1], path[1:]):
        # rock path from -> to
        xf, xt = sorted((A[0], B[0]))
        yf, yt = sorted((A[1], B[1]))
        m[xf : xt + 1, yf : yt + 1] = False


def solve_part1():
    input_dir = get_input_dir(fname=__file__)
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for path in get_rock_paths(f=f):
            create_path(path)

    # Add the initial path.
    counter = itertools.count()

    for i in counter:
        try:
            pos = update_sand_grain(pos=(500, 0))
            m[pos] = False
        except SandGrainOutOfBounds:
            break

    print(i)


def solve_part2():
    input_dir = get_input_dir(fname=__file__)
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for path in get_rock_paths(f=f):
            create_path(path)

    highest_y_idx = np.nonzero(m == False)[1].max()
    p = [(0, highest_y_idx + 2), (m.shape[0], highest_y_idx + 2)]
    create_path(path=p)

    # Add the initial path.
    counter = itertools.count(start=1)

    for i in counter:
        pos = update_sand_grain(pos=(500, 0))
        m[pos] = False
        if pos == (500, 0):
            break

    print(i)


def solve():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    solve()
