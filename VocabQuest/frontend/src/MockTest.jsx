import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Clock, CheckCircle, XCircle, ArrowRight, ArrowLeft } from 'lucide-react';
import confetti from 'canvas-confetti';
import { MODES, MOCK_TYPES, API_URL } from './constants';

export default function MockTest() {
  const navigate = useNavigate();
  const { type: paramType } = useParams();
  const type = paramType || MOCK_TYPES.MIXED;

  const [test, setTest] = useState(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({}); // { id: value }
  const [timeLeft, setTimeLeft] = useState(1200); // 20 mins default
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    // Fetch new mock test
    axios.get(`${API_URL}/mock_test?type=${type}`)
      .then(res => {
        setTest(res.data);
        setTimeLeft(res.data.duration_minutes * 60);
      })
      .catch(err => console.error(err));
  }, [type]);

  // Timer
  useEffect(() => {
    if (result) return;
    if (!test) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          handleSubmitTest();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [result, test]);

  const handleAnswerChange = (val) => {
    if (!test) return;
    const currentQ = test.items[currentIdx];
    setAnswers(prev => ({ ...prev, [currentQ.id]: val }));
  };

  const nextQuestion = () => {
    if (currentIdx < test.items.length - 1) {
      setCurrentIdx(currentIdx + 1);
    } else {
      handleSubmitTest();
    }
  };

  const handleSubmitTest = async () => {
    setSubmitting(true);
    const payload = test.items.map(item => ({
      id: item.id,
      type: item.type,
      user_answer: answers[item.id] || ""
    }));

    try {
      const res = await axios.post(`${API_URL}/submit_mock`, { answers: payload });
      setResult(res.data);
      if (res.data.percentage > 70) confetti();
    } catch (err) {
      console.error(err);
    }
    setSubmitting(false);
  };

  // --- RENDERING ---

  if (!test) return <div className="flex h-screen items-center justify-center font-bold text-indigo-600">Generating Mock Exam...</div>;

  if (result) {
    return (
      <div className="min-h-screen bg-white p-8 max-w-4xl mx-auto font-sans">
        <div className="text-center mb-10">
          <h1 className="text-5xl font-black text-indigo-900 mb-4">Test Complete!</h1>
          <div className="inline-block p-6 rounded-full bg-indigo-50 border-4 border-indigo-100">
             <span className="text-6xl font-black text-indigo-600">{result.percentage}%</span>
          </div>
          <p className="text-gray-500 mt-4">Score: {result.total_score} / {result.max_score}</p>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-800">Review</h2>
          {result.breakdown.map((item, i) => (
            <div key={i} className={`p-4 rounded-xl border-l-4 ${item.correct ? 'bg-green-50 border-green-500' : 'bg-red-50 border-red-500'}`}>
              <div className="flex justify-between">
                <span className="font-bold text-gray-700">Question {i + 1} ({item.type.toUpperCase()})</span>
                {item.correct ? <CheckCircle className="text-green-600" /> : <XCircle className="text-red-600" />}
              </div>
              <p className="text-sm text-gray-600 mt-1">Your Answer: <span className="font-mono font-bold">{item.your_answer || "(Skipped)"}</span></p>
              {!item.correct && (
                <div className="mt-2 text-sm">
                  <p className="text-green-700 font-semibold">Correct Answer: {item.correct_answer}</p>
                  {item.explanation && <p className="text-gray-500 italic mt-1">💡 {item.explanation}</p>}
                </div>
              )}
            </div>
          ))}
        </div>
        <button onClick={() => navigate('/')} className="mt-8 w-full bg-indigo-600 text-white py-4 rounded-xl font-bold hover:bg-indigo-700 transition">Return to Dashboard</button>
      </div>
    );
  }

  const currentQ = test.items[currentIdx];
  const progress = ((currentIdx + 1) / test.items.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4 font-sans">
      {/* Header */}
      <div className="w-full max-w-2xl flex justify-between items-center mb-8 bg-white p-4 rounded-xl shadow-sm">
        <button onClick={() => navigate('/')} className="text-gray-500 hover:text-indigo-600"><ArrowLeft /></button>
        <div className="flex items-center gap-2 font-mono text-xl font-bold text-gray-700">
            <Clock className="text-orange-500" />
            {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
        </div>
        <div className="text-sm font-bold text-gray-400">
            QUESTION {currentIdx + 1} / {test.items.length}
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-2xl min-h-[400px] flex flex-col relative overflow-hidden">
        {/* Progress Line */}
        <div className="absolute top-0 left-0 h-2 bg-gray-100 w-full">
            <div className="h-full bg-indigo-500 transition-all duration-300" style={{ width: `${progress}%` }}></div>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center text-center mt-6">
            <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-widest mb-4 ${currentQ.type === MODES.MATH ? 'bg-blue-100 text-blue-600' : 'bg-purple-100 text-purple-600'}`}>
                {currentQ.type === MODES.MATH ? 'MATHEMATICS' : 'VOCABULARY'}
            </span>

            {currentQ.type === MODES.VOCAB && currentQ.image && (
                <img src={`${API_URL}${currentQ.image}`} className="h-40 object-contain mb-4 rounded-lg" alt="Clue" onError={(e) => e.target.style.display = 'none'} />
            )}

            {currentQ.type === MODES.COMPREHENSION && (
                <div className="w-full mb-6 text-left bg-gray-50 p-4 rounded-xl border border-gray-200 max-h-60 overflow-y-auto">
                     {currentQ.passage_image && (
                         <div className="mb-2 rounded-lg overflow-hidden border border-gray-200">
                             <img src={currentQ.passage_image} alt={currentQ.passage_title} className="w-full h-32 object-cover" />
                         </div>
                     )}
                    <h3 className="font-bold text-lg mb-2">{currentQ.passage_title}</h3>
                    <p className="whitespace-pre-line text-sm text-gray-700">{currentQ.passage_content}</p>
                </div>
            )}

            <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-8 leading-snug">
                {currentQ.question}
            </h2>

            {currentQ.type === MODES.COMPREHENSION ? (
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                    {currentQ.options.map((opt, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleAnswerChange(opt)}
                            className={`p-3 rounded-lg border-2 font-bold text-left transition-all ${answers[currentQ.id] === opt ? 'bg-indigo-100 border-indigo-500 text-indigo-900' : 'bg-white border-gray-200 hover:border-indigo-300'}`}
                        >
                            {opt}
                        </button>
                    ))}
                 </div>
            ) : (
                <input
                    autoFocus
                    value={answers[currentQ.id] || ""}
                    onChange={(e) => handleAnswerChange(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && nextQuestion()}
                    className="w-full max-w-md p-4 text-center text-2xl border-b-4 border-gray-200 focus:border-indigo-500 outline-none bg-gray-50 rounded-t-lg transition-colors"
                    placeholder="Type answer..."
                    autoComplete="off"
                />
            )}
        </div>

        <button
            onClick={nextQuestion}
            disabled={submitting}
            className="mt-8 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg active:scale-95 disabled:opacity-50"
        >
            {submitting ? 'Submitting...' : (currentIdx === test.items.length - 1 ? 'Finish Test' : 'Next Question')} { !submitting && <ArrowRight size={20} /> }
        </button>
      </div>
    </div>
  );
}
