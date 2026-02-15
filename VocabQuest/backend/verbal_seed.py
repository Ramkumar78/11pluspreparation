VERBAL_LIST = [
    {
        "type": "move_one_letter",
        "text": "Move one letter from the first word to the second word to make two new words.",
        "content": "STEAM PEAR",
        "answer": "S",
        "difficulty": 3,
        "explanation": "Move 'S' from 'STEAM' to make 'TEAM'. Add 'S' to 'PEAR' to make 'SPEAR'."
    },
    {
        "type": "move_one_letter",
        "text": "Move one letter from the first word to the second word to make two new words.",
        "content": "SNAIL OIL",
        "answer": "S",
        "difficulty": 3,
        "explanation": "Move 'S' from 'SNAIL' to make 'NAIL'. Add 'S' to 'OIL' to make 'SOIL'."
    },
    {
        "type": "move_one_letter",
        "text": "Move one letter from the first word to the second word to make two new words.",
        "content": "PANT RAIL",
        "answer": "P",
        "difficulty": 4,
        "explanation": "Move 'P' from 'PANT' to make 'ANT'. Add 'P' to 'RAIL' to make 'TRAIL'."
    },
    {
        "type": "move_one_letter",
        "text": "Move one letter from the first word to the second word to make two new words.",
        "content": "BROAD ROOM",
        "answer": "B",
        "difficulty": 5,
        "explanation": "Move 'B' from 'BROAD' to make 'ROAD'. Add 'B' to 'ROOM' to make 'BROOM'."
    },
    {
        "type": "missing_word",
        "text": "Complete the word in the sentence by filling in the missing letters.",
        "content": "The sky is very _ l _ e today.",
        "answer": "blue",
        "difficulty": 2,
        "explanation": "The word is 'blue'."
    },
    {
        "type": "missing_word",
        "text": "Complete the word in the sentence by filling in the missing letters.",
        "content": "She _ a _ k _ d to school.",
        "answer": "walked",
        "difficulty": 3,
        "explanation": "The word is 'walked'."
    },
    {
        "type": "missing_word",
        "text": "Find the missing word that completes the sentence.",
        "content": "The opposite of hot is _____.",
        "answer": "cold",
        "difficulty": 1,
        "explanation": "Hot and cold are opposites (antonyms)."
    },
    {
        "type": "missing_word",
        "text": "Find the missing word that completes the sentence.",
        "content": "A _____ has four wheels.",
        "answer": "car",
        "difficulty": 1,
        "explanation": "A car is a common vehicle with four wheels."
    },
    {
        "type": "antonym",
        "text": "Select the word that is most OPPOSITE in meaning to the word in capital letters.",
        "content": "ANCIENT",
        "answer": "Modern",
        "difficulty": 4,
        "explanation": "Ancient means very old. Modern means new or current."
    },
    {
        "type": "antonym",
        "text": "Select the word that is most OPPOSITE in meaning to the word in capital letters.",
        "content": "EXPAND",
        "answer": "Contract",
        "difficulty": 5,
        "explanation": "Expand means to get bigger. Contract means to get smaller."
    },
    {
        "type": "odd_one_out",
        "text": "Find the word that does not belong in the group.",
        "content": "Apple, Pear, Potato, Grape, Banana",
        "answer": "Potato",
        "difficulty": 3,
        "explanation": "Potato is a vegetable (tuber); the others are fruits."
    },
    {
        "type": "odd_one_out",
        "text": "Find the word that does not belong in the group.",
        "content": "Sprint, Jog, Walk, Sleep, Run",
        "answer": "Sleep",
        "difficulty": 2,
        "explanation": "Sleep is a state of rest; the others are forms of movement."
    },
    {
        "type": "code_breaking",
        "text": "If CODE is coded as DPEF, how is TEAM coded?",
        "content": "TEAM",
        "answer": "UFBN",
        "difficulty": 6,
        "explanation": "The code is +1 letter (Next letter in alphabet). T->U, E->F, A->B, M->N."
    },
    {
        "type": "analogy",
        "text": "Complete the analogy.",
        "content": "Puppy is to Dog as Kitten is to ___?",
        "answer": "Cat",
        "difficulty": 2,
        "explanation": "A puppy is a young dog; a kitten is a young cat."
    },
    {
        "type": "analogy",
        "text": "Complete the analogy.",
        "content": "Doctor is to Hospital as Teacher is to ___?",
        "answer": "School",
        "difficulty": 2,
        "explanation": "A doctor works in a hospital; a teacher works in a school."
    },
    {
        "type": "code_breaking",
        "text": "If CODE is coded as DPEF, how is READ coded?",
        "content": "READ",
        "answer": "SFBE",
        "difficulty": 5,
        "explanation": "The rule is +1 letter. R->S, E->F, A->B, D->E."
    },
    {
        "type": "missing_letters",
        "text": "Fill in the missing letters to complete the word.",
        "content": "He was very _ n _ i _ u s about the test.",
        "answer": "anxious",
        "difficulty": 4,
        "explanation": "The word is 'anxious'."
    },
    {
        "type": "odd_one_out",
        "text": "Which word is the odd one out?",
        "content": "Square, Triangle, Circle, Rectangle",
        "answer": "Circle",
        "difficulty": 3,
        "explanation": "A circle has one curved side; the others are polygons with straight sides."
    }
]

CLOZE_LIST = [
    {
        "sentence": "The _____ brown fox jumps over the lazy dog.",
        "missing_word": "quick",
        "options": ["slow", "quick", "lazy", "red", "happy"]
    },
    {
        "sentence": "She has a _____ of chocolates.",
        "missing_word": "box",
        "options": ["box", "bag", "cup", "plate", "spoon"]
    },
    {
        "sentence": "The cat sat on the _____.",
        "missing_word": "mat",
        "options": ["mat", "bat", "hat", "rat", "fat"]
    },
    {
        "sentence": "He went to the _____ to buy some bread.",
        "missing_word": "shop",
        "options": ["shop", "park", "school", "beach", "gym"]
    },
    {
        "sentence": "The sun rises in the _____.",
        "missing_word": "east",
        "options": ["east", "west", "north", "south", "sky"]
    }
]
