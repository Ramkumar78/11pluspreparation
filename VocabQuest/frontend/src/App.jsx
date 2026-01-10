import React, { useState } from 'react';
import Game from './Game';
import Home from './Home';
import Dashboard from './Dashboard';
import MockTest from './MockTest';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'game' | 'dashboard' | 'mock'
  const [mode, setMode] = useState('vocab'); // 'vocab' | 'math' | 'comprehension' | 'mock_math' | 'mock_english'

  const handleStart = (selectedMode) => {
    setMode(selectedMode);
    if (selectedMode.startsWith('mock_')) {
        setView('mock');
    } else {
        setView('game');
    }
  };

  return (
    <>
      {view === 'home' && <Home onStart={handleStart} onViewChange={setView} />}
      {view === 'game' && <Game mode={mode} onBack={() => setView('home')} />}
      {view === 'dashboard' && <Dashboard onBack={() => setView('home')} />}
      {view === 'mock' && <MockTest type={mode === 'mock_math' ? 'math' : 'english'} onBack={() => setView('home')} />}
    </>
  );
}

export default App;
