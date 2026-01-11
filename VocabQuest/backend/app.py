import random
import socket
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach
import re

from sqlalchemy.sql.expression import func
from database import Session, Word, UserStats, MathQuestion, TopicProgress, ComprehensionPassage, ComprehensionQuestion
from seed_list import WORD_LIST
from math_seed import MATH_LIST
from comprehension_seed import COMPREHENSION_LIST

app = Flask(__name__)
CORS(app)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5000 per day", "1000 per hour"],
    storage_uri="memory://"
)

# Helper to Initialize Data
def init_db():
    session = Session()

    # 1. Init User Stats if not exists
    if not session.query(UserStats).first():
        session.add(UserStats(current_level=3, total_score=0, streak=0))

    # 2. Seed Words (Standard logic)
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

    # Track topics for TopicProgress init
    unique_topics = set()

    for m in MATH_LIST:
        unique_topics.add(m["topic"])
        existing_q = existing_math.get(m["text"])
        if existing_q:
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

    # 4. Init Topic Progress for new topics
    existing_progress = {p.topic: p for p in session.query(TopicProgress).all()}
    for topic in unique_topics:
        if topic not in existing_progress:
            session.add(TopicProgress(topic=topic, mastery_level=1))

    if "Mental Maths" not in existing_progress:
        session.add(TopicProgress(topic="Mental Maths", mastery_level=1))

    # 5. Seed Comprehension Passages
    print("Seeding Comprehension Passages...")
    existing_passages = {p.title: p for p in session.query(ComprehensionPassage).all()}

    for c in COMPREHENSION_LIST:
        passage = existing_passages.get(c["title"])
        if not passage:
            passage = ComprehensionPassage(
                title=c["title"],
                content=c["content"],
                topic=c["topic"]
            )
            session.add(passage)
            session.flush() # Flush to get the ID for questions
        else:
            # Update content/topic if needed
            passage.content = c["content"]
            passage.topic = c["topic"]

        # Seed Questions for this passage
        # Simple check: delete existing and re-add or check by text. Re-adding is safer for updates.
        # For simplicity in this script, we'll check by text.
        existing_qs = {q.question_text: q for q in session.query(ComprehensionQuestion).filter_by(passage_id=passage.id).all()}

        for q_data in c["questions"]:
            if q_data["text"] not in existing_qs:
                new_q = ComprehensionQuestion(
                    passage_id=passage.id,
                    question_text=q_data["text"],
                    options=json.dumps(q_data["options"]),
                    correct_answer=q_data["answer"],
                    explanation=q_data["explanation"]
                )
                session.add(new_q)
            else:
                # Update existing
                q_obj = existing_qs[q_data["text"]]
                q_obj.options = json.dumps(q_data["options"])
                q_obj.correct_answer = q_data["answer"]
                q_obj.explanation = q_data["explanation"]

    session.commit()
    session.close()

def generate_arithmetic(level):
    """Generates arithmetic questions suitable for the level."""
    ops = ['+', '-', '*', '/']
    if level <= 3:
        op = random.choice(['+', '-'])
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    elif level <= 7:
        op = random.choice(['+', '-', '*'])
        a = random.randint(10, 100)
        b = random.randint(2, 12)
    else:
        op = random.choice(['+', '-', '*', '/'])
        a = random.randint(50, 500)
        b = random.randint(5, 20)

    if op == '+':
        return f"{a} + {b}", str(a + b)
    elif op == '-':
        if a < b: a, b = b, a
        return f"{a} - {b}", str(a - b)
    elif op == '*':
        return f"{a} x {b}", str(a * b)
    elif op == '/':
        ans = random.randint(2, 12)
        a = b * ans
        return f"{a} ÷ {b}", str(ans)
    return f"{a} + {b}", str(a+b)

with app.app_context():
    init_db()

# --- NEW: FEATURES ---

