from __future__ import annotations

import math
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Callable, Optional

import numpy as np

from tools.tools import get_input_dir
from y2022.d11.monkey import parse_monkey


def solve_part(rounds: int, op_mod: int = 1, optimize: bool = False):
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        mk_string = f.read().split("Monkey")
        monkeys = [parse_monkey(multiline=mk_s) for mk_s in mk_string if mk_s]

    op_div = op_mod
    op_mod = np.prod([mk.test_div for mk in monkeys])
    for monkey in monkeys:
        monkey._monkeys = monkeys
        monkey.op_div = op_div
        if optimize:
            monkey.op_mod = op_mod

    for _ in range(rounds):
        for monkey in monkeys:
            monkey.inspect_items()

    mk_activities = [mk.items_inspected for mk in monkeys]
    mk_activities.sort(reverse=True)

    print(mk_activities[0] * mk_activities[1])


def solve():
    # solve_part(rounds=20, op_mod=3)
    solve_part(rounds=10_000, optimize=True)


if __name__ == "__main__":
    solve()
