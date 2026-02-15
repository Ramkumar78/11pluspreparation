from flask import Blueprint, jsonify
from database import Session, UserErrors, Word, MathQuestion, UserStats
import random

repair_bp = Blueprint('repair', __name__)

@repair_bp.route('/next_repair', methods=['GET'])
def next_repair():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
         user = UserStats(current_level=3, total_score=0, streak=0)
         session.add(user)
         session.commit()

    # Fetch all errors
    errors = session.query(UserErrors).all()

    if not errors:
        session.close()
        return jsonify({"empty": True, "message": "No errors found! Good job!"})

    # Pick a random error
    selected_error = random.choice(errors)

    response = {}

    if selected_error.mode == 'vocab':
        word = session.query(Word).filter_by(id=selected_error.question_id).first()
        if word:
            # Construct vocab response
            response = {
                "id": word.id,
                "type": "vocab",
                "difficulty": word.difficulty,
                "image": f"/images/{word.text}.jpg",
                "definition": word.definition,
                "length": len(word.text),
                "user_level": user.current_level,
                "score": user.total_score,
                "streak": user.streak,
                "tts_text": word.text,
                "word_type": word.word_type,
                "synonym": word.synonym,
                "mode": "repair"
            }
        else:
            # If word not found, clean up error
            session.delete(selected_error)
            session.commit()
            session.close()
            return next_repair()

    elif selected_error.mode == 'math':
        question = session.query(MathQuestion).filter_by(id=selected_error.question_id).first()
        if question:
             # Construct math response
             response = {
                "id": question.id,
                "type": "math",
                "topic": question.topic,
                "question": question.text,
                "generated_answer_check": None,
                "user_level": user.current_level,
                "score": user.total_score,
                "streak": user.streak,
                "mode": "repair"
             }
        else:
             # If question not found, clean up error
             session.delete(selected_error)
             session.commit()
             session.close()
             return next_repair()

    session.close()
    return jsonify(response)
