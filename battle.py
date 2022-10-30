from abc import ABC, abstractmethod
from enum import Enum
import sys
from typing import *


Grid = List[List[str]]
Cell = Tuple[int, int]


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


class Piece(Enum):
    # Water
    Water = 0
    # Submarine (1x1)
    Sub = 1

    # Destroyer (1x2)
    D_H_S = 2
    D_H_E = 3
    D_V_S = 4
    D_V_E = 5

    # Cruiser (1x3)
    C_H_S = 6
    C_H_E = 7
    C_M = 8
    C_V_S = 9
    C_V_E = 10

    # Cruiser (1x3)
    B_H_S = 11
    B_H_E = 12
    B_M = 13
    B_V_S = 14
    B_V_E = 15


class Constraint(ABC):

    scope: List[Cell] = []

    @abstractmethod
    # The order of variable assignments in parameter <assignment>
    # must match order of variables in scope
    def is_satisfied(self, assignment: List[Piece]) -> bool:
        pass


class HorizontalConstraint(Constraint):

    def __init__(self, cells: List[Cell]) -> None:

        row = cells[0][0]
        prev_col = cells[0][1] - 1

        for cell in cells:
            if cell[0] != row:
                raise Exception("All Cells must be on the same row")
            if prev_col + 1 != cell[1]:
                raise Exception("All Cells must be contiguous")
            prev_col = cell[1]

        self.scope = cells


class VerticalConstraint(Constraint):

    def __init__(self, cells: List[Cell]) -> None:

        col = cells[0][1]
        prev_row = cells[0][0] - 1

        for cell in cells:
            if cell[1] != col:
                raise Exception("All Cells must be on the same column")
            if prev_row + 1 != cell[0]:
                raise Exception("All Cells must be contiguous")
            prev_row = cell[0]

        self.scope = cells


class DestroyerHorizontal(HorizontalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 2:
            raise Exception("Invalid (horizontal) Destroyer Assignment")

        if assignment[0] != Piece.D_H_S:
            return True
        return assignment[1] == Piece.D_H_E;


class DestroyerVertical(VerticalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 2:
            raise Exception("Invalid (vertical) Destroyer Assignment")

        if assignment[0] != Piece.D_V_S:
            return True
        return assignment[1] == Piece.D_V_E;


class CruiserHorizontal(HorizontalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 3:
            raise Exception("Invalid (horizontal) Cruiser Assignment")

        if assignment[0] != Piece.C_H_S:
            return True
        return assignment[1] == Piece.C_M and assignment[2] == Piece.C_H_E;


class CruiserVertical(VerticalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 3:
            raise Exception("Invalid (vertical) Cruiser Assignment")

        if assignment[0] != Piece.C_V_S:
            return True
        return assignment[1] == Piece.C_M and assignment[2] == Piece.C_V_E;


class BattleshipHorizontal(HorizontalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 4:
            raise Exception("Invalid (horizontal) Battleship Assignment")

        if assignment[0] != Piece.B_H_S:
            return True
        return assignment[1] == Piece.B_M and assignment[2] == Piece.B_M \
            and assignment[3] == Piece.B_H_E;


class BattleshipVertical(VerticalConstraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 4:
            raise Exception("Invalid (vertical) Battleship Assignment")

        if assignment[0] != Piece.B_V_S:
            return True
        return assignment[1] == Piece.B_M and assignment[2] == Piece.B_M \
            and assignment[3] == Piece.B_V_E;


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
