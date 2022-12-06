from io import TextIOWrapper
from typing import Iterator


def item_value(item: str):
    val = ord(item)
    if item.islower():
        return val - ord("a") + 1
    return val - ord("A") + 27


def rucksacks(f: TextIOWrapper) -> Iterator[int]:
    for line in f:
        yield line[:-1]
