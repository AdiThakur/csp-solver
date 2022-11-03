import unittest
from battle import *


class TestCSP(unittest.TestCase):

    def test_fc_no_hint_one_sub(self):
        # Arrange
        grid = [
            ['0', '0'],
            ['0', '0']
        ]
        expected_grid = [
            ['S', 'W'],
            ['W', 'W']
        ]

        row_sums = [1, 0]
        cols_sums = [1, 0]
        ship_counts = [1, 0, 0, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)
        self.assertEqual(expected_grid, output_grid)

    def test_fc_no_hint_four_subs(self):
        # Arrange
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]

        row_sums = [2, 0, 2]
        cols_sums = [2, 0, 2]
        ship_counts = [4, 0, 0, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)

    def test_fc_no_hint_two_destroyers(self):
        # Arrange
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        expected_grid = [
            ['L', 'R', 'W'],
            ['W', 'W', 'W'],
            ['W', 'L', 'R']
        ]

        row_sums = [2, 0, 2]
        cols_sums = [1, 2, 1]
        ship_counts = [0, 2, 0, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)
        self.assertEqual(expected_grid, output_grid)

    def test_fc_no_hint_one_sub_one_destroyer(self):
        # Arrange
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        expected_grid = [
            ['L', 'R', 'W'],
            ['W', 'W', 'W'],
            ['W', 'W', 'S']
        ]

        row_sums = [2, 0, 1]
        cols_sums = [1, 1, 1]
        ship_counts = [1, 1, 0, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)
        self.assertEqual(expected_grid, output_grid)

    def test_fc_no_hint_one_cruiser1(self):
        # Arrange
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        expected_grid = [
            ['W', 'T', 'W'],
            ['W', 'M', 'W'],
            ['W', 'B', 'W']
        ]

        row_sums = [1, 1, 1]
        cols_sums = [0, 3, 0]
        ship_counts = [0, 0, 1, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)
        self.assertEqual(expected_grid, output_grid)

    def test_fc_no_hint_one_cruiser2(self):
        # Arrange
        grid = [
            ['0', '0', '0'],
            ['0', '0', '0'],
            ['0', '0', '0']
        ]
        expected_grid = [
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
            ['L', 'M', 'R']
        ]

        row_sums = [0, 0, 3]
        cols_sums = [1, 1, 1]
        ship_counts = [0, 0, 1, 0]

        # Act
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)
        self.assertEqual(expected_grid, output_grid)

    def test_fc_no_hint_one_sub_one_cruiser(self):
        # Arrange
        grid = [
            ['0', '0', '0', '0'],
            ['0', '0', '0', '0'],
            ['0', '0', '0', '0'],
            ['0', '0', '0', '0']
        ]
        expected_grid = [
            ['W', 'T', 'W', 'W'],
            ['W', 'B', 'W', 'W'],
            ['W', 'M', 'W', 'W'],
            ['W', 'W', 'W', 'S']
        ]
        row_sums = [1, 1, 1, 1]
        cols_sums = [0, 3, 0, 1]
        ship_counts = [1, 0, 1, 0]

        # Assert
        sol_found, output_grid, csp = run_csp(row_sums, cols_sums, ship_counts, grid)

        # Assert
        self.assertTrue(sol_found)


if __name__ == "__main__":
    unittest.main()
