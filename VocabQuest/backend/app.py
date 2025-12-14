import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach

from database import Session, Word, UserStats
from scraper import get_cartoon_image
from seed_list import WORD_LIST

app = Flask(__name__)
CORS(app)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Helper to Initialize Data
def init_db():
    session = Session()
    # 1. Init User Stats if not exists
    if not session.query(UserStats).first():
        session.add(UserStats(current_level=3, total_score=0, streak=0))

    # 2. Seed Words: Upsert Logic (Update existing, Insert new)
    print("Seeding/Updating Database...")

    # Optimization: Load all existing words into a dict for O(1) lookup
    existing_words = {word.text: word for word in session.query(Word).all()}

    for w in WORD_LIST:
        existing_word = existing_words.get(w["text"])

        # Handle list type for word_type
        w_type = w.get("type")
        if isinstance(w_type, list):
            w_type = ", ".join(w_type)

        if existing_word:
            # Update existing fields to ensure compliance
            # Only update if changed to minimize DB writes?
            # For simplicity, we assign (SQLAlchemy tracks changes)
            existing_word.difficulty = w["diff"]
            existing_word.definition = w["def"]
            existing_word.word_type = w_type
            existing_word.synonym = w.get("synonym")
        else:
            # Insert new word
            new_word = Word(
                text=w["text"],
                difficulty=w["diff"],
                definition=w["def"],
                word_type=w_type,
                synonym=w.get("synonym")
            )
            session.add(new_word)
            existing_words[w["text"]] = new_word # Keep track of added words in this session if needed

    session.commit()
    session.close()

with app.app_context():
    init_db()

@app.route('/next_word', methods=['GET'])
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

@app.route('/check_answer', methods=['POST'])
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

        # Increase Difficulty every 2 consecutive correct answers
        if user.streak % 2 == 0:
            user.current_level = min(10, user.current_level + 1)

    else:
        # Wrong Logic
        user.streak = 0
        # Decrease difficulty immediately
        user.current_level = max(1, user.current_level - 1)

    session.commit()

    result = {
        "correct": is_correct,
        "correct_word": word.text,
        "new_level": user.current_level,
        "score": user.total_score
    }
    session.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
