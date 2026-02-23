import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Dashboard from '../Dashboard';
import axios from 'axios';

// Mock axios
vi.mock('axios');

// Mock react-router-dom
const navigateMock = vi.fn();
vi.mock('react-router-dom', () => ({
  useNavigate: () => navigateMock
}));

describe('Dashboard Component', () => {
  const mockTopics = [
    {
      topic: 'Arithmetic',
      level: 2,
      mastery: 20,
      correct: 5,
      total: 25
    },
    {
      topic: 'Algebra Topic',
      level: 1,
      mastery: 10,
      correct: 1,
      total: 10
    }
  ];

  const mockUserStats = {
      score: 150,
      streak: 5,
      level: 3,
      badges: ['Novice']
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    axios.get.mockImplementation(() => new Promise(() => {}));
    render(<Dashboard />);
    expect(screen.getByText('Loading Analytics...')).toBeInTheDocument();
  });

  it('renders topics and stats after fetching', async () => {
    axios.get.mockImplementation((url) => {
        if (url.includes('/get_topics')) return Promise.resolve({ data: mockTopics });
        if (url.includes('/get_user_stats')) return Promise.resolve({ data: mockUserStats });
        return Promise.resolve({ data: [] });
    });

    render(<Dashboard />);

    await waitFor(() => {
        expect(screen.getByText('My Learning Journey')).toBeInTheDocument();
    });

    expect(screen.getByText('Arithmetic')).toBeInTheDocument();
    expect(screen.getByText('Level 2')).toBeInTheDocument();
    expect(screen.getByText('20%')).toBeInTheDocument();

    expect(screen.getByText('Algebra Topic')).toBeInTheDocument();
    expect(screen.getByText('Level 1')).toBeInTheDocument();
    expect(screen.getByText('10%')).toBeInTheDocument();

    // Check Stats
    expect(screen.getByText('150')).toBeInTheDocument(); // Score
    expect(screen.getByText('5')).toBeInTheDocument(); // Streak
    expect(screen.getByText('Novice')).toBeInTheDocument(); // Badge
  });

  it('handles empty data', async () => {
    axios.get.mockImplementation((url) => {
        if (url.includes('/get_topics')) return Promise.resolve({ data: [] });
        if (url.includes('/get_user_stats')) return Promise.resolve({ data: { score: 0, streak: 0, badges: [] } });
        return Promise.resolve({ data: [] });
    });

    render(<Dashboard />);

    await waitFor(() => {
        expect(screen.getByText('No topic data available yet. Start practicing!')).toBeInTheDocument();
    });
  });

  it('navigates back when back button clicked', async () => {
    axios.get.mockImplementation((url) => {
        if (url.includes('/get_topics')) return Promise.resolve({ data: [] });
        if (url.includes('/get_user_stats')) return Promise.resolve({ data: { score: 0, streak: 0, badges: [] } });
        return Promise.resolve({ data: [] });
    });

    render(<Dashboard />);

    await waitFor(() => {
        expect(screen.getByText('Back to Home')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Back to Home'));
    expect(navigateMock).toHaveBeenCalledWith('/');
  });
});
