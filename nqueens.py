import sys
from typing import Dict, List, Tuple

from csp import CSP, Assignment, Constraint, Domain, Variable


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


def main(input_filename: str) -> None:
    dimension, starting_queens = read_input(input_filename)
    solution = solve(dimension, starting_queens)
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


def solve(dimension: int, starting_queens: List[int]) -> Domain:
    vars, domains, assigned_vars = generate_vars_and_domains(dimension, starting_queens)
    constraints, vars_to_cons = generate_constraints(vars)
    solver = CSP(vars, domains, constraints, vars_to_cons, assigned_vars)
    _, solution = solver.satisfy()

    return solution


def generate_vars_and_domains(
    dimension: int, starting_queens: List[int]
    ) -> Tuple[List[Variable], Domain, List[Variable]]:

    variables: List[Variable] = []
    domains: Domain = {}
    assigned_vars: List[Variable] = []

    for i in range(dimension):

        variable = i
        variables.append(variable)

        if starting_queens[i] == NO_QUEEN_INDEX:
            domains[variable] = [x for x in range(dimension)]
        else:
            domains[variable] = [starting_queens[i]]
            assigned_vars.append(variable)

    return variables, domains, assigned_vars


def generate_constraints(
    vars: List[Variable]) -> Tuple[List[Constraint], Dict[Variable, List[Constraint]]]:

    constraints = []
    vars_to_cons = {}
    for variable in vars:
        vars_to_cons[variable] = []

    constraints += (generate_vertical_constraints(vars, vars_to_cons))
    constraints += (generate_diagonal_constraints(vars, vars_to_cons))

    return constraints, vars_to_cons


def generate_vertical_constraints(
    vars: List[Variable], vars_to_cons: Dict[Variable, List[Constraint]]
    ) -> List[Constraint]:

    vertical_constraints = []

    for var1 in range(len(vars)):
        for var2 in range(var1 + 1, len(vars), 1):
            constraint = VerticalConstraint([var1, var2])
            vertical_constraints.append(constraint)
            vars_to_cons[var1].append(constraint)
            vars_to_cons[var2].append(constraint)

    return vertical_constraints


def generate_diagonal_constraints(
    vars: List[Variable], vars_to_cons: Dict[Variable, List[Constraint]]
    ) -> List[Constraint]:

    diagonal_constraints = []

    for var1 in range(len(vars)):
        for var2 in range(var1 + 1, len(vars), 1):
            constraint = DiagonalConstraint([var1, var2])
            diagonal_constraints.append(constraint)
            vars_to_cons[var1].append(constraint)
            vars_to_cons[var2].append(constraint)

    return diagonal_constraints


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
        print("Usage: python3 <input_file>")
        exit()
    main(sys.argv[1])
