# test.py
import unittest
import copy
from core.logic import (
    initial_state,
    get_board,
    get_turn,
    make_move,
    is_in_check,
    is_checkmate,
    generate_fen,
)
from enums.piece import Color, Piece


class TestChessLogic(unittest.TestCase):
    def setUp(self):
        global game
        game = copy.deepcopy(initial_state)

    def test_initial_board_setup(self):
        # Test back rank pieces
        self.assertEqual(game["board"][0][0], Piece.bR)
        self.assertEqual(game["board"][7][4], Piece.wK)
        # Test pawns
        self.assertEqual(game["board"][1][3], Piece.bP)
        self.assertEqual(game["board"][6][5], Piece.wP)
        # Test empty squares
        self.assertIsNone(game["board"][3][2])

    def test_pawn_movement(self):
        # Valid white pawn move
        self.assertTrue(make_move(game, (6, 0), 5, 0))
        self.assertIsNone(get_board(game)[6][0])
        self.assertEqual(get_board(game)[5][0], Piece.wP)
        # Now it is black's turn, so this should be valid
        self.assertTrue(make_move(game, (1, 0), 2, 0))

    def test_bishop_blocked_movement(self):
        # Clear pawn blocking white bishop
        get_board(game)[6][1] = None
        # Valid bishop move
        self.assertTrue(make_move(game, (7, 2), 5, 0))  # White bishop c1 to a3
        # Blocked bishop move (should fail, path blocked by pawn)
        self.assertFalse(make_move(game, (0, 2), 2, 0))  # Black bishop c8 to a6

    def test_en_passant(self):
        # Setup en passant opportunity
        make_move(game, (6, 1), 4, 1)  # White pawn double move
        make_move(game, (1, 0), 3, 0)  # Black pawn double move
        make_move(game, (4, 1), 3, 0)  # White captures en passant
        # Check captured pawn is removed (was at 3,0)
        self.assertIsNone(get_board(game)[4][0])
        # Check capturing pawn moved to target square
        self.assertEqual(get_board(game)[3][0], Piece.wP)

    def test_castling(self):
        # Clear path for castling
        get_board(game)[7][1] = None
        get_board(game)[7][2] = None
        get_board(game)[7][3] = None
        get_board(game)[7][5] = None  # Also clear f1
        get_board(game)[7][6] = None

        # Kingside castle
        self.assertTrue(make_move(game, (7, 4), 7, 6))
        self.assertEqual(get_board(game)[7][6], Piece.wK)
        self.assertEqual(get_board(game)[7][5], Piece.wR)

    def test_check_detection(self):
        global game
        # Remove original white queen
        for r in range(8):
            for c in range(8):
                if get_board(game)[r][c] == Piece.wQ:
                    get_board(game)[r][c] = None
        # Place white queen at (1, 4) to attack black king at (0, 4)
        get_board(game)[1][4] = Piece.wQ
        # Set turn to black
        game["turn"] = Color.black
        self.assertTrue(is_in_check(game))
        self.assertEqual(get_turn(game), Color.black)

    def test_checkmate(self):
        # Fool's mate setup
        make_move(game, (6, 5), 5, 5)  # f3
        make_move(game, (1, 4), 3, 4)  # e5
        make_move(game, (6, 6), 4, 6)  # g4
        make_move(game, (0, 3), 4, 7)  # Qh4
        self.assertTrue(is_checkmate(game))

    def test_fen_generation(self):
        make_move(game, (6, 0), 4, 0)  # White pawn
        fen = generate_fen(game)
        # Should have white pawn at a4 and second rank missing a-pawn
        self.assertIn("rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR", fen)


if __name__ == "__main__":
    unittest.main()
