import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Activity, BookOpen, ArrowLeft, Trophy } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export default function Dashboard() {
  const navigate = useNavigate();
  const [topics, setTopics] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [scoreHistory, setScoreHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
        axios.get(`${API_URL}/get_topics`),
        axios.get(`${API_URL}/get_user_stats`),
        axios.get(`${API_URL}/get_score_history`)
    ])
    .then(([topicsRes, statsRes, historyRes]) => {
        setTopics(topicsRes.data);
        setUserStats(statsRes.data);

        // Process history data for chart
        const historyData = historyRes.data.map(h => ({
             ...h,
             date: new Date(h.timestamp).toLocaleDateString() + ' ' + new Date(h.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
        }));
        setScoreHistory(historyData);

        setLoading(false);
    })
    .catch(err => {
        console.error(err);
        setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-10 text-center text-indigo-600 font-bold">Loading Analytics...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans">
      <button onClick={() => navigate('/')} className="flex items-center gap-2 text-gray-600 hover:text-indigo-600 mb-6 font-bold">
        <ArrowLeft /> Back to Home
      </button>

      <div className="flex flex-col md:flex-row gap-8 mb-8">
          <div className="flex-1">
              <h1 className="text-4xl font-black text-indigo-900 mb-2">My Learning Journey</h1>
              <p className="text-gray-500">Track your mastery across all 11+ topics.</p>
          </div>
          {userStats && (
            <div className="flex gap-4">
                <div className="bg-white p-4 rounded-2xl shadow-sm border border-indigo-100 text-center min-w-[100px]">
                    <div className="text-3xl font-black text-indigo-600">{userStats.score}</div>
                    <div className="text-xs font-bold text-gray-400 uppercase">Score</div>
                </div>
                 <div className="bg-white p-4 rounded-2xl shadow-sm border border-orange-100 text-center min-w-[100px]">
                    <div className="text-3xl font-black text-orange-500">{userStats.streak}</div>
                    <div className="text-xs font-bold text-gray-400 uppercase">Streak</div>
                </div>
            </div>
          )}
      </div>

      {userStats && userStats.badges && userStats.badges.length > 0 && (
          <div className="mb-8">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <Trophy className="text-yellow-500" /> Earned Badges
              </h2>
              <div className="flex flex-wrap gap-4">
                  {userStats.badges.map((badge, i) => (
                      <div key={i} className="bg-gradient-to-br from-yellow-100 to-amber-100 border-2 border-yellow-200 px-4 py-2 rounded-xl flex items-center gap-2 shadow-sm">
                          <Trophy size={16} className="text-yellow-600" />
                          <span className="font-bold text-yellow-800">{badge}</span>
                      </div>
                  ))}
              </div>
          </div>
      )}

      {/* Score Trend Chart */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Score Progression</h2>
        <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={scoreHistory}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" hide />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="score" stroke="#8884d8" activeDot={{ r: 8 }} name="Total Score" />
                </LineChart>
            </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {topics.map((t, idx) => (
          <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-3 rounded-lg ${t.topic === 'Mental Maths' ? 'bg-orange-100 text-orange-600' : 'bg-indigo-100 text-indigo-600'}`}>
                  {t.topic === 'Mental Maths' ? <Activity size={24} /> : <BookOpen size={24} />}
                </div>
                <div>
                  <h3 className="font-bold text-lg text-gray-800">{t.topic}</h3>
                  <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Level {t.level}</span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-3xl font-black text-indigo-600">{t.mastery}%</span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-100 rounded-full h-3 mb-4">
              <div
                className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-1000"
                style={{ width: `${t.mastery}%` }}
              ></div>
            </div>

            <div className="mt-auto flex justify-between text-sm text-gray-500 font-medium border-t pt-4">
              <span>Questions Answered: {t.total}</span>
              <span className="text-green-600">Correct: {t.correct}</span>
            </div>
          </div>
        ))}
        {topics.length === 0 && (
             <div className="col-span-2 text-center text-gray-500 p-10">
                 No topic data available yet. Start practicing!
             </div>
        )}
      </div>
    </div>
  );
}
