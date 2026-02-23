# API Schema Contract

This document outlines the JSON response structure for key API endpoints.

## 1. Mathematics

### `GET /next_math`
Fetches a random Math question.

#### Request Parameters
- `topic`: (Optional) Filter by topic (e.g., "Algebra", "Geometry").

#### Response
```json
{
  "id": -1, // -1 for generated, >0 for database questions
  "type": "math",
  "topic": "Mental Maths",
  "question": "What is 12 + 5?",
  "question_type": "Mental",
  "generated_answer_check": "17", // Only present for generated questions (id=-1)
  "options": [], // Empty for mental/generated, array for Multiple Choice
  "explanation": "The answer is 17.",
  "user_level": 3,
  "score": 100,
  "streak": 5,
  "is_boss": false, // True every 5th streak for "Boss Battle"
  "boss_name": null, // E.g., "The Number Cruncher"
  "boss_hp": 100
}
```

### `POST /check_math`
Validates a user's answer.

#### Request Body
```json
{
  "id": -1,
  "answer": "17",
  "repair_mode": false,
  "is_boss": false,
  "correct_answer": "17" // Only for generated questions where answer is sent back
}
```

#### Response
```json
{
  "correct": true,
  "correct_answer": "17",
  "explanation": "Correct calculation!",
  "score": 110,
  "new_level": 4,
  "topic": "Mental Maths",
  "new_badges": [],
  "streak": 6
}
```

---

## 2. Verbal Reasoning

### `GET /next_verbal`
Fetches a random Verbal Reasoning question.

#### Response
```json
{
  "id": 101,
  "type": "missing_word",
  "topic": "Verbal Reasoning",
  "question": "Choose the word that completes the sentence.",
  "content": "The cat ___ on the mat.",
  "options": ["sat", "ran", "jumped"],
  "user_level": 2,
  "score": 110,
  "streak": 6
}
```

### `POST /check_verbal`
Validates a Verbal Reasoning answer.

#### Request Body
```json
{
  "id": 101,
  "answer": "sat"
}
```

#### Response
```json
{
  "correct": true,
  "correct_answer": "sat",
  "explanation": "Past tense fits best.",
  "score": 120,
  "new_level": 3,
  "topic": "Verbal Reasoning",
  "new_badges": []
}
```

---

## 3. Comprehension

### `GET /next_comprehension`
Fetches a comprehension passage and questions.

#### Request Parameters
- `topic`: (Optional) Filter by topic.

#### Response
```json
{
  "id": 1,
  "title": "The Industrial Revolution",
  "topic": "History",
  "content": "Full text of the passage...",
  "image_url": "/images/comprehension/The_Industrial_Revolution.jpg",
  "questions": [
    {
      "id": 5,
      "text": "When did it start?",
      "options": ["1700s", "1800s", "1900s"]
    }
  ]
}
```

### `POST /check_comprehension`
Validates a specific comprehension question.

#### Request Body
```json
{
  "question_id": 5,
  "answer": "1700s",
  "evidence": "started in the late 1700s" // Optional: selected text for bonus points
}
```

#### Response
```json
{
  "correct": true,
  "correct_answer": "1700s",
  "explanation": "It began in Britain in the late 18th century.",
  "score": 135,
  "evidence_bonus": true,
  "new_badges": []
}
```

---

## 4. SPaG (Spelling, Punctuation, Grammar)

### `GET /api/spag/generate`
Fetches a random SPaG question.

**NOTE:** Unlike other endpoints, this returns the raw question object directly from the seed list without user stats wrapper.

#### Response
```json
{
  "id": 1,
  "type": "spelling",
  "question": "The weather was atroshus.",
  "options": ["The", "weather", "was", "atroshus"],
  "answer": "atroshus",
  "explanation": "The correct spelling is 'atrocious'."
}
```

---

## 5. Mock Tests

### `GET /mock_test`
Generates a full mock test.

#### Response
Array of question objects (similar to `next_math` but bulk).

```json
[
  { "id": 10, "question": "...", "options": [...] },
  { "id": 11, "question": "...", "options": [...] }
]
```
