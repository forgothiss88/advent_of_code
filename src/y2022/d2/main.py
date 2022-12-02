from io import TextIOWrapper
from typing import Callable, Iterator

from tools.tools import get_input_dir
from y2022.d2 import part_1, part_2
from y2022.d2.rps import RPS, Outcome


def calc_score(play: RPS, outcome: Outcome) -> int:
    return play.score + outcome.score


def solve_part(
    round_iterator: Callable[[TextIOWrapper], Iterator[tuple[RPS, Outcome]]]
):
    input_dir = get_input_dir(fname=__file__)
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        scores = [
            calc_score(my_play, my_outcome)
            for my_play, my_outcome in round_iterator(f)
        ]

    tot_score = sum(scores)

    print(tot_score)


def solve():
    solve_part(round_iterator=part_1.rounds)
    solve_part(round_iterator=part_2.rounds)


if __name__ == "__main__":
    solve()
