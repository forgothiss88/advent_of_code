from io import TextIOWrapper
from typing import Iterator

from y2022.d2.rps import RPS, Outcome

opponents_mapper = {"A": RPS.Rock, "B": RPS.Paper, "C": RPS.Scissor}
my_mapper = {"X": Outcome.Lose, "Y": Outcome.Draw, "Z": Outcome.Win}


def rounds(f: TextIOWrapper) -> Iterator[tuple[RPS, Outcome]]:
    for line in f:
        opponents_play = opponents_mapper[line[0]]
        my_outcome = my_mapper[line[2]]
        my_play = my_outcome.predict_play(opponents_play=opponents_play)
        yield my_play, my_outcome
