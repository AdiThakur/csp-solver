import unittest
from battle import *


class TestGeneratePieces(unittest.TestCase):
    def test_subs(self):
        ship_count = [2, 0, 0, 0]

        subs = generate_ship_pieces(ship_count)[0]

        self.assertEqual(2, len(subs))
        self.assertNotEqual(subs[0].id, subs[1].id)

    def test_destroyers(self):
        ship_count = [0, 2, 0, 0]

        result = generate_ship_pieces(ship_count)
        destroyers = result[1] + result[3]

        self.assertEqual(8, len(destroyers))

    def test_cruisers(self):
        ship_count = [0, 0, 2, 0]

        result = generate_ship_pieces(ship_count)
        cruisers = result[1] + result[2] + result[3]

        self.assertEqual(12, len(cruisers))

    def test_battle_ships(self):
        ship_count = [0, 0, 0, 2]

        result = generate_ship_pieces(ship_count)
        battle_ships = result[1] + result[2] + result[3]

        self.assertEqual(16, len(battle_ships))


class TestGenerateDomainFromHint(unittest.TestCase):
    def test_sub_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('S', pieces)

        self.assertEqual(1, len(result))
        for piece in result:
            self.assertEqual(PieceType.Sub, piece.ptype)

    def test_top_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('T', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.V, piece.orientation)

    def test_top_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('B', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.V, piece.orientation)

    def test_left_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('L', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.H, piece.orientation)

    def test_right_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('R', pieces)

        self.assertEqual(3, len(result))
        for piece in result:
            self.assertEqual(Piece.H, piece.orientation)

    def test_middle_hint(self):
        pieces = generate_ship_pieces([1, 1, 1, 1])

        result = generate_domain_from_hint('M', pieces)

        self.assertEqual(6, len(result))


class TestGenerateDomainFromCoordinate(unittest.TestCase):
    def test_3_spots_avail_to_the_right(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [7] [8] [9] |
        fitting_pieces = generate_domain_from_coordinate((0, 7), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.B_S, piece.ptype)

    def test_2_spots_avail_to_the_right(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [8] [9] |
        fitting_pieces = generate_domain_from_coordinate((0, 8), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.B_S, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)
            self.assertNotEqual(PieceType.C_S, piece.ptype)

    def test_1_spots_avail_to_the_right(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [9] |
        fitting_pieces = generate_domain_from_coordinate((0, 9), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.D_S, piece.ptype)
            self.assertNotEqual(PieceType.C_S, piece.ptype)
            self.assertNotEqual(PieceType.C_M, piece.ptype)
            self.assertNotEqual(PieceType.B_S, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)

    def test_3_spots_avail_to_the_left(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: | [0] [1] [2] ...
        fitting_pieces = generate_domain_from_coordinate((2, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_2_spots_avail_to_the_left(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: | [0] [1] ...
        fitting_pieces = generate_domain_from_coordinate((1, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.C_E, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_1_spots_avail_to_the_left(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: | [0] ...
        fitting_pieces = generate_domain_from_coordinate((0, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.V:
                continue
            self.assertNotEqual(PieceType.D_E, piece.ptype)
            self.assertNotEqual(PieceType.C_M, piece.ptype)
            self.assertNotEqual(PieceType.C_E, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_3_spots_avail_above(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # vertical: | [0] [1] [2] ...
        fitting_pieces = generate_domain_from_coordinate((2, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_2_spots_avail_above(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # vertical: | [0] [1] ...
        fitting_pieces = generate_domain_from_coordinate((1, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.C_E, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_1_spots_avail_above(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # vertical: | [0] ...
        fitting_pieces = generate_domain_from_coordinate((0, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.D_E, piece.ptype)
            self.assertNotEqual(PieceType.C_M, piece.ptype)
            self.assertNotEqual(PieceType.C_E, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)
            self.assertNotEqual(PieceType.B_E, piece.ptype)

    def test_3_spots_avail_below(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [7] [8] [9] |
        fitting_pieces = generate_domain_from_coordinate((7, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.B_S, piece.ptype)

    def test_2_spots_avail_below(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [8] [9] |
        fitting_pieces = generate_domain_from_coordinate((8, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.C_S, piece.ptype)
            self.assertNotEqual(PieceType.B_S, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)

    def test_1_spots_avail_below(self):
        dimension = 10
        pieces = generate_ship_pieces([1, 1, 1, 1])
        flattened = pieces[0] + pieces[1] + pieces[2] + pieces[3]

        # horizontal: ... [8] [9] |
        fitting_pieces = generate_domain_from_coordinate((9, 0), dimension, flattened)

        for piece in fitting_pieces:
            if piece.orientation == Piece.H:
                continue
            self.assertNotEqual(PieceType.D_S, piece.ptype)
            self.assertNotEqual(PieceType.C_S, piece.ptype)
            self.assertNotEqual(PieceType.C_M, piece.ptype)
            self.assertNotEqual(PieceType.B_S, piece.ptype)
            self.assertNotEqual(PieceType.B_M1, piece.ptype)
            self.assertNotEqual(PieceType.B_M2, piece.ptype)


if __name__ == "__main__":
    unittest.main()
