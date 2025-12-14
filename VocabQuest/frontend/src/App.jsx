import React, { useState } from 'react';
import Game from './Game';
import Home from './Home';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'game'

  return (
    <>
      {view === 'home' && <Home onStart={() => setView('game')} />}
      {view === 'game' && <Game onBack={() => setView('home')} />}
    </>
  );
}

export default App;
