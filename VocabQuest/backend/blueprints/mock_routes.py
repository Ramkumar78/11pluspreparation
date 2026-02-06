from flask import Blueprint, jsonify, request
import random
import json
from sqlalchemy.sql.expression import func
from database import Session, UserStats, MathQuestion, Word, ComprehensionPassage, ComprehensionQuestion, ScoreHistory
from utils import sanitize_filename

mock_bp = Blueprint('mock', __name__)

@mock_bp.route('/mock_test', methods=['GET'])
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

@mock_bp.route('/submit_mock', methods=['POST'])
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

    # Save Score History
    history = ScoreHistory(
        score=score,
        max_score=max_score,
        mode="Mock Test",
        details=json.dumps({"percentage": int((score/max_score)*100) if max_score > 0 else 0})
    )
    session.add(history)

    session.commit()
    session.close()

    return jsonify({
        "total_score": score,
        "max_score": max_score,
        "percentage": int((score/max_score)*100) if max_score > 0 else 0,
        "breakdown": results_breakdown
    })
