from flask import Blueprint, jsonify, request
import json
from database import Session, TopicProgress, UserStats, ScoreHistory, UserErrors, Mistakes
from sqlalchemy import desc

core_bp = Blueprint('core', __name__)

@core_bp.route('/api/record_mistake', methods=['POST'])
def record_mistake():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['question_type', 'question_text', 'user_answer', 'correct_answer']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    session = Session()
    try:
        new_mistake = Mistakes(
            user_id=data.get('user_id', 1), # Default to 1 if not provided
            question_type=data['question_type'],
            question_text=data['question_text'],
            user_answer=data['user_answer'],
            correct_answer=data['correct_answer']
        )
        session.add(new_mistake)
        session.commit()
        return jsonify({"message": "Mistake recorded successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@core_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    session = Session()
    scores = session.query(ScoreHistory).order_by(desc(ScoreHistory.score)).limit(10).all()
    result = []
    for s in scores:
        result.append({
            "score": s.score,
            "max_score": s.max_score,
            "mode": s.mode,
            "date": s.timestamp.strftime("%Y-%m-%d %H:%M")
        })
    session.close()
    return jsonify(result)

@core_bp.route('/get_user_stats', methods=['GET'])
def get_user_stats():
    session = Session()
    user = session.query(UserStats).first()
    if not user:
        user = UserStats(current_level=3, total_score=0, streak=0)
        session.add(user)
        session.commit()

    badges = []
    if user.badges:
        try:
            badges = json.loads(user.badges)
        except:
            badges = []

    error_count = session.query(UserErrors).filter_by(user_id=user.id).count()

    result = {
        "score": user.total_score,
        "streak": user.streak,
        "level": user.current_level,
        "badges": badges,
        "error_count": error_count
    }
    session.close()
    return jsonify(result)

@core_bp.route('/get_score_history', methods=['GET'])
def get_score_history():
    session = Session()
    # Fetch all history, ordered by time
    history = session.query(ScoreHistory).order_by(ScoreHistory.timestamp).all()

    result = []
    for h in history:
        result.append({
            "timestamp": h.timestamp.isoformat(),
            "score": h.score,
            "mode": h.mode
        })

    session.close()
    return jsonify(result)

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
