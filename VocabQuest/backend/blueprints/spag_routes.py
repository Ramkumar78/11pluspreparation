from flask import Blueprint, jsonify
import random
from spag_seed import SPAG_QUESTIONS
from database import Session, UserStats

# Import procedural generators
try:
    from spag_new_generators import generate_shuffled_sentence
except ImportError:
    # Fallback/Dummy if file missing or error
    def generate_shuffled_sentence(n): return []

try:
    from verbal_new_generators import generate_word_families
except ImportError:
    def generate_word_families(n): return []

spag_bp = Blueprint('spag', __name__)

@spag_bp.route('/api/spag/generate', methods=['GET'])
def generate_spag():
    """Generates a random SPaG question (Spelling, Grammar, Syntax, Morphology)."""

    session = Session()
    try:
        user = session.query(UserStats).first()
        if not user:
            user = UserStats(current_level=3, total_score=0, streak=0, badges="[]")
            session.add(user)
            session.commit()

        # Decide source: Static vs Procedural
        # 60% Static, 20% Shuffled Sentence, 20% Word Families
        roll = random.random()

        question_data = None

        if roll < 0.6 and SPAG_QUESTIONS:
            # Static Question
            selected = random.choice(SPAG_QUESTIONS)
            question_data = {
                "id": selected.get('id'),
                "type": "spag", # Standardize type
                "topic": selected.get('type', 'General').capitalize(), # Map 'spelling' -> 'Spelling'
                "question": selected.get('question'),
                "options": selected.get('options'),
                "answer": selected.get('answer'),
                "explanation": selected.get('explanation'),
                "difficulty": 3 # Default difficulty for static
            }
        elif roll < 0.8:
            # Shuffled Sentence
            generated = generate_shuffled_sentence(1)
            if generated:
                question_data = generated[0]
                question_data['type'] = "spag"
        else:
            # Word Families
            generated = generate_word_families(1)
            if generated:
                question_data = generated[0]
                question_data['type'] = "spag"

        # Fallback if generator returned empty
        if not question_data:
            if SPAG_QUESTIONS:
                selected = random.choice(SPAG_QUESTIONS)
                question_data = {
                    "id": selected.get('id'),
                    "type": "spag",
                    "topic": selected.get('type', 'General').capitalize(),
                    "question": selected.get('question'),
                    "options": selected.get('options'),
                    "answer": selected.get('answer'),
                    "explanation": selected.get('explanation'),
                    "difficulty": 3
                }
            else:
                return jsonify({"error": "No SPaG questions available"}), 404

        response = {
            "id": question_data.get('id'),
            "type": question_data.get('type', 'spag'),
            "topic": question_data.get('topic', 'General'),
            "question": question_data.get('question'),
            "options": question_data.get('options'),
            "answer": question_data.get('answer'),
            "explanation": question_data.get('explanation'),
            "user_level": user.current_level,
            "score": user.total_score,
            "streak": user.streak
        }
        return jsonify(response)
    finally:
        session.close()
