from io import TextIOWrapper
from typing import Iterator

from tools.tools import get_input_dir


def elves_calories(f: TextIOWrapper) -> Iterator[int]:
    cals = 0
    for line in f:
        try:
            cals += int(line)
        except ValueError:
            yield cals
            cals = 0

    return cals


def part_1():
    max_elf_cals = 0
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for cur_elf_cals in elves_calories(f):
            max_elf_cals = max(max_elf_cals, cur_elf_cals)

    print(max_elf_cals)


def part_2():
    top_elves = [0, 0, 0]
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        for cur_elf_cals in elves_calories(f):
            top_elves.append(cur_elf_cals)
            top_elves.sort(reverse=True)
            top_elves.pop()

    print(sum(top_elves))


def solve():
    part_1()
    part_2()


if __name__ == "__main__":
    solve()
