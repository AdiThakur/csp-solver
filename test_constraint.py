import unittest
from battle import *


class TestDestroyerHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.C_H_S), Piece(1, PieceType.C_M)]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.D_H_S), Piece(1, PieceType.D_H_E)]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment1(self):
        assignment = [Piece(1, PieceType.D_H_S), Piece(0, PieceType.Water)]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment2(self):
        assignment = [Piece(1, PieceType.D_H_S), Piece(1, PieceType.D_V_E)]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [Piece(1, PieceType.D_H_S), Piece(2, PieceType.D_H_E)]
        sut = DestroyerHorizontal([(0, 0), (0, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestDestroyerVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.C_V_S), Piece(1, PieceType.C_M)]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.D_V_S), Piece(1, PieceType.D_V_E)]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_invalid_assignment1(self):
        assignment = [Piece(1, PieceType.D_V_S), Piece(0, PieceType.Water)]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment2(self):
        assignment = [Piece(1, PieceType.D_V_S), Piece(1, PieceType.D_H_E)]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [Piece(1, PieceType.D_V_S), Piece(2, PieceType.D_V_E)]
        sut = DestroyerVertical([(0, 0), (1, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(1, PieceType.B_M_F), Piece(1, PieceType.B_M_S)]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.C_H_S), Piece(1, PieceType.C_M), Piece(1, PieceType.C_H_E)]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [Piece(1, PieceType.C_H_S), Piece(0, PieceType.Water), Piece(1, PieceType.C_H_E)]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece(1, PieceType.C_H_S), Piece(1, PieceType.C_M), Piece(0, PieceType.Water)]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [Piece(1, PieceType.C_H_S), Piece(1, PieceType.C_M), Piece(2, PieceType.C_H_E)]
        sut = CruiserHorizontal([(0, 0), (0, 1), (0, 2)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestCruiserVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.B_V_S), Piece(1, PieceType.C_M), Piece(1, PieceType.C_V_E)]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.C_V_S), Piece(1, PieceType.C_M), Piece(1, PieceType.C_V_E)]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle(self):
        assignment = [Piece(1, PieceType.C_V_S), Piece(0, PieceType.Water), Piece(1, PieceType.C_V_E)]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece(1, PieceType.C_V_S), Piece(1, PieceType.C_M), Piece(1, PieceType.Water)]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [Piece(1, PieceType.C_V_S), Piece(2, PieceType.C_M), Piece(1, PieceType.C_V_E)]
        sut = CruiserVertical([(0, 0), (1, 0), (2, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipHorizontal(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.Sub), Piece(0, PieceType.Water), Piece(2, PieceType.Sub), Piece(2, PieceType.Sub)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(1, PieceType.B_M_F), Piece(1, PieceType.B_M_S), Piece(1, PieceType.B_H_E)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(0, PieceType.Water), Piece(1, PieceType.B_M_S), Piece(1, PieceType.B_H_E)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(1, PieceType.B_M_F), Piece(0, PieceType.Water), Piece(1, PieceType.B_H_E)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(1, PieceType.B_M_F), Piece(1, PieceType.B_M_S), Piece(0, PieceType.Water)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_invalid_assignment_wrong_id(self):
        assignment = [Piece(1, PieceType.B_H_S), Piece(1, PieceType.B_M_F), Piece(2, PieceType.B_M_S), Piece(3, PieceType.B_H_E)]
        sut = BattleshipHorizontal([(0, 0), (0, 1), (0, 2), (0, 3)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestBattleshipVertical(unittest.TestCase):

    def test_vacuous_assignment(self):
        assignment = [Piece(1, PieceType.Sub), Piece(0, PieceType.Water), Piece(0, PieceType.Water), Piece(2, PieceType.Sub)]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_ideal_assignment(self):
        assignment = [Piece(1, PieceType.B_V_S), Piece(1, PieceType.B_M_F), Piece(1, PieceType.B_M_S), Piece(1, PieceType.B_V_E)]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_missing_middle1(self):
        assignment = [Piece(1, PieceType.B_V_S), Piece(0, PieceType.Water), Piece(1, PieceType.B_M_S), Piece(1, PieceType.B_V_E)]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_middle2(self):
        assignment = [Piece(1, PieceType.B_V_S), Piece(1, PieceType.B_M_F), Piece(0, PieceType.Water), Piece(1, PieceType.B_V_E)]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_missing_end(self):
        assignment = [Piece(1, PieceType.B_V_S), Piece(1, PieceType.B_M_F), Piece(1, PieceType.B_M_S), Piece(0, PieceType.Water)]
        sut = BattleshipVertical([(0, 0), (1, 0), (2, 0), (3, 0)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


class TestSum(unittest.TestCase):
    def test_all_water(self):
        assignment = [Piece(0, PieceType.Water)] * 4
        sut = ShipSum(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_less_than_sum(self):
        assignment = [
            Piece(0, PieceType.Water), Piece(0, PieceType.Water),
            Piece(0, PieceType.Water), Piece(1, PieceType.Sub)
        ]
        sut = ShipSum(
            sum=4,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_more_than_sum(self):
        assignment = [
            Piece(1, PieceType.C_H_S), Piece(1, PieceType.Sub),
            Piece(0, PieceType.Water), Piece(2, PieceType.Sub)
        ]
        sut = ShipSum(
            sum=2,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)

    def test_just_right(self):
        assignment = [
            Piece(1, PieceType.C_H_S), Piece(1, PieceType.Sub),
            Piece(0, PieceType.Water), Piece(2, PieceType.Sub)
        ]
        sut = ShipSum(
            sum=3,
            scope=[(0, 1), (0, 2), (0, 3), (0, 4)]
        )

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)


class TestWater(unittest.TestCase):
    def test_both_water(self):
        assignment = [Piece(0, PieceType.Water)] * 2
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_first_water(self):
        assignment = [Piece(0, PieceType.Water), Piece(1, PieceType.C_M)]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_second_water(self):
        assignment = [Piece(1, PieceType.C_M), Piece(0, PieceType.Water)]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertTrue(result)

    def test_both_ship(self):
        assignment = [Piece(1, PieceType.C_M), Piece(1, PieceType.Sub)]
        sut = DiagonalWater([(0, 0), (1, 1)])

        result = sut.is_satisfied(assignment)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()