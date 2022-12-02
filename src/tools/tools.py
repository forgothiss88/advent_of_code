from pathlib import Path


def get_input_dir(fname: str) -> Path:
    this_path = Path(fname)
    day = this_path.parent.name
    year = this_path.parent.parent.name
    root = this_path.parent.parent.parent.parent
    return root / "input" / year / day
