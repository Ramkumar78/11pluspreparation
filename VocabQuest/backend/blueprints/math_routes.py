from flask import Blueprint, jsonify, request
from sqlalchemy import func
import random
import json
from database import Session, UserStats, MathQuestion, TopicProgress, ScoreHistory, UserErrors
from utils import generate_arithmetic, check_badges
from math_seed import (
    sutton_challenge_questions,
    generate_algebra_substitution,
    generate_ratio_proportion,
    generate_fdp_conversion
)

try:
    from math_geometry_generators import generate_nets_of_cubes
    from math_new_generators import generate_line_graphs
except ImportError:
    try:
        from VocabQuest.backend.math_geometry_generators import generate_nets_of_cubes
        from VocabQuest.backend.math_new_generators import generate_line_graphs
    except ImportError:
        def generate_nets_of_cubes(n=1): return []
        def generate_line_graphs(n=1): return []

BOSS_NAMES = [
    "The Number Cruncher", "Count Calamity", "The Fraction Phantom",
    "Captain Calculator", "The Geometry Giant", "Professor Percent",
    "The Algebra Alien"
]

math_bp = Blueprint('math', __name__)

@math_bp.route('/api/math/challenge', methods=['GET'])
def math_challenge():
    """Serves a random Sutton Challenge question."""
    selected = random.choice(sutton_challenge_questions)

    # Standardize response format with regular math questions
    response = {
        "id": -1, # Using -1 to indicate it's not a DB question
        "type": "math",
        "topic": selected["topic"],
        "question": selected["text"],
        "question_type": "Challenge",
        "generated_answer_check": selected["answer"],
        "explanation_text": selected["explanation_text"],
        "user_level": 10, # Challenge mode implies high level
        "score": 0,
        "streak": 0
    }
    return jsonify(response)

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
    # Boss Battle Logic
    is_boss = False
    boss_name = None
    boss_hp = 100

    if user.streak > 0 and user.streak % 5 == 0:
        is_boss = True
        boss_name = random.choice(BOSS_NAMES)
        min_diff = min(10, current_level + 2)
        max_diff = min(10, current_level + 3)
    else:
        # Range: -1 to +2 of current level to keep it challenging but doable
        min_diff = max(1, current_level - 1)
        max_diff = min(10, current_level + 2)

    q_type_str = "Mental"
    q_options = []
    q_explanation = ""

    # --- New Generator Logic ---
    generated_data = None
    use_generator = False

    if not is_boss and selected_topic == "Algebra" and random.random() < 0.6:
         generated_data = generate_algebra_substitution(current_level)
         use_generator = True
    elif selected_topic == "Ratio" and random.random() < 0.6:
         generated_data = generate_ratio_proportion(current_level)
         use_generator = True
    elif selected_topic in ["Fractions", "Percentages"] and random.random() < 0.6:
         generated_data = generate_fdp_conversion(current_level)
         use_generator = True

    elif selected_topic == "Geometry" and random.random() < 0.4:
         g_list = generate_nets_of_cubes(1)
         if g_list:
             generated_data = g_list[0]
             use_generator = True

    elif selected_topic == "Statistics" and random.random() < 0.4:
         g_list = generate_line_graphs(1)
         if g_list:
             generated_data = g_list[0]
             use_generator = True

    if use_generator and generated_data:
        q_text = generated_data.get('question', generated_data.get('text', ''))
        q_ans = generated_data['answer']
        q_id = -1
        topic_display = selected_topic
        q_type_str = "Sutton SET Generated"
        q_options = generated_data.get('options', [])
        q_explanation = generated_data.get('explanation', "")

    elif selected_topic and selected_topic != "Mental Maths":
        # Fetch DB question for specific topic
        query = session.query(MathQuestion).filter(
            MathQuestion.topic == selected_topic,
            MathQuestion.difficulty >= min_diff,
            MathQuestion.difficulty <= max_diff
        )

        selected = None
        # New logic: Fetch 'Standard Written' questions when mastery_level > 7 for specific topics
        if current_level > 7 and selected_topic in ["Ratio", "Algebra"]:
            selected = query.filter(MathQuestion.question_type == "Standard Written").order_by(func.random()).first()
            if not selected:
                selected = query.order_by(func.random()).first()
        else:
            selected = query.order_by(func.random()).first()

        # Fallback if no questions in that difficulty range for this topic
        if not selected:
             selected = session.query(MathQuestion).filter_by(topic=selected_topic).order_by(func.random()).first()

        if selected:
            q_text = selected.text
            q_id = selected.id
            topic_display = selected.topic
            q_type_str = getattr(selected, 'question_type', "Multiple Choice")
            q_explanation = getattr(selected, 'explanation', "")
            if selected.options:
                try:
                    q_options = json.loads(selected.options)
                except:
                    q_options = []
        else:
            # Fallback if topic valid but no questions (shouldn't happen with good seed)
            q_text = "No questions available for this topic yet."
            q_ans = "0"
            q_id = -2 # Error code

    elif selected_topic == "Mental Maths":
        q_text, q_ans = generate_arithmetic(current_level)
        q_id = -1
        topic_display = "Mental Maths"
        q_type_str = "Mental"
        q_explanation = f"The answer is {q_ans}."

    else:
        # Mixed Mode (Default behaviour)
        if random.random() > 0.3:
            selected = session.query(MathQuestion).filter(
                MathQuestion.difficulty >= min_diff,
                MathQuestion.difficulty <= max_diff
            ).order_by(func.random()).first()
            if selected:
                q_text = selected.text
                q_id = selected.id
                topic_display = selected.topic
                q_type_str = getattr(selected, 'question_type', "Multiple Choice")
                q_explanation = getattr(selected, 'explanation', "")
                if selected.options:
                    try:
                        q_options = json.loads(selected.options)
                    except:
                        q_options = []
            else:
                q_text, q_ans = generate_arithmetic(current_level)
                topic_display = "Mental Maths"
                q_type_str = "Mental"
                q_explanation = f"The answer is {q_ans}."
        else:
            q_text, q_ans = generate_arithmetic(current_level)
            topic_display = "Mental Maths"
            q_type_str = "Mental"
            q_explanation = f"The answer is {q_ans}."

    response = {
        "id": q_id,
        "type": "math",
        "topic": topic_display,
        "question": q_text,
        "question_type": q_type_str,
        "generated_answer_check": q_ans if q_id == -1 else None,
        "options": q_options,
        "explanation": q_explanation,
        "user_level": current_level,
        "score": user.total_score,
        "streak": user.streak,
        "is_boss": is_boss,
        "boss_name": boss_name,
        "boss_hp": boss_hp
    }
    session.close()
    return jsonify(response)

