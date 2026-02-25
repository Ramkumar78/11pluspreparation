from utils import rng

SENTENCES = [
    {"text": "The quick brown fox jumps over the lazy dog.", "diff": 3},
    {"text": "She sells seashells by the seashore.", "diff": 4},
    {"text": "How much wood would a woodchuck chuck if a woodchuck could chuck wood?", "diff": 5},
    {"text": "To be or not to be, that is the question.", "diff": 6},
    {"text": "All that glitters is not gold.", "diff": 4},
    {"text": "A journey of a thousand miles begins with a single step.", "diff": 5},
    {"text": "Actions speak louder than words.", "diff": 3},
    {"text": "Beauty is in the eye of the beholder.", "diff": 5},
    {"text": "Better late than never.", "diff": 2},
    {"text": "Birds of a feather flock together.", "diff": 4},
    {"text": "Cleanliness is next to godliness.", "diff": 5},
    {"text": "Don't count your chickens before they hatch.", "diff": 5},
    {"text": "Don't put all your eggs in one basket.", "diff": 4},
    {"text": "Early to bed and early to rise makes a man healthy, wealthy, and wise.", "diff": 6},
    {"text": "Every cloud has a silver lining.", "diff": 4},
    {"text": "Good things come to those who wait.", "diff": 3},
    {"text": "Haste makes waste.", "diff": 2},
    {"text": "Honesty is the best policy.", "diff": 3},
    {"text": "If it ain't broke, don't fix it.", "diff": 3},
    {"text": "Knowledge is power.", "diff": 2},
    {"text": "Laughter is the best medicine.", "diff": 3},
    {"text": "Look before you leap.", "diff": 2},
    {"text": "Practice makes perfect.", "diff": 2},
    {"text": "The early bird catches the worm.", "diff": 3},
    {"text": "The pen is mightier than the sword.", "diff": 5},
    {"text": "Time flies when you're having fun.", "diff": 4},
    {"text": "Two heads are better than one.", "diff": 3},
    {"text": "Variety is the spice of life.", "diff": 4},
    {"text": "When in Rome, do as the Romans do.", "diff": 5},
    {"text": "You can't judge a book by its cover.", "diff": 4}
]

def generate_shuffled_sentence(num_questions=1):
    """
    Generates 'Shuffled Sentence' questions.
    """
    questions = []
    attempts = 0
    max_attempts = num_questions * 50

    while len(questions) < num_questions and attempts < max_attempts:
        attempts += 1
        selected = rng.choice(SENTENCES)
        sentence = selected['text']

        words = sentence.split()
        if len(words) < 3:
            continue

        shuffled = words[:]
        rng.shuffle(shuffled)

        # Ensure it's not same as original
        if shuffled == words:
            continue

        # Check dupe
        if any(q['answer'] == sentence for q in questions):
            continue

        questions.append({
            "id": -1, # Generated
            "type": "shuffled_sentence",
            "topic": "Syntax",
            "question": "Rearrange the words to form a correct sentence.",
            "options": shuffled,
            "answer": sentence,
            "difficulty": selected['diff'],
            "explanation": f"The correct order is: '{sentence}'"
        })

    return questions
