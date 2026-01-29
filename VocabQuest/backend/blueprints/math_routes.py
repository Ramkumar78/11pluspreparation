from flask import Blueprint, jsonify, request
import random
from database import Session, UserStats, MathQuestion, TopicProgress
from utils import generate_arithmetic

math_bp = Blueprint('math', __name__)

@math_bp.route('/next_math', methods=['GET'])
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

@math_bp.route('/check_math', methods=['POST'])
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
