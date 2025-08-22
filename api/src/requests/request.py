from pydantic import BaseModel
from typing import Tuple
from ..enums.piece import Piece


class MovesRequest(BaseModel):
    piece: Piece | None
    row: int
    col: int


class MoveRequest(BaseModel):
    piece: Tuple[int, int]
    update_row: int
    update_col: int