@app.route('/mock_test', methods=['GET'])
def get_mock_test():
    """Generates a mock test based on type (math, english, or mixed)."""
    session = Session()
    test_type = request.args.get('type', 'mixed') # mixed, math, english
    test_items = []
    duration = 20

    if test_type == 'math':
        duration = 30
        math_qs = session.query(MathQuestion).order_by(func.random()).limit(20).all()
        for m in math_qs:
            test_items.append({
                "id": m.id,
                "type": "math",
                "question": m.text,
                "topic": m.topic,
                "difficulty": m.difficulty
            })

    elif test_type == 'english':
        duration = 40
        # 1. Vocab (15 questions)
        vocab_qs = session.query(Word).order_by(func.random()).limit(15).all()
        for v in vocab_qs:
            test_items.append({
                "id": v.id,
                "type": "vocab",
                "question": v.definition,
                "image": f"/images/{v.text}.jpg",
                "length": len(v.text),
                "difficulty": v.difficulty
            })

        # 2. Comprehension (1 Passage, all questions)
        passage = session.query(ComprehensionPassage).order_by(func.random()).first()
        if passage:
            p_image = passage.image_url
            if not p_image:
                p_image = f"/images/comprehension/{sanitize_filename(passage.title)}.jpg"

            questions = session.query(ComprehensionQuestion).filter_by(passage_id=passage.id).all()
            for q in questions:
                test_items.append({
                    "id": q.id,
                    "type": "comprehension",
                    "question": q.question_text,
                    "options": json.loads(q.options),
                    "passage_title": passage.title,
                    "passage_content": passage.content,
                    "passage_image": p_image,
                    "topic": passage.topic
                })
    else:
        # Mixed (Original behavior)
        math_qs = session.query(MathQuestion).order_by(func.random()).limit(10).all()
        vocab_qs = session.query(Word).order_by(func.random()).limit(10).all()

        for m in math_qs:
            test_items.append({
                "id": m.id,
                "type": "math",
                "question": m.text,
                "topic": m.topic,
                "difficulty": m.difficulty
            })

        for v in vocab_qs:
            test_items.append({
                "id": v.id,
                "type": "vocab",
                "question": v.definition,
                "image": f"/images/{v.text}.jpg",
                "length": len(v.text),
                "difficulty": v.difficulty
            })

        random.shuffle(test_items)

    session.close()

    return jsonify({
        "test_id": f"mock-{random.randint(1000,9999)}",
        "duration_minutes": duration,
        "items": test_items
    })

@app.route('/submit_mock', methods=['POST'])
def submit_mock():
    """Batch processes mock test results and returns a scorecard."""
    data = request.json
    answers = data.get('answers', [])

    session = Session()
    user = session.query(UserStats).first()

    score = 0
    max_score = len(answers) * 10
    results_breakdown = []

    for item in answers:
        is_correct = False
        correct_val = ""
        explanation = ""

        if item['type'] == 'math':
            q = session.query(MathQuestion).filter_by(id=item['id']).first()
            if q:
                correct_val = q.answer
                explanation = q.explanation
                if str(item['user_answer']).strip().lower() == str(q.answer).strip().lower():
                    is_correct = True

        elif item['type'] == 'vocab':
            w = session.query(Word).filter_by(id=item['id']).first()
            if w:
                correct_val = w.text
                if str(item['user_answer']).strip().lower() == w.text.lower():
                    is_correct = True

        elif item['type'] == 'comprehension':
            q = session.query(ComprehensionQuestion).filter_by(id=item['id']).first()
            if q:
                correct_val = q.correct_answer
                explanation = q.explanation
                # Exact match expected for multiple choice options usually, but let's be safe with strip/lower
                if str(item['user_answer']).strip().lower() == q.correct_answer.lower():
                    is_correct = True

        if is_correct:
            score += 10

        results_breakdown.append({
            "id": item['id'],
            "type": item['type'],
            "correct": is_correct,
            "your_answer": item['user_answer'],
            "correct_answer": correct_val,
            "explanation": explanation
        })

    # Update User Stats
    user.total_score += score
    # Simple logic: if score > 80%, boost level
    if max_score > 0 and (score / max_score) > 0.8:
        user.current_level = min(10, user.current_level + 1)

    session.commit()
    session.close()

    return jsonify({
        "total_score": score,
        "max_score": max_score,
        "percentage": int((score/max_score)*100) if max_score > 0 else 0,
        "breakdown": results_breakdown
    })