@math_bp.route('/check_math', methods=['POST'])
def check_math():
    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"error": "No data provided"}), 400
    user_answer = str(data.get('answer', '')).strip().lower()
    q_id = data.get('id')
    repair_mode = data.get('repair_mode', False)
    is_boss = data.get('is_boss', False)

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
        points = 10

        if is_boss:
            points = 50
            explanation += " BOSS DEFEATED! +50 POINTS!"

        if repair_mode:
            points *= 2
            # Remove from UserErrors
            if q_id and int(q_id) > 0:
                error = session.query(UserErrors).filter_by(user_id=user.id, question_id=q_id, mode='math').first()
                if error:
                    session.delete(error)

        user.total_score += points

        # Record Score History
        session.add(ScoreHistory(score=user.total_score, mode='math'))
    else:
        user.streak = 0

        # Add to UserErrors if DB question
        if q_id and int(q_id) > 0:
            existing = session.query(UserErrors).filter_by(user_id=user.id, question_id=q_id, mode='math').first()
            if not existing:
                session.add(UserErrors(user_id=user.id, question_id=q_id, mode='math'))

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

    new_badges = check_badges(user)
    session.commit()

    result = {
        "correct": is_correct,
        "correct_answer": correct_val,
        "explanation": explanation,
        "score": user.total_score,
        "new_level": topic_prog.mastery_level, # Return specific topic level
        "topic": actual_topic,
        "new_badges": new_badges,
        "streak": user.streak
    }
    session.close()
    return jsonify(result)
