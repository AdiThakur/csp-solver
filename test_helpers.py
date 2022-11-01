import unittest
from battle import *


class TestGeneratePieces(unittest.TestCase):
    def test_subs(self):
        ship_count = [2, 0, 0, 0]

        subs = generate_pieces(ship_count)[0]

        self.assertEqual(2, len(subs))
        self.assertNotEqual(subs[0].id, subs[1].id)

    def test_destroyers(self):
        ship_count = [0, 2, 0, 0]

        result = generate_pieces(ship_count)
        destroyers = result[1] + result[3]

        self.assertEqual(8, len(destroyers))

    def test_cruisers(self):
        ship_count = [0, 0, 2, 0]

        result = generate_pieces(ship_count)
        cruisers = result[1] + result[2] + result[3]

        self.assertEqual(12, len(cruisers))

    def test_battle_ships(self):
        ship_count = [0, 0, 0, 2]

        result = generate_pieces(ship_count)
        battle_ships = result[1] + result[2] + result[3]

        self.assertEqual(16, len(battle_ships))

if __name__ == "__main__":
    unittest.main()
