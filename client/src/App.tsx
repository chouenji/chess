
import { useState } from 'react';
import './App.css';
import Board from './components/Board';
import Menu from './components/Menu';
import { GameMode } from './enums/game-mode';
import BotLevel from './components/BotLevel';


function App() {
  const [gameMode, setGameMode] = useState<GameMode>(GameMode.menu);
  const [botLevel, setBotLevel] = useState<string>("");

  const handleSelectMode = (mode: GameMode) => {
    setGameMode(mode);
  };

  const handleLevelChange = (level: string) => {
    setBotLevel(level);
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-screen bg-zinc-800 text-white">
      {gameMode === GameMode.menu && <Menu onSelectMode={handleSelectMode} />}
      {gameMode === GameMode.bot && (
        botLevel === ""
          ? <BotLevel level={botLevel} onLevelChange={handleLevelChange} />
          : <Board mode={GameMode.bot} botLevel={botLevel} onReturnToMenu={() => { setGameMode(GameMode.menu); setBotLevel(""); }} />
      )}
      {gameMode === GameMode.local && <Board mode={GameMode.local} onReturnToMenu={() => setGameMode(GameMode.menu)} />}
      {gameMode === GameMode.online && <Board mode={GameMode.online} onReturnToMenu={() => setGameMode(GameMode.menu)} />}
    </div>
  )
}

export default App
