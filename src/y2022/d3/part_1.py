from tools.tools import get_input_dir
from y2022.d3.rucksack import item_value, rucksacks


def find_wrong_item(rucksack: str):
    left_compt = set(rucksack[: len(rucksack) // 2])
    right_compt = set(rucksack[len(rucksack) // 2 :])
    return list(left_compt.intersection(right_compt))[0]


def solve():
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        item_sum = sum(
            item_value(item=find_wrong_item(rucksack=rucksack))
            for rucksack in rucksacks(f)
        )

    print(item_sum)


if __name__ == "__main__":
    solve()