# --- Comprehension Routes ---

@app.route('/next_comprehension', methods=['GET'])
def next_comprehension():
    """Returns a random comprehension passage and its questions."""
    session = Session()
    topic = request.args.get('topic')

    query = session.query(ComprehensionPassage)
    if topic:
        query = query.filter_by(topic=topic)

    passages = query.all()

    if not passages:
        # Fallback to all if topic yielded nothing
        passages = session.query(ComprehensionPassage).all()

    if not passages:
        return jsonify({"error": "No passages available"}), 404

    selected = random.choice(passages)

    # Get questions
    questions_objs = session.query(ComprehensionQuestion).filter_by(passage_id=selected.id).all()
    questions_data = []
    for q in questions_objs:
        questions_data.append({
            "id": q.id,
            "text": q.question_text,
            "options": json.loads(q.options)
        })

    image_url = selected.image_url
    if not image_url:
        image_url = f"/images/comprehension/{sanitize_filename(selected.title)}.jpg"

    response = {
        "id": selected.id,
        "title": selected.title,
        "topic": selected.topic,
        "content": selected.content,
        "image_url": image_url,
        "questions": questions_data
    }

    session.close()
    return jsonify(response)

@app.route('/check_comprehension', methods=['POST'])
def check_comprehension():
    """Checks the answer for a specific comprehension question."""
    data = request.json
    q_id = data.get('question_id')
    user_answer = data.get('answer', '').strip()

    session = Session()
    user = session.query(UserStats).first()
    question = session.query(ComprehensionQuestion).filter_by(id=q_id).first()

    if not question:
        session.close()
        return jsonify({"error": "Question not found"}), 404

    is_correct = (user_answer.lower() == question.correct_answer.lower())

    # Update score
    if is_correct:
        user.total_score += 15 # Comprehensions might be worth more
        user.streak += 1
    else:
        user.streak = 0

    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "score": user.total_score
    }

    session.close()
    return jsonify(result)

# --- Existing Routes (Math & Words) ---

@app.route('/get_topics', methods=['GET'])
def get_topics():
    """Returns list of topics and user's current mastery level in them."""
    session = Session()
    topics = session.query(TopicProgress).all()

    # Calculate percentage completion or simple level
    result = []
    for t in topics:
        # Simple heuristic for 'mastery percentage': (level / 10) * 100
        # Or based on correct answers. Let's use Level.
        mastery_pct = (t.mastery_level / 10.0) * 100
        result.append({
            "topic": t.topic,
            "level": t.mastery_level,
            "mastery": min(100, int(mastery_pct)),
            "correct": t.questions_correct,
            "total": t.questions_answered
        })

    session.close()
    return jsonify(result)

