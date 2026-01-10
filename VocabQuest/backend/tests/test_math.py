import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, MathQuestion

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

    # Monkeypatch the Session in app.py to return our test_db session
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('app.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_next_math(client):
    rv = client.get('/next_math')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'id' in data
    assert 'question' in data
    assert data['type'] == 'math'

    # Check if generated or from DB
    if data['id'] == -1:
        assert 'generated_answer_check' in data
    else:
        assert 'topic' in data

def test_check_math_correct(client, test_db):
    # Retrieve the question ID from DB
    q = test_db.query(MathQuestion).first()
    q_id = q.id # Store id to avoid access after potential expire

    res = client.post('/check_math', json={
        'id': q_id,
        'answer': '4',
        'correct_answer': '4' # Should be ignored for DB questions
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is True
    assert res_data['explanation'] == "2 plus 2 is 4."
    assert res_data['score'] == 10 # 0 + 10

def test_check_math_incorrect(client, test_db):
    q = test_db.query(MathQuestion).first()
    q_id = q.id

    res = client.post('/check_math', json={
        'id': q_id,
        'answer': '5',
        'correct_answer': '4'
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is False
    assert res_data['explanation'] == "2 plus 2 is 4."
    assert res_data['score'] == 0

def test_math_level_up(client, test_db):
    # User streak starts at 0.
    # We need 2 correct answers to level up.

    q = test_db.query(MathQuestion).first()
    q_id = q.id

    # 1
    client.post('/check_math', json={'id': q_id, 'answer': '4', 'correct_answer': '4'})
    # 2
    res = client.post('/check_math', json={'id': q_id, 'answer': '4', 'correct_answer': '4'})

    data = res.get_json()
    assert data['new_level'] == 4 # Started at 3, +1 after 2 correct
