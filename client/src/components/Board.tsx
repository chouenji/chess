import { useEffect, useState } from "react";
import { Piece, Color } from "../enums/piece"
import { sendRequest, methods } from "../utils/request"
import EvaluationBar from "./Evaluation";

function Board() {
  type Cell = Piece | null;
  type FenResponse = { fen: string }
  type IsCheckMateResponse = { checkmate: boolean, check: boolean }
  type StockFishData = {
    bestmove?: string;
    continuation?: string;
    evaluation?: number | null;
    mate?: number | null;
    success?: boolean;
  };

  const [board, setBoard] = useState<Cell[][]>([]);
  const [turn, setTurn] = useState<Color>("white");
  const [bot, _] = useState<boolean>(true);
  const [possibleMoves, setPossibleMoves] = useState<[number, number][]>([]);
  const [selectedPiece, setSelectedPiece] = useState<[number, number] | null>(null);
  const [isBotThinking, setIsBotThinking] = useState(false);
  const [evaluation, setEvaluation] = useState<number | null>(null);

  useEffect(() => {
    const init = (async () => {
      try {
        await sendRequest("/board", setBoard)
        await sendRequest("/turn", setTurn)
      }
      catch (err) {
        console.error(err);
      }
    })

    init();
  }, [])

  useEffect(() => {
    if (bot && turn === Color.black && !isBotThinking) {
      makeBotMove();
    }

    const checkForCheckmate = async () => {
      try {
        const res = await sendRequest<IsCheckMateResponse>("/is-checkmate");
        await sendRequest("/turn", setTurn);

        if (res.checkmate) {
          alert("Checkmate! Game over. " + (turn === Color.white ? "Black" : "White") + " wins!");
          await sendRequest("/board", setBoard);
          setEvaluation(null);
        }
        else if (res.check && turn === Color.white) {
          alert("Check! You need to make a move to get out of check.");
        }
      } catch (err) {
        console.error("Failed to check for checkmate:", err);
      }
    }




    checkForCheckmate();
  }, [turn, bot])

  async function handleCellClick(row: number, col: number) {
    try {
      if (possibleMoves.length > 0 && isPossibleMove(row, col)) {
        await move(row, col);
      }
      else {
        await availableMoves(row, col);
      }
    }
    catch (err) {
      console.error(err);
    }
  }

  async function move(row: number, col: number) {
    try {
      Promise.all([
        await sendRequest("/move", null, methods.POST, { piece: selectedPiece, update_row: row, update_col: col }),
        await sendRequest("/turn", setTurn),
        await sendRequest("/board", setBoard),
      ]);

      setPossibleMoves([]);
    } catch (err) {
      console.error(err);
    }
  }

  const makeBotMove = async () => {
    if (!bot || turn !== Color.black || isBotThinking) return;

    setIsBotThinking(true);

    try {
      const stockFishData = await getStockFishData();
      const bestMoveMatch = stockFishData.bestmove?.match(/bestmove (\w+)/);

      setEval(stockFishData);

      if (!bestMoveMatch) {
        throw new Error("Stockfish API error: No move found in response");
      }

      const uciMove = bestMoveMatch[1];
      await executeBotMove(uciMove);
    } catch (err) {
      console.error("Bot move failed:", err);
    } finally {
      setIsBotThinking(false);
    }
  };

  const getStockFishData = async () => {
    const fenRes = await sendRequest<FenResponse>("/fen");

    const stockfishRes = await fetch(
      `https://www.stockfish.online/api/s/v2.php?fen=${encodeURIComponent(fenRes.fen)}&depth=12`
    );

    const stockFishData: StockFishData = await stockfishRes.json();

    return stockFishData;
  }

  const setEval = (stockFishData: StockFishData) => {
    if (stockFishData.evaluation !== null && stockFishData.evaluation !== undefined) {
      setEvaluation(stockFishData.evaluation);
    } else if (stockFishData.mate !== null && stockFishData.mate !== undefined) {
      setEvaluation(stockFishData.mate);
    } else {
      setEvaluation(0);
    }
  }

  const executeBotMove = async (uciMove: string) => {
    const fromCol = uciMove.charCodeAt(0) - 97; // 'a' -> 0
    const fromRow = 8 - parseInt(uciMove[1]);
    const toCol = uciMove.charCodeAt(2) - 97;
    const toRow = 8 - parseInt(uciMove[3]);

    if ([fromRow, fromCol, toRow, toCol].some(coord =>
      coord < 0 || coord > 7)) {
      throw new Error(`Invalid UCI move: ${uciMove}`);
    }

    await sendRequest("/move", null, "POST", {
      piece: [fromRow, fromCol],
      update_row: toRow,
      update_col: toCol
    });

    await Promise.all([
      sendRequest("/board", setBoard),
      sendRequest("/turn", setTurn)
    ]);
  };

  async function availableMoves(row: number, col: number) {
    if (!isSelectedPieceAllowed(row, col)) return;

    const cell = board[row][col];

    if (cell == null) return;

    setSelectedPiece([row, col]);
    try {
      await sendRequest("/moves", setPossibleMoves, methods.POST, { piece: cell, row, col })
    } catch (err) {
      console.error("Failed to fetch moves:", err);
    }
  }

  function isSelectedPieceAllowed(row: number, col: number) {
    const piece = board[row]?.[col];
    if (!piece) return false;

    const isWhitePiece = piece[0] === 'w';
    const isBlackPiece = piece[0] === 'b';

    if (bot && isBlackPiece) return false;

    return (
      (isWhitePiece && turn === Color.white) ||
      (isBlackPiece && turn === Color.black)
    );
  }

  function isPossibleMove(row: number, col: number): boolean {
    return possibleMoves.some(([r, c]) => r === row && c === col);
  }

  return (
    <>
      {turn &&
        <h1 className="pb-5">{turn == Color.white ? 'White' : 'Black'} to move</h1>
      }
      {isBotThinking && <div className="bot-thinking">Bot is thinking...</div>}
      <div className="flex items-center gap-10">
        <EvaluationBar evaluation={evaluation} />
        <div className="grid grid-cols-8 w-[800px] h-[800px]">
          {board.map((r, rIdx) =>
            r.map((piece, cIdx) => {
              const isLightSqr = (rIdx + cIdx) % 2 === 0;
              return (
                <div
                  key={`${rIdx}-${cIdx}`}
                  className={`relative box-border flex justify-center items-center w-[100px] h-[100px] ${isLightSqr ? 'bg-[#f0d9b5]' : 'bg-[#b58863]'} ${isPossibleMove(rIdx, cIdx) ? 'cursor-pointer hover:bg-yellow-100' : ''}`}
                  onClick={() => handleCellClick(rIdx, cIdx)}
                >
                  {piece && (
                    <img
                      src={`/pieces/${piece}.svg`}
                      alt={piece}
                      className="w-20 h-20"
                    />
                  )}
                  {isPossibleMove(rIdx, cIdx) && (
                    piece
                      ? (
                        <span className="absolute left-1/2 top-1/2 w-20 h-20 -translate-x-1/2 -translate-y-1/2 rounded-full border-6 border-gray-600 opacity-50"></span>
                      )
                      : (
                        <span className="absolute left-1/2 top-1/2 w-4 h-4 -translate-x-1/2 -translate-y-1/2 rounded-full bg-gray-600 opacity-50"></span>
                      )
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
    </>
  )
}


export default Board;
