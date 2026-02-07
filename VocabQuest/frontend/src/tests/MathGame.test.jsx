import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MathGame from '../components/MathGame';

describe('MathGame Component', () => {
  const mockGameState = {
    question: 'Calculate 5 + 5',
    id: 1,
  };

  const defaultProps = {
    gameState: mockGameState,
    input: '',
    setInput: vi.fn(),
    status: 'playing',
    canType: true,
    inputRef: { current: null },
    handleSubmit: vi.fn(e => e.preventDefault()),
    feedback: null,
    topic: '',
    onTopicChange: vi.fn(),
  };

  it('renders question and topic selector', () => {
    render(<MathGame {...defaultProps} />);
    expect(screen.getByText('Calculate 5 + 5')).toBeInTheDocument();
    expect(screen.getByRole('combobox')).toBeInTheDocument();
    // Verify default option is selected
    expect(screen.getByRole('combobox').value).toBe('');
  });

  it('handles topic switching', () => {
    const onTopicChange = vi.fn();
    render(<MathGame {...defaultProps} onTopicChange={onTopicChange} />);

    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'Algebra' } });

    expect(onTopicChange).toHaveBeenCalledWith('Algebra');
  });

  it('handles input changes', () => {
    const setInput = vi.fn();
    render(<MathGame {...defaultProps} setInput={setInput} />);

    const input = screen.getByPlaceholderText('ENTER NUMBER');
    fireEvent.change(input, { target: { value: '10' } });

    expect(setInput).toHaveBeenCalledWith('10');
  });

  it('displays feedback when provided', () => {
    const feedback = <div>Correct!</div>;
    render(<MathGame {...defaultProps} feedback={feedback} />);

    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });

  it('disables input and selector when status is not playing (Time Up logic)', () => {
    render(<MathGame {...defaultProps} status="wrong" canType={false} />);

    // Check if input is disabled
    const input = screen.getByRole('spinbutton'); // input type="number"
    expect(input).toBeDisabled();

    // Check if topic selector is disabled
    const select = screen.getByRole('combobox');
    expect(select).toBeDisabled();
  });

  it('calls handleSubmit on form submission', () => {
      const handleSubmit = vi.fn(e => e.preventDefault());
      render(<MathGame {...defaultProps} handleSubmit={handleSubmit} input="10" />);

      const button = screen.getByText('GO!');
      fireEvent.click(button);

      expect(handleSubmit).toHaveBeenCalled();
  });
});
