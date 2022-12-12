import math
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper
from typing import Optional

import numpy as np

from tools.tools import get_input_dir


class Direction(Enum):
    """Docstring for Direction."""

    U = "U"
    D = "D"
    L = "L"
    R = "R"

    def get_shift(self) -> tuple[int, int]:
        if self == Direction.U:
            return (0, 1)
        if self == Direction.D:
            return (0, -1)
        if self == Direction.L:
            return (-1, 0)
        if self == Direction.R:
            return (1, 0)


def moves(f: TextIOWrapper):
    for line in f:
        yield (Direction(value=line[0]), int(line[2:-1]))


def move_head(
    head_pos: tuple[int, int], direction: Direction, steps: int
) -> np.ndarray:
    delta_x, delta_y = direction.get_shift()
    return head_pos[0] + delta_x * steps, head_pos[1] + delta_y * steps


def move_tail(head_pos: tuple[int, int], tail_pos: tuple[int, int]):
    delta_x = head_pos[0] - tail_pos[0]
    delta_y = head_pos[1] - tail_pos[1]
    if abs(delta_x) <= 1 and abs(delta_y) <= 1:
        return tail_pos

    delta_x = np.clip(delta_x, a_min=-1, a_max=1)
    delta_y = np.clip(delta_y, a_min=-1, a_max=1)
    return tail_pos[0] + delta_x, tail_pos[1] + delta_y


def solve_part(knots: int):
    input_dir = get_input_dir(fname=__file__)
    rope = [(0, 0)] * knots
    positions = set()
    positions.add((0, 0))
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for direction, steps in moves(f=f):
            for _ in range(steps):
                rope[0] = move_head(
                    head_pos=rope[0], direction=direction, steps=1
                )
                for t_idx in range(1, len(rope)):
                    rope[t_idx] = move_tail(
                        head_pos=rope[t_idx - 1], tail_pos=rope[t_idx]
                    )

                positions.add(rope[-1])

    print(len(positions))


def solve():
    solve_part(knots=2)
    solve_part(knots=10)


if __name__ == "__main__":
    solve()