@app.route('/next_math', methods=['GET'])
def next_math():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)
         session.commit()

    selected_topic = request.args.get('topic') # Frontend can pass ?topic=Algebra

    q_id = -1
    q_text = ""
    q_ans = ""
    topic_display = ""

    # 1. Determine Difficulty Level
    # If topic selected, use topic mastery level. Else use global user level.
    current_level = user.current_level
    if selected_topic:
        topic_prog = session.query(TopicProgress).filter_by(topic=selected_topic).first()
        if topic_prog:
            current_level = topic_prog.mastery_level
            topic_display = selected_topic
        else:
            # Handle case where topic name is not in progress table for some reason
            topic_display = selected_topic

    # 2. Select Question
    # Range: -1 to +2 of current level to keep it challenging but doable
    min_diff = max(1, current_level - 1)
    max_diff = min(10, current_level + 2)

    if selected_topic and selected_topic != "Mental Maths":
        # Fetch DB question for specific topic
        questions = session.query(MathQuestion).filter(
            MathQuestion.topic == selected_topic,
            MathQuestion.difficulty >= min_diff,
            MathQuestion.difficulty <= max_diff
        ).all()

        # Fallback if no questions in that difficulty range for this topic
        if not questions:
             questions = session.query(MathQuestion).filter_by(topic=selected_topic).all()

        if questions:
            selected = random.choice(questions)
            q_text = selected.text
            q_id = selected.id
            topic_display = selected.topic
        else:
            # Fallback if topic valid but no questions (shouldn't happen with good seed)
            q_text = "No questions available for this topic yet."
            q_ans = "0"
            q_id = -2 # Error code

    elif selected_topic == "Mental Maths":
        q_text, q_ans = generate_arithmetic(current_level)
        q_id = -1
        topic_display = "Mental Maths"

    else:
        # Mixed Mode (Default behaviour)
        if random.random() > 0.3:
            questions = session.query(MathQuestion).filter(
                MathQuestion.difficulty >= min_diff,
                MathQuestion.difficulty <= max_diff
            ).all()
            if questions:
                selected = random.choice(questions)
                q_text = selected.text
                q_id = selected.id
                topic_display = selected.topic
            else:
                q_text, q_ans = generate_arithmetic(current_level)
                topic_display = "Mental Maths"
        else:
            q_text, q_ans = generate_arithmetic(current_level)
            topic_display = "Mental Maths"

    response = {
        "id": q_id,
        "type": "math",
        "topic": topic_display,
        "question": q_text,
        "generated_answer_check": q_ans if q_id == -1 else None,
        "user_level": current_level,
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

    session = Session()
    user = session.query(UserStats).first()

    is_correct = False
    explanation = ""
    correct_val = ""

    # Identify Topic for progress update
    actual_topic = "Mental Maths"

    if q_id and q_id > 0:
        # DB lookup
        question = session.query(MathQuestion).filter_by(id=q_id).first()
        if question:
            correct_val = question.answer
            actual_topic = question.topic
            # Loose comparison for strings/numbers
            if user_answer == str(correct_val).strip().lower():
                is_correct = True
            else:
                is_correct = False
            explanation = question.explanation
    else:
        # Generated arithmetic
        generated_correct_answer = str(data.get('correct_answer', '')).strip().lower()
        correct_val = generated_correct_answer
        actual_topic = "Mental Maths"
        if user_answer == correct_val:
            is_correct = True
            explanation = "Correct calculation!"
        else:
            is_correct = False
            explanation = f"The correct answer was {correct_val}."

    # Update Global Stats
    if is_correct:
        user.streak += 1
        user.total_score += 10
    else:
        user.streak = 0

    # Update Topic Stats
    topic_prog = session.query(TopicProgress).filter_by(topic=actual_topic).first()
    if not topic_prog:
        topic_prog = TopicProgress(topic=actual_topic, mastery_level=1, questions_answered=0, questions_correct=0)
        session.add(topic_prog)

    topic_prog.questions_answered += 1
    if is_correct:
        topic_prog.questions_correct += 1
        # Progression Logic: 3 correct in a row effectively (simple heuristic based on total count)
        # Simple Adaptive: If they get it right, small chance to bump level up.
        if topic_prog.questions_correct % 3 == 0:
             topic_prog.mastery_level = min(10, topic_prog.mastery_level + 1)
    else:
        # Regression Logic: If they get it wrong, and level > 1, chance to drop
        # For child friendliness, we are lenient. Only drop if level > 1
        pass

    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": correct_val,
        "explanation": explanation,
        "score": user.total_score,
        "new_level": topic_prog.mastery_level, # Return specific topic level
        "topic": actual_topic
    }
    session.close()
    return jsonify(result)

# Existing word routes
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

def find_available_port(start_port, max_port=5100):
    """Finds the first available port in the range."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('0.0.0.0', port)) != 0:
                return port
    return start_port

if __name__ == '__main__':
    port = find_available_port(5000)
    app.run(host='0.0.0.0', port=port)
