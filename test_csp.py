import unittest
from battle import *


class TestFindSupport(unittest.TestCase):
    def test_one_valid_support(self):
        # Arrange
        variables = [(0, 1), (0, 2), (0, 3)]
        domains = {
            (0, 1): { Piece.C_H_S },
            (0, 2): { Piece.Water, Piece.C_H_S, Piece.C_M, Piece.C_H_E },
            (0, 3): { Piece.Water, Piece.C_H_S, Piece.C_M, Piece.C_H_E }
        }
        constraint = CruiserHorizontal(variables)

        support_for = 0
        assignment = [-1] * 3
        assignment[support_for] = Piece.C_H_S

        sut = CSP(variables, domains, [constraint])

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
            (3, 3): { Piece.C_H_S },
            (3, 4): { Piece.Water, Piece.C_H_S, Piece.C_H_E },
            (3, 5): { Piece.Water, Piece.C_H_S, Piece.C_M, Piece.C_H_E }
        }
        constraint = CruiserHorizontal(variables)

        support_for = 0
        assignment = [-1] * 3
        assignment[support_for] = Piece.C_H_S

        sut = CSP(variables, domains, [constraint])

        # Act
        result = sut._find_support(
            support_for, constraint, assignment, 0
        )

        # Assert
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()