import { loadFeature, defineFeature } from 'jest-cucumber';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import Game from '../Game';

// Mock axios
vi.mock('axios');

// Mock Confetti
vi.mock('canvas-confetti', () => ({
    default: vi.fn()
}));

// Mock SpeechSynthesis
const mockSpeak = vi.fn();
Object.defineProperty(window, 'speechSynthesis', {
    value: {
        speak: mockSpeak,
    },
});
global.SpeechSynthesisUtterance = vi.fn();

const feature = loadFeature('/app/features/GameUI.feature', {
    loadRelativePath: false
});

defineFeature(feature, test => {
    const mockWord = {
        id: 1,
        definition: 'A large cat',
        image: '/images/lion.jpg',
        length: 4,
        user_level: 3,
        score: 0,
        streak: 0,
        tts_text: 'lion'
    };

    beforeEach(() => {
        vi.resetAllMocks();
        axios.get.mockResolvedValue({ data: mockWord });
        axios.post.mockResolvedValue({ data: { correct: true, correct_word: 'lion' } });
        // Use real timers
        vi.useRealTimers();
    });

    // Helper sleep
    const sleep = (ms) => new Promise(r => setTimeout(r, ms));

    test('Typing in the Custom Input', ({ given, when, then }) => {
        given(/^the game is loaded with the word "(.*)"$/, async (word) => {
            render(<Game onBack={() => { }} userId={1} />);
            await waitFor(() => expect(screen.getByText('"A large cat"')).toBeInTheDocument());
        });

        when('I wait for the reading phase to complete', async () => {
            await act(async () => {
                await sleep(3100);
            });
        });

        when(/^I type "(.*)" into the input box$/, async (text) => {
            const inputDiv = screen.getByText('TYPE HERE').closest('div');
            for (let char of text) {
                fireEvent.keyDown(inputDiv, { key: char });
            }
        });

        then(/^the input box should display "(.*)"$/, async (expectedText) => {
            await waitFor(() => {
                for (let char of expectedText) {
                    expect(screen.getByText(char)).toBeInTheDocument();
                }
            });
        });
    });

    test('Submitting a Correct Answer', ({ given, when, then }) => {
        given(/^the game is loaded with the word "(.*)"$/, async (word) => {
            render(<Game onBack={() => { }} userId={1} />);
            await waitFor(() => expect(screen.getByText('"A large cat"')).toBeInTheDocument());
        });

        when('I wait for the reading phase to complete', async () => {
            await act(async () => {
                await sleep(3100);
            });
        });

        when(/^I type "(.*)" into the input box$/, async (text) => {
            const inputDiv = screen.getByText('TYPE HERE').closest('div');
            for (let char of text) {
                fireEvent.keyDown(inputDiv, { key: char });
            }
        });

        when('I click the "GO!" button', async () => {
            await waitFor(() => expect(screen.getByText('L')).toBeInTheDocument());
            const goBtn = screen.getByText('GO!');
            fireEvent.click(goBtn);
        });

        then('the answer should be submitted to the backend', async () => {
            await waitFor(() => {
                expect(axios.post).toHaveBeenCalled();
            });
        });
    });
});
