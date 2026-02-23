# Skills Matrix: UK 11+ Entrance Exams (GL & CEM)

This document outlines the core competencies required for UK 11+ entrance examinations (Grammar & Independent Schools). It tracks the implementation status within the current codebase.

**Status Key:**
- [x] Implemented
- [ ] Missing / To Be Implemented

---

## 1. Mathematics
The 11+ Maths syllabus covers the KS2 National Curriculum with extensions into KS3 topics for highly competitive schools.

### 1.1 Number & Place Value
- [x] Place Value (Digits, Ordering, Rounding)
- [x] Negative Numbers (Basic operations)
- [x] Roman Numerals
- [x] Number Sequences (Linear, Square, Cube, Prime)

### 1.2 Calculation
- [x] Addition, Subtraction, Multiplication, Division (Integers & Decimals)
- [x] Order of Operations (BIDMAS/BODMAS)
- [x] Mental Arithmetic Strategies
- [x] Prime Numbers, Factors, Multiples (HCF/LCM)

### 1.3 Fractions, Decimals, Percentages (FDP)
- [x] Equivalence between F/D/P
- [x] Operations with Fractions (Add, Subtract, Multiply, Divide)
- [x] Calculating Percentages of Amounts
- [x] Percentage Increase/Decrease (Reverse Percentages)

### 1.4 Ratio & Proportion
- [x] Simplifying Ratios
- [x] Sharing in a Ratio
- [x] Direct Proportion (Recipes, Currency)
- [x] Scale Factors (Maps & Diagrams)

### 1.5 Algebra
- [x] Substitution
- [x] Solving Linear Equations
- [x] Forming Expressions/Equations
- [x] Sequences (Nth Term)

### 1.6 Measurement
- [x] Length, Mass, Volume/Capacity (Unit conversions)
- [x] Time (Analogue/Digital, 12/24hr, Timetables, Time Zones)
- [x] Perimeter & Area (Rectangles, Triangles, Compound Shapes)
- [x] Volume (Cubes, Cuboids)

### 1.7 Geometry
- [x] Properties of 2D Shapes (Polygons, Symmetry)
- [x] Properties of 3D Shapes (Faces, Edges, Vertices)
- [x] Angles (Triangle, Quadrilateral, Straight Line, Around a Point)
- [x] Coordinates (1st & 4th Quadrant, Midpoints)
- [ ] Transformations (Reflection, Rotation, Translation)
- [ ] Bearings (Compass points)
- [ ] Nets of 3D Shapes

### 1.8 Statistics & Data
- [x] Averages (Mean, Median, Mode, Range)
- [x] Reverse Mean Problems
- [ ] Pie Charts & Bar Charts (Interpretation)
- [ ] Line Graphs & Pictograms
- [x] Venn Diagrams (Sorting Data)
- [x] Probability (Scale 0-1, Combined Events, 'Without Replacement')

---

## 2. English
Focuses on reading accuracy, fluency, vocabulary, and grammatical precision.

### 2.1 Reading Comprehension
- [x] Fiction (Classic Literature, Modern Fiction)
- [x] Non-Fiction (Articles, Biographies, Historical, Scientific)
- [x] Poetry (Figurative Language, Structure)
- [x] Question Types: Retrieval, Inference, Vocabulary in Context, Summary

### 2.2 Vocabulary
- [x] Synonyms & Antonyms
- [x] Cloze Procedure (Word Bank & Missing Letters)
- [x] Homophones/Homographs (Contextual usage)
- [ ] Word Families (Prefixes, Suffixes, Roots)
- [ ] Compound Words

### 2.3 Grammar & Punctuation (SPaG)
- [x] Word Classes (Nouns, Verbs, Adjectives, Adverbs, Prepositions, Pronouns)
- [x] Sentence Structure (Main/Subordinate Clauses, Active/Passive Voice)
- [x] Punctuation (Commas, Apostrophes, Speech Marks, Semicolons, Colons)
- [x] Spelling Rules (Plurals, 'i before e', Double Consonants)
- [ ] Shuffled Sentences (Syntax construction)

---

## 3. Verbal Reasoning (VR)
Tests the ability to process verbal information and solve problems using words and letters.

