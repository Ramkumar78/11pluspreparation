import { describe, it, expect } from 'vitest';
import { MOCK_TYPES, MODES, TIMING } from '../constants';

describe('Constants', () => {
  describe('MOCK_TYPES', () => {
    it('should have the correct keys', () => {
      expect(Object.keys(MOCK_TYPES)).toEqual(['MATH', 'ENGLISH', 'MIXED', 'SET_SIMULATION']);
    });

    it('should have the correct values', () => {
      expect(MOCK_TYPES.MATH).toBe('math');
      expect(MOCK_TYPES.ENGLISH).toBe('english');
      expect(MOCK_TYPES.MIXED).toBe('mixed');
      expect(MOCK_TYPES.SET_SIMULATION).toBe('set_simulation');
    });
  });

  describe('MODES', () => {
    it('should have the correct keys', () => {
      expect(Object.keys(MODES)).toEqual(['VOCAB', 'MATH', 'COMPREHENSION', 'REPAIR']);
    });

    it('should have the correct values', () => {
      expect(MODES.VOCAB).toBe('vocab');
      expect(MODES.MATH).toBe('math');
      expect(MODES.COMPREHENSION).toBe('comprehension');
      expect(MODES.REPAIR).toBe('repair');
    });
  });

  describe('TIMING', () => {
    it('should have the correct structure', () => {
      expect(TIMING).toHaveProperty('GAME_DURATION');
      expect(TIMING).toHaveProperty('TIMER_INTERVAL');
      expect(TIMING).toHaveProperty('BADGE_DISPLAY');
      expect(TIMING).toHaveProperty('INPUT_FOCUS_DELAY');
      expect(TIMING).toHaveProperty('FEEDBACK_DELAY');
    });

    it('should have the correct default values for durations', () => {
      expect(TIMING.GAME_DURATION.DEFAULT).toBe(60);
      expect(TIMING.TIMER_INTERVAL).toBe(1000);
      expect(TIMING.BADGE_DISPLAY).toBe(5000);
    });
  });
});
