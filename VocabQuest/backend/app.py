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
    default_limits=["2000 per day", "500 per hour"], # Increased for testing
    storage_uri="memory://"
)

# Helper to Initialize Data
def init_db():
    session = Session()
    # 1. Init User Stats if not exists
    if not session.query(UserStats).first():
        session.add(UserStats(current_level=1, total_score=0, streak=0))

    # 2. Seed Words (Existing logic...)
    existing_words = {word.text: word for word in session.query(Word).all()}
    for w in WORD_LIST:
        existing_word = existing_words.get(w["text"])
        w_type = w.get("type")
        if isinstance(w_type, list):
            w_type = ", ".join(w_type)

        if existing_word:
            existing_word.difficulty = w["diff"]
            existing_word.definition = w["def"]
            existing_word.word_type = w_type
            existing_word.synonym = w.get("synonym")
        else:
            session.add(Word(
                text=w["text"],
                difficulty=w["diff"],
                definition=w["def"],
                word_type=w_type,
                synonym=w.get("synonym")
            ))

    # 3. Seed Math Questions
    print("Seeding Math Questions...")
    existing_math = {m.text: m for m in session.query(MathQuestion).all()}

    for m in MATH_LIST:
        existing_q = existing_math.get(m["text"])
        if existing_q:
            # Update explanation/difficulty if changed
            existing_q.answer = m["answer"]
            existing_q.difficulty = m["diff"]
            existing_q.topic = m["topic"]
            existing_q.explanation = m.get("explanation", "")
        else:
            session.add(MathQuestion(
                text=m["text"],
                answer=m["answer"],
                difficulty=m["diff"],
                topic=m["topic"],
                explanation=m.get("explanation", "")
            ))

    session.commit()
    session.close()

def generate_arithmetic(level):
    """Generates arithmetic questions suitable for the level if DB runs out."""
    ops = ['+', '-', '*', '/']
    # Level 1-3: Easy ops
    if level <= 3:
        op = random.choice(['+', '-'])
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    # Level 4-7: Medium ops
    elif level <= 7:
        op = random.choice(['+', '-', '*'])
        a = random.randint(10, 100)
        b = random.randint(2, 12)
    # Level 8+: Hard ops
    else:
        op = random.choice(['+', '-', '*', '/'])
        a = random.randint(50, 500)
        b = random.randint(5, 20)

    if op == '+':
        return f"{a} + {b}", str(a + b)
    elif op == '-':
        if a < b: a, b = b, a # Ensure positive result for younger kids usually
        return f"{a} - {b}", str(a - b)
    elif op == '*':
        return f"{a} x {b}", str(a * b)
    elif op == '/':
        # Ensure clean division
        ans = random.randint(2, 12)
        a = b * ans
        return f"{a} ÷ {b}", str(ans)

    return f"{a} + {b}", str(a+b)

with app.app_context():
    init_db()

@app.route('/next_math', methods=['GET'])
def next_math():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=1, total_score=0, streak=0)
         session.add(user)
         session.commit()

    current_level = user.current_level

    # Adaptive Logic: Select questions based on difficulty range
    # Easy: 1-3, Medium: 4-7, Hard: 8-10
    # We broaden the search slightly: +/- 1 of current level
    min_diff = max(1, current_level - 1)
    max_diff = min(10, current_level + 2)

    # 70% chance of DB question (Concepts), 30% Generated (Mental Maths)
    if random.random() > 0.3:
        # Fetch appropriate questions from DB
        questions = session.query(MathQuestion).filter(
            MathQuestion.difficulty >= min_diff,
            MathQuestion.difficulty <= max_diff
        ).all()

        # If no questions in range (e.g. at very high level), fallback to all
        if not questions:
            questions = session.query(MathQuestion).all()

        if questions:
            selected = random.choice(questions)
            q_text = selected.text
            q_id = selected.id
            q_type = selected.topic # e.g. "Algebra", "Geometry"
        else:
            # Fallback if DB completely empty
            q_text, q_ans = generate_arithmetic(current_level)
            q_id = -1
            q_type = "Mental Maths"
    else:
        # Generate on fly
        q_text, q_ans = generate_arithmetic(current_level)
        q_id = -1
        q_type = "Mental Maths"

    response = {
        "id": q_id,
        "type": "math",
        "topic": q_type, # Frontend can display this
        "question": q_text,
        "generated_answer_check": q_ans if q_id == -1 else None,
        "user_level": user.current_level,
        "score": user.total_score,
        "streak": user.streak
    }
    session.close()
    return jsonify(response)

@app.route('/check_math', methods=['POST'])
def check_math():
    data = request.json
    user_answer = str(data.get('answer', '')).strip().lower()
    q_id = data.get('id')
    generated_correct_answer = str(data.get('correct_answer', '')).strip().lower()

    session = Session()
    user = session.query(UserStats).first()

    is_correct = False
    explanation = ""
    correct_val = ""

    if q_id and q_id != -1:
        # DB lookup
        question = session.query(MathQuestion).filter_by(id=q_id).first()
        if question:
            correct_val = question.answer
            if user_answer == correct_val.lower():
                is_correct = True
            else:
                is_correct = False
            explanation = question.explanation
    else:
        # Generated arithmetic
        correct_val = generated_correct_answer
        if user_answer == correct_val:
            is_correct = True
            explanation = "Great mental maths!"
        else:
            is_correct = False
            explanation = f"Let's double check. The answer is {correct_val}."

    if is_correct:
        user.streak += 1
        user.total_score += 10
        # Adaptive Progression: Increase level every 2 correct answers in a row
        if user.streak % 2 == 0:
            user.current_level = min(10, user.current_level + 1)
    else:
        user.streak = 0
        # Optional: Drop level if struggling repeatedly?
        # For now, we keep it encouraging.

    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": correct_val,
        "explanation": explanation,
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
