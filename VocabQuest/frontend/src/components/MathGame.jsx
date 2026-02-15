import React from 'react';

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
  onTopicChange
}) {
  const topics = ["Mental Maths", "BIDMAS", "Fractions", "Percentages", "Ratio", "Algebra", "Geometry", "Statistics"];

  return (
    <>
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

      <div className="mb-8 px-2 text-center min-h-[200px] flex items-center justify-center">
        <p className="text-3xl md:text-4xl font-black text-indigo-900 leading-tight drop-shadow-sm">
          {gameState.question}
        </p>
      </div>

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
