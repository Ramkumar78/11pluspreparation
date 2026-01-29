import socket
import json
from flask import Flask
from flask_cors import CORS
from extensions import limiter

from database import Session, Word, UserStats, MathQuestion, TopicProgress, ComprehensionPassage, ComprehensionQuestion
from seed_list import WORD_LIST
from math_seed import MATH_LIST
from comprehension_seed import COMPREHENSION_LIST

# Blueprints
from blueprints.vocab_routes import vocab_bp
from blueprints.math_routes import math_bp
from blueprints.comprehension_routes import comprehension_bp
from blueprints.mock_routes import mock_bp
from blueprints.core_routes import core_bp

app = Flask(__name__)
CORS(app)

# Initialize Limiter
limiter.init_app(app)

# Register Blueprints
app.register_blueprint(vocab_bp)
app.register_blueprint(math_bp)
app.register_blueprint(comprehension_bp)
app.register_blueprint(mock_bp)
app.register_blueprint(core_bp)

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

with app.app_context():
    init_db()

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
