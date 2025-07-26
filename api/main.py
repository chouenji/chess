from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from request import MovesRequest, MoveRequest
from chess_logic import get_board, get_turn, available_moves, make_move, generate_fen, reset_board, is_in_check, is_checkmate

app = FastAPI()
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/board")
def get_board_endpoint():
    return get_board()


@router.get("/turn")
def get_turn_endpoint():
    return get_turn()


@router.get("/fen")
def get_fen():
    return {"fen": generate_fen()}


@router.get("/is-checkmate")
def is_checkmate_endpoint():
    if is_checkmate():
        reset_board()
        return {"checkmate": True, "check": False}

    if is_in_check():
        return {"checkmate": False, "check": True}

    return {"checkmate": False, "check": False}

@router.post("/moves")
def available_moves_endpoint(req: MovesRequest):
    return available_moves(req.row, req.col)


@router.post("/move")
def move_endpoint(req: MoveRequest):
    return [make_move(req.piece, req.update_row, req.update_col)]


app.include_router(router)
