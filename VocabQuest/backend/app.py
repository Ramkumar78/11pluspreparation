import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Session, Word, UserStats
from scraper import get_cartoon_image
from seed_list import WORD_LIST

app = Flask(__name__)
CORS(app)

# Helper to Initialize Data
def init_db():
    session = Session()
    # 1. Init User Stats if not exists
    if not session.query(UserStats).first():
        session.add(UserStats(current_level=3, total_score=0, streak=0))

    # 2. Seed Words if empty
    if session.query(Word).count() < 5:
        print("Seeding Database...")
        for w in WORD_LIST:
            if not session.query(Word).filter_by(text=w["text"]).first():
                # Lazy-load image to avoid ban on startup? No, fetch usually on demand is better
                # but for simplicity we store null and fetch on demand in the endpoint
                session.add(Word(text=w["text"], difficulty=w["diff"], definition=w["def"]))
        session.commit()
    session.close()

with app.app_context():
    init_db()

@app.route('/next_word', methods=['GET'])
def next_word():
    session = Session()
    user = session.query(UserStats).first()

    # Adaptive Logic: Get words +/- 1 of user level
    # If not enough words at level, widen search
    target_diff = user.current_level
    candidates = session.query(Word).filter(
        Word.difficulty >= target_diff - 1,
        Word.difficulty <= target_diff + 1
    ).all()

    if not candidates:
        # Fallback to all words
        candidates = session.query(Word).all()

    selected = random.choice(candidates)

    # Fetch image if missing (On-Demand Scraping)
    if not selected.image_url:
        print(f"Fetching image for {selected.text}...")
        selected.image_url = get_cartoon_image(selected.text)
        session.commit()

    response = {
        "id": selected.id,
        "difficulty": selected.difficulty,
        "image": selected.image_url,
        "definition": selected.definition,
        "length": len(selected.text),
        "user_level": user.current_level,
        "score": user.total_score,
        "streak": user.streak
    }
    session.close()
    return jsonify(response)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    word_id = data.get('id')
    user_spelling = data.get('spelling', '').strip().lower()

    session = Session()
    word = session.query(Word).filter_by(id=word_id).first()
    user = session.query(UserStats).first()

    is_correct = (word.text == user_spelling)

    if is_correct:
        # Correct Logic
        user.streak += 1
        user.total_score += 10 + (user.streak * 2) # Bonus for streaks

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
