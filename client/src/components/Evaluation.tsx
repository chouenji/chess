interface EvaluationBarProps {
  evaluation: number | null;
}


// Evaluation is in pawns: positive = white advantage, negative = black advantage
const clamp = (val: number, min: number, max: number) => Math.max(min, Math.min(max, val));

function EvaluationBar({ evaluation }: EvaluationBarProps) {
  const evalClamped = clamp(evaluation ?? 0, -20, 20);

  const isMate = evaluation !== null && Number.isInteger(evaluation) && Math.abs(evaluation) <= 10;
  let percent = ((evalClamped + 20) / 40) * 100;
  if (isMate) {
    percent = evaluation! > 0 ? 100 : 0;
  }

  return (
    <div className="relative w-10 h-[800px] bg-gradient-to-t from-zinc-900 to-white mx-auto">
      {/* White advantage (bottom) */}
      <div
        className="absolute left-0 bottom-0 w-full bg-white transition-all duration-500"
        style={{ height: `${percent}%` }}
      />
      {/* Black advantage (top) */}
      <div
        className="absolute left-0 top-0 w-full bg-zinc-800 transition-all duration-500"
        style={{ height: `${100 - percent}%` }}
      />
      {/* Evaluation text */}
      <div className="absolute left-0 top-[780px] w-full text-center font-bold text-sm -translate-y-1/2 pointer-events-none drop-shadow-sm select-none"
        style={{ color: (isMate && evaluation !== null && evaluation < 0) || (evaluation !== null && evaluation < -19) ? 'white' : '#1f2937' }}>
        <span>
          {evaluation !== null
            ? (isMate
              ? `#${evaluation}`
              : evaluation.toFixed(2))
            : '0.0'}
        </span>
      </div>
    </div>
  );
};

export default EvaluationBar;
