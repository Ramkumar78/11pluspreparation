from flask import Blueprint, jsonify, request
import random
import bleach
from extensions import limiter
from database import Session, Word, UserStats, ScoreHistory
from utils import check_badges

vocab_bp = Blueprint('vocab', __name__)

@vocab_bp.route('/next_word', methods=['GET'])
@limiter.limit("20 per minute")
def next_word():
    session = Session()
    user = session.query(UserStats).first()
    if not user: # Safety check
         # Handle case where user table might be empty if DB init failed or reset
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)
         session.commit()

    # Adaptive Logic: Get words +/- 1 of user level
    target_diff = user.current_level
    candidates = session.query(Word).filter(
        Word.difficulty >= target_diff - 1,
        Word.difficulty <= target_diff + 1
    ).all()

    if not candidates:
        # Fallback to all words
        candidates = session.query(Word).all()

    selected = random.choice(candidates)

    # Use local image path
    image_url = f"/images/{selected.text}.jpg"

    response = {
        "id": selected.id,
        "difficulty": selected.difficulty,
        "image": image_url,
        "definition": selected.definition,
        "length": len(selected.text),
        "user_level": user.current_level,
        "score": user.total_score,
        "streak": user.streak,
        # Send text for TTS but frontend should hide it.
        # For a 10yo, we prioritize learning features (pronunciation) over absolute anti-cheat.
        "tts_text": selected.text,
        "word_type": selected.word_type,
        "synonym": selected.synonym
    }
    session.close()
    return jsonify(response)

@vocab_bp.route('/check_answer', methods=['POST'])
@limiter.limit("20 per minute")
def check_answer():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    word_id = data.get('id')
    raw_spelling = data.get('spelling', '')

    # Input Validation
    if not isinstance(word_id, int):
        return jsonify({"error": "Invalid ID"}), 400

    if not isinstance(raw_spelling, str):
        return jsonify({"error": "Invalid spelling format"}), 400

    # Sanitize
    user_spelling = bleach.clean(raw_spelling).strip().lower()

    session = Session()
    word = session.query(Word).filter_by(id=word_id).first()
    user = session.query(UserStats).first()

    if not word or not user:
         session.close()
         return jsonify({"error": "Game state invalid"}), 400

    is_correct = (word.text.lower() == user_spelling)

    if is_correct:
        # Correct Logic
        user.streak += 1
        user.total_score += 10 + (user.streak * 2)

        # Record Score History
        session.add(ScoreHistory(score=user.total_score, mode='vocab'))

        # Increase Difficulty every 2 consecutive correct answers
        if user.streak % 2 == 0:
            user.current_level = min(10, user.current_level + 1)

    else:
        # Wrong Logic
        user.streak = 0
        # Decrease difficulty immediately
        user.current_level = max(1, user.current_level - 1)

    new_badges = check_badges(user)
    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": word.text,
        "correct_word": word.text, # Keep for backward compatibility if needed, or remove. keeping for safety but plan said standardize.
        "new_level": user.current_level,
        "score": user.total_score,
        "new_badges": new_badges,
        "streak": user.streak
    }
    session.close()
    return jsonify(result)
