import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import Game from '../Game';

// Mock axios
vi.mock('axios');

// Mock window.speechSynthesis
const mockSpeak = vi.fn();
const mockCancel = vi.fn();
const mockUtterance = vi.fn();

// Add mocks to global window object
Object.defineProperty(window, 'speechSynthesis', {
  value: {
    speak: mockSpeak,
    cancel: mockCancel,
  },
  writable: true,
});

window.SpeechSynthesisUtterance = mockUtterance;

describe('Game Audio Logic', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Default mock response for a vocab game
    axios.get.mockResolvedValue({
      data: {
        id: 1,
        word: 'TEST',
        definition: 'A test word',
        image: 'test.jpg',
        length: 4,
        tts_text: 'Test Word',
        type: 'vocab',
        scramble: 'ETST'
      }
    });
  });

  it('cancels previous speech before speaking new word', async () => {
    // Render the Game component
    render(
      <MemoryRouter initialEntries={['/game/vocab']}>
        <Routes>
          <Route path="/game/:mode" element={<Game />} />
        </Routes>
      </MemoryRouter>
    );

    // Wait for the initial speak call
    await waitFor(() => {
      expect(mockSpeak).toHaveBeenCalled();
    });

    // Check if cancel was called. Ideally, it should be called before every speak.
    // Even on the first call, calling cancel is safe and good practice to clear any lingering audio.
    expect(mockCancel).toHaveBeenCalled();

    // Check call order: cancel should be called before speak
    const cancelCallOrder = mockCancel.mock.invocationCallOrder[0];
    const speakCallOrder = mockSpeak.mock.invocationCallOrder[0];

    expect(cancelCallOrder).toBeLessThan(speakCallOrder);
  });
});
