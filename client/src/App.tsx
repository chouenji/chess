
import { useEffect, useState } from 'react';
import './App.css';
import Board from './components/Board';
import Menu from './components/Menu';
import { GameMode } from './enums/game-mode';

function App() {
  const [gameMode, setGameMode] = useState<GameMode>();

  useEffect(() => {
    setGameMode(GameMode.menu);
  }, []);

  const handleSelectMode = (mode: GameMode) => {
    setGameMode(mode);
  };

  return (
    <div className="flex flex-col items-center justify-center w-full h-screen bg-zinc-800 text-white">
      {gameMode === 'menu' && <Menu onSelectMode={handleSelectMode} />}
      {gameMode === 'bot' && <Board />}
      {gameMode === 'offline' && <Board />}
      {gameMode === 'multiplayer' && <Board />}
    </div>
  )
}

export default App
