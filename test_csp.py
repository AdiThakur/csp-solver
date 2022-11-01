import unittest
from battle import *


class TestFindSupport(unittest.TestCase):
    def test_one_valid_support(self):
        # Arrange
        variables = [(0, 1), (0, 2), (0, 3)]
        domains = {
            (0, 1): [
                Piece(1, PieceType.C_S, Piece.H)
            ],
            (0, 2): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ],
            (0, 3): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ]
        }
        constraint = CruiserConstraint(variables)

        support_for = 0
        assignment = [-1] * 3
        assignment[support_for] = Piece(1, PieceType.C_S, Piece.H)

        sut = CSP(variables, domains, [constraint], { (0, 1): constraint })

        # Act
        result = sut._find_support(
            support_for, constraint, assignment, 0
        )

        # Assert
        self.assertTrue(result)

    def test_no_valid_support(self):
        # Arrange
        variables = [(3, 3), (3, 4), (3, 5)]
        domains = {
            (3, 3): [
                Piece(1, PieceType.C_S, Piece.V)
            ],
            (3, 4): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ],
            (3, 5): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ]
        }
        constraint = CruiserConstraint(variables)

        support_for = 0
        assignment = [-1] * 3
        assignment[support_for] = Piece(1, PieceType.C_S, Piece.V)

        sut = CSP(variables, domains, [constraint], { (3, 3): constraint })

        # Act
        result = sut._find_support(
            support_for, constraint, assignment, 0
        )

        # Assert
        self.assertFalse(result)


class TestGacEnforce(unittest.TestCase):
    def test_basic_case(self):
        # Arrange
        variables = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2),
        ]

        domains = {
            (0, 0): [ Piece(1, PieceType.C_S, Piece.H)],
            (0, 1): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H),
            ],
            (0, 2): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ],
            (1, 0): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ],
            (2, 0): [
                Piece(0, PieceType.Water, Piece.H),
                Piece(1, PieceType.C_S, Piece.H),
                Piece(1, PieceType.C_M, Piece.H),
                Piece(1, PieceType.C_E, Piece.H)
            ]
        }

        cruiser_h_con = CruiserConstraint([(0, 0), (0, 1), (0, 2)])
        cruiser_v_con = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        vars_to_cons = {
            (0, 0): [cruiser_h_con, cruiser_v_con],
            (0, 1): [cruiser_h_con],
            (0, 2): [cruiser_h_con],
            (1, 0): [cruiser_v_con],
            (2, 0): [cruiser_v_con],
        }

        sut = CSP(
            variables,
            domains,
            [cruiser_h_con, cruiser_v_con],
            vars_to_cons
        )
        sut.gac_stack = [cruiser_h_con, cruiser_v_con]
        sut.pruned_domains[0] = {}

        # Act
        result = sut._gac_enforce(0)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
