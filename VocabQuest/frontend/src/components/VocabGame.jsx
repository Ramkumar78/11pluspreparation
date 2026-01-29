import React from 'react';
import { Volume2 } from 'lucide-react';

export default function VocabGame({
  gameState,
  input,
  setInput,
  status,
  canType,
  inputRef,
  handleSubmit,
  handleSpeakClick,
  feedback
}) {
  return (
    <>
      <div className="mb-6 px-2 text-center">
        <p className="text-2xl md:text-3xl font-black text-indigo-900 leading-tight drop-shadow-sm">
          "{gameState.definition}"
        </p>
      </div>
      <div className="relative w-full h-64 bg-gray-100 rounded-2xl overflow-hidden mb-8 group border-4 border-white shadow-lg mx-auto max-w-md">
        <img src={gameState.image} alt="Clue" className="w-full h-full object-cover" />
      </div>
      <div className="flex justify-center mb-6">
        <button onClick={handleSpeakClick} type="button" className="flex items-center gap-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-6 py-2 rounded-full font-bold transition-colors">
          <Volume2 className="w-5 h-5" /> <span>Hear Word</span>
        </button>
      </div>
      <div className="text-center mb-10">
        <div className="flex flex-wrap justify-center gap-2 md:gap-3 text-3xl md:text-5xl font-mono text-indigo-900 font-bold">
          {Array(gameState.length).fill("_").map((_, i) => (
            <span key={i} className="border-b-4 border-indigo-300 w-8 md:w-12 h-14 md:h-16 flex items-center justify-center bg-indigo-50/50 rounded-t-lg">
              {input[i] || ""}
            </span>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} autoComplete="off" className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto relative">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          maxLength={gameState.length}
          disabled={status !== "playing" || !canType}
          type="search"
          className={`flex-1 p-4 rounded-xl border-4 text-2xl focus:outline-none text-center uppercase tracking-widest shadow-inner font-bold transition-all
                  ${!canType ? 'bg-gray-200 border-gray-300 text-gray-400 cursor-wait' : 'border-indigo-100 focus:border-indigo-500 text-indigo-800 bg-white'}
              `}
          placeholder={canType ? "TYPE HERE" : "WAIT..."}
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
