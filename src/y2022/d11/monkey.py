from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


class Monkey:
    def __init__(
        self,
        items: list[int],
        op: Callable[[int], int],
        test_div: int,
        monkey_if_test_true: int,
        monkey_if_test_false: int,
        op_mod: Optional[int] = None,
        op_div: Optional[int] = None,
        monkeys: Optional[list[Monkey]] = None,
    ):
        self.items = items
        self.op = op
        self.test_div = test_div
        self.op_mod = op_mod
        self.op_div = op_div
        self._monkey_if_test_true = monkey_if_test_true
        self._monkey_if_test_false = monkey_if_test_false
        self._monkeys = monkeys
        self.items_inspected = 0

    def add_item(self, item: int):
        self.items.insert(0, item)

    def pop_item(self):
        return self.items.pop()

    def get_next_monkey(self, item: int):
        if (item % self.test_div) == 0:
            next_monkey = self._monkeys[self._monkey_if_test_true]
        else:
            next_monkey = self._monkeys[self._monkey_if_test_false]
        return next_monkey

    def inspect_item(self):
        item = self.pop_item()

        item = self.op(item)
        if self.op_div is not None:
            item = item // self.op_div
        if self.op_mod is not None:
            item = item % self.op_mod

        next_monkey = self.get_next_monkey(item=item)

        next_monkey.add_item(item)

        self.items_inspected += 1

    def inspect_items(self):
        while self.items:
            self.inspect_item()


def parse_items(line: str) -> list[int]:
    # Starting items: 83, 96, 86, 58, 92
    item_str = line.split(":")[1]
    ret = [int(item.strip()) for item in item_str.split(",")]
    ret.reverse()
    return ret


def parse_operation(line: int) -> Callable[[int], int]:
    # Operation: new = old + 8
    op = line.split("new =")[1].strip()

    def operation(old: int) -> int:
        return eval(op, {}, {"old": old})

    return operation


def parse_test_div(line: str) -> Callable[[int], bool]:
    # Test: divisible by 3
    div = line.split("divisible by")[1].strip()
    return int(div)


def parse_if(line: str) -> int:
    # If true: throw to monkey 2
    monkey = line.split("throw to monkey")[1].strip()
    return int(monkey)


def parse_monkey(multiline: str):
    # Monkey 4:
    # Starting items: 99
    # Operation: new = old * old
    # Test: divisible by 5
    #     If true: throw to monkey 0
    #     If false: throw to monkey 5
    multiline = multiline.split("\n")
    items = parse_items(multiline[1])
    op = parse_operation(multiline[2])
    test_div = parse_test_div(multiline[3])
    mk_true = parse_if(multiline[4])
    mk_false = parse_if(multiline[5])

    return Monkey(
        items=items,
        op=op,
        test_div=test_div,
        monkey_if_test_false=mk_false,
        monkey_if_test_true=mk_true,
    )
