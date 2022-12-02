from __future__ import annotations

from enum import Enum


class Outcome(Enum):
    Lose = -1
    Draw = 0
    Win = 1

    def predict_play(self, opponents_play: RPS) -> RPS:
        return rps_order[(rps_order.index(opponents_play) + self.value) % 3]

    @property
    def score(self):
        return 3 + self.value * 3

    @classmethod
    def from_plays(cls, my_play: RPS, opponents_play: RPS) -> Outcome:
        if my_play < opponents_play:
            return cls.Lose
        elif my_play == opponents_play:
            return cls.Draw
        return cls.Win


class RPS(Enum):
    Rock = 1
    Paper = 2
    Scissor = 3

    @property
    def score(self):
        return self.value

    def __lt__(self, other: RPS):
        return (rps_order.index(self) + 1) % 3 == (rps_order.index(other)) % 3


rps_order = [RPS.Rock, RPS.Paper, RPS.Scissor]
