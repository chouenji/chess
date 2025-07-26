import { useEffect, useState } from "react";
import { Piece, Color } from "../enums/piece"
import { sendRequest, methods } from "../utils/request"

function Board() {
  type Cell = Piece | null;
  type FenResponse = { fen: string }
  type IsCheckMateResponse = { checkmate: boolean, check: boolean }

  const [board, setBoard] = useState<Cell[][]>([]);
  const [turn, setTurn] = useState<Color>("white");
  const [bot, _] = useState<boolean>(true);
  const [possibleMoves, setPossibleMoves] = useState<[number, number][]>([]);
  const [selectedPiece, setSelectedPiece] = useState<[number, number] | null>(null);
  const [isBotThinking, setIsBotThinking] = useState(false);

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
    const checkForCheckmate = async () => {
      try {
        const res = await sendRequest<IsCheckMateResponse>("/is-checkmate");
        await sendRequest("/turn", setTurn);

        if (res.checkmate) {
          alert("Checkmate! Game over. " + (turn === Color.white ? "Black" : "White") + " wins!");
          await sendRequest("/board", setBoard);
        } 
        else if (res.check && turn === Color.white) {
          alert("Check! You need to make a move to get out of check.");
        }
      } catch (err) {
        console.error("Failed to check for checkmate:", err);
    }
  }

    checkForCheckmate();

    if (bot && turn === Color.black && !isBotThinking) {
      makeBotMove();
    }

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
        await sendRequest("/board", setBoard)
      ]);
      setPossibleMoves([]);
    } catch (err) {
      console.error(err)
    }
  }


  const makeBotMove = async () => {
    if (!bot || turn !== Color.black || isBotThinking) return;

    setIsBotThinking(true);

    try {
      const res = await sendRequest<FenResponse>("/fen");

      const stockfishResponse = await fetch(
        `https://www.stockfish.online/api/s/v2.php?fen=${encodeURIComponent(res.fen)}&depth=12`
      );

      const resText = await stockfishResponse.text();

      const bestMoveMatch = resText.match(/bestmove (\w+)/);
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
      <div className="grid grid-cols-8 w-[800px] h-[800px]">
        {board.map((r, rIdx) =>
          r.map((piece, cIdx) => {
            const isLightSqr = (rIdx + cIdx) % 2 === 0;
            return (
              <div
                key={`${rIdx}-${cIdx}`}
                className={`box-border flex justify-center items-center w-[100px] h-[100px]
                        ${isLightSqr ? 'bg-[#f0d9b5]' : 'bg-[#b58863]'}
                        ${isPossibleMove(rIdx, cIdx) ? 'border-4 border-orange-800 cursor-pointer hover:bg-yellow-100' : ''}
                      `}
                onClick={() => handleCellClick(rIdx, cIdx)}
              >              {piece && (
                <img
                  src={`/public/pieces/${piece}.svg`}
                  alt={piece}
                  className="w-20 h-20"
                />
              )}
              </div>
            );
          })
        )}
      </div>
    </>
  )
}


export default Board;
