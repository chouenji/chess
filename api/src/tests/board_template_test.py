from enums.piece import Piece, Color


en_passant_state = {
    "board": [
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None, None, None, Piece.bP, Piece.wP, None, None, None],
        [None] * 8,
        [None] * 8,
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ],
    "turn": Color.white,
    "bot": False,
    "castling": {
        "white_king_side": False,
        "white_queen_side": False,
        "black_king_side": False,
        "black_queen_side": False,
    },
    "en_passant": (4, 4),  # e3 square
    "last_move": ((1, 3), (3, 3)),  # e2 -> e4
    "halfmove_clock": 0,
    "fullmove_number": 3,
}

castling_state = {
    "board": [
        [
            Piece.bR,
            None,
            None,
            None,
            Piece.bK,
            None,
            None,
            Piece.bR,
        ],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [
            Piece.wR,
            None,
            None,
            None,
            Piece.wK,
            None,
            None,
            Piece.wR,
        ],
    ],
    "turn": Color.white,
    "bot": False,
    "castling": {
        "white_king_side": True,
        "white_queen_side": True,
        "black_king_side": True,
        "black_queen_side": True,
    },
    "en_passant": None,
    "last_move": None,
    "halfmove_clock": 0,
    "fullmove_number": 1,
}

illegal_kings_state = {
    "board": [
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None, None, None, None, Piece.bK, Piece.wK, None, None],
        [None] * 8,
        [None] * 8,
        [None] * 8,
    ],
    "turn": Color.white,
    "bot": False,
    "castling": {
        "white_king_side": False,
        "white_queen_side": False,
        "black_king_side": False,
        "black_queen_side": False,
    },
    "en_passant": None,
    "last_move": None,
    "halfmove_clock": 0,
    "fullmove_number": 20,
}

white_castling_ready_state = {
    "board": [
        [Piece.bR, None, None, None, Piece.bK, None, None, Piece.bR],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Piece.wR, None, None, None, Piece.wK, None, None, Piece.wR],
    ],
    "turn": Color.white,
    "bot": False,
    "castling": {
        "white_king_side": True,
        "white_queen_side": True,
        "black_king_side": True,
        "black_queen_side": True,
    },
    "en_passant": None,
    "last_move": None,
    "halfmove_clock": 0,
    "fullmove_number": 10,
}
