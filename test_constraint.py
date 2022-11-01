import unittest
from battle import *


class TestDestroyerHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.C_M, Piece.H)
        ]
        sut = DestroyerConstraint([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.H),
            Piece(1, PieceType.D_E, Piece.H)
        ]
        sut = DestroyerConstraint([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment_missing_end(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.H),
            Piece(0, PieceType.Water, Piece.H)
        ]
        sut = DestroyerConstraint([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.H),
            Piece(2, PieceType.D_E, Piece.H)
        ]
        sut = DestroyerConstraint([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestDestroyerVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.V),
            Piece(1, PieceType.C_M, Piece.V)
        ]
        sut = DestroyerConstraint([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.V),
            Piece(1, PieceType.D_E, Piece.V)
        ]
        sut = DestroyerConstraint([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment_missing_end(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.V),
            Piece(0, PieceType.Water, Piece.V)
        ]
        sut = DestroyerConstraint([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.V),
            Piece(2, PieceType.D_E, Piece.V)
        ]
        sut = DestroyerConstraint([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_orientation(self):
        assignment = [
            Piece(1, PieceType.D_S, Piece.H),
            Piece(1, PieceType.D_E, Piece.V)
        ]
        sut = DestroyerConstraint([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(1, PieceType.B_M2, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.C_M, Piece.H),
            Piece(1, PieceType.C_E, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(1, PieceType.C_E, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.C_M, Piece.H),
            Piece(0, PieceType.Water, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.C_M, Piece.H),
            Piece(2, PieceType.C_E, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_orientation(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.C_M, Piece.V),
            Piece(1, PieceType.C_E, Piece.H)
        ]
        sut = CruiserConstraint([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(1, PieceType.C_M, Piece.V),
            Piece(1, PieceType.C_E, Piece.V)
        ]
        sut = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.V),
            Piece(1, PieceType.C_M, Piece.V),
            Piece(1, PieceType.C_E, Piece.V)
        ]
        sut = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.V),
            Piece(0, PieceType.Water, Piece.V),
            Piece(1, PieceType.C_E, Piece.V)
        ]
        sut = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.V),
            Piece(1, PieceType.C_M, Piece.V),
            Piece(1, PieceType.Water, Piece.V)
        ]
        sut = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.V),
            Piece(2, PieceType.C_M, Piece.V),
            Piece(1, PieceType.C_E, Piece.V)
        ]
        sut = CruiserConstraint([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.Sub, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(2, PieceType.Sub, Piece.H),
            Piece(2, PieceType.Sub, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(1, PieceType.B_M2, Piece.H),
            Piece(1, PieceType.B_E, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(1, PieceType.B_M2, Piece.H),
            Piece(1, PieceType.B_E, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(1, PieceType.B_E, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(1, PieceType.B_M2, Piece.H),
            Piece(0, PieceType.Water, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.H),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(2, PieceType.B_M2, Piece.H),
            Piece(3, PieceType.B_E, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_orientation(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(1, PieceType.B_M1, Piece.H),
            Piece(2, PieceType.B_M2, Piece.V),
            Piece(3, PieceType.B_E, Piece.H)
        ]
        sut = BattleshipConstraint([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [
            Piece(1, PieceType.Sub, Piece.V),
            Piece(0, PieceType.Water, Piece.V),
            Piece(0, PieceType.Water, Piece.V),
            Piece(2, PieceType.Sub, Piece.V)
        ]
        sut = BattleshipConstraint([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(1, PieceType.B_M1, Piece.V),
            Piece(1, PieceType.B_M2, Piece.V),
            Piece(1, PieceType.B_E, Piece.V)
        ]
        sut = BattleshipConstraint([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(0, PieceType.Water, Piece.V),
            Piece(1, PieceType.B_M1, Piece.V),
            Piece(1, PieceType.B_E, Piece.V)
        ]

        sut = BattleshipConstraint([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(1, PieceType.B_M1, Piece.V),
            Piece(0, PieceType.Water, Piece.V),
            Piece(1, PieceType.B_E, Piece.V)
        ]
        sut = BattleshipConstraint([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [
            Piece(1, PieceType.B_S, Piece.V),
            Piece(1, PieceType.B_M1, Piece.V),
            Piece(1, PieceType.B_M2, Piece.V),
            Piece(0, PieceType.Water, Piece.V)
        ]
        sut = BattleshipConstraint([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestSum(unittest.TestCase):
    def test_all_water(self):
        assignment = [Piece(0, PieceType.Water, Piece.H)] * 4
        sut = LineSumConstraint(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_less_than_sum(self):
        assignment = [
            Piece(0, PieceType.Water, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(1, PieceType.Sub, Piece.H)
        ]
        sut = LineSumConstraint(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_more_than_sum(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.Sub, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(2, PieceType.Sub, Piece.H)
        ]
        sut = LineSumConstraint(
            sum=2,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_just_right(self):
        assignment = [
            Piece(1, PieceType.C_S, Piece.H),
            Piece(1, PieceType.Sub, Piece.H),
            Piece(0, PieceType.Water, Piece.H),
            Piece(2, PieceType.Sub, Piece.H)
        ]
        sut = LineSumConstraint(
            sum=3,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)


class TestWater(unittest.TestCase):
    def test_both_water(self):
        assignment = [Piece(0, PieceType.Water, Piece.H)] * 2
        sut = DiagonalConstraint([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_first_water(self):
        assignment = [
            Piece(0, PieceType.Water, Piece.H),
            Piece(1, PieceType.C_M, Piece.H)
        ]
        sut = DiagonalConstraint([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_second_water(self):
        assignment = [
            Piece(1, PieceType.C_M, Piece.H),
            Piece(0, PieceType.Water, Piece.H)
        ]
        sut = DiagonalConstraint([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_both_ship(self):
        assignment = [
            Piece(1, PieceType.C_M, Piece.H),
            Piece(1, PieceType.Sub, Piece.H)
        ]
        sut = DiagonalConstraint([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()