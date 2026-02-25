# Agent Tasks

This document tracks outstanding tasks, technical debt, and feature requests.

## 1. Missing Skills (from `skills.md`)

### Mathematics
- [ ] **Geometry**: Nets of 3D Shapes
- [ ] **Statistics**: Line Graphs

### English
- [ ] **Vocabulary**: Word Families (Prefixes, Suffixes, Roots)
- [ ] **SPaG**: Shuffled Sentences (Syntax construction)

### Verbal Reasoning
- [ ] **Codes & Sequences**: Number Sequences (VR specific patterns)
- [ ] **Codes & Sequences**: Letter Connections (Word ladders)
- [ ] **Logic**: Seating Arrangements / Order Puzzles

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

### Math: Nets of Cubes
- [ ] Implement Net Validator:
    1.  Define the 11 valid nets.
    2.  Generate invalid variations.
    3.  Create "Identify the valid net" questions.

### NVR: Matrices
- [ ] Implement Matrix Generator:
    1. Define Shape, Fill, Rotation features.
    2. Create rules for row/column progression.
    3. Generate SVG/Canvas based questions.

## 4. Strategic Initiatives (New Features)

### Adaptive & Exam-Specific
- [ ] **Algorithm**: Develop adaptive difficulty algorithm (ELO-based) for maths and vocab.
- [ ] **Exam Mode**: Create `ExamBoardSelector` toggle (GL/ISEB/CSSE) to filter question types and adjust timer logic.

### Analytics & Reporting
- [ ] **Data Model**: Design schema for detailed analytics tracking (question history, timestamps, topic tags).
- [ ] **Visualization**: Implement heatmaps for "Problem Areas" on the Parent Dashboard.

### Content & Multimedia
- [ ] **Flashcards**: Implement `FlashcardComponent` with flip animation for vocabulary and formulas.
- [ ] **Video**: Integrate video player for per-question explanation solutions (Modal or Inline).
- [ ] **Community**: Create basic structure (routes/schema) for Parent Community Forum.
