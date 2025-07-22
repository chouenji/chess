export const Piece = {
  // White
  wR: "wR", // Rook
  wN: "wN", // Knight
  wB: "wB", // Bishop
  wQ: "wQ", // Queen
  wK: "wK", // King
  wP: "wP", // Pawn

  // Black
  bR: "bR", // Rook
  bN: "bN", // Knight
  bB: "bB", // Bishop
  bQ: "bQ", // Queen
  bK: "bK", // King
  bP: "bP" // Pawn
};

export const Color = {
  white: "white",
  black: "black"
}


export type Piece = typeof Piece[keyof typeof Piece];
export type Color = typeof Color[keyof typeof Color];
