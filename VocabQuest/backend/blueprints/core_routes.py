from flask import Blueprint, jsonify
from database import Session, TopicProgress

core_bp = Blueprint('core', __name__)

@core_bp.route('/get_topics', methods=['GET'])
def get_topics():
    """Returns list of topics and user's current mastery level in them."""
    session = Session()
    topics = session.query(TopicProgress).all()

    # Calculate percentage completion or simple level
    result = []
    for t in topics:
        # Simple heuristic for 'mastery percentage': (level / 10) * 100
        # Or based on correct answers. Let's use Level.
        mastery_pct = (t.mastery_level / 10.0) * 100
        result.append({
            "topic": t.topic,
            "level": t.mastery_level,
            "mastery": min(100, int(mastery_pct)),
            "correct": t.questions_correct,
            "total": t.questions_answered
        })

    session.close()
    return jsonify(result)
