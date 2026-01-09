import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach

from database import Session, Word, UserStats, MathQuestion
from scraper import get_cartoon_image
from seed_list import WORD_LIST
from math_seed import MATH_LIST

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

    # 3. Seed Math Questions
    print("Seeding Math...")
    for m in MATH_LIST:
        if not session.query(MathQuestion).filter_by(text=m["text"]).first():
            session.add(MathQuestion(
                text=m["text"],
                answer=m["answer"],
                difficulty=m["diff"],
                topic=m["topic"]
            ))

    session.commit()
    session.close()

def generate_arithmetic(level):
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)

    if op == '+':
        a = random.randint(10, 50 * level)
        b = random.randint(10, 50 * level)
        return f"{a} + {b}", str(a + b)
    elif op == '-':
        a = random.randint(20, 100 * level)
        b = random.randint(1, a)
        return f"{a} - {b}", str(a - b)
    elif op == '*':
        a = random.randint(2, 12)
        b = random.randint(2, 10 * level)
        return f"{a} x {b}", str(a * b)
    elif op == '/':
        b = random.randint(2, 12)
        ans = random.randint(2, 10 * level)
        a = b * ans
        return f"{a} ÷ {b}", str(ans)

with app.app_context():
    init_db()

@app.route('/next_math', methods=['GET'])
def next_math():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)
         session.commit()

    # 50% chance of Word Problem (DB) vs 50% Arithmetic (Generated)
    if random.random() > 0.5:
        # Fetch from DB
        questions = session.query(MathQuestion).all()
        if not questions:
            # Fallback if DB empty
            q_text, q_ans = generate_arithmetic(user.current_level)
            q_id = -1
            q_type = "arithmetic"
        else:
            selected = random.choice(questions)
            q_text = selected.text
            q_ans = selected.answer
            q_id = selected.id
            q_type = "word_problem"
    else:
        # Generate on fly
        q_text, q_ans = generate_arithmetic(user.current_level)
        q_id = -1 # ID -1 indicates generated
        q_type = "arithmetic"

    response = {
        "id": q_id,
        "type": "math",
        "question": q_text,
        "hashed_answer": q_ans, # We encrypt or hide the answer in production
        "user_level": user.current_level,
        "score": user.total_score,
        "streak": user.streak
    }
    session.close()
    return jsonify(response)

@app.route('/check_math', methods=['POST'])
def check_math():
    data = request.json
    user_answer = str(data.get('answer', '')).strip()
    correct_answer = str(data.get('correct_answer', '')).strip()

    is_correct = (user_answer == correct_answer)

    session = Session()
    user = session.query(UserStats).first()

    if is_correct:
        user.streak += 1
        user.total_score += 10
        if user.streak % 3 == 0:
            user.current_level = min(10, user.current_level + 1)
    else:
        user.streak = 0
        # Optional: decrease level on wrong answer?
        # For now, keeping logic simple as per prompt.

    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": correct_answer,
        "score": user.total_score,
        "new_level": user.current_level
    }
    session.close()
    return jsonify(result)


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
