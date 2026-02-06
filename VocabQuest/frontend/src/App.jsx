import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Game from './Game';
import Home from './Home';
import Dashboard from './Dashboard';
import MockTest from './MockTest';
import Leaderboard from './Leaderboard';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/game/:mode" element={<Game />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/mock/:type" element={<MockTest />} />
      <Route path="/leaderboard" element={<Leaderboard />} />
    </Routes>
  );
}

export default App;
