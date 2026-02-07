import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import VocabGame from './VocabGame';

/**
 * VocabGame is a presentational component that receives its state and handlers via props.
 * API calls (Axios) and business logic (Score, TTS on load) are handled by the parent Game component.
 * Therefore, this unit test mocks the props to simulate the game state and interaction outcomes,
 * rather than mocking Axios directly.
 */
describe('VocabGame Component', () => {
  const mockGameState = {
    id: 1,
    word: 'TEST',
    definition: 'A trial run',
    image: '/images/test.jpg',
    length: 4,
    scramble: 'TSET',
    score: 10,
    streak: 2,
    user_level: 5,
    tts_text: 'Test',
  };

  const defaultProps = {
    gameState: mockGameState,
    input: '',
    setInput: vi.fn(),
    status: 'playing',
    canType: true,
    inputRef: { current: null },
    handleSubmit: vi.fn(e => e.preventDefault()),
    handleSpeakClick: vi.fn(),
    feedback: ''
  };

  it('renders correctly with image and definition', () => {
    render(<VocabGame {...defaultProps} />);
    expect(screen.getByText('"A trial run"')).toBeInTheDocument();
    expect(screen.getByAltText('Clue')).toHaveAttribute('src', '/images/test.jpg');
    expect(screen.getByPlaceholderText('TYPE HERE')).toBeInTheDocument();
  });

  it('handles input changes', () => {
    render(<VocabGame {...defaultProps} />);
    const input = screen.getByPlaceholderText('TYPE HERE');
    fireEvent.change(input, { target: { value: 'TEST' } });
    expect(defaultProps.setInput).toHaveBeenCalledWith('TEST');
  });

  it('handles submission', () => {
    render(<VocabGame {...defaultProps} input="TEST" />);
    const submitBtn = screen.getByText('GO!');
    fireEvent.click(submitBtn);
    expect(defaultProps.handleSubmit).toHaveBeenCalled();
  });

  it('displays feedback when provided (simulating correct answer)', () => {
    // Simulate parent component passing "Correct!" feedback
    const { rerender } = render(<VocabGame {...defaultProps} />);
    expect(screen.queryByText('Correct!')).not.toBeInTheDocument();

    const updatedProps = {
        ...defaultProps,
        feedback: 'Correct!'
    };
    rerender(<VocabGame {...updatedProps} />);

    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });

  it('triggers TTS handler when requested', () => {
    render(<VocabGame {...defaultProps} />);
    const speakBtn = screen.getByText('Hear Word').closest('button');
    fireEvent.click(speakBtn);
    expect(defaultProps.handleSpeakClick).toHaveBeenCalled();
  });

  it('displays error warning in feedback area', () => {
    // Simulate parent passing an error message
    render(<VocabGame {...defaultProps} feedback="Rate Limit Exceeded" />);
    expect(screen.getByText('Rate Limit Exceeded')).toBeInTheDocument();
  });
});
