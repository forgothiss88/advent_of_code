import itertools
from io import TextIOWrapper
from typing import Iterator

from tools.tools import get_input_dir
from y2022.d3.rucksack import item_value


def rucksack_groups(f: TextIOWrapper) -> Iterator[list[str]]:
    while True:
        lines = list(itertools.islice(f, 3))
        if lines:
            yield lines
        else:
            return


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        group_ids: list[set[str]] = []
        for group in rucksack_groups(f):
            cur_group = set()
            for racksack in group:
                com = cur_group.intersection(set(racksack[:-1]))
                com = com or set(racksack[:-1])
                if com:
                    cur_group = com
            group_ids.append(cur_group)

    print(sum(item_value(item) for item in itertools.chain(*group_ids)))


if __name__ == "__main__":
    solve()
