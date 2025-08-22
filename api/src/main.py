from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .requests.request import MovesRequest, MoveRequest
from .core.logic import (
    game,
    get_board,
    get_turn,
    available_moves,
    is_stalemate,
    make_move,
    generate_fen,
    reset_board,
    is_in_check,
    is_checkmate,
)

app = FastAPI()
router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chouenji-chess.duckdns.org", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/board")
def get_board_endpoint():
    return get_board(game)


@router.get("/turn")
def get_turn_endpoint():
    return get_turn(game)


@router.get("/fen")
def get_fen():
    return {"fen": generate_fen(game)}


@router.get("/game-condition")
def game_condition_endpoint():
    if is_checkmate(game):
        reset_board(game)
        return {"checkmate": True, "check": False}

    if is_in_check(game):
        return {"checkmate": False, "check": True}

    if is_stalemate(game):
        reset_board(game)
        return {"checkmate": False, "check": False, "stalemate": True}

    return {"checkmate": False, "check": False, "stalemate": False}


@router.post("/reset-board")
def reset_board_endpoint():
    reset_board(game)
    return {"status": "Board reset successfully"}


@router.post("/moves")
def available_moves_endpoint(req: MovesRequest):
    return available_moves(game, req.row, req.col)


@router.post("/move")
def move_endpoint(req: MoveRequest):
    return [make_move(game, req.piece, req.update_row, req.update_col)]


app.include_router(router)
