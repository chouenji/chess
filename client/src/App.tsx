
import { useState } from 'react';
import './App.css';
import Board from './components/Board';
import Menu from './components/Menu';
import { GameMode } from './enums/game-mode';

function App() {
  const [gameMode, setGameMode] = useState<GameMode>(GameMode.menu);

  const handleSelectMode = (mode: GameMode) => {
    setGameMode(mode);
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-screen bg-zinc-800 text-white">
      {gameMode === GameMode.menu && <Menu onSelectMode={handleSelectMode} />}
      {gameMode === GameMode.bot && <Board mode={GameMode.bot} onReturnToMenu={() => setGameMode(GameMode.menu)} />}
      {gameMode === GameMode.local && <Board mode={GameMode.local} onReturnToMenu={() => setGameMode(GameMode.menu)} />}
      {gameMode === GameMode.online && <Board mode={GameMode.online} onReturnToMenu={() => setGameMode(GameMode.menu)} />}
    </div>
  )
}

export default App
