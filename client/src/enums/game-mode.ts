export const GameMode = {
  menu: "menu",
  bot: "bot",
  local: "local",
  online: "online"
};

export type GameMode = typeof GameMode[keyof typeof GameMode];