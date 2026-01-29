import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';
import Home from './Home';

// Mock Home component to isolate tests
vi.mock('./Home', () => ({
  default: ({ onStart }) => (
    <div data-testid="home-screen">
      <h1>VocabQuest</h1>
      <button onClick={() => onStart('vocab')}>Start Game</button>
    </div>
  ),
}));

// Mock Game component
vi.mock('./Game', () => ({
  default: ({ onBack }) => (
    <div data-testid="game-screen">
      <h1>Game Screen</h1>
      <button onClick={onBack}>Back</button>
    </div>
  ),
}));

describe('App Navigation', () => {
  it('renders Home screen initially', () => {
    render(<App />);
    expect(screen.getByTestId('home-screen')).toBeInTheDocument();
  });

  it('switches to Game screen when Start is clicked', () => {
    render(<App />);
    fireEvent.click(screen.getByText('Start Game'));
    expect(screen.getByTestId('game-screen')).toBeInTheDocument();
  });

  it('switches back to Home screen when Back is clicked', () => {
    render(<App />);
    fireEvent.click(screen.getByText('Start Game')); // Go to game
    fireEvent.click(screen.getByText('Back')); // Go back
    expect(screen.getByTestId('home-screen')).toBeInTheDocument();
  });
});
