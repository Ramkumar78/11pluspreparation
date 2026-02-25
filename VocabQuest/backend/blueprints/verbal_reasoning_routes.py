from flask import Blueprint, jsonify, request
import random
import json
from database import Session, UserStats, VerbalReasoningQuestion, TopicProgress, ScoreHistory
from utils import check_badges
from verbal_seed import CLOZE_LIST
from verbal_new_generators import generate_number_sequences, generate_letter_connections, generate_seating_arrangements

verbal_reasoning_bp = Blueprint('verbal_reasoning', __name__)

@verbal_reasoning_bp.route('/number_sequences', methods=['GET'])
def get_number_sequence():
    """Generates a random Number Sequence question."""
    questions = generate_number_sequences(1)
    if questions:
        return jsonify(questions[0])
    return jsonify({"error": "Could not generate question"}), 500

@verbal_reasoning_bp.route('/letter_connections', methods=['GET'])
def get_letter_connection():
    """Generates a random Word Ladder question."""
    questions = generate_letter_connections(1)
    if questions:
        return jsonify(questions[0])
    return jsonify({"error": "Could not generate question"}), 500

@verbal_reasoning_bp.route('/seating_arrangements', methods=['GET'])
def get_seating_arrangement():
    """Generates a random Seating Arrangement question."""
    questions = generate_seating_arrangements(1)
    if questions:
        return jsonify(questions[0])
    return jsonify({"error": "Could not generate question"}), 500

@verbal_reasoning_bp.route('/cloze', methods=['GET'])
def get_cloze():
    """Returns a random Cloze (sentence completion) task."""
    if not CLOZE_LIST:
        return jsonify({"error": "No cloze questions available"}), 404

    question = random.choice(CLOZE_LIST)
    return jsonify(question)

@verbal_reasoning_bp.route('/next_verbal', methods=['GET'])
def next_verbal():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)
         session.commit()

    # Use TopicProgress for 'Verbal Reasoning'
    topic_display = "Verbal Reasoning"
    topic_prog = session.query(TopicProgress).filter_by(topic=topic_display).first()

    current_level = user.current_level
    if topic_prog:
        current_level = topic_prog.mastery_level
    else:
        # Fallback to init topic progress
        topic_prog = TopicProgress(topic=topic_display, mastery_level=1)
        session.add(topic_prog)
        session.commit()
        current_level = 1

    # Select Question based on difficulty
    min_diff = max(1, current_level - 1)
    max_diff = min(10, current_level + 2)

    questions = session.query(VerbalReasoningQuestion).filter(
        VerbalReasoningQuestion.difficulty >= min_diff,
        VerbalReasoningQuestion.difficulty <= max_diff
    ).all()

    if not questions:
        questions = session.query(VerbalReasoningQuestion).all()

    if questions:
        selected = random.choice(questions)
        q_id = selected.id
        q_text = selected.question_text
        q_content = selected.content
        q_type = selected.question_type
        q_options = json.loads(selected.options) if selected.options else None
    else:
        q_id = -1
        q_text = "No questions available."
        q_content = ""
        q_type = "error"
        q_options = None

    response = {
        "id": q_id,
        "type": q_type,
        "topic": topic_display,
        "question": q_text,
        "content": q_content,
        "options": q_options,
        "user_level": current_level,
        "score": user.total_score,
        "streak": user.streak
    }
    session.close()
    return jsonify(response)

@verbal_reasoning_bp.route('/check_verbal', methods=['POST'])
def check_verbal():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400
    user_answer = str(data.get('answer', '')).strip().lower()
    q_id = data.get('id')

    if q_id is not None:
        try:
            q_id = int(q_id)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid ID format"}), 400

    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)

    is_correct = False
    explanation = ""
    correct_val = ""

    question = session.query(VerbalReasoningQuestion).filter_by(id=q_id).first()

    if question:
        correct_val = question.answer
        if user_answer == str(correct_val).strip().lower():
            is_correct = True
        explanation = question.explanation
    else:
        is_correct = False
        explanation = "Question not found."

    # Update Global Stats
    if is_correct:
        user.streak += 1
        user.total_score += 10
        session.add(ScoreHistory(score=user.total_score, mode='verbal_reasoning'))
    else:
        user.streak = 0

    # Update Topic Stats
    topic_display = "Verbal Reasoning"
    topic_prog = session.query(TopicProgress).filter_by(topic=topic_display).first()
    if not topic_prog:
        topic_prog = TopicProgress(topic=topic_display, mastery_level=1, questions_answered=0, questions_correct=0)
        session.add(topic_prog)

    topic_prog.questions_answered += 1
    if is_correct:
        topic_prog.questions_correct += 1
        # Adaptive: Every 3 correct answers increases level
        if topic_prog.questions_correct % 3 == 0:
             topic_prog.mastery_level = min(10, topic_prog.mastery_level + 1)

    new_badges = check_badges(user)
    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": correct_val,
        "explanation": explanation,
        "score": user.total_score,
        "new_level": topic_prog.mastery_level,
        "topic": topic_display,
        "new_badges": new_badges
    }
    session.close()
    return jsonify(result)
