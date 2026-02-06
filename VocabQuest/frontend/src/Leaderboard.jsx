import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Trophy, ArrowLeft, Calendar, Medal } from 'lucide-react';
import { API_URL } from './constants';

export default function Leaderboard() {
  const navigate = useNavigate();
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/leaderboard`)
      .then(res => {
        setScores(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans flex flex-col items-center">
      <div className="w-full max-w-4xl">
          <button onClick={() => navigate('/')} className="flex items-center gap-2 text-gray-600 hover:text-indigo-600 mb-6 font-bold">
            <ArrowLeft /> Back to Home
          </button>

          <div className="bg-white rounded-3xl shadow-xl p-8 border-4 border-yellow-200">
              <div className="text-center mb-8">
                  <div className="inline-block p-4 bg-yellow-100 rounded-full mb-4 text-yellow-600">
                      <Trophy size={48} strokeWidth={3} />
                  </div>
                  <h1 className="text-4xl font-black text-indigo-900">Hall of Fame</h1>
                  <p className="text-gray-500 font-bold mt-2">Top Recent Scores</p>
              </div>

              {loading ? (
                  <div className="text-center text-indigo-600 font-bold p-10">Loading Scores...</div>
              ) : (
                  <div className="overflow-hidden rounded-xl border border-gray-100">
                      <table className="w-full text-left">
                          <thead className="bg-indigo-50 text-indigo-900 font-black uppercase text-sm">
                              <tr>
                                  <th className="p-4">Rank</th>
                                  <th className="p-4">Mode</th>
                                  <th className="p-4">Date</th>
                                  <th className="p-4 text-right">Score</th>
                              </tr>
                          </thead>
                          <tbody className="divide-y divide-gray-100">
                              {scores.length === 0 ? (
                                  <tr>
                                      <td colSpan="4" className="p-8 text-center text-gray-400 font-bold">No scores yet. Be the first!</td>
                                  </tr>
                              ) : (
                                  scores.map((s, idx) => (
                                      <tr key={idx} className="hover:bg-indigo-50/50 transition">
                                          <td className="p-4 font-black text-gray-500 flex items-center gap-2">
                                              {idx === 0 && <Medal className="text-yellow-500" />}
                                              {idx === 1 && <Medal className="text-gray-400" />}
                                              {idx === 2 && <Medal className="text-orange-400" />}
                                              {idx + 1}
                                          </td>
                                          <td className="p-4 font-bold text-gray-700 capitalize">{s.mode}</td>
                                          <td className="p-4 text-gray-500 text-sm flex items-center gap-1">
                                              <Calendar size={14} /> {s.date}
                                          </td>
                                          <td className="p-4 text-right">
                                              <span className="font-black text-indigo-600 text-lg">{s.score}</span>
                                              <span className="text-gray-400 text-xs font-bold ml-1">/ {s.max_score}</span>
                                          </td>
                                      </tr>
                                  ))
                              )}
                          </tbody>
                      </table>
                  </div>
              )}
          </div>
      </div>
    </div>
  );
}
