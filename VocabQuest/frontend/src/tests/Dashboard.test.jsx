import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Dashboard from '../Dashboard';
import axios from 'axios';

// Mock axios
vi.mock('axios');

// Mock lucide-react (optional if you don't need to test icons specifically, but good practice if they crash)
// Since we are using shallow render or standard render, lucide icons usually render fine as SVGs.
// If not, we can mock them.

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
      topic: 'Algebra',
      level: 1,
      mastery: 10,
      correct: 1,
      total: 10
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    axios.get.mockImplementation(() => new Promise(() => {}));
    render(<Dashboard onBack={() => {}} />);
    expect(screen.getByText('Loading Analytics...')).toBeInTheDocument();
  });

  it('renders topics after fetching', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTopics });
    render(<Dashboard onBack={() => {}} />);

    await waitFor(() => {
        expect(screen.getByText('My Learning Journey')).toBeInTheDocument();
    });

    expect(screen.getByText('Arithmetic')).toBeInTheDocument();
    expect(screen.getByText('Level 2')).toBeInTheDocument();
    expect(screen.getByText('20%')).toBeInTheDocument();

    expect(screen.getByText('Algebra')).toBeInTheDocument();
    expect(screen.getByText('Level 1')).toBeInTheDocument();
    expect(screen.getByText('10%')).toBeInTheDocument();
  });

  it('handles empty data', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });
    render(<Dashboard onBack={() => {}} />);

    await waitFor(() => {
        expect(screen.getByText('No topic data available yet. Start practicing!')).toBeInTheDocument();
    });
  });

  it('calls onBack when back button clicked', async () => {
    axios.get.mockResolvedValueOnce({ data: [] });
    const onBackMock = vi.fn();
    render(<Dashboard onBack={onBackMock} />);

    await waitFor(() => {
        expect(screen.getByText('Back to Home')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Back to Home'));
    expect(onBackMock).toHaveBeenCalled();
  });
});
