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


class PieceType(Enum):
    # Water
    Water = 0
    # Submarine (1x1)
    Sub = 1
    # Destroyer (1x2)
    D_S = 20
    D_E = 21
    # Cruiser (1x3)
    C_S = 31
    C_M = 32
    C_E = 33
    # Battleship (1x4)
    B_S = 41
    B_M1 = 42
    B_M2 = 43
    B_E = 44

class Piece:

    id: int
    orientation: int
    ptype: PieceType

    # Horizontal Orientation
    H = 0
    # Vertical Orientation
    V = 1

    def __init__(self, id: int, ptype: PieceType, orientation: int) -> None:
        self.id = id
        self.ptype = ptype
        self.orientation = orientation


class Constraint(ABC):

    scope: List[Cell] = []

    def  __init__(self, scope: List[Cell]) -> None:
        self.scope = scope

    def _id_and_orient_match(self, assignment: List[Piece]) -> bool:
        id = assignment[0].id
        orientation = assignment[0].orientation
        for a in assignment:
            if (a.id != id) or (a.orientation != orientation):
                return False
        return True

    @abstractmethod
    # The order of variable assignments in parameter <assignment>
    # must match order of variables in scope
    def is_satisfied(self, assignment: List[Piece]) -> bool:
        pass


class DestroyerConstraint(Constraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 2:
            raise Exception("Invalid (horizontal) Destroyer Assignment")

        if assignment[0].ptype != PieceType.D_S:
            return True
        return assignment[1].ptype == PieceType.D_E and \
            self._id_and_orient_match(assignment)


class CruiserConstraint(Constraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 3:
            raise Exception("Invalid (horizontal) Cruiser Assignment")

        if assignment[0].ptype != PieceType.C_S:
            return True
        return assignment[1].ptype == PieceType.C_M and \
            assignment[2].ptype == PieceType.C_E and \
            self._id_and_orient_match(assignment)


class BattleshipConstraint(Constraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        if len(assignment) != 4:
            raise Exception("Invalid (horizontal) Battleship Assignment")

        if assignment[0].ptype != PieceType.B_S:
            return True
        return assignment[1].ptype == PieceType.B_M1 and \
            assignment[2].ptype == PieceType.B_M2 and \
            assignment[3].ptype == PieceType.B_E and \
            self._id_and_orient_match(assignment)


class LineSumConstraint(Constraint):

    sum: int = 0

    def __init__(self, scope: List[Cell], sum: int) -> None:
        super().__init__(scope)
        self.sum = sum

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        curr_sum = 0
        for value in assignment:
            if value.ptype != PieceType.Water:
                curr_sum += 1

        return self.sum == curr_sum


class DiagonalConstraint(Constraint):

    # d1 is the top diagonal in pair, d2 is bottom
    def __init__(self, scope: List[Cell]) -> None:
        d1, d2 = scope
        if (d1[0] == d2[0]) or (d1[1] == d2[1]):
            raise Exception("Invalid diagonal")
        super().__init__(scope)

    def is_satisfied(self, assignment: List[Piece]) -> bool:
        return assignment[0].ptype == PieceType.Water or assignment[1].ptype == PieceType.Water


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

def generate_domain_from_hint(hint: str) -> List[PieceType]:

    if hint == 'S':
        return [PieceType.Sub]
    if hint == 'W':
        return [PieceType.Water]
    if hint == 'L':
        return [PieceType.D_H_S, PieceType.C_H_S, PieceType.B_H_S]
    if hint == 'R':
        return [PieceType.D_H_E, PieceType.C_H_E, PieceType.B_H_E]
    if hint == 'T':
        return [PieceType.D_V_S, PieceType.C_V_S, PieceType.B_V_S]
    if hint == 'B':
        return [PieceType.D_V_E, PieceType.C_V_E, PieceType.B_V_E]
    if hint == 'M':
        return [PieceType.C_M, PieceType.B_M]

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