from flask import Blueprint, jsonify
import random
from spag_seed import SPAG_QUESTIONS
from database import Session, UserStats

spag_bp = Blueprint('spag', __name__)

@spag_bp.route('/api/spag/generate', methods=['GET'])
def generate_spag():
    """Generates a random SPaG question (Spelling or Grammar)."""
    if not SPAG_QUESTIONS:
        return jsonify({"error": "No SPaG questions available"}), 404

    session = Session()
    try:
        user = session.query(UserStats).first()
        if not user:
            user = UserStats(current_level=3, total_score=0, streak=0, badges="[]")
            session.add(user)
            session.commit()

        question = random.choice(SPAG_QUESTIONS)

        response = {
            **question, # id, type, question, options, answer, explanation
            "user_level": user.current_level,
            "score": user.total_score,
            "streak": user.streak
        }
        return jsonify(response)
    finally:
        session.close()
