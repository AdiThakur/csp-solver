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

    def  __init__(self, scope: List[Cell]) -> None:
        self.scope = scope

    @abstractmethod
    # The order of variable assignments in parameter <assignment>
    # must match order of variables in scope
    def is_satisfied(self, assignment: List[Piece]) -> bool:
        pass


class HorizontalConstraint(Constraint):

    def __init__(self, scope: List[Cell]) -> None:

        row = scope[0][0]
        prev_col = scope[0][1] - 1

        for cell in scope:
            if cell[0] != row:
                raise Exception("All Cells must be on the same row")
            if prev_col + 1 != cell[1]:
                raise Exception("All Cells must be contiguous")
            prev_col = cell[1]

        super().__init__(scope)


class VerticalConstraint(Constraint):

    def __init__(self, scope: List[Cell]) -> None:

        col = scope[0][1]
        prev_row = scope[0][0] - 1

        for cell in scope:
            if cell[1] != col:
                raise Exception("All Cells must be on the same column")
            if prev_row + 1 != cell[0]:
                raise Exception("All Cells must be contiguous")
            prev_row = cell[0]

        super().__init__(scope)


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


class ShipSum(Constraint):

    sum: int = 0

    def __init__(self, scope: List[Cell], sum: int) -> None:
        super().__init__(scope)
        self.sum = sum

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        curr_sum = 0
        for value in assignment:
            if value != Piece.Water:
                curr_sum += 1

        return self.sum == curr_sum


class DiagonalWater(Constraint):

    # d1 is the top diagonal in pair, d2 is bottom
    def __init__(self, scope: List[Cell]) -> None:
        d1, d2 = scope
        if (d1[0] == d2[0]) or (d1[1] == d2[1]):
            raise Exception("Invalid diagonal")
        super().__init__(scope)

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        return assignment[0] == Piece.Water or assignment[1] == Piece.Water


class CSP:

    variables: List[Cell]
    domains: Dict[Cell, List[Piece]]
    constraints: List[Constraint]

    vars_to_cons: Dict[Cell, List[Constraint]]
    pruned_domains: Dict[int, Dict[Cell, List[Piece]]]
    assigned: Dict[Cell, bool]
    gac_stack: List[Constraint]

    def __init__(
        self,
        variables: List[Cell],
        domains: Dict[Cell, List[Piece]],
        constraints: List[Constraint],
        vars_to_cons: Dict[Cell, List[Constraint]]
        ) -> None:

        self.variables = variables
        self.domains = domains
        self.constraints = constraints

        self.vars_to_cons = vars_to_cons
        self.pruned_domains = {}
        self._init_assigned()
        self.gac_stack = []

    def satisfy(self) -> bool:
        self._gac_enforce(0)
        return self._gac(0)

    def _init_assigned(self) -> None:
        self.assigned = {}
        for variable in self.variables:
            self.assigned[variable] = False

    def _gac(self, gac_level: int) -> bool:

        var = self._pick_unassigned_variable()
        if var is None:
            return True

        self.pruned_domains[gac_level] = {}
        self.assigned[var] = True

        for val_index in range(self.domains[var]):

            # Prune all other values for current variable
            for other_index in range(self.domains[var]):
                if val_index != other_index:
                    self._prune_value(gac_level, var, other_index)

            # Build gac-stack
            for constraint in self.vars_to_cons[var]:
                self.gac_stack.append(constraint)

            # CSP is GAC
            if self._gac_enforce(gac_level):
                if self._gac(gac_level + 1):
                    return True

            # Restore domains of all affected variables
            for affected_var in self.pruned_domains[gac_level]:
                self.domains[affected_var].extend(
                    self.pruned_domains[gac_level][affected_var]
                )
                self.pruned_domains[gac_level][affected_var] = []

        self.assigned[var] = False
        self.pruned_domains.pop(gac_level, None)

        return False

    def _prune_value(
        self, gac_level: int, variable: Cell, index_to_prune: int
        ) -> None:

        val_to_prune = self.domains[variable][index_to_prune]
        self.domains[variable][index_to_prune] = self.domains[variable][-1]
        self.domains[variable].pop()

        if variable not in self.pruned_domains[gac_level]:
            self.pruned_domains[gac_level][variable] = []

        self.pruned_domains[gac_level][variable].append(val_to_prune)

    def _pick_unassigned_variable(self) -> Optional[Cell]:

        mrv_variable: Optional[Cell] = None
        min_domain = 100

        for variable in self.variables:
            if self.assigned[variable]:
                continue
            domain_len = len(self.domains[variable])
            if domain_len < min_domain:
                min_domain = domain_len
                mrv_variable = variable

        return mrv_variable

    # Returns True if CSP is GAC, False if DWO occurs
    def _gac_enforce(self, gac_level: int) -> bool:

        while len(self.gac_stack) > 0:

            constraint = self.gac_stack.pop()

            for variable_index, variable in enumerate(constraint.scope):
                for value_index, value in enumerate(self.domains[variable]):

                    assignment = [-1] * len(constraint.scope)
                    assignment[variable_index] = value
                    support_found = self._find_support(
                        variable_index, constraint, assignment, 0
                    )

                    if support_found:
                        continue

                    self._prune_value(gac_level, variable, value_index)

                    # DWO
                    if len(self.domains[variable]) == 0:
                        self.gac_stack = []
                        return False

                    for constraint in self.vars_to_cons[variable]:
                        # TODO: Implement a Hash augmented stack for faster lookup
                        if constraint not in self.gac_stack:
                            self.gac_stack.append(constraint)

        return True

    def _find_support(
        self,
        support_for: int,
        constraint: Constraint,
        assignment: List[Piece],
        variable_index: int
        ) -> bool:

        if variable_index == len(constraint.scope):
            return constraint.is_satisfied(assignment)
        if variable_index == support_for:
            return self._find_support(
                support_for, constraint, assignment, variable_index + 1
            )

        for value in self.domains[constraint.scope[variable_index]]:
            assignment[variable_index] = value
            valid = self._find_support(
                support_for, constraint, assignment, variable_index + 1
            )
            if valid:
                return True

        return False


