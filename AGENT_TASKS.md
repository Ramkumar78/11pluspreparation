# Agent Tasks

This document tracks outstanding tasks, technical debt, and feature requests.

## 1. Missing Skills (from `skills.md`)

### Mathematics
- [ ] **Geometry**: Transformations (Reflection, Rotation, Translation)
- [ ] **Geometry**: Bearings (Compass points)
- [ ] **Geometry**: Nets of 3D Shapes
- [ ] **Statistics**: Pie Charts & Bar Charts (Interpretation)
- [ ] **Statistics**: Line Graphs & Pictograms

### English
- [ ] **Vocabulary**: Word Families (Prefixes, Suffixes, Roots)
- [ ] **Vocabulary**: Compound Words
- [ ] **SPaG**: Shuffled Sentences (Syntax construction)

### Verbal Reasoning
- [ ] **Constructing Words**: Hidden Words (finding a 4-letter word across two words)
- [ ] **Constructing Words**: Join Two Words (Compound words)
- [ ] **Understanding Words**: Synonyms/Antonyms (Matching pairs)
- [ ] **Codes & Sequences**: Number Sequences (VR specific patterns)
- [ ] **Codes & Sequences**: Letter Connections (Word ladders)
- [ ] **Logic**: Logical Deduction (e.g., "If All Zogs are Pogs...")
- [ ] **Logic**: Seating Arrangements / Order Puzzles
- [ ] **Logic**: Statement Logic (True/False/Impossible)

### Non-Verbal Reasoning (Priority: Low)
- [ ] **Patterns & Series**: Complete the Series (Sequence of shapes)
- [ ] **Patterns & Series**: Matrices (2x2 or 3x3 Grids)
- [ ] **Patterns & Series**: Odd One Out (Visual)
- [ ] **Patterns & Series**: Analogies (A is to B as C is to ?)
- [ ] **Spatial Awareness**: 2D Representations of 3D Shapes
- [ ] **Spatial Awareness**: Nets of Cubes (Fold/Unfold)
- [ ] **Spatial Awareness**: Reflections & Rotations
- [ ] **Spatial Awareness**: Hidden Shapes

## 2. Technical Debt & Refactoring

### API Standardization
- [ ] **SPaG Endpoint**: Refactor `/api/spag/generate` to return a standard response wrapper (including `user_level`, `score`, `streak`) instead of the raw question object. This will match `next_math` and `next_verbal`.

### Testing
- [ ] **E2E Testing**: Add Cypress/Playwright tests for "Focus Mode" toggling.
- [ ] **Unit Tests**: Increase coverage for `verbal_new_generators.py`.

## 3. Procedural Generation (Next Steps)

### VR: Hidden Words
- [ ] Implement `generate_hidden_word` algorithm:
    1.  Load dictionary of 4-letter words.
    2.  Find word pairs $(W_1, W_2)$ where the end of $W_1$ and start of $W_2$ form a target word.
    3.  Filter for uniqueness.

### VR: Logical Deduction
- [ ] Implement Syllogism Generator:
    1.  Define entities and relationships (All A are B).
    2.  Generate statements.
    3.  Generate questions ("Which must be true?").

### Math: Nets of Cubes
- [ ] Implement Net Validator:
    1.  Define the 11 valid nets.
    2.  Generate invalid variations.
    3.  Create "Identify the valid net" questions.
