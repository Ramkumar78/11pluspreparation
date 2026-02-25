import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import Home from '../Home';
import { MODES, MOCK_TYPES } from '../constants';

describe('Home Component Navigation', () => {

  it('navigates to vocab game when PLAY VOCAB is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/game/${MODES.VOCAB}`} element={<div data-testid="vocab-game">Vocab Game</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('PLAY VOCAB'));
    expect(screen.getByTestId('vocab-game')).toBeInTheDocument();
  });

  it('navigates to math game when PLAY MATHS is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/game/${MODES.MATH}`} element={<div data-testid="math-game">Math Game</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('PLAY MATHS'));
    expect(screen.getByTestId('math-game')).toBeInTheDocument();
  });

  it('navigates to comprehension game when PLAY COMP is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/game/${MODES.COMPREHENSION}`} element={<div data-testid="comp-game">Comp Game</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('PLAY COMP'));
    expect(screen.getByTestId('comp-game')).toBeInTheDocument();
  });

  it('navigates to maths mock when MATHS MOCK is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/mock/${MOCK_TYPES.MATH}`} element={<div data-testid="math-mock">Math Mock</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('MATHS MOCK'));
    expect(screen.getByTestId('math-mock')).toBeInTheDocument();
  });

  it('navigates to english mock when ENGLISH MOCK is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/mock/${MOCK_TYPES.ENGLISH}`} element={<div data-testid="english-mock">English Mock</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('ENGLISH MOCK'));
    expect(screen.getByTestId('english-mock')).toBeInTheDocument();
  });

  it('navigates to set simulation when SET SIMULATION (45 MINS) is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path={`/mock/${MOCK_TYPES.SET_SIMULATION}`} element={<div data-testid="set-sim">Set Sim</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('SET SIMULATION (45 MINS)'));
    expect(screen.getByTestId('set-sim')).toBeInTheDocument();
  });

  it('navigates to dashboard when MY DASHBOARD is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<div data-testid="dashboard">Dashboard</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('MY DASHBOARD'));
    expect(screen.getByTestId('dashboard')).toBeInTheDocument();
  });

  it('navigates to leaderboard when LEADERBOARD is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/leaderboard" element={<div data-testid="leaderboard">Leaderboard</div>} />
        </Routes>
      </MemoryRouter>
    );
    fireEvent.click(screen.getByText('LEADERBOARD'));
    expect(screen.getByTestId('leaderboard')).toBeInTheDocument();
  });
});
