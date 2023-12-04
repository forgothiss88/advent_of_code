from __future__ import annotations

import re

from tools.tools import get_input_dir

word_digit_map = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
}
word_digit_bw_map = {k[::-1]: v for k, v in word_digit_map.items()}

digit_words = "|".join(word_digit_map.keys())
digit_words_bw = "|".join(word_digit_bw_map.keys())

def get_leftmost_digit(s: str) -> int:
    # get the first digit occured in the string with a regex
    match = re.search(rf'(?P<d>\d)|(?P<w>{digit_words})', s)
    if not match:
        raise ValueError("No digit found in string")
    d = match.groupdict()
    if m := d["d"]:
        return int(m)
    m = d["w"]
    return word_digit_map[m]

def get_rightmost_digit(s: str) -> int:
        # get the first digit occured in the string with a regex
    match = re.search(rf'(?P<d>\d)|(?P<w>{digit_words_bw})', s[::-1])
    if not match:
        raise ValueError("No digit found in string")
    d = match.groupdict()
    if m := d["d"]:
        return int(m)
    m = d["w"]
    return word_digit_bw_map[m]

def solve_part1():
    input_dir = get_input_dir(fname=__file__)
    with open(file=(input_dir / "input.txt"), mode="r") as f:
        tot = 0
        for l in f:
            l_num = get_leftmost_digit(l)
            r_num = get_rightmost_digit(l)
            tot = tot + l_num * 10 + r_num

    return tot



def solve():
    print(solve_part1())
    # solve_part2()


if __name__ == "__main__":
    solve()
