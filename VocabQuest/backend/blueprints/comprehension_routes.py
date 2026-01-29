from flask import Blueprint, jsonify, request
import random
import json
from database import Session, UserStats, ComprehensionPassage, ComprehensionQuestion
from utils import sanitize_filename

comprehension_bp = Blueprint('comprehension', __name__)

@comprehension_bp.route('/next_comprehension', methods=['GET'])
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
        session.close()
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

@comprehension_bp.route('/check_comprehension', methods=['POST'])
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
