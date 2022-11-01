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


class TestGenerateDomainFromHint(unittest.TestCase):
    def test_sub_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('S', pieces)

        self.assertEqual(1, len(result))
        for piece in result:
            self.assertEqual(PieceType.Sub, piece.ptype)

    def test_top_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('T', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.V, piece.orientation)

    def test_top_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('B', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.V, piece.orientation)

    def test_left_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('L', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.H, piece.orientation)

    def test_right_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('R', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.H, piece.orientation)

    def test_middle_hint(self):
        pieces = generate_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('M', pieces)

        self.assertEqual(6, len(result))


if __name__ == "__main__":
    unittest.main()
