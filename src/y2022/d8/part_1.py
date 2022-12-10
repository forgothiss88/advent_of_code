import numpy as np

from tools.tools import get_input_dir
from y2022.d8.main import input_rows


def line_visibility(tree_line: np.ndarray[int]) -> np.ndarray[int]:
    cur_visibility = np.zeros_like(tree_line)
    _vis = 0
    for i, tree in enumerate(tree_line):
        if tree <= _vis and i > 0:
            continue
        _vis = tree
        cur_visibility[i] = 1
    return cur_visibility


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        rows = [row for row in input_rows(f=f)]

    m = np.array(rows, dtype=int)

    vis_l = np.apply_along_axis(line_visibility, 1, m)

    vis_r = np.flip(
        np.apply_along_axis(line_visibility, 1, np.flip(m, 1)), axis=1
    )

    vis_t = np.apply_along_axis(line_visibility, 0, m)

    vis_b = np.flip(
        np.apply_along_axis(line_visibility, 0, np.flip(m, 0)), axis=0
    )
    tot: np.ndarray = vis_l + vis_r + vis_t + vis_b
    print(tot.clip(max=1).sum())
