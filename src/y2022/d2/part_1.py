from io import TextIOWrapper
from typing import Iterator

from y2022.d2.rps import RPS, Outcome

opponents_mapper = {"A": RPS.Rock, "B": RPS.Paper, "C": RPS.Scissor}
my_mapper = {"X": RPS.Rock, "Y": RPS.Paper, "Z": RPS.Scissor}


def rounds(f: TextIOWrapper) -> Iterator[tuple[RPS, Outcome]]:
    for line in f:
        opponents_play = opponents_mapper[line[0]]
        my_play = my_mapper[line[2]]
        my_outcome = Outcome.from_plays(
            my_play=my_play, opponents_play=opponents_play
        )
        yield my_play, my_outcome
