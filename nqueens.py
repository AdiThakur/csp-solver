import sys
from typing import List, Tuple

from csp_builder import CSPBuilder
from csp import Assignment, Constraint, Domain


QUEEN_CHAR = 'Q'
NO_QUEEN_CHAR = '-'
NO_QUEEN_INDEX = -1


class VerticalConstraint(Constraint):
    def is_satisfied(self, assignment: Assignment) -> bool:
        var1, var2 = self.scope
        return assignment[var1] != assignment[var2]

    def __repr__(self) -> str:
        return f"VC: {self.scope}"


class DiagonalConstraint(Constraint):
    def is_satisfied(self, assignment: Assignment) -> bool:
        var1, var2 = self.scope
        return (var2 - var1) != (abs(assignment[var2] - assignment[var1]))

    def __repr__(self) -> str:
        return f"DC: {self.scope}"


class NQueensSolver():

    def __init__(self, dimension: int, starting_queens: List[int]) -> None:
        self.dimension: int = dimension
        self.starting_queens: List[int] = starting_queens
        self.builder: CSPBuilder = CSPBuilder()

    def solve(self) -> Domain:
        self._add_variables()
        self._add_constraints()
        csp = self.builder.build()
        _, solution = csp.satisfy()

        return solution

    def _add_variables(self) -> None:
        for var in range(self.dimension):
            if self.starting_queens[var] == NO_QUEEN_INDEX:
                self.builder.add_variable(var, [col for col in range(self.dimension)])
            else:
                self.builder.add_variable(var, [self.starting_queens[var]])

    def _add_constraints(self) -> None:
        self._add_vertical_constraints()
        self._add_diagonal_constraints()

    def _add_vertical_constraints(self) -> None:
        for var1 in range(self.dimension):
            for var2 in range(var1 + 1, self.dimension, 1):
                constraint = VerticalConstraint([var1, var2])
                self.builder.add_constraint(constraint)

    def _add_diagonal_constraints(self) -> None:
        for var1 in range(self.dimension):
            for var2 in range(var1 + 1, self.dimension, 1):
                constraint = DiagonalConstraint([var1, var2])
                self.builder.add_constraint(constraint)


def main(input_filename: str) -> None:
    dimension, starting_queens = read_input(input_filename)
    solver = NQueensSolver(dimension, starting_queens)
    solution = solver.solve()
    print_solution(dimension, solution)


def read_input(input_filename: str) -> Tuple[int, List[int]]:

    dimension = 0
    starting_queens: List[int] = []

    with open(input_filename, mode='r') as input_file:
        dimension = int(input_file.readline())
        for line in input_file:
            char = line.strip()
            if char == NO_QUEEN_CHAR:
                starting_queens.append(NO_QUEEN_INDEX)
            else:
                starting_queens.append(int(char))

    return dimension, starting_queens


def print_solution(dimension: int, solution: Domain) -> None:

    if not solution:
        print("No valid solutions found")
        return

    SPACING = " "
    grid: List[List[str]] = []

    for i in range(dimension):
        grid.append([NO_QUEEN_CHAR for j in range(dimension)])

    for variable in solution:
        queen_index = solution[variable][0]
        grid[variable][queen_index] = QUEEN_CHAR

    header_str = "  " + SPACING.join([str(i) for i in range(dimension)])
    grid_str = ""

    for index, row in enumerate(grid):
        grid_str += f'{str(index)} {SPACING.join(row)}\n'

    print(header_str)
    print(grid_str)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 nqueens.py <input_file>")
        exit()
    main(sys.argv[1])
