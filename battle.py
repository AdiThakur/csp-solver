import sys
from typing import *


Grid = List[List[str]]
Coord = Tuple[int, int]


input_chars = {
    '0',
    'S',
    'W',
    'L',
    'R',
    'T',
    'B',
    'M'
}


def read_input(
    input_filename: str
) -> Tuple[Grid, List[str], List[str], List[str]]:

    row_cons = []
    col_cons = []
    ship_cons = []
    grid = []

    with open(input_filename) as file:

        lines = file.readlines()

        row_cons = [*lines[0].strip()]
        col_cons = [*lines[1].strip()]
        ship_cons = [*lines[2].strip()]

        for line in lines[3:]:
            grid.append([*line.strip()])

    return grid, row_cons, col_cons, ship_cons


def main(input_filename: str, output_filename: str) -> None:
    grid, row_cons, col_cons, ship_cons = read_input(input_filename)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 battle.py <input_file> <output_file>")
        exit()

    main(
        input_filename=sys.argv[1],
        output_filename=sys.argv[2]
    )
