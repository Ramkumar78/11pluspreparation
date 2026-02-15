import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Game from './Game';
import Home from './Home';
import Dashboard from './Dashboard';
import MockTest from './MockTest';
import Leaderboard from './Leaderboard';

function FocusHeader({ focusMode, setFocusMode, seconds }) {
  const formatTime = (totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className={`w-full px-6 py-3 flex justify-between items-center z-50 shadow-sm border-b transition-colors duration-300 ${focusMode ? 'bg-gray-100 border-gray-300' : 'bg-white border-gray-200'}`}>
      <div className="font-bold text-indigo-900 text-xl flex items-center gap-2">
        <span className={focusMode ? 'text-gray-800' : 'text-indigo-600'}>VocabQuest</span>
      </div>
      <div className="flex items-center gap-6">
        <label className="flex items-center cursor-pointer gap-2 select-none">
          <div className="relative">
            <input
              type="checkbox"
              className="sr-only"
              checked={focusMode}
              onChange={() => setFocusMode(!focusMode)}
            />
            <div className={`block w-12 h-7 rounded-full transition-colors duration-300 ${focusMode ? 'bg-indigo-600' : 'bg-gray-300'}`}></div>
            <div className={`dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition-transform duration-300 ${focusMode ? 'transform translate-x-5' : ''}`}></div>
          </div>
          <span className={`font-semibold text-sm ${focusMode ? 'text-gray-800' : 'text-gray-500'}`}>Focus Mode</span>
        </label>

        <div className={`font-mono text-lg font-bold px-3 py-1 rounded-md border flex items-center gap-2 ${focusMode ? 'bg-white text-gray-800 border-gray-300' : 'bg-gray-50 text-gray-600 border-gray-200'}`}>
          <span>⏱</span>
          {formatTime(seconds)}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [focusMode, setFocusMode] = useState(false);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`min-h-screen flex flex-col ${focusMode ? 'focus-mode-active' : ''}`}>
      <FocusHeader focusMode={focusMode} setFocusMode={setFocusMode} seconds={seconds} />
      <div className="flex-grow relative">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/game/:mode" element={<Game />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/mock/:type" element={<MockTest />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
