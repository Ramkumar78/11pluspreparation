import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import confetti from 'canvas-confetti';
import { Trophy, Flame, ArrowLeft, Lightbulb, Clock, Zap, RotateCcw } from 'lucide-react';
import { MODES, API_URL } from './constants';
import VocabGame from './components/VocabGame';
import MathGame from './components/MathGame';
import ComprehensionGame from './components/ComprehensionGame';

export default function Game() {
  const navigate = useNavigate();
  const { mode: paramMode } = useParams();
  const mode = paramMode || MODES.VOCAB;

  const [gameState, setGameState] = useState(null);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("playing");
  const [feedback, setFeedback] = useState("");
  const [canType, setCanType] = useState(false);
  const [mathAnswer, setMathAnswer] = useState(null);
  const [explanation, setExplanation] = useState("");
  const [compQuestionId, setCompQuestionId] = useState(null);
  const [currentCompQuestion, setCurrentCompQuestion] = useState(null);
  const [isTimed, setIsTimed] = useState(false);
  const [timeLeft, setTimeLeft] = useState(60);
  const [topic, setTopic] = useState("");
  const [newBadge, setNewBadge] = useState(null);

  // Blitz Mode State
  const [isBlitz, setIsBlitz] = useState(false);
  const [blitzTimeLeft, setBlitzTimeLeft] = useState(60);
  const [blitzStats, setBlitzStats] = useState({ correct: 0, total: 0 });
  const [showBlitzSummary, setShowBlitzSummary] = useState(false);

  const inputRef = useRef(null);

  useEffect(() => {
    loadNextChallenge();
  }, [mode, topic]);

  // Per-Question Timer
  useEffect(() => {
    if (!isTimed || status !== 'playing') return;
    if (timeLeft === 0) {
      handleTimeout();
      return;
    }
    const timer = setInterval(() => setTimeLeft(t => t - 1), 1000);
    return () => clearInterval(timer);
  }, [isTimed, status, timeLeft]);

  // Blitz Timer
  useEffect(() => {
    if (!isBlitz || showBlitzSummary) return;
    if (blitzTimeLeft === 0) {
      setShowBlitzSummary(true);
      setIsBlitz(false);
      return;
    }
    const timer = setInterval(() => setBlitzTimeLeft(t => t - 1), 1000);
    return () => clearInterval(timer);
  }, [isBlitz, blitzTimeLeft, showBlitzSummary]);

  const startBlitz = () => {
    setIsBlitz(true);
    setBlitzTimeLeft(60);
    setBlitzStats({ correct: 0, total: 0 });
    setShowBlitzSummary(false);
    setIsTimed(false); // Disable per-question timer
    loadNextChallenge();
  };

  const loadNextChallenge = async () => {
    setStatus("loading");
    setTimeLeft(60);
    try {
      let endpoint = '/next_word';
      if (mode === MODES.MATH) {
        endpoint = `/next_math${topic ? `?topic=${encodeURIComponent(topic)}` : ''}`;
      }
      if (mode === MODES.COMPREHENSION) endpoint = '/next_comprehension';

      const res = await axios.get(`${API_URL}${endpoint}`);
      setGameState(res.data);

      if (mode === MODES.MATH) {
        setMathAnswer(res.data.generated_answer_check);
        setExplanation(res.data.explanation);
      } else if (mode === MODES.COMPREHENSION) {
        if (res.data.questions && res.data.questions.length > 0) {
            // Select a random question from the list
            const randomQ = res.data.questions[Math.floor(Math.random() * res.data.questions.length)];
            setCompQuestionId(randomQ.id);
            setCurrentCompQuestion(randomQ);
        }
      }

      setInput("");
      setFeedback("");
      setCanType(false);
      setStatus("playing");

      const delay = isBlitz ? 100 : (mode === MODES.MATH ? 500 : (mode === MODES.COMPREHENSION ? 1000 : 3000));
      setTimeout(() => {
        setCanType(true);
        if (inputRef.current && mode !== MODES.COMPREHENSION) {
            inputRef.current.focus();
        }
      }, delay);

    } catch (err) {
      console.error("Failed to load challenge", err);
    }
  };

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

  const checkAndShowBadges = (res) => {
    if (res.data.new_badges && res.data.new_badges.length > 0) {
      setNewBadge(res.data.new_badges[0]);
      confetti({
          particleCount: 200,
          spread: 100,
          origin: { y: 0.5 },
          colors: ['#FFD700', '#FFA500', '#FF4500']
      });
      setTimeout(() => setNewBadge(null), 5000);
    }
  };

  const handleTimeout = () => {
    setStatus("wrong");

    if (mode === MODES.MATH) {
        setFeedback(
            <div className="flex flex-col items-center gap-2">
                <span>⏰ Time's Up! The answer was: {mathAnswer}</span>
                {explanation && (
                        <div className="text-lg bg-yellow-100 text-yellow-800 p-3 rounded-xl border border-yellow-200 mt-2 flex items-start gap-2 text-left max-w-md">
                        <Lightbulb className="w-6 h-6 shrink-0 mt-1" />
                        <span>{explanation}</span>
                        </div>
                )}
            </div>
        );
        setTimeout(loadNextChallenge, 5000);
    } else if (mode === MODES.VOCAB) {
        axios.post(`${API_URL}/check_answer`, {
                id: gameState.id,
                spelling: "TIMEOUT"
            }).then(res => {
                setFeedback(`⏰ Time's Up! The word was: ${res.data.correct_word}`);
                speakWord(res.data.correct_word);
                setTimeout(loadNextChallenge, 3500);
            }).catch(err => {
                console.error(err);
                setTimeout(loadNextChallenge, 2000);
            });
    } else if (mode === MODES.COMPREHENSION) {
         axios.post(`${API_URL}/check_comprehension`, {
              question_id: compQuestionId,
              answer: "TIMEOUT"
          }).then(res => {
              setFeedback(
                  <div className="flex flex-col items-center gap-2">
                      <span>⏰ Time's Up! The answer was: {res.data.correct_answer}</span>
                      {res.data.explanation && (
                           <div className="text-lg bg-yellow-100 text-yellow-800 p-3 rounded-xl border border-yellow-200 mt-2 flex items-start gap-2 text-left max-w-md">
                              <Lightbulb className="w-6 h-6 shrink-0 mt-1" />
                              <span>{res.data.explanation}</span>
                           </div>
                      )}
                  </div>
              );
              setTimeout(loadNextChallenge, 5000);
          }).catch(err => {
               console.error(err);
               setTimeout(loadNextChallenge, 2000);
          });
    }
  };

  const handleCompOptionClick = async (option) => {
      if (status !== 'playing') return;

      try {
          const res = await axios.post(`${API_URL}/check_comprehension`, {
              question_id: compQuestionId,
              answer: option
          });

          if (res.data.correct) {
              if (isBlitz) setBlitzStats(s => ({ ...s, correct: s.correct + 1, total: s.total + 1 }));
              setStatus("correct");
              setFeedback("🎉 Correct!");
              checkAndShowBadges(res);
              if (!isBlitz) confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
              setTimeout(loadNextChallenge, isBlitz ? 500 : 2000);
          } else {
              if (isBlitz) setBlitzStats(s => ({ ...s, total: s.total + 1 }));
              setStatus("wrong");
              setFeedback(
                  <div className="flex flex-col items-center gap-2">
                      <span>❌ Incorrect. The answer was: {res.data.correct_answer}</span>
                      {res.data.explanation && !isBlitz && (
                           <div className="text-lg bg-yellow-100 text-yellow-800 p-3 rounded-xl border border-yellow-200 mt-2 flex items-start gap-2 text-left max-w-md">
                              <Lightbulb className="w-6 h-6 shrink-0 mt-1" />
                              <span>{res.data.explanation}</span>
                           </div>
                      )}
                  </div>
              );
              setTimeout(loadNextChallenge, isBlitz ? 1000 : 8000);
          }
      } catch (err) {
          console.error(err);
      }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (mode === MODES.VOCAB) {
        try {
            const res = await axios.post(`${API_URL}/check_answer`, {
                id: gameState.id,
                spelling: input
            });

            if (res.data.correct) {
                if (isBlitz) setBlitzStats(s => ({ ...s, correct: s.correct + 1, total: s.total + 1 }));
                setStatus("correct");
                setFeedback("🎉 Excellent!");
                checkAndShowBadges(res);
                if (!isBlitz) confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
                speakWord(res.data.correct_word);
                setTimeout(loadNextChallenge, isBlitz ? 500 : 2000);
            } else {
                if (isBlitz) setBlitzStats(s => ({ ...s, total: s.total + 1 }));
                setStatus("wrong");
                setFeedback(`❌ Oops! The word was: ${res.data.correct_word}`);
                speakWord(res.data.correct_word);
                setTimeout(loadNextChallenge, isBlitz ? 1000 : 3500);
            }
        } catch (err) {
            console.error(err);
        }
    } else if (mode === MODES.MATH) {
        try {
            const res = await axios.post(`${API_URL}/check_math`, {
                id: gameState.id,
                answer: input,
                correct_answer: mathAnswer
            });

            if (res.data.correct) {
                if (isBlitz) setBlitzStats(s => ({ ...s, correct: s.correct + 1, total: s.total + 1 }));
                setStatus("correct");
                setFeedback("🎉 Correct!");
                checkAndShowBadges(res);
                if (!isBlitz) confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } });
                setTimeout(loadNextChallenge, isBlitz ? 500 : 1500);
            } else {
                if (isBlitz) setBlitzStats(s => ({ ...s, total: s.total + 1 }));
                setStatus("wrong");
                setFeedback(
                    <div className="flex flex-col items-center gap-2">
                        <span>❌ The answer was: {res.data.correct_answer}</span>
                        {explanation && !isBlitz && (
                             <div className="text-lg bg-yellow-100 text-yellow-800 p-3 rounded-xl border border-yellow-200 mt-2 flex items-start gap-2 text-left max-w-md">
                                <Lightbulb className="w-6 h-6 shrink-0 mt-1" />
                                <span>{explanation}</span>
                             </div>
                        )}
                    </div>
                );
                setTimeout(loadNextChallenge, isBlitz ? 1000 : 8000);
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
      <button onClick={() => navigate('/')} className="absolute top-6 left-6 p-2 bg-white rounded-full shadow-md hover:bg-gray-100 transition">
        <ArrowLeft className="w-6 h-6 text-indigo-600" />
      </button>

      <div className="absolute top-6 right-6 flex gap-3">
        {!isBlitz && (
            <button
                onClick={() => setIsTimed(!isTimed)}
                className={`p-2 rounded-full shadow-md transition flex items-center gap-2 font-bold ${isTimed ? 'bg-indigo-600 text-white' : 'bg-white text-gray-500 hover:bg-gray-100'}`}
            >
                <Clock className="w-6 h-6" />
                <span className="hidden md:inline">{isTimed ? `TIME: ${timeLeft}s` : 'TIMER OFF'}</span>
            </button>
        )}

        <button
            onClick={isBlitz ? () => setIsBlitz(false) : startBlitz}
            className={`p-2 rounded-full shadow-md transition flex items-center gap-2 font-bold ${isBlitz ? 'bg-orange-600 text-white' : 'bg-white text-orange-600 hover:bg-orange-50'}`}
        >
            <Zap className="w-6 h-6" />
            <span className="hidden md:inline">{isBlitz ? `BLITZ: ${blitzTimeLeft}s` : 'BLITZ MODE'}</span>
        </button>
      </div>

      {showBlitzSummary && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/50 backdrop-blur-sm animate-in fade-in duration-300">
           <div className="bg-white p-8 rounded-3xl shadow-2xl flex flex-col items-center text-center max-w-sm mx-4 transform scale-110">
               <div className="p-4 bg-orange-100 rounded-full mb-4 text-orange-600 animate-bounce">
                   <Zap size={64} strokeWidth={3} />
               </div>
               <h3 className="text-3xl font-black text-indigo-900 mb-2">BLITZ COMPLETE!</h3>
               <div className="grid grid-cols-2 gap-4 w-full mb-6">
                   <div className="bg-green-50 p-4 rounded-xl">
                       <div className="text-3xl font-black text-green-600">{blitzStats.correct}</div>
                       <div className="text-sm font-bold text-green-800 uppercase">Correct</div>
                   </div>
                   <div className="bg-gray-50 p-4 rounded-xl">
                       <div className="text-3xl font-black text-gray-600">{blitzStats.total}</div>
                       <div className="text-sm font-bold text-gray-800 uppercase">Total</div>
                   </div>
               </div>
               <div className="text-xl font-bold text-indigo-600 mb-6">
                   Accuracy: {blitzStats.total > 0 ? Math.round((blitzStats.correct / blitzStats.total) * 100) : 0}%
               </div>
               <div className="flex gap-3 w-full">
                    <button onClick={() => setShowBlitzSummary(false)} className="flex-1 bg-gray-200 text-gray-700 font-bold py-3 rounded-xl hover:bg-gray-300 transition">
                        CLOSE
                    </button>
                    <button onClick={startBlitz} className="flex-1 bg-orange-600 text-white font-bold py-3 rounded-xl hover:bg-orange-700 transition flex items-center justify-center gap-2">
                        <RotateCcw size={20} /> RETRY
                    </button>
               </div>
           </div>
        </div>
      )}

      {newBadge && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/50 backdrop-blur-sm animate-in fade-in duration-300">
           <div className="bg-white p-8 rounded-3xl shadow-2xl flex flex-col items-center text-center max-w-sm mx-4 transform scale-110">
               <div className="p-4 bg-yellow-100 rounded-full mb-4 text-yellow-600 animate-bounce">
                   <Trophy size={64} strokeWidth={3} />
               </div>
               <h3 className="text-3xl font-black text-indigo-900 mb-2">BADGE UNLOCKED!</h3>
               <p className="text-2xl font-bold text-yellow-600 mb-6">{newBadge}</p>
               <button onClick={() => setNewBadge(null)} className="bg-indigo-600 text-white font-bold py-3 px-8 rounded-xl hover:bg-indigo-700 transition">
                   AWESOME!
               </button>
           </div>
        </div>
      )}

      {/* Stats Bar */}
      <div className="w-full max-w-2xl flex justify-between bg-white p-4 rounded-2xl shadow-lg mb-8">
        <div className="flex items-center gap-3 text-yellow-600 font-black text-2xl">
          <Trophy className="w-8 h-8 fill-current" />
          <span>{gameState.score !== undefined ? gameState.score : 0}</span>
        </div>
        {mode !== MODES.COMPREHENSION && (
            <div className="flex flex-col items-center">
            <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">LEVEL</span>
            <span className="text-2xl font-black text-indigo-600">{gameState.user_level}</span>
            </div>
        )}
        <div className="flex items-center gap-3 text-orange-500 font-black text-2xl">
          <Flame className="w-8 h-8 fill-current" />
          <span>{gameState.streak !== undefined ? gameState.streak : 0}</span>
        </div>
      </div>

      <div className={`bg-white p-8 rounded-3xl shadow-2xl w-full border-4 border-indigo-200 relative ${mode === MODES.COMPREHENSION ? 'max-w-4xl' : 'max-w-2xl'}`}>

        {mode === MODES.VOCAB && (
            <VocabGame
                gameState={gameState}
                input={input}
                setInput={setInput}
                status={status}
                canType={canType}
                inputRef={inputRef}
                handleSubmit={handleSubmit}
                handleSpeakClick={handleSpeakClick}
                feedback={feedback}
            />
        )}

        {mode === MODES.MATH && (
            <MathGame
                gameState={gameState}
                input={input}
                setInput={setInput}
                status={status}
                canType={canType}
                inputRef={inputRef}
                handleSubmit={handleSubmit}
                feedback={feedback}
                topic={topic}
                onTopicChange={setTopic}
            />
        )}

        {mode === MODES.COMPREHENSION && (
            <ComprehensionGame
                gameState={gameState}
                currentCompQuestion={currentCompQuestion}
                handleCompOptionClick={handleCompOptionClick}
                status={status}
                feedback={feedback}
            />
        )}
      </div>
    </div>
  );
}
