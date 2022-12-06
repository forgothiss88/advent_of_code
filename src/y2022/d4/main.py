import re
from io import TextIOWrapper
from typing import Iterator

from tools.tools import get_input_dir

pair_re = re.compile("(\d+)-(\d+),(\d+)-(\d+)")


def allocations(f: TextIOWrapper) -> Iterator[tuple[set[int], set[int]]]:
    for line in f:
        m = pair_re.match(line)
        pair1 = range(int(m[1]), int(m[2]) + 1)
        pair2 = range(int(m[3]), int(m[4]) + 1)
        yield set(pair1), set(pair2)


def is_any_set_a_subset(s1: set[int], s2: set[int]) -> bool:
    return s1.issubset(s2) or s2.issubset(s1)


def are_set_overlapping(s1: set[int], s2: set[int]) -> bool:
    return not s1.isdisjoint(s2)


def part_1():
    count_rearranges = 0
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for elf1, elf2 in allocations(f):
            if is_any_set_a_subset(s1=elf1, s2=elf2):
                count_rearranges += 1

    print(count_rearranges)


def part_2():
    count_overlapping = 0
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for elf1, elf2 in allocations(f):
            if are_set_overlapping(s1=elf1, s2=elf2):
                count_overlapping += 1

    print(count_overlapping)


def solve():
    part_1()
    part_2()


if __name__ == "__main__":
    solve()
