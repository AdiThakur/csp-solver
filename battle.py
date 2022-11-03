from abc import ABC, abstractmethod
from enum import Enum
import sys
from typing import *


Grid = List[List[str]]
Cell = Tuple[int, int]
# list of sub pieces, list of starting segment pieces, list of middle segment pieces, list of ending segment pieces
PossiblePieces = Tuple[List['Piece'], List['Piece'], List['Piece'], List['Piece']]


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

    def __str__(self) -> str:
        return str(self.ptype)

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


class UniqueConstraint(Constraint):

    def is_satisfied(self, assignment: List[Piece]) -> bool:

        c1, c2 = assignment

        if (c1.ptype == PieceType.Water) or (c2.ptype == PieceType.Water):
            return True
        if c1.ptype != c2.ptype:
            return True
        return c1.id != c2.id


class CSP:

    values: Dict[Cell, Piece]
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
        self.values = {}
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

        self.vars_to_cons = vars_to_cons
        self.pruned_domains = {}
        self._init_assigned()
        self.gac_stack = []

    def satisfy(self) -> bool:
        return self._fc(0)

    def _init_assigned(self) -> None:
        self.assigned = {}
        for variable in self.variables:
            self.assigned[variable] = False
            self.values[variable] = None

    def _fc(self, level: int) -> bool:

        var = self._pick_unassigned_variable()
        if var is None:
            return True

        self.pruned_domains[level] = {}
        self.assigned[var] = True

        for value in self.domains[var]:

            self.values[var] = value
            dwo = False

            for constraint in self.vars_to_cons[var]:
                count, unassigned_var = self._get_last_unassigned(constraint)
                # Only one unassigned variable in scope
                if count == 1:
                    if self._fc_check(constraint, unassigned_var, level):
                        dwo = True
                        break

            if not dwo:
                if self._fc(level + 1):
                    return True
            # Restore all pruned values
            for pruned_var in self.pruned_domains[level]:
                self.domains[pruned_var].extend(self.pruned_domains[level][pruned_var])
                self.pruned_domains[level][pruned_var] = []

        self.values[var] = None
        self.assigned[var] = False

        return False

    def _fc_check(self, constraint: Constraint, var: Cell, level: int) -> bool:

        assignment = [None] * len(constraint.scope)
        var_i = 0

        for i in range(len(constraint.scope)):
            con_var = constraint.scope[i]
            if con_var == var:
                var_i = i
            else:
                assignment[i] = self.values[con_var]

        for value in self.domains[var]:
            assignment[var_i] = value
            if not constraint.is_satisfied(assignment):
                # Prune value
                self.domains[var].remove(value)
                if var not in self.pruned_domains[level]:
                    self.pruned_domains[level][var] = []
                self.pruned_domains[level][var].append(value)
            if len(self.domains[var]) == 0:
                return True

        return False

    def _get_last_unassigned(
        self, constraint: Constraint) -> Tuple[int, Optional[Cell]]:

        unassigned_count = 0
        unassigned_var = None

        for var in constraint.scope:
            if self.assigned[var] == False:
                unassigned_count += 1
                unassigned_var = var

        return unassigned_count, unassigned_var

    def _pick_unassigned_variable(self) -> Optional[Cell]:

        mrv_variable: Optional[Cell] = None
        min_domain = 1000

        for variable in self.variables:
            if self.assigned[variable]:
                continue
            domain_len = len(self.domains[variable])
            if domain_len < min_domain:
                min_domain = domain_len
                mrv_variable = variable

        return mrv_variable


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


def generate_ship_pieces(ship_count: List[int]) -> PossiblePieces:

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
    if len(ship_count) > 1:
        for i in range(ship_count[1]):

            pieces[START].append(Piece(i, PieceType.D_S, Piece.H))
            pieces[END].append(Piece(i, PieceType.D_E, Piece.H))

            pieces[START].append(Piece(i, PieceType.D_S, Piece.V))
            pieces[END].append(Piece(i, PieceType.D_E, Piece.V))

    # Cruisers
    if len(ship_count) > 2:
        for i in range(ship_count[2]):

            pieces[START].append(Piece(i, PieceType.C_S, Piece.H))
            pieces[MID].append(Piece(i, PieceType.C_M, Piece.H))
            pieces[END].append(Piece(i, PieceType.C_E, Piece.H))

            pieces[START].append(Piece(i, PieceType.C_S, Piece.V))
            pieces[MID].append(Piece(i, PieceType.C_M, Piece.V))
            pieces[END].append(Piece(i, PieceType.C_E, Piece.V))

    # Battleships
    if len(ship_count) > 3:
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
    grid: Grid, pieces: PossiblePieces) -> Dict[Cell, List[Piece]]:

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


def add_constraint_for_var(
    vars_to_cons: Dict[Cell, List[Constraint]],
    var: Cell,
    constraint: Constraint) -> None:
    if var not in vars_to_cons:
        vars_to_cons[var] = []
    vars_to_cons[var].append(constraint)


def add_constraint_for_vars(
    vars_to_cons: Dict[Cell, List[Constraint]],
    vars: List[Cell],
    constraint: Constraint) -> None:
    for var in vars:
        add_constraint_for_var(vars_to_cons, var, constraint)


