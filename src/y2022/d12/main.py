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

Path = list[Pos]

import sys

sys.setrecursionlimit(10000)  # 10000 is an example, try with different values


@dc.dataclass(eq=True)
class SemiPath:
    nodes: Path = dc.field(compare=False, hash=False)
    m: npt.NDArray[np.integer] = dc.field(compare=False, hash=False)

    @property
    def fr(self):
        return self.nodes[0]

    @property
    def to(self):
        return self.nodes[-1]

    def __len__(self):
        return len(self.nodes)

    def extend(self, to: Pos):
        self.nodes.append(to)

    def extend_new(self, to: Pos):
        return dc.replace(
            self,
            nodes=[*self.nodes, to],
        )

    def __getitem__(self, idx):
        return self.nodes[idx]

    def merge(self, other: SemiPath) -> SemiPath:
        pass


@dc.dataclass
class History:
    end: Pos
    m: npt.NDArray[np.integer]  # matrix of input data
    steps_m: npt.NDArray[np.integer] = dc.field(
        init=False
    )  # matrix of steps required to reach each pos

    def __post_init__(self):
        self.steps_m = np.full_like(self.m, fill_value=np.inf)

    def choices(self, cur: Pos):
        cur = np.array(cur)
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = cur + [dx, dy]
            if np.all(new_pos >= 0) and np.all(new_pos < self.m.shape):
                yield tuple(new_pos)

    def find_min_walk_from_start(self, steps_walked: int, cur_pos: Pos):
        for new_pos in self.choices(cur_pos):
            steps = steps_walked + 1
            if (
                self.m[cur_pos] + 1 >= self.m[new_pos]
                and self.steps_m[new_pos] > steps
            ):
                # new pos is reachable (max 1 uphill)
                # and it's convenient
                self.steps_m[new_pos] = steps
                if new_pos != self.end:
                    self.min_walk_start(steps_walked=steps, cur_pos=new_pos)

    def find_start_backwards(self, steps_walked: int, cur_pos: Pos):
        self.steps_m[cur_pos] = steps_walked
        if self.m[cur_pos] == 0:
            return
        steps = steps_walked + 1
        for prev_pos in self.choices(cur_pos):
            if (
                self.m[prev_pos] + 1 >= self.m[cur_pos]
                and self.steps_m[prev_pos] > steps
            ):
                # new pos is reachable (min 1 downhill)
                self.find_start_backwards(steps_walked=steps, cur_pos=prev_pos)


def input_matrix(
    f: TextIOWrapper,
) -> tuple[npt.NDArray[np.integer], Pos, Pos]:
    lines = []
    for line in f:
        _buff = line[:-1]
        lines.append([ord(c) for c in _buff])
    _m = np.array(lines)
    start = np.where(_m == ord("S"))
    end = np.where(_m == ord("E"))
    _m[start] = ord("a")
    _m[end] = ord("z")
    _m = _m - ord("a")
    return (
        _m,
        tuple(np.array(start).flatten()),
        tuple(np.array(end).flatten()),
    )


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        m, start, end = input_matrix(f=f)

    # h = History(end=end, m=m.copy())

    # h.min_walk_from_start(cur_pos=start, steps_walked=0)

    # print(h.steps_m[end])

    h = History(end=start, m=m.copy())

    h.find_start_backwards(cur_pos=end, steps_walked=0)

    ground = np.where(m == 0)

    steps_from_ground = h.steps_m[ground]
    print(np.min(steps_from_ground))


if __name__ == "__main__":
    solve()
