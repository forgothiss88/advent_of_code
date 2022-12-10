from io import TextIOWrapper


def input_rows(f: TextIOWrapper):
    for line in f:
        yield [int(tree) for tree in line[:-1]]


def solve():
    from y2022.d8 import part_1, part_2

    part_1.solve()
    part_2.solve()


if __name__ == "__main__":
    solve()
