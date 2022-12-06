import re
from collections import defaultdict
from dataclasses import dataclass
from io import TextIOWrapper

from tools.tools import get_input_dir

move_re = re.compile("move (\d+) from (\d+) to (\d+)")
# [T] [G] [T] [R] [B] [P] [B] [G] [G]
#     [A] [B]             [C]

StateRow = dict[int, str]


@dataclass
class Move:
    from_pile: int
    to_pile: int
    num_crates: int


def read_move(line: str):
    m = move_re.match(line)
    return Move(num_crates=int(m[1]), from_pile=int(m[2]), to_pile=int(m[3]))


def mover(one_by_one: bool = True):
    def make_move(state: dict[int, str], move: Move):
        _buf = state[move.from_pile]
        new_pile = (
            _buf[-move.num_crates :][::-1]
            if one_by_one
            else _buf[-move.num_crates :]
        )
        state[move.to_pile] = state[move.to_pile] + new_pile
        state[move.from_pile] = _buf[: -move.num_crates]

    return make_move


def read_state_row(line: str) -> list[tuple[int, str]]:
    row = []
    idx = 1
    while True:
        try:
            cur_crate = line[idx]
        except IndexError:
            break
        if cur_crate.isalpha():
            row.append((idx // 4 + 1, cur_crate))
        idx += 4
    return row


def read_initial_state(
    f: TextIOWrapper,
) -> dict[int, list[str]]:
    init_state = defaultdict(str)
    for line in f:
        if line == "\n":
            break
        cur_state = read_state_row(line=line)
        for pile, crate in cur_state:
            init_state[pile] = crate + init_state[pile]

    return init_state


def solve_part(mover):
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        piles = read_initial_state(f=f)
        for line in f:
            move = read_move(line=line)
            mover(state=piles, move=move)
    top_crates = [piles[idx + 1][-1] for idx in range(len(piles))]
    print("".join(top_crates))


def solve():
    solve_part(mover=mover(one_by_one=True))
    solve_part(mover=mover(one_by_one=False))


if __name__ == "__main__":
    solve()
