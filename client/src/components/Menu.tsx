import { GameMode } from "../enums/game-mode";

interface MenuProps {
    onSelectMode: (mode: GameMode) => void;
}

function Menu({ onSelectMode }: MenuProps) {
    return (
        <div className="flex flex-col items-center justify-center w-full h-screen gap-6 ">
            <h1 className="text-4xl font-bold mb-8">Chess Menu</h1>
            <button
                className="w-64 py-3 rounded bg-black hover:bg-zinc-900 text-white text-xl font-semibold transition"
                onClick={() => onSelectMode(GameMode.bot)}
            >
                Player vs Bot
            </button>
            <button className="w-64 py-3 mb-2 rounded bg-zinc-400 text-white text-xl font-semibold cursor-not-allowed opacity-60" disabled>
                Player vs Player (Multiplayer)
                <span className="block text-xs text-zinc-200">Coming soon</span>
            </button>
            <button className="w-64 py-3 mb-2 rounded bg-zinc-400 text-white text-xl font-semibold cursor-not-allowed opacity-60" disabled>
                Player vs Player (Offline)
                <span className="block text-xs text-zinc-200">Coming soon</span>
            </button>

        </div>
    );
}


export default Menu;