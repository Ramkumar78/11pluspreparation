import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import MockTest from '../MockTest';
import axios from 'axios';

// Mock axios
vi.mock('axios');

// Mock react-router-dom
const navigateMock = vi.fn();
vi.mock('react-router-dom', () => ({
  useNavigate: () => navigateMock,
  useParams: () => ({ type: 'mixed' })
}));

// Mock canvas-confetti
vi.mock('canvas-confetti', () => ({
  default: vi.fn(),
}));

describe('MockTest Exam Mode', () => {
  const mockTest = {
    test_id: 'mock-exam-1234',
    duration_minutes: 20,
    items: [
      {
        id: 1,
        type: 'math',
        question: 'What is 2 + 2?',
        options: ['3', '4', '5', '6'],
        topic: 'Math',
        difficulty: 1
      },
      {
        id: 2,
        type: 'vocab',
        question: 'Synonym for Happy?',
        options: ['Sad', 'Joyful', 'Angry', 'Bored'],
        length: 6,
        difficulty: 1
      }
    ]
  };

  const mockResult = {
    total_score: 20,
    max_score: 20,
    percentage: 100,
    breakdown: []
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders Bubble Sheet UI in Exam Mode', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });

    // Render with isExamMode={true}
    render(<MockTest isExamMode={true} />);

    await waitFor(() => {
        expect(screen.getByText('What is 2 + 2?')).toBeInTheDocument();
    });

    // Check for Bubble labels A, B, C, D
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('B')).toBeInTheDocument();
    expect(screen.getByText('C')).toBeInTheDocument();
    expect(screen.getByText('D')).toBeInTheDocument();

    // Check that text is also there
    expect(screen.getByText('4')).toBeInTheDocument();
  });

  it('allows flagging a question', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    render(<MockTest isExamMode={true} />);

    await waitFor(() => {
        expect(screen.getByText('Flag for Review')).toBeInTheDocument();
    });

    const flagBtn = screen.getByText('Flag for Review');
    fireEvent.click(flagBtn);

    expect(screen.getByText('Flagged')).toBeInTheDocument();
  });

  it('navigates to previous question', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    render(<MockTest isExamMode={true} />);

    await waitFor(() => {
        expect(screen.getByText('What is 2 + 2?')).toBeInTheDocument();
    });

    // Go Next
    fireEvent.click(screen.getByText('Next Question'));

    await waitFor(() => {
        expect(screen.getByText('Synonym for Happy?')).toBeInTheDocument();
    });

    // Go Previous
    const prevBtn = screen.getByText('Previous');
    fireEvent.click(prevBtn);

    await waitFor(() => {
        expect(screen.getByText('What is 2 + 2?')).toBeInTheDocument();
    });
  });

  it('uses Question Navigator to jump', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    render(<MockTest isExamMode={true} />);

    await waitFor(() => {
        expect(screen.getByText('QUESTION 1 / 2')).toBeInTheDocument();
    });

    // Open Navigator (title="Question Navigator")
    const navBtn = screen.getByTitle('Question Navigator');
    fireEvent.click(navBtn);

    // Should see buttons 1 and 2
    // Note: The navigator renders buttons with text "1", "2".
    // Since "1" might be in the text "QUESTION 1 / 2", we should be specific.
    // The buttons have specific classes.
    // Or we can just look for text "2" which is unique enough here inside the button.
    const btn2 = screen.getByText('2');

    // Click 2
    fireEvent.click(btn2);

    await waitFor(() => {
        expect(screen.getByText('Synonym for Happy?')).toBeInTheDocument();
        expect(screen.getByText('QUESTION 2 / 2')).toBeInTheDocument();
    });
  });

});
