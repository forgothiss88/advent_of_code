from io import TextIOWrapper

from tools.tools import get_input_dir


def reader(f: TextIOWrapper):
    yield f.read(1)


def marker_finder(marker_len: int):
    def find_marker_pos(packet: str):
        for idx in range(marker_len, len(packet)):
            _buf = packet[idx - marker_len : idx]
            if len(set(_buf)) == marker_len:
                return idx

        raise ValueError()

    return find_marker_pos


def solve_part(marker_finder):
    input_dir = get_input_dir(fname=__file__)

    with open(file=(input_dir / "input.txt"), mode="r") as f:
        packet = f.read()
        marker_pos = marker_finder(packet)

    print(marker_pos)


def solve():
    solve_part(marker_finder=marker_finder(marker_len=4))
    solve_part(marker_finder=marker_finder(marker_len=14))


if __name__ == "__main__":
    solve()
