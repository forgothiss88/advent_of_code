from importlib import import_module

import click


@click.command()
@click.argument("day", type=int)
@click.argument("year", type=int, default=2022)
def main(day: int, year: int):
    challenge = import_module(name=f"y{year}.d{day}.main")
    challenge.solve()


if __name__ == "__main__":
    main()
