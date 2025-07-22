from enum import Enum


class Piece(str, Enum):
    # White
    wP = "wP"  # Pawn
    wR = "wR"  # Rook
    wN = "wN"  # Knight
    wB = "wB"  # Bishop
    wQ = "wQ"  # Queen
    wK = "wK"  # King
    # Black
    bP = "bP"  # Pawn
    bR = "bR"  # Rook
    bN = "bN"  # Knight
    bB = "bB"  # Bishop
    bQ = "bQ"  # Queen
    bK = "bK"  # King


class Color(str, Enum):
    white = "white"
    black = "black"
