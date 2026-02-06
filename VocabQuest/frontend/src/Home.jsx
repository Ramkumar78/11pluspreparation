import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Play, Star, ShieldCheck, Zap, BookOpen, Clock, LayoutDashboard, Trophy } from 'lucide-react';
import { MODES, MOCK_TYPES } from './constants';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center text-white p-4">

      <div className="max-w-5xl w-full bg-white/10 backdrop-blur-md rounded-3xl p-8 border-4 border-white/20 shadow-2xl flex flex-col items-center text-center animate-fade-in-up">

        <div className="mb-6 animate-bounce">
            <span className="text-8xl">🦁</span>
        </div>

        <h1 className="text-6xl font-extrabold mb-4 drop-shadow-lg tracking-tight">
          Scholar<span className="text-yellow-300">Quest</span>
        </h1>

        <p className="text-xl mb-8 font-medium text-indigo-100 max-w-xl">
          The ultimate 11+ prep adventure! Master Vocabulary, Mathematics and Comprehension to become a true scholar.
          <br/>
          <span className="text-yellow-300 text-sm mt-2 block">
            Focused on Wilson's, Wallington, Sutton, and Nonsuch (SET & Stage 2)
          </span>
        </p>

        <div className="flex flex-col md:flex-row gap-4 flex-wrap justify-center mb-6">
          <button
            onClick={() => navigate(`/game/${MODES.VOCAB}`)}
            className="group relative inline-flex items-center gap-3 bg-indigo-600 hover:bg-indigo-500 text-white font-black text-xl py-6 px-8 rounded-full shadow-[0_10px_0_rgb(55,48,163)] hover:shadow-[0_6px_0_rgb(55,48,163)] hover:translate-y-1 transition-all"
          >
            <Play className="w-8 h-8 fill-current text-yellow-300" />
            PLAY VOCAB
          </button>

          <button
            onClick={() => navigate(`/game/${MODES.MATH}`)}
            className="group relative inline-flex items-center gap-3 bg-orange-500 hover:bg-orange-400 text-white font-black text-xl py-6 px-8 rounded-full shadow-[0_10px_0_rgb(194,65,12)] hover:shadow-[0_6px_0_rgb(194,65,12)] hover:translate-y-1 transition-all"
          >
            <Play className="w-8 h-8 fill-current text-yellow-300" />
            PLAY MATHS
          </button>

          <button
            onClick={() => navigate(`/game/${MODES.COMPREHENSION}`)}
            className="group relative inline-flex items-center gap-3 bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xl py-6 px-8 rounded-full shadow-[0_10px_0_rgb(5,150,105)] hover:shadow-[0_6px_0_rgb(5,150,105)] hover:translate-y-1 transition-all"
          >
            <BookOpen className="w-8 h-8 text-yellow-300" />
            PLAY COMP
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl mb-8">
            <button onClick={() => navigate(`/mock/${MOCK_TYPES.MATH}`)} className="bg-indigo-800/50 hover:bg-indigo-800/70 border-2 border-indigo-400 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition text-lg">
                <Clock className="text-orange-300" /> MATHS MOCK
            </button>
            <button onClick={() => navigate(`/mock/${MOCK_TYPES.ENGLISH}`)} className="bg-indigo-800/50 hover:bg-indigo-800/70 border-2 border-indigo-400 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition text-lg">
                <Clock className="text-emerald-300" /> ENGLISH MOCK
            </button>
        </div>
        <div className="w-full max-w-2xl mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <button onClick={() => navigate('/dashboard')} className="bg-indigo-800/50 hover:bg-indigo-800/70 border-2 border-indigo-400 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition text-lg">
                <LayoutDashboard className="text-yellow-300" /> MY DASHBOARD
            </button>
             <button onClick={() => navigate('/leaderboard')} className="bg-indigo-800/50 hover:bg-indigo-800/70 border-2 border-indigo-400 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition text-lg">
                <Trophy className="text-yellow-300" /> LEADERBOARD
            </button>
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
            <FeatureCard icon={<Zap className="w-8 h-8 text-yellow-400" />} title="Power Up!" desc="Build your streak to unlock higher levels." />
            <FeatureCard icon={<Star className="w-8 h-8 text-yellow-400" />} title="Earn Rewards" desc="Get points for every correct answer." />
            <FeatureCard icon={<ShieldCheck className="w-8 h-8 text-yellow-400" />} title="Safe & Fun" desc="A secure place to learn and grow." />
        </div>

      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
    return (
        <div className="bg-black/20 p-4 rounded-xl flex flex-col items-center">
            <div className="mb-2">{icon}</div>
            <h3 className="font-bold text-lg">{title}</h3>
            <p className="text-sm text-indigo-100">{desc}</p>
        </div>
    )
}
