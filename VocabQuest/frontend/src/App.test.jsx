import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';

// Mock child components
vi.mock('./Home', () => ({
  default: () => <div data-testid="home-screen">Home</div>
}));
vi.mock('./Game', () => ({
  default: () => <div data-testid="game-screen">Game</div>
}));
vi.mock('./Dashboard', () => ({
  default: () => <div data-testid="dashboard-screen">Dashboard</div>
}));
vi.mock('./MockTest', () => ({
  default: () => <div data-testid="mock-screen">Mock</div>
}));

describe('App Routing', () => {
  it('renders Home on root route', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('home-screen')).toBeInTheDocument();
  });

  it('renders Game on /game/vocab', () => {
    render(
      <MemoryRouter initialEntries={['/game/vocab']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('game-screen')).toBeInTheDocument();
  });

  it('renders Dashboard on /dashboard', () => {
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('dashboard-screen')).toBeInTheDocument();
  });

  it('renders MockTest on /mock/math', () => {
    render(
      <MemoryRouter initialEntries={['/mock/math']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('mock-screen')).toBeInTheDocument();
  });
});
