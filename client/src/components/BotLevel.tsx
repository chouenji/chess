

import React from "react";

interface BotLevelProps {
    level: string;
    onLevelChange: (level: string) => void;
}

const BotLevel: React.FC<BotLevelProps> = ({ level, onLevelChange }) => {
    return (
        <div className="bot-level">
            <h2>Bot Level</h2>
            <p>Choose the difficulty level of the bot:</p>
            <select value={level} onChange={(e) => onLevelChange(e.target.value)} className="bg-zinc-700 text-white p-2 rounded">
                <option value="" disabled>Select difficulty...</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
        </div>
    );
};

export default BotLevel;