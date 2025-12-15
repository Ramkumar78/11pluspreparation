import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import confetti from 'canvas-confetti';
import { Volume2, Trophy, Flame, ArrowLeft } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export default function Game({ onBack }) {
  const [gameState, setGameState] = useState(null); // The current word object
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("playing"); // playing, correct, wrong
  const [feedback, setFeedback] = useState("");
  const [canType, setCanType] = useState(false); // New state for reading delay
  const inputRef = useRef(null);

  // Initial Load
  useEffect(() => {
    loadNextWord();
  }, []);

  const loadNextWord = async () => {
    setStatus("loading");
    try {
      const res = await axios.get(`${API_URL}/next_word`);
      setGameState(res.data);
      setInput("");
      setFeedback("");
      setCanType(false); // Lock input
      setStatus("playing");

      // Force read time: 3 seconds delay
      setTimeout(() => {
        setCanType(true);
        inputRef.current?.focus();
      }, 3000);

    } catch (err) {
      console.error("Failed to load word", err);
      // Fallback state or error message could go here
    }
  };

  // Real TTS Function
  const speakWord = (text) => {
    if (!text) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-GB';
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  };

  const handleSpeakClick = () => {
    // Use the tts_text from backend if available
    if (gameState && gameState.tts_text) {
      speakWord(gameState.tts_text);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      const res = await axios.post(`${API_URL}/check_answer`, {
        id: gameState.id,
        spelling: input
      });

      if (res.data.correct) {
        setStatus("correct");
        setFeedback("🎉 Excellent!");
        confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
        speakWord(res.data.correct_word); // Pronounce on success
        setTimeout(loadNextWord, 2000);
      } else {
        setStatus("wrong");
        setFeedback(`❌ Oops! The word was: ${res.data.correct_word}`);
        speakWord(res.data.correct_word); // Pronounce correction
        setTimeout(loadNextWord, 3500); // Give time to read correction
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (!gameState || status === "loading") return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-50">
      <div className="animate-bounce text-6xl mb-4">🦁</div>
      <div className="text-xl font-bold text-indigo-800 animate-pulse">Loading Next Challenge...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-100 flex flex-col items-center py-6 px-4 font-sans relative">

      {/* Back Button */}
      <button onClick={onBack} className="absolute top-6 left-6 p-2 bg-white rounded-full shadow-md hover:bg-gray-100 transition">
        <ArrowLeft className="w-6 h-6 text-indigo-600" />
      </button>

      {/* Header Stats */}
      <div className="w-full max-w-2xl flex justify-between bg-white p-4 rounded-2xl shadow-lg mb-8 transform hover:scale-[1.02] transition-transform">
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

      {/* Main Game Card */}
      <div className="bg-white p-8 rounded-3xl shadow-2xl max-w-2xl w-full border-4 border-indigo-200 relative">

        {/* Definition Area - High Priority */}
        <div className="mb-6 px-2 text-center">
          <p className="text-2xl md:text-3xl font-black text-indigo-900 leading-tight drop-shadow-sm">
            "{gameState.definition}"
          </p>
        </div>

        {/* Image Area */}
        <div className="relative w-full h-64 bg-gray-100 rounded-2xl overflow-hidden mb-8 group border-4 border-white shadow-lg mx-auto max-w-md">
          <img
            src={gameState.image}
            alt="Clue"
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
          />
        </div>

        {/* Audio Clue */}
        <div className="flex justify-center mb-6">
          <button
            onClick={handleSpeakClick}
            type="button"
            className="flex items-center gap-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-6 py-2 rounded-full font-bold transition-colors"
          >
            <Volume2 className="w-5 h-5" />
            <span>Hear Word</span>
          </button>
        </div>

        {/* Word Dashes */}
        <div className="text-center mb-10">
          <div className="flex flex-wrap justify-center gap-2 md:gap-3 text-3xl md:text-5xl font-mono text-indigo-900 font-bold">
            {Array(gameState.length).fill("_").map((_, i) => (
              <span key={i} className="border-b-4 border-indigo-300 w-8 md:w-12 h-14 md:h-16 flex items-center justify-center bg-indigo-50/50 rounded-t-lg">
                {input[i] || ""}
              </span>
            ))}
          </div>
        </div>

        {/* Input Area */}
        {/* Input Area */}
        <form onSubmit={handleSubmit} autoComplete="off" className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto relative">
          <input
            ref={inputRef}
            type="text"
            name="vocab_input_no_autofill"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            maxLength={gameState.length}
            disabled={status !== "playing" || !canType}
            className={`flex-1 p-4 rounded-xl border-4 text-2xl focus:outline-none text-center uppercase tracking-widest shadow-inner font-bold transition-all
                    ${!canType ? 'bg-gray-200 border-gray-300 text-gray-400 cursor-wait' : 'border-indigo-100 focus:border-indigo-500 text-indigo-800 bg-white'}
                `}
            placeholder={canType ? "TYPE HERE" : "READ DEFINITION..."}
            autoComplete="one-time-code"
            autoCorrect="off"
            autoCapitalize="none"
            spellCheck="false"
            data-lpignore="true"
          />
          <button
            type="submit"
            disabled={status !== "playing"}
            className="bg-gradient-to-r from-green-400 to-green-600 hover:from-green-500 hover:to-green-700 text-white font-black text-xl py-4 px-8 rounded-xl shadow-[0_6px_0_rgb(21,128,61)] hover:shadow-[0_4px_0_rgb(21,128,61)] hover:translate-y-1 active:translate-y-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none disabled:translate-y-0"
          >
            GO!
          </button>
        </form>

        <div className="text-center mt-8 h-12">
          {feedback && (
            <div className={`text-2xl font-black ${status === 'correct' ? 'text-green-500' : 'text-red-500'} animate-bounce`}>
              {feedback}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
