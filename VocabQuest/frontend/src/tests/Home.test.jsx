import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Home from '../Home';
import { MODES, MOCK_TYPES } from '../constants';

// Variables used in vi.mock must start with 'mock'
const mockNavigate = vi.fn();

vi.mock('react-router-dom', async (importActual) => {
  const actual = await importActual();
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('Home Component Navigation', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('navigates to vocab game when PLAY VOCAB is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('PLAY VOCAB'));
    expect(mockNavigate).toHaveBeenCalledWith(`/game/${MODES.VOCAB}`);
  });

  it('navigates to math game when PLAY MATHS is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('PLAY MATHS'));
    expect(mockNavigate).toHaveBeenCalledWith(`/game/${MODES.MATH}`);
  });

  it('navigates to comprehension game when PLAY COMP is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('PLAY COMP'));
    expect(mockNavigate).toHaveBeenCalledWith(`/game/${MODES.COMPREHENSION}`);
  });

  it('navigates to maths mock when MATHS MOCK is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('MATHS MOCK'));
    expect(mockNavigate).toHaveBeenCalledWith(`/mock/${MOCK_TYPES.MATH}`);
  });

  it('navigates to english mock when ENGLISH MOCK is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('ENGLISH MOCK'));
    expect(mockNavigate).toHaveBeenCalledWith(`/mock/${MOCK_TYPES.ENGLISH}`);
  });

  it('navigates to set simulation when SET SIMULATION (45 MINS) is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('SET SIMULATION (45 MINS)'));
    expect(mockNavigate).toHaveBeenCalledWith(`/mock/${MOCK_TYPES.SET_SIMULATION}`);
  });

  it('navigates to dashboard when MY DASHBOARD is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('MY DASHBOARD'));
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });

  it('navigates to leaderboard when LEADERBOARD is clicked', () => {
    render(<Home />);
    fireEvent.click(screen.getByText('LEADERBOARD'));
    expect(mockNavigate).toHaveBeenCalledWith('/leaderboard');
  });
});
