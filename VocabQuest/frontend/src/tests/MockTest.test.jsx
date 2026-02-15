import { render, screen, fireEvent, waitFor } from '@testing-library/react';
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

describe('MockTest Component', () => {
  const mockTest = {
    test_id: 'mock-1234',
    duration_minutes: 20,
    items: [
      {
        id: 1,
        type: 'math',
        question: '2 + 2',
        topic: 'Math',
        difficulty: 1
      },
      {
        id: 2,
        type: 'vocab',
        question: 'Definition of test',
        image: '/images/test.jpg',
        length: 4,
        difficulty: 1
      }
    ]
  };

  const mockResult = {
    total_score: 20,
    max_score: 20,
    percentage: 100,
    breakdown: [
      {
        id: 1,
        type: 'math',
        correct: true,
        your_answer: '4',
        correct_answer: '4',
        explanation: ''
      },
      {
        id: 2,
        type: 'vocab',
        correct: true,
        your_answer: 'test',
        correct_answer: 'test',
        explanation: ''
      }
    ]
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    // Setup axios to return promise that doesn't resolve immediately
    axios.get.mockImplementation(() => new Promise(() => {}));
    render(<MockTest />);
    expect(screen.getByText('Generating Mock Exam...')).toBeInTheDocument();
  });

  it('renders test items after loading', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    render(<MockTest />);

    await waitFor(() => {
        expect(screen.getByText(/QUESTION 1 \/ 2/)).toBeInTheDocument();
    });

    expect(screen.getByText('2 + 2')).toBeInTheDocument();
    expect(screen.getByText('MATHEMATICS')).toBeInTheDocument();
  });

  it('allows navigation and submission', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    axios.post.mockResolvedValueOnce({ data: mockResult });

    render(<MockTest />);

    // Wait for load
    await waitFor(() => {
        expect(screen.getByText('2 + 2')).toBeInTheDocument();
    });

    // Answer first question
    const input = screen.getByPlaceholderText('Type answer...');
    fireEvent.change(input, { target: { value: '4' } });

    // Click next
    const nextBtn = screen.getByText('Next Question');
    fireEvent.click(nextBtn);

    // Should be on question 2
    expect(screen.getByText(/QUESTION 2 \/ 2/)).toBeInTheDocument();
    expect(screen.getByText('Definition of test')).toBeInTheDocument();
    expect(screen.getByText('VOCABULARY')).toBeInTheDocument();

    // Answer second question
    const input2 = screen.getByPlaceholderText('Type answer...');
    fireEvent.change(input2, { target: { value: 'test' } });

    // Submit
    const finishBtn = screen.getByText('Finish Test');
    fireEvent.click(finishBtn);

    // Expect submit call
    expect(axios.post).toHaveBeenCalledWith(expect.stringContaining('/submit_mock'), expect.objectContaining({
        answers: expect.arrayContaining([
            expect.objectContaining({ id: 1, user_answer: '4' }),
            expect.objectContaining({ id: 2, user_answer: 'test' })
        ])
    }));

    // Wait for results
    await waitFor(() => {
        expect(screen.getByText('Test Complete!')).toBeInTheDocument();
    });

    expect(screen.getByText('100%')).toBeInTheDocument();
  });

  it('includes timing data in submission', async () => {
    axios.get.mockResolvedValueOnce({ data: mockTest });
    axios.post.mockResolvedValueOnce({ data: mockResult });

    render(<MockTest />);

    // Wait for load
    await waitFor(() => {
        expect(screen.getByText('2 + 2')).toBeInTheDocument();
    });

    // Answer first question
    const input = screen.getByPlaceholderText('Type answer...');
    fireEvent.change(input, { target: { value: '4' } });

    // Click next
    const nextBtn = screen.getByText('Next Question');
    fireEvent.click(nextBtn);

    // Answer second question
    const input2 = screen.getByPlaceholderText('Type answer...');
    fireEvent.change(input2, { target: { value: 'test' } });

    // Submit
    const finishBtn = screen.getByText('Finish Test');
    fireEvent.click(finishBtn);

    // Expect submit call with time_taken
    expect(axios.post).toHaveBeenCalledWith(expect.stringContaining('/submit_mock'), expect.objectContaining({
        answers: expect.arrayContaining([
            expect.objectContaining({
                id: 1,
                user_answer: '4',
                time_taken: expect.any(Number)
            }),
            expect.objectContaining({
                id: 2,
                user_answer: 'test',
                time_taken: expect.any(Number)
            })
        ])
    }));
  });
});
