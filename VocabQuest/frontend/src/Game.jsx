import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import confetti from 'canvas-confetti';
import { Volume2, Trophy, Flame, ArrowLeft, Lightbulb } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export default function Game({ onBack, mode = 'vocab' }) {
  const [gameState, setGameState] = useState(null);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("playing");
  const [feedback, setFeedback] = useState("");
  const [canType, setCanType] = useState(false);
  const [mathAnswer, setMathAnswer] = useState(null);
  const [explanation, setExplanation] = useState(""); // State for explanation
  const inputRef = useRef(null);

  useEffect(() => {
    loadNextChallenge();
  }, [mode]);

  const loadNextChallenge = async () => {
    setStatus("loading");
    try {
      const endpoint = mode === 'math' ? '/next_math' : '/next_word';
      const res = await axios.get(`${API_URL}${endpoint}`);
      setGameState(res.data);

      if (mode === 'math') {
        setMathAnswer(res.data.hashed_answer);
        setExplanation(res.data.explanation); // Store the explanation
      }

      setInput("");
      setFeedback("");
      setCanType(false);
      setStatus("playing");

      const delay = mode === 'math' ? 500 : 3000;
      setTimeout(() => {
        setCanType(true);
        inputRef.current?.focus();
      }, delay);

    } catch (err) {
      console.error("Failed to load challenge", err);
    }
  };

  // ... (speakWord and handleSpeakClick functions remain the same) ...
  const speakWord = (text) => {
    if (!text) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-GB';
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  };

  const handleSpeakClick = () => {
    if (gameState && gameState.tts_text) {
      speakWord(gameState.tts_text);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (mode === 'vocab') {
        // ... (Vocab logic remains the same) ...
        try {
            const res = await axios.post(`${API_URL}/check_answer`, {
                id: gameState.id,
                spelling: input
            });

            if (res.data.correct) {
                setStatus("correct");
                setFeedback("🎉 Excellent!");
                confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
                speakWord(res.data.correct_word);
                setTimeout(loadNextChallenge, 2000);
            } else {
                setStatus("wrong");
                setFeedback(`❌ Oops! The word was: ${res.data.correct_word}`);
                speakWord(res.data.correct_word);
                setTimeout(loadNextChallenge, 3500);
            }
        } catch (err) {
            console.error(err);
        }
    } else {
        // MATH SUBMIT LOGIC
        try {
            const res = await axios.post(`${API_URL}/check_math`, {
                answer: input,
                correct_answer: mathAnswer
            });

            if (res.data.correct) {
                setStatus("correct");
                setFeedback("🎉 Correct!");
                confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
                setTimeout(loadNextChallenge, 1500);
            } else {
                setStatus("wrong");
                // Use the stored explanation
                setFeedback(
                    <div className="flex flex-col items-center gap-2">
                        <span>❌ The answer was: {res.data.correct_answer}</span>
                        {explanation && (
                             <div className="text-lg bg-yellow-100 text-yellow-800 p-3 rounded-xl border border-yellow-200 mt-2 flex items-start gap-2 text-left max-w-md">
                                <Lightbulb className="w-6 h-6 shrink-0 mt-1" />
                                <span>{explanation}</span>
                             </div>
                        )}
                    </div>
                );
                // Longer delay to let them read the explanation
                setTimeout(loadNextChallenge, 8000);
            }
        } catch (err) {
            console.error(err);
        }
    }
  };

  if (!gameState || status === "loading") return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-50">
      <div className="animate-bounce text-6xl mb-4">🦁</div>
      <div className="text-xl font-bold text-indigo-800 animate-pulse">Loading...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-100 flex flex-col items-center py-6 px-4 font-sans relative">
      <button onClick={onBack} className="absolute top-6 left-6 p-2 bg-white rounded-full shadow-md hover:bg-gray-100 transition">
        <ArrowLeft className="w-6 h-6 text-indigo-600" />
      </button>

      {/* Stats Bar */}
      <div className="w-full max-w-2xl flex justify-between bg-white p-4 rounded-2xl shadow-lg mb-8">
        <div className="flex items-center gap-3 text-yellow-600 font-black text-2xl">
          <Trophy className="w-8 h-8 fill-current" />
          <span>{gameState.score}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">LEVEL</span>
          <span className="text-2xl font-black text-indigo-600">{gameState.user_level}</span>
        </div>
        <div className="flex items-center gap-3 text-orange-500 font-black text-2xl">
          <Flame className="w-8 h-8 fill-current" />
          <span>{gameState.streak}</span>
        </div>
      </div>

      <div className="bg-white p-8 rounded-3xl shadow-2xl max-w-2xl w-full border-4 border-indigo-200 relative">
        {mode === 'math' ? (
            <div className="mb-8 px-2 text-center min-h-[200px] flex items-center justify-center">
                <p className="text-3xl md:text-4xl font-black text-indigo-900 leading-tight drop-shadow-sm">
                    {gameState.question}
                </p>
            </div>
        ) : (
            // ... (Vocab UI code remains same) ...
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
            </>
        )}

        {/* Input Form */}
        <form onSubmit={handleSubmit} autoComplete="off" className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto relative">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            maxLength={mode === 'vocab' ? gameState.length : 10}
            disabled={status !== "playing" || !canType}
            type={mode === 'math' ? "number" : "search"}
            className={`flex-1 p-4 rounded-xl border-4 text-2xl focus:outline-none text-center uppercase tracking-widest shadow-inner font-bold transition-all
                    ${!canType ? 'bg-gray-200 border-gray-300 text-gray-400 cursor-wait' : 'border-indigo-100 focus:border-indigo-500 text-indigo-800 bg-white'}
                `}
            placeholder={canType ? (mode === 'math' ? "ENTER NUMBER" : "TYPE HERE") : "WAIT..."}
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
      </div>
    </div>
  );
}
