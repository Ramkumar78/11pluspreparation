import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter, Routes, Route, useLocation } from 'react-router-dom';
import Home from '../Home';
import { MODES, MOCK_TYPES } from '../constants';

const LocationDisplay = () => {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
};

describe('Home Component Integration Navigation', () => {
  const renderWithRouter = (ui) => {
    return render(
      <MemoryRouter initialEntries={['/']}>
        <Routes>
          <Route path="/" element={ui} />
          <Route path="*" element={<LocationDisplay />} />
        </Routes>
      </MemoryRouter>
    );
  };

  it('navigates to vocab game when PLAY VOCAB is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('PLAY VOCAB'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/game/${MODES.VOCAB}`);
  });

  it('navigates to math game when PLAY MATHS is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('PLAY MATHS'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/game/${MODES.MATH}`);
  });

  it('navigates to comprehension game when PLAY COMP is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('PLAY COMP'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/game/${MODES.COMPREHENSION}`);
  });

  it('navigates to maths mock when MATHS MOCK is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('MATHS MOCK'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/mock/${MOCK_TYPES.MATH}`);
  });

  it('navigates to english mock when ENGLISH MOCK is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('ENGLISH MOCK'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/mock/${MOCK_TYPES.ENGLISH}`);
  });

  it('navigates to set simulation when SET SIMULATION (45 MINS) is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('SET SIMULATION (45 MINS)'));
    expect(screen.getByTestId('location-display')).toHaveTextContent(`/mock/${MOCK_TYPES.SET_SIMULATION}`);
  });

  it('navigates to dashboard when MY DASHBOARD is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('MY DASHBOARD'));
    expect(screen.getByTestId('location-display')).toHaveTextContent('/dashboard');
  });

  it('navigates to leaderboard when LEADERBOARD is clicked', () => {
    renderWithRouter(<Home />);
    fireEvent.click(screen.getByText('LEADERBOARD'));
    expect(screen.getByTestId('location-display')).toHaveTextContent('/leaderboard');
  });
});