def read_input(
    input_filename: str
) -> Tuple[List[int], List[int], List[int], Grid]:

    row_cons = []
    col_cons = []
    ship_cons = []
    grid = []

    with open(input_filename) as file:

        lines = file.readlines()

        row_cons = [int(i) for i in lines[0].strip()]
        col_cons = [int(i) for i in lines[1].strip()]
        ship_cons = [int(i) for i in lines[2].strip()]

        for line in lines[3:]:
            grid.append([*line.strip()])

    return row_cons, col_cons, ship_cons, grid


def generate_domain_from_coordinate(coord: Cell) -> List[Piece]:
    pass

def generate_domain_from_hint(hint: str) -> List[Piece]:

    if hint == 'S':
        return [Piece.Sub]
    if hint == 'W':
        return [Piece.Water]
    if hint == 'L':
        return [Piece.D_H_S, Piece.C_H_S, Piece.B_H_S]
    if hint == 'R':
        return [Piece.D_H_E, Piece.C_H_E, Piece.B_H_E]
    if hint == 'T':
        return [Piece.D_V_S, Piece.C_V_S, Piece.B_V_S]
    if hint == 'B':
        return [Piece.D_V_E, Piece.C_V_E, Piece.B_V_E]
    if hint == 'M':
        return [Piece.C_M, Piece.B_M]

def main(input_filename: str, output_filename: str) -> None:
    # generate constraints for grid;
    # generate row constraints
    # generate col constraints

    row_cons, col_cons, ship_cons, grid = read_input(input_filename)
    dimension = len(grid)

    # Normally variables are stored in a 1D list, but here it is stored as a
    # 2D grid for easier domain and constrain generations
    vars_in_grid = []
    domains: Dict[Cell, List[Piece]] = []

    # Create variables
    for row in range(len(grid)):
        vars_in_row = []
        for col in range(len(grid[row])):
            vars_in_row.append((row, col))
        vars_in_grid.append(vars_in_row)

    # Create domains for variables
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '0':
                domain = generate_domain_from_coordinate((row, col))
            else:
                domain = generate_domain_from_hint(grid[row][col])
            domains[(row, col)] = domain

    print(domains)




if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 battle.py <input_file> <output_file>")
        exit()

    main(
        input_filename=sys.argv[1],
        output_filename=sys.argv[2]
    )

# TODO: Prune domain based off coordinates; clearly cell at (0,0) can't have a middle or end piece type