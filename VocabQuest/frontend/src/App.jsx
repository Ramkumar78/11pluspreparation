import React, { useState } from 'react';
import Game from './Game';
import Home from './Home';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'game'
  const [mode, setMode] = useState('vocab'); // 'vocab' | 'math'

  const handleStart = (selectedMode) => {
    setMode(selectedMode);
    setView('game');
  };

  return (
    <>
      {view === 'home' && <Home onStart={handleStart} />}
      {view === 'game' && <Game mode={mode} onBack={() => setView('home')} />}
    </>
  );
}

export default App;
