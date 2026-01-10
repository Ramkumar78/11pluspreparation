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
        difficulty=1,
        topic="Arithmetic"
    ))
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(monkeypatch, test_db):
    app.config['TESTING'] = True

    # Monkeypatch the Session in app.py to return our test_db session
    # Note: Since Session() is called as a constructor, we need a lambda that returns the session object
    # However, Session() returns a NEW session. Our test_db IS a session instance.
    # So we need `app.Session` to be a callable that returns `test_db`.
    TestSessionMaker = lambda: test_db
    monkeypatch.setattr('app.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_next_math(client):
    rv = client.get('/next_math')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'id' in data
    assert 'question' in data
    assert 'hashed_answer' in data
    assert data['type'] == 'math'

def test_check_math_correct(client):
    # Test checking a known answer
    # Since next_math is random (DB or generated), we can't easily rely on the previous flow
    # unless we force it. But we can test the check_math endpoint directly.

    # We'll rely on the fact that the test DB has UserStats seeded.

    res = client.post('/check_math', json={
        'answer': '4',
        'correct_answer': '4'
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is True
    assert res_data['score'] == 10 # 0 + 10

def test_check_math_incorrect(client):
    res = client.post('/check_math', json={
        'answer': '5',
        'correct_answer': '4'
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is False
    assert res_data['score'] == 0

def test_math_level_up(client):
    # User streak starts at 0.
    # We need 3 correct answers to level up.

    # 1
    client.post('/check_math', json={'answer': '4', 'correct_answer': '4'})
    # 2
    client.post('/check_math', json={'answer': '4', 'correct_answer': '4'})
    # 3
    res = client.post('/check_math', json={'answer': '4', 'correct_answer': '4'})

    data = res.get_json()
    assert data['new_level'] == 4 # Started at 3, +1 after 3 correct
