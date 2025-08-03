export const GameMode = {
  menu: "menu",
  bot: "bot",
  offline: "offline",
  multiplayer: "multiplayer"
};

export type GameMode = typeof GameMode[keyof typeof GameMode];