from typing import List, Optional, Tuple
from enums.piece import Color, Piece
from tests.board_template_test import en_passant_state

ROWS = 8
COLS = 8

state = en_passant_state

def get_board() -> List[List[Optional[Piece]]]:
    return state["board"]


def reset_board():
    global state
    state = {
        "board": [
            [
                Piece.bR,
                Piece.bN,
                Piece.bB,
                Piece.bQ,
                Piece.bK,
                Piece.bB,
                Piece.bN,
                Piece.bR,
            ],
            [Piece.bP] * COLS,
            [None] * COLS,
            [None] * COLS,
            [None] * COLS,
            [None] * COLS,
            [Piece.wP] * COLS,
            [
                Piece.wR,
                Piece.wN,
                Piece.wB,
                Piece.wQ,
                Piece.wK,
                Piece.wB,
                Piece.wN,
                Piece.wR,
            ],
        ],
        "turn": Color.white,
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
    


def get_turn() -> Color:
    return state["turn"]


def is_within_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def is_opponent(piece: Piece, target: Optional[Piece]) -> bool:
    if target is None:
        return False
    return piece.name[0] != target.name[0]


def get_king_position(color: Color) -> Tuple[int, int]:
    king = Piece.wK if color == Color.white else Piece.bK
    for r in range(ROWS):
        for c in range(COLS):
            if state["board"][r][c] == king:
                return (r, c)
    return (-1, -1)  # Should never happen


def is_square_under_attack(row: int, col: int, attacker_color: Color) -> bool:
    board = state["board"]
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece and piece.name[0] == (
                "w" if attacker_color == Color.white else "b"
            ):
                if can_attack(r, c, row, col):
                    return True
    return False


def can_attack(from_r: int, from_c: int, to_r: int, to_c: int) -> bool:
    piece = state["board"][from_r][from_c]
    if not piece:
        return False


    # Rook-like movement (rook, queen)
    if piece in {Piece.wR, Piece.bR, Piece.wQ, Piece.bQ}:
        if from_r == to_r or from_c == to_c:
            dr = 0 if from_r == to_r else (1 if to_r > from_r else -1)
            dc = 0 if from_c == to_c else (1 if to_c > from_c else -1)
            r, c = from_r + dr, from_c + dc
            while r != to_r or c != to_c:
                if state["board"][r][c] is not None:
                    return False
                r += dr
                c += dc
            return True

    # Bishop-like movement (bishop, queen)
    if piece in {Piece.wB, Piece.bB, Piece.wQ, Piece.bQ}:
        if abs(from_r - to_r) == abs(from_c - to_c):
            dr = 1 if to_r > from_r else -1
            dc = 1 if to_c > from_c else -1
            r, c = from_r + dr, from_c + dc
            while r != to_r or c != to_c:
                if state["board"][r][c] is not None:
                    return False
                r += dr
                c += dc
            return True

    # Knight
    if piece in {Piece.wN, Piece.bN}:
        return (abs(from_r - to_r) == 2 and abs(from_c - to_c) == 1) or (
            abs(from_r - to_r) == 1 and abs(from_c - to_c) == 2
        )

    # Pawn attacks
    if piece in {Piece.wP, Piece.bP}:
        direction = -1 if piece == Piece.wP else 1
        return to_r == from_r + direction and abs(to_c - from_c) == 1

    # King (adjacent squares)
    if piece in {Piece.wK, Piece.bK}:
        if from_r == to_r and from_c == to_c:
            return False
        return abs(from_r - to_r) <= 1 and abs(from_c - to_c) <= 1

    return False


def is_in_check() -> bool:
    color = get_turn()
    king_r, king_c = get_king_position(color)
    attacker_color = Color.black if color == Color.white else Color.white
    is_check = is_square_under_attack(king_r, king_c, attacker_color)

    if is_check:
        state["is_check"] = True
    else:
        state["is_check"] = False

    return is_check


def is_checkmate() -> bool:
    color = get_turn()

    if not is_in_check():
        return False

    for r in range(ROWS):
        for c in range(COLS):
            piece = state["board"][r][c]
            if piece and piece.name[0] == ("w" if color == Color.white else "b"):
                moves = available_moves(r, c)
                for move in moves:
                    if is_move_safe(r, c, move[0], move[1]):
                        return False

    return True


def is_stalemate() -> bool:
    color = get_turn()

    if is_in_check():
        return False 

    for r in range(ROWS):
        for c in range(COLS):
            piece = state["board"][r][c]
            if piece and piece.name[0] == ("w" if color == Color.white else "b"):
                moves = available_moves(r, c)
                if moves:
                    return False

    return True


def is_move_safe(from_r: int, from_c: int, to_r: int, to_c: int) -> bool:
    # Simulate move to check if king is safe
    original_board = [row[:] for row in state["board"]]
    piece = state["board"][from_r][from_c]

    # Handle en passant capture
    if piece in {Piece.wP, Piece.bP} and (to_r, to_c) == state["en_passant"]:
        state["board"][from_r][to_c] = None  # Remove captured pawn

    # Make the move
    state["board"][to_r][to_c] = piece
    state["board"][from_r][from_c] = None

    # Handle castling - move rook too
    if piece in {Piece.wK, Piece.bK} and abs(from_c - to_c) == 2:
        rook_col = 7 if to_c == 6 else 0
        new_rook_col = 5 if to_c == 6 else 3
        state["board"][to_r][new_rook_col] = state["board"][to_r][rook_col]
        state["board"][to_r][rook_col] = None

    # Check if king is safe
    king_safe = not is_in_check()

    # Restore board
    state["board"] = original_board
    return king_safe


def get_sliding_moves(
    r: int, c: int, directions: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    """Helper function for sliding pieces (rook, bishop, queen)"""
    moves = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while is_within_bounds(nr, nc):
            target = state["board"][nr][nc]
            if target is None:
                moves.append((nr, nc))
            elif is_opponent(state["board"][r][c], target):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves


def available_moves(r: int, c: int) -> List[Tuple[int, int]]:
    piece = state["board"][r][c]
    if not piece:
        return []

    color = get_turn()

    # Prevent client from making moves for opponent's pieces
    if color == Color.white and piece.name[0] != "w":
        return []
    elif color == Color.black and piece.name[0] != "b":
        return []

    moves = []

    # White Pawn
    if piece == Piece.wP:
        if r > 0 and state["board"][r - 1][c] is None:
            moves.append((r - 1, c))
            if r == 6 and state["board"][r - 2][c] is None:
                moves.append((r - 2, c))

        # Diagonal captures
        for dc in [-1, 1]:
            nr, nc = r - 1, c + dc
            if not is_within_bounds(nr, nc):
                continue

            # Regular capture (opponent piece)
            if state["board"][nr][nc] is not None and is_opponent(
                piece, state["board"][nr][nc]
            ):
                moves.append((nr, nc))
            # En passant capture
            elif (nr, nc) == state["en_passant"]:
                moves.append((nr, nc))

    # Black Pawn
    elif piece == Piece.bP:
        if r < 7 and state["board"][r + 1][c] is None:
            moves.append((r + 1, c))
            if r == 1 and state["board"][r + 2][c] is None:
                moves.append((r + 2, c))

        # Diagonal captures
        for dc in [-1, 1]:
            nr, nc = r + 1, c + dc
            if not is_within_bounds(nr, nc):
                continue

            # Regular capture (opponent piece)
            if state["board"][nr][nc] is not None and is_opponent(
                piece, state["board"][nr][nc]
            ):
                moves.append((nr, nc))
            # En passant capture
            elif (nr, nc) == state["en_passant"]:
                moves.append((nr, nc))

    # Rook
    elif piece in {Piece.wR, Piece.bR}:
        rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves.extend(get_sliding_moves(r, c, rook_directions))

    # Bishop
    elif piece in {Piece.wB, Piece.bB}:
        bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves.extend(get_sliding_moves(r, c, bishop_directions))

    # Queen
    elif piece in {Piece.wQ, Piece.bQ}:
        rook_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        bishop_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        moves.extend(get_sliding_moves(r, c, rook_directions))
        moves.extend(get_sliding_moves(r, c, bishop_directions))

    # Knight
    elif piece in {Piece.wN, Piece.bN}:
        knight_moves = [
            (r - 2, c - 1),
            (r - 2, c + 1),
            (r - 1, c - 2),
            (r - 1, c + 2),
            (r + 1, c - 2),
            (r + 1, c + 2),
            (r + 2, c - 1),
            (r + 2, c + 1),
        ]
        for nr, nc in knight_moves:
            if is_within_bounds(nr, nc) and (
                state["board"][nr][nc] is None
                or is_opponent(piece, state["board"][nr][nc])
            ):
                moves.append((nr, nc))

    # King
    elif piece in {Piece.wK, Piece.bK}:
        king_moves = [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c - 1),
            (r, c + 1),
            (r + 1, c - 1),
            (r + 1, c),
            (r + 1, c + 1),
        ]
        for nr, nc in king_moves:
            if is_within_bounds(nr, nc) and (
                state["board"][nr][nc] is None
                or is_opponent(piece, state["board"][nr][nc])
            ):
                moves.append((nr, nc))

        # Castling
        row = 7 if color == Color.white else 0

        if not is_in_check():
            if r == row and c == 4:  # King on starting position
                # Kingside
                if state["castling"][f"{color.value}_king_side"]:
                    if (
                        state["board"][row][5] is None
                        and state["board"][row][6] is None
                        and not is_square_under_attack(
                            row, 5, Color.black if color == Color.white else Color.white
                        )
                        and not is_square_under_attack(
                            row, 6, Color.black if color == Color.white else Color.white
                        )
                    ):
                        moves.append((row, 6))

                # Queenside
                if state["castling"][f"{color.value}_queen_side"]:
                    if (
                        state["board"][row][3] is None
                        and state["board"][row][2] is None
                        and state["board"][row][1] is None
                        and not is_square_under_attack(
                            row, 3, Color.black if color == Color.white else Color.white
                        )
                        and not is_square_under_attack(
                            row, 2, Color.black if color == Color.white else Color.white
                        )
                    ):
                        moves.append((row, 2))

    # Filter moves that would leave king in check
    safe_moves = [move for move in moves if is_move_safe(r, c, move[0], move[1])]
    return safe_moves


def make_move(piece_pos: Tuple[int, int], update_row: int, update_col: int) -> bool:
    global state
    r0, c0 = piece_pos
    piece = state["board"][r0][c0]

    if not piece:
        return False

    target = state["board"][update_row][update_col]

    # Reset halfmove clock on captures/pawn moves
    if piece in {Piece.wP, Piece.bP} or target is not None:
        state["halfmove_clock"] = 0
    else:
        state["halfmove_clock"] += 1

    # Validate turn
    if state["turn"] == Color.white and piece.name[0] != "w":
        return False
    if state["turn"] == Color.black and piece.name[0] != "b":
        return False

    # Validate move is in available moves
    if (update_row, update_col) not in available_moves(r0, c0):
        return False

    # Update castling rights if king or rook moves
    color = get_turn()

    if piece in {Piece.wK, Piece.bK}:
        state["castling"][f"{color}_king_side"] = False
        state["castling"][f"{color}_queen_side"] = False

    if piece in {Piece.wR, Piece.bR}:
        if r0 == 7 and c0 == 0:  # White queenside rook
            state["castling"]["white_queen_side"] = False
        elif r0 == 7 and c0 == 7:  # White kingside rook
            state["castling"]["white_king_side"] = False
        elif r0 == 0 and c0 == 0:  # Black queenside rook
            state["castling"]["black_queen_side"] = False
        elif r0 == 0 and c0 == 7:  # Black kingside rook
            state["castling"]["black_king_side"] = False

    # Handle en passant capture
    if (
        piece in {Piece.wP, Piece.bP}
        and (update_row, update_col) == state["en_passant"]
    ):
        # Remove the captured pawn
        captured_row = r0  # Same row as moving pawn before move
        captured_col = update_col
        state["board"][captured_row][captured_col] = None

    # Handle castling - move rook too
    if piece in {Piece.wK, Piece.bK} and abs(c0 - update_col) == 2:
        rook_col = 7 if update_col == 6 else 0
        new_rook_col = 5 if update_col == 6 else 3
        rook_row = 7 if piece == Piece.wK else 0
        state["board"][rook_row][new_rook_col] = state["board"][rook_row][rook_col]
        state["board"][rook_row][rook_col] = None

    # Make the move
    state["board"][r0][c0] = None
    state["board"][update_row][update_col] = piece

    # Handle pawn promotion
    if piece in {Piece.wP, Piece.bP}:
        # White pawn reaches last rank (row 0)
        if piece == Piece.wP and update_row == 0:
            state["board"][update_row][update_col] = Piece.wQ
        # Black pawn reaches last rank (row 7)
        elif piece == Piece.bP and update_row == 7:
            state["board"][update_row][update_col] = Piece.bQ

    # Set en passant target if pawn moves two squares
    state["en_passant"] = None
    if piece in {Piece.wP, Piece.bP} and abs(r0 - update_row) == 2:
        state["en_passant"] = ((r0 + update_row) // 2, c0)

    # Switch turn
    state["turn"] = Color.black if state["turn"] == Color.white else Color.white

    # Increment fullmove after black's turn (after turn switch)
    if state["turn"] == Color.white:
        state["fullmove_number"] += 1

    # Store last move for en passant
    state["last_move"] = (piece, r0, c0, update_row, update_col)

    return True


def generate_fen():
    board = state["board"]
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for piece in row:
            if piece is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += (
                    piece.name[1].lower()
                    if piece.name.startswith("b")
                    else piece.name[1]
                )
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    placement = "/".join(fen_rows)
    color = "w" if state["turn"] == Color.white else "b"
    castling = (
        "".join(
            [
                "K" if state["castling"]["white_king_side"] else "",
                "Q" if state["castling"]["white_queen_side"] else "",
                "k" if state["castling"]["black_king_side"] else "",
                "q" if state["castling"]["black_queen_side"] else "",
            ]
        )
        or "-"
    )

    en_passant = "-"
    if state["en_passant"]:
        row, col = state["en_passant"]
        # Convert to algebraic notation (files a-h, ranks 1-8)
        file_letter = chr(97 + col)  # 0=a, 1=b, ... 7=h
        rank_number = 8 - row  # 0=8, 1=7, ... 7=1
        en_passant = f"{file_letter}{rank_number}"

    halfmove = state["halfmove_clock"]
    fullmove = state["fullmove_number"]

    return f"{placement} {color} {castling} {en_passant} {halfmove} {fullmove}"
