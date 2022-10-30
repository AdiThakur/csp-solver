import unittest
from battle import *


class TestDestroyerHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.C_H_S, Piece.C_M]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.D_H_S, Piece.D_H_E]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment1(self):
        assignment = [Piece.D_H_S, Piece.Water]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment2(self):
        assignment = [Piece.D_H_S, Piece.D_V_E]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestDestroyerVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.C_V_S, Piece.C_M]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.D_V_S, Piece.D_V_E]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment1(self):
        assignment = [Piece.D_V_S, Piece.Water]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment2(self):
        assignment = [Piece.D_V_S, Piece.D_H_E]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.B_H_S, Piece.B_M, Piece.B_M]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.C_H_S, Piece.C_M, Piece.C_H_E]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [Piece.C_H_S, Piece.Water, Piece.C_H_E]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece.C_H_S, Piece.C_M, Piece.Water]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.B_V_S, Piece.B_M, Piece.B_M]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.C_V_S, Piece.C_M, Piece.C_V_E]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [Piece.C_V_S, Piece.Water, Piece.C_V_E]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece.C_V_S, Piece.C_M, Piece.Water]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.Sub, Piece.Water, Piece.Water, Piece.Sub]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.B_H_S, Piece.B_M, Piece.B_M, Piece.B_H_E]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [Piece.B_H_S, Piece.Water, Piece.B_M, Piece.B_H_E]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [Piece.B_H_S, Piece.B_M, Piece.Water, Piece.B_H_E]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece.B_H_S, Piece.B_M, Piece.B_M, Piece.Water]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece.Sub, Piece.Water, Piece.Water, Piece.Sub]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece.B_V_S, Piece.B_M, Piece.B_M, Piece.B_V_E]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [Piece.B_V_S, Piece.Water, Piece.B_M, Piece.B_V_E]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [Piece.B_V_S, Piece.B_M, Piece.Water, Piece.B_V_E]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece.B_V_S, Piece.B_M, Piece.B_M, Piece.Water]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestSum(unittest.TestCase):
    def test_all_water(self):
        assignment = [Piece.Water] * 4
        sut = ShipSum(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_less_than_sum(self):
        assignment = [Piece.Water, Piece.Water, Piece.Sub, Piece.Water]
        sut = ShipSum(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_more_than_sum(self):
        assignment = [Piece.Sub, Piece.B_H_S, Piece.Sub, Piece.Water]
        sut = ShipSum(
            sum=2,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_just_right(self):
        assignment = [Piece.Sub, Piece.B_H_S, Piece.Sub, Piece.Water]
        sut = ShipSum(
            sum=3,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)


class TestWater(unittest.TestCase):
    def test_both_water(self):
        assignment = [Piece.Water, Piece.Water]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_first_water(self):
        assignment = [Piece.Water, Piece.B_M]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_second_water(self):
        assignment = [Piece.Sub, Piece.Water]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_both_ship(self):
        assignment = [Piece.Sub, Piece.B_H_E]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()