import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import StreakVisualizer from './StreakVisualizer';
import { vi } from 'vitest';

describe('StreakVisualizer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    // Mock AudioContext
    window.AudioContext = vi.fn().mockImplementation(() => ({
      createOscillator: () => ({
        connect: vi.fn(),
        start: vi.fn(),
        stop: vi.fn(),
        frequency: { setValueAtTime: vi.fn() },
        type: 'sine'
      }),
      createGain: () => ({
        connect: vi.fn(),
        gain: { setValueAtTime: vi.fn(), exponentialRampToValueAtTime: vi.fn() }
      }),
      close: vi.fn().mockResolvedValue(),
      currentTime: 0,
      destination: {}
    }));
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.clearAllMocks();
  });

  test('renders streak count', () => {
    render(<StreakVisualizer streak={5} onClose={() => {}} />);
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('STREAK ON FIRE!')).toBeInTheDocument();
  });

  test('closes automatically after timeout', () => {
    const handleClose = vi.fn();
    render(<StreakVisualizer streak={5} onClose={handleClose} />);

    act(() => {
      vi.advanceTimersByTime(3000);
    });

    expect(handleClose).toHaveBeenCalled();
  });

  test('handles AudioContext errors gracefully', () => {
    // Mock AudioContext to throw error
    window.AudioContext.mockImplementation(() => {
      throw new Error('AudioContext failed');
    });

    const handleClose = vi.fn();

    // Should not throw
    expect(() => {
      render(<StreakVisualizer streak={5} onClose={handleClose} />);
    }).not.toThrow();

    // Timer should still work
    act(() => {
      vi.advanceTimersByTime(3000);
    });
    expect(handleClose).toHaveBeenCalled();
  });

  test('can be closed manually via close button', () => {
    const handleClose = vi.fn();
    render(<StreakVisualizer streak={5} onClose={handleClose} />);

    const closeButton = screen.getByRole('button', { name: /close/i });
    fireEvent.click(closeButton);

    expect(handleClose).toHaveBeenCalled();
  });
});
