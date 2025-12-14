import React from 'react';
import { Play, Star, ShieldCheck, Zap } from 'lucide-react';

export default function Home({ onStart }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex flex-col items-center justify-center text-white p-4">

      <div className="max-w-4xl w-full bg-white/10 backdrop-blur-md rounded-3xl p-8 border-4 border-white/20 shadow-2xl flex flex-col items-center text-center animate-fade-in-up">

        <div className="mb-6 animate-bounce">
            <span className="text-8xl">🦁</span>
        </div>

        <h1 className="text-6xl font-extrabold mb-4 drop-shadow-lg tracking-tight">
          Vocab<span className="text-yellow-300">Quest</span>
        </h1>

        <p className="text-xl mb-8 font-medium text-indigo-100 max-w-xl">
          Embark on an epic journey to master words! Solve puzzles, earn points, and become a vocabulary legend.
        </p>

        <button
          onClick={onStart}
          className="group relative inline-flex items-center gap-3 bg-yellow-400 hover:bg-yellow-300 text-indigo-900 font-black text-3xl py-6 px-16 rounded-full shadow-[0_10px_0_rgb(180,83,9)] hover:shadow-[0_6px_0_rgb(180,83,9)] hover:translate-y-1 transition-all"
        >
          <Play className="w-8 h-8 fill-current" />
          PLAY NOW
        </button>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
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