### 3.1 Constructing Words
- [x] Move a Letter (to make new words)
- [x] Missing Letters (in words/sentences)
- [ ] Hidden Words (finding a 4-letter word across two words)
- [ ] Join Two Words (Compound words)

### 3.2 Understanding Words
- [x] Analogies (A is to B as C is to ?)
- [x] Odd One Out (Semantic)
- [ ] Synonyms/Antonyms (Matching pairs)

### 3.3 Codes & Sequences
- [x] Letter Sequences
- [ ] Number Sequences (VR specific patterns)
- [x] Code Breaking (Letter shifting / Number substitution)
- [ ] Letter Connections (Word ladders)

### 3.4 Logic
- [ ] Logical Deduction (e.g., "If All Zogs are Pogs...")
- [ ] Seating Arrangements / Order Puzzles
- [ ] Statement Logic (True/False/Impossible)

---

## 4. Non-Verbal Reasoning (NVR)
Tests visual problem-solving using shapes and patterns. (Currently unimplemented)

### 4.1 Patterns & Series
- [ ] Complete the Series (Sequence of shapes)
- [ ] Matrices (2x2 or 3x3 Grids)
- [ ] Odd One Out (Visual)
- [ ] Analogies (A is to B as C is to ?)

### 4.2 Spatial Awareness
- [ ] 2D Representations of 3D Shapes
- [ ] Nets of Cubes (Fold/Unfold)
- [ ] Reflections & Rotations
- [ ] Hidden Shapes

---

## Procedural Generation Specifications for Missing Skills

### 1. VR: Hidden Words (Search across boundaries)
**Goal:** Find a 4-letter word hidden between the end of one word and the start of the next (e.g., "The **cat** **s**at" -> CATS).

**Algorithm:**
1.  Load a dictionary of common 4-letter nouns/verbs.
2.  Generate/Load pairs of words $(W_1, W_2)$.
3.  Check if $W_1[-k:] + W_2[:4-k]$ forms a valid word for $k \in \{1, 2, 3\}$.
4.  Filter for "valid" hidden words and "accidental" hidden words to ensure only one answer exists.
5.  *Output:* "Find the hidden word in: THE CAT SAT" (Answer: CATS).

### 2. VR: Logical Deduction (Syllogisms)
**Goal:** Generate "If/Then" logic puzzles.

**Algorithm:**
1.  Define entities (e.g., Zogs, Pogs, Bloops).
2.  Define relationships:
    -   All A are B.
    -   Some B are C.
    -   No C are A.
3.  Generate statements based on these rules.
4.  Question: "Based on the above, which statement is definitely true?"
    -   (a) Some A are C (False)
    -   (b) All Zogs are Bloops (True)
5.  Use a simple dependency graph to validate truth.

### 3. NVR: Matrices (Procedural Shapes)
**Goal:** Generate 2x2 or 3x3 grids where one cell is missing.

**Algorithm:**
1.  Define **Features**: Shape (Circle, Square), Fill (Solid, Striped, Empty), Number (1, 2, 3), Rotation (0, 90, 180).
2.  Define **Rules** for Rows/Columns:
    -   *Constant:* Feature X stays the same.
    -   *Progression:* Feature X increases (+1, +90 deg).
    -   *Addition:* Col 1 + Col 2 = Col 3 (e.g., overlapping lines).
3.  Select a Rule set (e.g., Row 1: Shape Constant, Fill Progression).
4.  Populate grid.
5.  Remove bottom-right cell as the Target.
6.  Generate Distractors by violating one rule at a time.

### 4. Math: Nets of Cubes
**Goal:** Identify which 2D net folds into a valid cube.

**Algorithm:**
1.  Define the 11 valid nets of a cube (hardcoded geometric graphs).
2.  Define a set of invalid nets (e.g., 6 in a row, 'T' shapes with too many arms).
3.  *Task 1:* "Which of these is a valid net?" (Select 1 valid, 3 invalid).
4.  *Task 2 (Advanced):* "Opposite Faces". Map symbols to faces on a valid net. Ask which symbols are opposite.
    -   Use graph traversal (BFS) on the net structure to determine opposite pairs (distance = 2 in specific directions).