def generate_sum_cons(
    vars: List[List[Cell]],
    vars_to_cons: Dict[Cell, List[Constraint]],
    row_sums: List[int],
    col_sums: List[int]) -> List[LineSumConstraint]:

    constraints = []

    # Add rows
    for index, row in enumerate(vars):
        row_sum_con = LineSumConstraint(scope=row, sum=row_sums[index])
        constraints.append(row_sum_con)
        add_constraint_for_vars(vars_to_cons, row, row_sum_con)

    # Add cols
    for col in range(len(vars)):
        cells_in_col = [row[col] for row in vars]
        col_sum_con = LineSumConstraint(scope=cells_in_col, sum=col_sums[col])
        constraints.append(col_sum_con)
        add_constraint_for_vars(vars_to_cons, cells_in_col, col_sum_con)

    return constraints


def generate_water_cons(
    vars: List[List[Cell]],
    vars_to_cons: Dict[Cell, List[Constraint]]) -> List[DiagonalConstraint]:

    dim = len(vars)
    constraints = []

    for row in range(dim):
        for col in range(len(vars[row])):

            coord = (row, col)
            bot_left_diag = (row + 1, col - 1)
            bot_right_diag = (row + 1, col + 1)

            if bot_left_diag[0] < dim and bot_left_diag[1] >= 0:
                scope = [coord, bot_left_diag]
                diag_con = DiagonalConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, diag_con)
                constraints.append(diag_con)

            if bot_right_diag[0] < dim and bot_right_diag[1] < dim:
                scope = [coord, bot_right_diag]
                diag_con = DiagonalConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, diag_con)
                constraints.append(diag_con)

    return constraints


def generate_ship_cons(
    vars: List[List[Cell]],
    vars_to_cons: Dict[Cell, List[Constraint]]) -> List[Constraint]:

    dim = len(vars)
    constraints = []

    for row in range(len(vars)):
        for col in range(len(vars)):

            # horizontal
            fitting_types = get_fitting_ship_types(col, dim - col)

            if PieceType.D_S in fitting_types:
                scope = [(row, col), (row, col + 1)]
                ship_con = DestroyerConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

            if PieceType.C_S in fitting_types:
                scope = [(row, col), (row, col + 1), (row, col + 2)]
                ship_con = CruiserConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

            if PieceType.B_S in fitting_types:
                scope = [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]
                ship_con = BattleshipConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

            # vertical
            fitting_types = get_fitting_ship_types(row, dim - row)

            if PieceType.D_S in fitting_types:
                scope = [(row, col), (row + 1, col)]
                ship_con = DestroyerConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

            if PieceType.C_S in fitting_types:
                scope = [(row, col), (row + 1, col), (row + 2, col)]
                ship_con = CruiserConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

            if PieceType.B_S in fitting_types:
                scope = [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]
                ship_con = BattleshipConstraint(scope)
                add_constraint_for_vars(vars_to_cons, scope, ship_con)
                constraints.append(ship_con)

    return constraints


def generate_unique_cons(
    flattened_vars: List[Cell],
    vars_to_cons: Dict[Cell, List[Constraint]]) -> List[Constraint]:

    constraints = []

    for cell1 in flattened_vars:
        for cell2 in flattened_vars:
            if cell1 == cell2:
                continue
            scope = [cell1, cell2]
            unique_con = UniqueConstraint(scope)
            add_constraint_for_vars(vars_to_cons, scope, unique_con)
            constraints.append(unique_con)

    return constraints


def get_output_symbol(piece: Piece) -> str:

    if piece.ptype == PieceType.Water:
        return 'W'
    if piece.ptype == PieceType.Sub:
        return 'S'
    if piece.ptype in [PieceType.C_M, PieceType.B_M1, PieceType.B_M2]:
        return 'M'

    # Oriented pieces
    if piece.orientation == Piece.H:
        if piece.ptype in [PieceType.D_S, PieceType.C_S, PieceType.B_S]:
            return 'L'
        if piece.ptype in [PieceType.D_E, PieceType.C_E, PieceType.B_E]:
            return 'R'
    else:
        if piece.ptype in [PieceType.D_S, PieceType.C_S, PieceType.B_S]:
            return 'T'
        if piece.ptype in [PieceType.D_E, PieceType.C_E, PieceType.B_E]:
            return 'B'

    return ''


def print_goal_state(
    vars: List[List[Cell]], values: Dict[Cell, Piece]
    ) -> None:

    for row in vars:
        output_row = ""
        for cell in row:
            out_symbol = get_output_symbol(values[cell])
            output_row += f"{out_symbol} "
        print(output_row)


def main(input_filename: str, output_filename: str) -> None:

    row_sums, col_sums, ship_count, grid = read_input(input_filename)
    pieces = generate_ship_pieces(ship_count)

    vars = generate_variables(grid)
    domains = generate_domains(grid, pieces)
    constraints = []
    vars_to_cons = {}

    flattened_vars: List[Cell] = []
    for row in vars:
        flattened_vars.extend(row)

    constraints += generate_sum_cons(vars, vars_to_cons, row_sums, col_sums)
    constraints += generate_water_cons( vars, vars_to_cons)
    constraints += generate_ship_cons(vars, vars_to_cons)
    constraints += generate_unique_cons(flattened_vars, vars_to_cons)

    csp = CSP(
        flattened_vars,
        domains,
        constraints,
        vars_to_cons
    )

    sol_found = csp.satisfy()
    if sol_found:
        print_goal_state(vars, csp.values)
    else:
        print("No sol found")


if __name__ == "__main__":

    # if len(sys.argv) != 3:
    #     print("Usage: python3 battle.py <input_file> <output_file>")
    #     exit()

    # main(
    #     input_filename=sys.argv[1],
    #     output_filename=sys.argv[2]
    # )

    main(f"./battle_validate/input_{'easy1'}.txt", "out.txt")
