import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, test, expect } from 'vitest';
import SkillMatrix from './SkillMatrix';

describe('SkillMatrix', () => {
  test('renders the component title', () => {
    render(<SkillMatrix />);
    expect(screen.getByText('Skills Mastery Matrix')).toBeInTheDocument();
  });

  test('renders all domain tabs', () => {
    render(<SkillMatrix />);
    // Handle responsive duplicate text
    expect(screen.getAllByText('Mathematics').length).toBeGreaterThan(0);
    expect(screen.getAllByText('English').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Verbal Reasoning').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Non-Verbal Reasoning').length).toBeGreaterThan(0);
  });

  test('defaults to Mathematics tab active and shows math skills', () => {
    render(<SkillMatrix />);
    // Check for a math skill
    expect(screen.getByText('Number & Place Value')).toBeInTheDocument();
    expect(screen.getByText('80%')).toBeInTheDocument();

    // Should not show English skills initially
    expect(screen.queryByText('Reading Comprehension')).not.toBeInTheDocument();
  });

  test('switches content when clicking a tab', () => {
    render(<SkillMatrix />);

    // Click English tab
    const englishTexts = screen.getAllByText('English');
    fireEvent.click(englishTexts[0]);

    // Should show English skills
    expect(screen.getByText('Reading Comprehension')).toBeInTheDocument();

    // Should not show Math skills anymore
    expect(screen.queryByText('Number & Place Value')).not.toBeInTheDocument();
  });
});
