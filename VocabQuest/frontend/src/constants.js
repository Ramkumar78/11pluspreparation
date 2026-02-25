export const MODES = {
  VOCAB: 'vocab',
  MATH: 'math',
  COMPREHENSION: 'comprehension',
  REPAIR: 'repair',
};

export const MOCK_TYPES = {
  MATH: 'math',
  ENGLISH: 'english',
  MIXED: 'mixed',
  SET_SIMULATION: 'set_simulation',
};

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export const TIMING = {
  GAME_DURATION: {
    DEFAULT: 60,
    BLITZ: 60
  },
  TIMER_INTERVAL: 1000,
  BADGE_DISPLAY: 5000,
  INPUT_FOCUS_DELAY: {
    BLITZ: 100,
    MATH: 500,
    COMPREHENSION: 1000,
    DEFAULT: 3000
  },
  FEEDBACK_DELAY: {
    DEFAULT_ERROR: 2000,
    MATH: {
      TIMEOUT: 5000,
      CORRECT: 1500,
      WRONG: 8000
    },
    VOCAB: {
      TIMEOUT: 3500,
      CORRECT: 2000,
      WRONG: 3500
    },
    COMPREHENSION: {
      TIMEOUT: 5000,
      CORRECT: 2000,
      WRONG: 8000
    },
    BLITZ: {
      CORRECT: 500,
      WRONG: 1000
    }
  }
};
