import React, { useState, useEffect } from 'react';
import { Lightbulb } from 'lucide-react';

export default function MathGame({
  gameState,
  input,
  setInput,
  status,
  canType,
  inputRef,
  handleSubmit,
  feedback,
  topic,
  onTopicChange,
  hideTopicSelector
}) {
  const topics = ["Mental Maths", "BIDMAS", "Fractions", "Percentages", "Ratio", "Algebra", "Geometry", "Statistics"];
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    if (status === 'wrong') {
      setShowExplanation(true);
    } else if (status === 'playing') {
      setShowExplanation(false);
    }
  }, [status]);

  return (
    <>
      {!hideTopicSelector && (
          <div className="mb-4 flex justify-center">
            <select
              value={topic || ""}
              onChange={(e) => onTopicChange && onTopicChange(e.target.value)}
              className="p-2 border-2 border-indigo-200 rounded-lg text-indigo-700 font-bold focus:outline-none focus:border-indigo-500"
              disabled={status !== "playing"}
            >
               <option value="">Mixed (Default)</option>
               {topics.map(t => (
                   <option key={t} value={t}>{t}</option>
               ))}
            </select>
          </div>
      )}

      <div className="mb-8 px-2 text-center min-h-[200px] flex items-center justify-center">
        <p className="text-3xl md:text-4xl font-black text-indigo-900 leading-tight drop-shadow-sm">
          {gameState.question}
        </p>
      </div>

      {showExplanation && (
        <div className="bg-yellow-50 p-4 rounded-xl border border-yellow-200 mb-6 flex flex-col items-center max-w-lg mx-auto animate-in fade-in slide-in-from-top-4 duration-300">
             <div className="flex items-center gap-2 mb-2 text-yellow-800 font-bold text-lg">
                 <Lightbulb className="w-6 h-6" />
                 <span>Worked Solution</span>
             </div>
             <p className="text-yellow-900 text-center font-medium">
                 {gameState.explanation || "Step 1: Calculate total... Step 2: Divide by..."}
             </p>
        </div>
      )}

      <form onSubmit={handleSubmit} autoComplete="off" className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto relative">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          maxLength={10}
          disabled={status !== "playing" || !canType}
          type="text"
          inputMode="text"
          className={`flex-1 p-4 rounded-xl border-4 text-2xl focus:outline-none text-center uppercase tracking-widest shadow-inner font-bold transition-all
                  ${!canType ? 'bg-gray-200 border-gray-300 text-gray-400 cursor-wait' : 'border-indigo-100 focus:border-indigo-500 text-indigo-800 bg-white'}
              `}
          placeholder={canType ? "ENTER ANSWER" : "WAIT..."}
        />
        <button
          type="submit"
          disabled={status !== "playing"}
          className="bg-green-500 hover:bg-green-600 text-white font-black text-xl py-4 px-8 rounded-xl shadow-[0_6px_0_rgb(21,128,61)] hover:translate-y-1 active:translate-y-2 transition-all disabled:opacity-50"
        >
          GO!
        </button>
      </form>

      <div className="text-center mt-8 min-h-[3rem]">
        {feedback}
      </div>
    </>
  );
}
