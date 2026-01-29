import React from 'react';

export default function ComprehensionGame({
  gameState,
  currentCompQuestion,
  handleCompOptionClick,
  status,
  feedback
}) {
  return (
    <>
      {currentCompQuestion && (
        <div className="flex flex-col md:flex-row gap-6">
          {/* Passage Column */}
          <div className="flex-1 bg-indigo-50 p-6 rounded-2xl max-h-[60vh] overflow-y-auto">
            {gameState.image_url && (
              <div className="mb-4 rounded-xl overflow-hidden border-2 border-indigo-200 shadow-sm">
                <img src={gameState.image_url} alt={gameState.title} className="w-full h-48 object-cover" />
              </div>
            )}
            <h2 className="text-2xl font-bold text-indigo-900 mb-2">{gameState.title}</h2>
            <span className="inline-block bg-indigo-200 text-indigo-800 text-xs px-2 py-1 rounded-full mb-4 uppercase tracking-wider font-bold">
              {gameState.topic}
            </span>
            <p className="text-lg text-indigo-800 leading-relaxed whitespace-pre-line font-medium">
              {gameState.content}
            </p>
          </div>

          {/* Question Column */}
          <div className="flex-1 flex flex-col justify-center">
            <div className="mb-6">
              <span className="text-sm font-bold text-gray-400 uppercase tracking-widest block mb-2">QUESTION</span>
              <p className="text-xl font-bold text-gray-800">
                {currentCompQuestion.text}
              </p>
            </div>

            <div className="space-y-3">
              {currentCompQuestion.options.map((option, idx) => (
                <button
                  key={idx}
                  onClick={() => handleCompOptionClick(option)}
                  disabled={status !== 'playing'}
                  className="w-full p-4 text-left bg-white border-2 border-indigo-100 hover:border-indigo-500 hover:bg-indigo-50 rounded-xl transition-all font-medium text-lg text-indigo-900 shadow-sm"
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="text-center mt-8 min-h-[3rem]">
        {feedback}
      </div>
    </>
  );
}
