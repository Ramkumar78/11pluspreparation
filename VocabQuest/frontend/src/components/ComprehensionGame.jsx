import React, { useState, useEffect } from 'react';

export default function ComprehensionGame({
  gameState,
  currentCompQuestion,
  handleCompOptionClick,
  status,
  feedback
}) {
  const [selectedEvidence, setSelectedEvidence] = useState("");

  useEffect(() => {
    setSelectedEvidence("");
  }, [currentCompQuestion]);

  const handleMouseUp = () => {
    const selection = window.getSelection().toString().trim();
    if (selection.length > 0) {
      setSelectedEvidence(selection);
    }
  };

  return (
    <>
      {currentCompQuestion && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-[65vh]">
          {/* Passage Column */}
          <div
            className="bg-indigo-50 p-6 rounded-2xl overflow-y-auto h-full pr-6 shadow-inner select-text cursor-text"
            onMouseUp={handleMouseUp}
          >
            {gameState.image_url && (
              <div className="mb-4 rounded-xl overflow-hidden border-2 border-indigo-200 shadow-sm">
                <img src={gameState.image_url} alt={gameState.title} className="w-full h-48 object-cover" />
              </div>
            )}
            <h2 className="text-2xl font-bold text-indigo-900 mb-2 sticky top-0 bg-indigo-50 pb-2 z-10">{gameState.title}</h2>
            <span className="inline-block bg-indigo-200 text-indigo-800 text-xs px-2 py-1 rounded-full mb-4 uppercase tracking-wider font-bold">
              {gameState.topic}
            </span>
            <p className="text-lg text-indigo-800 leading-relaxed whitespace-pre-line font-medium selection:bg-yellow-200 selection:text-indigo-900">
              {gameState.content}
            </p>
          </div>

          {/* Question Column */}
          <div className="flex flex-col justify-center h-full overflow-y-auto pl-2">
            <div className="mb-6">
              <span className="text-sm font-bold text-gray-400 uppercase tracking-widest block mb-2">QUESTION</span>
              <p className="text-xl font-bold text-gray-800 mb-4">
                {currentCompQuestion.text}
              </p>

              {selectedEvidence && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 animate-in fade-in zoom-in duration-300">
                  <div className="text-xs font-bold text-yellow-600 uppercase tracking-wider mb-1">Evidence Selected</div>
                  <p className="text-sm text-yellow-800 italic line-clamp-3">"{selectedEvidence}"</p>
                </div>
              )}
            </div>

            <div className="space-y-3">
              {currentCompQuestion.options.map((option, idx) => (
                <button
                  key={idx}
                  onClick={() => handleCompOptionClick(option, selectedEvidence)}
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
