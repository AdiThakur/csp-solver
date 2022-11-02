from abc import ABC, abstractmethod
from enum import Enum
import sys
from typing import *


Grid = List[List[str]]
Cell = Tuple[int, int]
# list of sub pieces, list of starting segment pieces, list of middle segment pieces, list of ending segment pieces
PossiblePieces = Tuple[List['Piece'], List['Piece'], List['Piece'], List['Piece']]


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

    def __repr__(self) -> str:
        return f"Id: {self.id}, Type: {self.ptype}, orient: {self.orientation}"


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


# Returns pieces in three groups: subs and water, start pieces, middle pieces, end pieces
# This does not include water; that should included in the domain generation logic
def generate_ship_pieces(
    ship_count: List[int]
    ) -> Tuple[List[Piece], List[Piece], List[Piece], List[Piece]]:

    # submarines, destroyers, cruisers and battleships
    SUB = 0
    START = 1
    MID = 2
    END = 3
    pieces = ([], [], [], [])

    # Subs
    for i in range(ship_count[0]):
        pieces[SUB].append(
            Piece(i, PieceType.Sub, Piece.H)
        )

    # Destroyers
    for i in range(ship_count[1]):

        pieces[START].append(Piece(i, PieceType.D_S, Piece.H))
        pieces[END].append(Piece(i, PieceType.D_E, Piece.H))

        pieces[START].append(Piece(i, PieceType.D_S, Piece.V))
        pieces[END].append(Piece(i, PieceType.D_E, Piece.V))

    # Cruisers
    for i in range(ship_count[2]):

        pieces[START].append(Piece(i, PieceType.C_S, Piece.H))
        pieces[MID].append(Piece(i, PieceType.C_M, Piece.H))
        pieces[END].append(Piece(i, PieceType.C_E, Piece.H))

        pieces[START].append(Piece(i, PieceType.C_S, Piece.V))
        pieces[MID].append(Piece(i, PieceType.C_M, Piece.V))
        pieces[END].append(Piece(i, PieceType.C_E, Piece.V))

    # Cruisers
    for i in range(ship_count[3]):

        pieces[START].append(Piece(i, PieceType.B_S, Piece.H))
        pieces[MID].append(Piece(i, PieceType.B_M1, Piece.H))
        pieces[MID].append(Piece(i, PieceType.B_M2, Piece.H))
        pieces[END].append(Piece(i, PieceType.B_E, Piece.H))

        pieces[START].append(Piece(i, PieceType.B_S, Piece.V))
        pieces[MID].append(Piece(i, PieceType.B_M1, Piece.V))
        pieces[MID].append(Piece(i, PieceType.B_M2, Piece.V))
        pieces[END].append(Piece(i, PieceType.B_E, Piece.V))

    return pieces


def generate_variables(grid: Grid) -> List[List[Cell]]:

    vars = []

    for row in range(len(grid)):
        vars_in_row = []
        for col in range(len(grid[row])):
            vars_in_row.append((row, col))
        vars.append(vars_in_row)

    return vars


def generate_domains(
    grid: Grid, pieces: List[Piece]
    ) -> Dict[Cell, List[Piece]]:

    domains = {}

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '0':
                flattened_pieces: List[Piece] = pieces[0] + pieces[1] + pieces[2] + pieces[3]
                domain = generate_domain_from_coordinate(
                    (row, col), len(grid), flattened_pieces
                )
            else:
                domain = generate_domain_from_hint(grid[row][col], pieces)
            domains[(row, col)] = domain

    return domains


def get_fitting_ship_types(start: int, space_avail: int) -> List[PieceType]:

    # All cells can hold subs
    fitting_types = [PieceType.Sub]

    # Add starting pieces if they fit
    if space_avail >= 4:
        fitting_types.append(PieceType.B_S)
    if space_avail >= 3:
        fitting_types.append(PieceType.C_S)
    if space_avail >= 2:
        fitting_types.append(PieceType.D_S)

    # Add middle pieces if they fit
    if start >= 1 and space_avail >= 2:
        fitting_types.append(PieceType.C_M)
    if start >= 1 and space_avail >= 3:
        fitting_types.append(PieceType.B_M1)
    if start >= 2 and space_avail >= 2:
        fitting_types.append(PieceType.B_M2)

    # Add ending pieces if they fit
    if start >= 3:
        fitting_types.append(PieceType.B_E)
    if start >= 2:
        fitting_types.append(PieceType.C_E)
    if start >= 1:
        fitting_types.append(PieceType.D_E)

    return fitting_types


def generate_domain_from_coordinate(
    coord: Cell, dimension: int, possible_ship_pieces: List[Piece]) -> List[Piece]:

    # Every non hint cell can contain water
    domain = [
        Piece(id=0, ptype=PieceType.Water, orientation=Piece.H)
    ]

    vertical_types = get_fitting_ship_types(coord[0], dimension - coord[0])
    horizontal_types = get_fitting_ship_types(coord[1], dimension - coord[1])

    for piece in possible_ship_pieces:
        if piece.orientation == Piece.H and piece.ptype in horizontal_types:
            domain.append(piece)
        if piece.orientation == Piece.V and piece.ptype in vertical_types:
            domain.append(piece)

    return domain


def filter_pieces_by_orientation(
    pieces: List[Piece], orientation: int) -> List[Piece]:

    matching_pieces = []
    for piece in pieces:
        if piece.orientation == orientation:
            matching_pieces.append(piece)
    return matching_pieces


# TODO: Test this
def generate_domain_from_hint(
    hint: str, pieces: PossiblePieces) -> List[Piece]:

    if hint == 'S':
        return pieces[0]
    if hint == 'W':
        return [Piece(id=0, ptype=PieceType.Water, orientation=Piece.H)]
    if hint == 'L':
        return filter_pieces_by_orientation(pieces[1], Piece.H)
    if hint == 'R':
        return filter_pieces_by_orientation(pieces[3], Piece.H)
    if hint == 'T':
        return filter_pieces_by_orientation(pieces[1], Piece.V)
    if hint == 'B':
        return filter_pieces_by_orientation(pieces[3], Piece.V)
    if hint == 'M':
        return pieces[2]

    return []


def main(input_filename: str, output_filename: str) -> None:
    # generate pieces (based on ship counts)
    # generate variables
    # assign starting domain to each variable
    # generate constraints for grid;
        # generate row constraints
        # generate col constraints
        # generate diagonal water constraints
        # generate ship constraints for each ship
        # generate unique ship constraints for every pair of cells

    row_cons, col_cons, ship_count, grid = read_input(input_filename)
    vars = generate_variables(grid)
    pieces = generate_ship_pieces(ship_count)
    domains = generate_domains(grid, pieces)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 battle.py <input_file> <output_file>")
        exit()

    main(
        input_filename=sys.argv[1],
        output_filename=sys.argv[2]
    )

# TODO: Prune domain based off coordinates; clearly cell at (0,0) can't have a middle or end piece type