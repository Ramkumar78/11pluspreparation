import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, MathQuestion, TopicProgress

@pytest.fixture(scope='function')
def test_db():
    # Create an in-memory SQLite database for testing
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)

    # Create a configured "Session" class
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Seed initial data
    session.add(UserStats(current_level=3, total_score=0, streak=0))
    session.add(MathQuestion(
        text="What is 2+2?",
        answer="4",
        difficulty=3,
        topic="Arithmetic",
        explanation="2 plus 2 is 4."
    ))
    session.add(MathQuestion(
        text="What is 3x3?",
        answer="9",
        difficulty=3,
        topic="Algebra",
        explanation="3 times 3 is 9."
    ))
    session.add(TopicProgress(topic="Arithmetic", mastery_level=1))
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(monkeypatch, test_db):
    app.config['TESTING'] = True

    # Proxy class to prevent closing the session
    class NoCloseSession:
        def __init__(self, session):
            self.session = session

        def close(self):
            pass

        def __getattr__(self, attr):
            return getattr(self.session, attr)

    # Monkeypatch the Session in app.py and blueprints to return our test_db session
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)
    monkeypatch.setattr('blueprints.core_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_get_topics(client, test_db):
    rv = client.get('/get_topics')
    assert rv.status_code == 200
    data = rv.get_json()

    # We seeded "Arithmetic"
    topics = [t['topic'] for t in data]
    assert "Arithmetic" in topics

    arithmetic = next(t for t in data if t['topic'] == "Arithmetic")
    assert arithmetic['level'] == 1
    assert arithmetic['correct'] == 0

def test_next_math_with_topic(client, test_db):
    rv = client.get('/next_math?topic=Arithmetic')
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['topic'] == 'Arithmetic'
    assert data['question'] == 'What is 2+2?'

def test_next_math_with_topic_not_in_db(client, test_db):
    # Requesting a topic that has no questions seeded
    rv = client.get('/next_math?topic=Geometry')
    assert rv.status_code == 200
    data = rv.get_json()

    # It should fallback or return error message. Implementation says fallback to query all filtered by topic.
    # If no questions found, it sets q_id = -2 and text "No questions available..."
    assert data['question'] == "No questions available for this topic yet."

def test_check_math_updates_topic_progress(client, test_db):
    # Get question id for Arithmetic
    q = test_db.query(MathQuestion).filter_by(topic="Arithmetic").first()

    # Answer correctly
    client.post('/check_math', json={
        'id': q.id,
        'answer': '4',
        'topic': 'Arithmetic'
    })

    # Verify progress update
    tp = test_db.query(TopicProgress).filter_by(topic="Arithmetic").first()
    assert tp.questions_answered == 1
    assert tp.questions_correct == 1

    # Answer incorrectly
    client.post('/check_math', json={
        'id': q.id,
        'answer': '5',
        'topic': 'Arithmetic'
    })

    tp = test_db.query(TopicProgress).filter_by(topic="Arithmetic").first()
    assert tp.questions_answered == 2
    assert tp.questions_correct == 1

def test_check_math_creates_topic_progress(client, test_db):
    # Algebra was seeded in questions but not in TopicProgress
    q = test_db.query(MathQuestion).filter_by(topic="Algebra").first()

    client.post('/check_math', json={
        'id': q.id,
        'answer': '9'
    })

    tp = test_db.query(TopicProgress).filter_by(topic="Algebra").first()
    assert tp is not None
    assert tp.questions_answered == 1
    assert tp.questions_correct == 1

def test_topic_level_up(client, test_db):
    # Arithmetic starts at level 1. Need 3 correct to level up.
    q = test_db.query(MathQuestion).filter_by(topic="Arithmetic").first()

    client.post('/check_math', json={'id': q.id, 'answer': '4'}) # 1st
    client.post('/check_math', json={'id': q.id, 'answer': '4'}) # 2nd
    client.post('/check_math', json={'id': q.id, 'answer': '4'}) # 3rd

    tp = test_db.query(TopicProgress).filter_by(topic="Arithmetic").first()
    assert tp.mastery_level == 2
