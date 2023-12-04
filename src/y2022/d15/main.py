from __future__ import annotations

import dataclasses as dc
import itertools
import re
from collections import defaultdict
from io import TextIOWrapper
from typing import Iterator, Optional

import numpy as np
import numpy.typing as npt

from tools.tools import get_input_dir

Pos = tuple[int, int]

sensor_reg = re.compile(
    # Sensor at x=168413, y=3989039: closest beacon is at x=-631655, y=3592291
    "Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)"
)


def manhattan_distance(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Sensor at x=407069, y=1770807: closest beacon is at x=105942, y=2000000
def read_sensors(f: TextIOWrapper) -> Iterator[tuple[Pos, Pos]]:
    for line in f:
        m = sensor_reg.match(line.strip())
        sensor_pos = int(m[1]), int(m[2])
        beacon_pos = int(m[3]), int(m[4])
        # manhattan distance where shouldn't be any beacons
        # field = manhattan_distance(sensor_pos, beacon_pos)
        yield sensor_pos, beacon_pos


def find_covered_spots_in_row(
    s: Pos, b: Pos, y: int, min_x: int = None, max_x: int = None
) -> set[Pos]:
    field = manhattan_distance(s, b)
    cur_dist = manhattan_distance(s, (s[0], y))
    if cur_dist > field:
        # the sensor field cannot reach y
        return set()
    d = field - cur_dist

    min_x = s[0] - d if min_x is None else max(s[0] - d, min_x)
    max_x = s[0] + d + 1 if max_x is None else min(max_x, s[0] + d + 1)

    covered_spots = set((ix, y) for ix in range(min_x, max_x))

    return covered_spots


def find_uncovered_spots_in_row(
    s: Pos, b: Pos, y: int, min_x: int, max_x: int
) -> set[Pos]:
    field = manhattan_distance(s, b)
    cur_dist = manhattan_distance(s, (s[0], y))
    if cur_dist > field:
        # the sensor field cannot reach y, returning all points
        uncovered_spots = set((x, y) for x in range(min_x, max_x + 1))
        return uncovered_spots
    d = field - cur_dist
    uncovered_spots = set((ix, y) for ix in range(min_x, s[0] - d)).union(
        set((x, y) for x in range(s[0] + d + 1, max_x))
    )

    return uncovered_spots


def solve_part1(fname: str = "input.txt", y: int = 2_000_000):
    input_dir = get_input_dir(fname=__file__)
    covered_spots = set()
    sensors = []
    beacons = []
    with open(file=(input_dir / fname), mode="r") as f:
        for s, b in read_sensors(f=f):
            sensors.append(s)
            beacons.append(b)
            covered_spots.update(find_covered_spots_in_row(s=s, b=b, y=y))

    beacons_set = set(beacons)
    covered_spots.difference_update(beacons_set)

    return len(covered_spots), sensors, beacons


def solve_part2(
    sensors: list[Pos], beacons: list[Pos], search_area: tuple[Pos, Pos]
):
    min_x, min_y = search_area[0]
    max_x, max_y = search_area[1]
    uncovered_spots = set(
        (x, y)
        for x, y in itertools.product(
            range(min_x, max_x + 1), range(min_y, max_y + 1)
        )
    )
    for s, b in zip(sensors, beacons):
        _spots = set().update(
            find_uncovered_spots_in_row(
                s=s, b=b, y=y, min_x=min_x, max_x=max_x
            )
            for y in range(min_y, max_y + 1)
        )

        uncovered_spots.intersection_update(_spots)
    beacons_set = set(beacons)
    uncovered_spots.difference_update(beacons_set)

    assert len(uncovered_spots) == 1
    spot = uncovered_spots.pop()

    return spot[0] * 4_000_000 + spot[1]


def solve():
    ret, sensors, beacons = solve_part1(fname="input.txt", y=2_000_000)
    print(ret)
    ret = solve_part2(
        beacons=sensors,
        sensors=beacons,
        search_area=((0, 0), (4_000_000, 4_000_000)),
    )
    print(ret)


def test():
    test_ret, test_sensors, test_beacons = solve_part1(
        fname="dummy_input.txt", y=10
    )
    print(f"Test {test_ret} vs Expected 26")
    assert test_ret == 26
    test_ret = solve_part2(
        beacons=test_sensors,
        sensors=test_beacons,
        search_area=((0, 0), (20, 20)),
    )
    print(f"Test {test_ret} vs Expected 56000011")
    assert test_ret == 56000011


if __name__ == "__main__":
    test()
    solve()
