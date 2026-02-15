import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, VerbalReasoningQuestion, TopicProgress

@pytest.fixture(scope='function')
def test_db():
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    user = UserStats(current_level=3, total_score=0, streak=0)
    session.add(user)
    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(monkeypatch, test_db):
    app.config['TESTING'] = True
    app.config['RATELIMIT_ENABLED'] = False

    # Define a session maker that returns our test session
    def get_test_session():
        return test_db

    monkeypatch.setattr('blueprints.verbal_reasoning_routes.Session', get_test_session)
    monkeypatch.setattr('database.Session', get_test_session)

    with app.test_client() as client:
        yield client

def test_next_verbal(client, test_db):
    # Seed a question
    q = VerbalReasoningQuestion(
        question_type="move_one_letter",
        question_text="Move one letter...",
        content="TEST CONTENT",
        answer="T",
        difficulty=3,
        explanation="Explanation"
    )
    test_db.add(q)
    test_db.commit()

    response = client.get('/next_verbal')
    assert response.status_code == 200
    data = response.get_json()
    assert data['question'] == "Move one letter..."
    assert data['content'] == "TEST CONTENT"
    assert data['topic'] == "Verbal Reasoning"

def test_check_verbal_correct(client, test_db):
    q = VerbalReasoningQuestion(
        question_type="missing_word",
        question_text="Fill in...",
        content="The c_t sat.",
        answer="cat",
        difficulty=1,
        explanation="It is a cat."
    )
    test_db.add(q)
    test_db.commit()

    response = client.post('/check_verbal', json={'id': q.id, 'answer': 'cat'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is True
    assert data['score'] == 10
    assert data['explanation'] == "It is a cat."

    # Verify stats update
    user = test_db.query(UserStats).first()
    assert user.total_score == 10
    assert user.streak == 1

    # Verify Topic Progress
    tp = test_db.query(TopicProgress).filter_by(topic="Verbal Reasoning").first()
    assert tp is not None
    assert tp.questions_correct == 1

def test_check_verbal_wrong(client, test_db):
    q = VerbalReasoningQuestion(
        question_type="missing_word",
        question_text="Fill in...",
        content="The d_g sat.",
        answer="dog",
        difficulty=1,
        explanation="It is a dog."
    )
    test_db.add(q)
    test_db.commit()

    response = client.post('/check_verbal', json={'id': q.id, 'answer': 'cat'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is False
    assert data['explanation'] == "It is a dog."

    user = test_db.query(UserStats).first()
    assert user.streak == 0
