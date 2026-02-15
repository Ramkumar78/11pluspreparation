import React, { useEffect } from 'react';
import { Sparkles, Trophy } from 'lucide-react';

export default function StreakVisualizer({ streak, onClose }) {
  useEffect(() => {
    // Play sound on mount
    const playSound = () => {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.connect(gain);
      gain.connect(ctx.destination);

      // Play a cheerful "Level Up" sound
      const now = ctx.currentTime;
      osc.type = 'triangle';

      // Arpeggio C-E-G-C
      osc.frequency.setValueAtTime(523.25, now); // C5
      osc.frequency.setValueAtTime(659.25, now + 0.1); // E5
      osc.frequency.setValueAtTime(783.99, now + 0.2); // G5
      osc.frequency.setValueAtTime(1046.50, now + 0.3); // C6

      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);

      osc.start(now);
      osc.stop(now + 0.8);
    };

    playSound();

    // Auto close after 3 seconds
    const timer = setTimeout(() => {
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-black/40 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="relative bg-gradient-to-br from-yellow-300 to-orange-400 p-8 rounded-3xl shadow-2xl flex flex-col items-center text-center transform scale-110 border-4 border-white animate-bounce">
        <div className="absolute -top-12 animate-pulse">
            <Sparkles size={64} className="text-yellow-100 drop-shadow-lg" />
        </div>

        <h2 className="text-4xl font-black text-white drop-shadow-md mt-4 mb-2">
            STREAK ON FIRE!
        </h2>

        <div className="bg-white/20 p-4 rounded-full mb-4">
             <Trophy size={80} className="text-white drop-shadow-sm" strokeWidth={2.5} />
        </div>

        <div className="text-6xl font-black text-white drop-shadow-lg mb-2">
            {streak}
        </div>

        <div className="text-xl font-bold text-white/90 uppercase tracking-widest">
            Correct Answers in a Row!
        </div>
      </div>
    </div>
  );
}
