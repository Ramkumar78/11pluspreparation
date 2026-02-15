from flask import Blueprint, jsonify
import random
from spag_seed import SPAG_QUESTIONS

spag_bp = Blueprint('spag', __name__)

@spag_bp.route('/api/spag/generate', methods=['GET'])
def generate_spag():
    """Generates a random SPaG question (Spelling or Grammar)."""
    if not SPAG_QUESTIONS:
        return jsonify({"error": "No SPaG questions available"}), 404

    question = random.choice(SPAG_QUESTIONS)

    # Structure matches existing question format: question, options, answer
    # We also include id, type, and explanation for completeness and consistency.
    return jsonify(question)
