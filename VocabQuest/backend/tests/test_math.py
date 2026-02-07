import pytest
import sys
import os
from unittest.mock import MagicMock
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
    user = UserStats(current_level=3, total_score=0, streak=0)
    session.add(user)
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

        def commit(self):
            self.session.commit()

        def add(self, instance):
            self.session.add(instance)

        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)

        def __getattr__(self, attr):
            return getattr(self.session, attr)

    # Monkeypatch the Session in blueprints to return our test_db session
    # We need to return a new NoCloseSession each time Session() is called
    TestSessionMaker = lambda: NoCloseSession(test_db)

    # Patch where Session is imported in the blueprints
    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)

    # Also patch database.Session if used elsewhere, though math_routes imports from database
    monkeypatch.setattr('database.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_mental_maths(client, monkeypatch):
    """Mock generate_arithmetic and verify next_math returns the correct generated question and answer check."""
    # Mock generate_arithmetic to return a fixed tuple
    # Note: generate_arithmetic returns (question_text, answer_string)
    mock_generate = MagicMock(return_value=("What is 10+10?", "20"))
    monkeypatch.setattr('blueprints.math_routes.generate_arithmetic', mock_generate)

    # Call next_math with topic 'Mental Maths'
    response = client.get('/next_math?topic=Mental Maths')
    assert response.status_code == 200
    data = response.get_json()

    # Verify the mocked question is returned
    assert data['question'] == "What is 10+10?"
    # Verify the mocked answer is present in generated_answer_check
    assert data['generated_answer_check'] == "20"
    # Verify topic
    assert data['topic'] == "Mental Maths"

    # Verify mock was called
    mock_generate.assert_called_once()

def test_topic_progress(client, test_db):
    """Verify that answering correctly updates the TopicProgress table and increases mastery_level every 3 correct answers."""
    # Seed a question for a specific topic
    topic_name = "Addition"
    q = MathQuestion(text="2+2", answer="4", difficulty=1, topic=topic_name, explanation="Add 2 and 2")
    test_db.add(q)
    test_db.commit()

    # Ensure initial state
    tp = test_db.query(TopicProgress).filter_by(topic=topic_name).first()
    assert tp is None

    # 1st Correct Answer
    response = client.post('/check_math', json={'id': q.id, 'answer': '4'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is True

    # Check TopicProgress created and updated
    tp = test_db.query(TopicProgress).filter_by(topic=topic_name).first()
    assert tp is not None
    assert tp.questions_correct == 1
    assert tp.mastery_level == 1 # Default start

    # 2nd Correct Answer
    client.post('/check_math', json={'id': q.id, 'answer': '4'})
    # Need to refresh or re-query to see updates if session isolation wasn't perfect,
    # but since we share the session object, it should be fine.
    # However, SQLAlchemy objects might be stale.
    test_db.expire_all()
    tp = test_db.query(TopicProgress).filter_by(topic=topic_name).first()
    assert tp.questions_correct == 2
    assert tp.mastery_level == 1

    # 3rd Correct Answer -> Mastery Level Increase
    client.post('/check_math', json={'id': q.id, 'answer': '4'})
    test_db.expire_all()
    tp = test_db.query(TopicProgress).filter_by(topic=topic_name).first()
    assert tp.questions_correct == 3
    assert tp.mastery_level == 2 # Increased!

def test_question_selection(client, test_db):
    """Verify that providing a topic argument in the GET request returns a question from that specific topic."""
    # Seed questions for two topics
    q1 = MathQuestion(text="Q1", answer="A1", difficulty=1, topic="TopicA")
    q2 = MathQuestion(text="Q2", answer="A2", difficulty=1, topic="TopicB")
    test_db.add_all([q1, q2])
    test_db.commit()

    # Request TopicA
    response = client.get('/next_math?topic=TopicA')
    assert response.status_code == 200
    data = response.get_json()
    assert data['topic'] == "TopicA"
    assert data['question'] == "Q1"

    # Request TopicB
    response = client.get('/next_math?topic=TopicB')
    assert response.status_code == 200
    data = response.get_json()
    assert data['topic'] == "TopicB"
    assert data['question'] == "Q2"

def test_explanations(client, test_db):
    """Ensure the check_math response includes the correct explanation from the database."""
    explanation_text = "5 times 5 is 25 because multiplication."
    q = MathQuestion(text="5*5", answer="25", difficulty=1, topic="Multiplication", explanation=explanation_text)
    test_db.add(q)
    test_db.commit()

    # Test correct answer
    response = client.post('/check_math', json={'id': q.id, 'answer': '25'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is True
    assert data['explanation'] == explanation_text

    # Test incorrect answer also returns explanation
    response = client.post('/check_math', json={'id': q.id, 'answer': '0'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is False
    assert data['explanation'] == explanation_text
