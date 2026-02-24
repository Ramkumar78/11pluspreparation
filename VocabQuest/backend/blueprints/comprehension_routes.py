from flask import Blueprint, jsonify, request
import random
import json
from database import Session, UserStats, ComprehensionPassage, ComprehensionQuestion
from utils import sanitize_filename, check_badges

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
    if not data:
        return jsonify({"error": "No data provided"}), 400
    q_id = data.get('question_id')
    user_answer = data.get('answer', '').strip()

    session = Session()
    user = session.query(UserStats).first()
    question = session.query(ComprehensionQuestion).filter_by(id=q_id).first()

    if not question:
        session.close()
        return jsonify({"error": "Question not found"}), 404

    is_correct = (user_answer.lower() == question.correct_answer.lower())

    evidence_bonus = False
    evidence_found = data.get('evidence', '').strip()

    # Update score
    if is_correct:
        user.total_score += 15 # Comprehensions might be worth more

        # Check for Evidence Bonus
        if evidence_found and question.evidence_text:
            # Check if user selected text overlaps with evidence
            # Simple check: if evidence_text contains user selection (sufficient length) OR user selection contains evidence_text
            clean_evidence = evidence_found.lower()
            clean_target = question.evidence_text.lower()

            # Ensure user selected enough text (e.g. at least 5 chars) to avoid random clicks
            if len(clean_evidence) > 5:
                if clean_target in clean_evidence or clean_evidence in clean_target:
                    user.total_score += 5
                    evidence_bonus = True

        user.streak += 1
    else:
        user.streak = 0

    new_badges = check_badges(user)
    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "score": user.total_score,
        "new_badges": new_badges,
        "evidence_bonus": evidence_bonus
    }

    session.close()
    return jsonify(result)
