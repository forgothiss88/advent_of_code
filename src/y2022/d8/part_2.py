import numpy as np

from tools.tools import get_input_dir
from y2022.d8.main import input_rows


def rec_line_visibility(
    cur_tree: int,
    cur_res: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    if not cur_res:
        return [(cur_tree, 0)]

    _it = iter(i for i, el in enumerate(cur_res) if el[0] >= cur_tree)
    try:
        idx = next(_it)
    except StopIteration:
        idx = len(cur_res)
    new_vis = sum(el[1] for el in cur_res[:idx]) + 1
    new_res = [(cur_tree, new_vis)]
    new_res.extend(cur_res[idx:])
    return new_res


def rec_wrapper(tree_line: np.ndarray[int]):
    result = np.zeros_like(tree_line)
    prev_res = []
    for i in range(len(tree_line)):
        last_tree = tree_line[i]
        prev_res = rec_line_visibility(cur_tree=last_tree, cur_res=prev_res)
        result[i] = prev_res[0][1]
    return result


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        rows = [row for row in input_rows(f=f)]

    m = np.array(rows, dtype=int)

    vis_l = np.apply_along_axis(rec_wrapper, 1, m)

    vis_r = np.flip(np.apply_along_axis(rec_wrapper, 1, np.flip(m, 1)), axis=1)

    vis_t = np.apply_along_axis(rec_wrapper, 0, m)

    vis_b = np.flip(np.apply_along_axis(rec_wrapper, 0, np.flip(m, 0)), axis=0)

    tot: np.ndarray = vis_l * vis_r * vis_t * vis_b
    print(tot.max())
