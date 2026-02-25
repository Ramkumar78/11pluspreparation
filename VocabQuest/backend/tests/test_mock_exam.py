import pytest
import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import MagicMock
sys.modules['seeder'] = MagicMock()

from app import app
from database import Base, UserStats, Word, MathQuestion

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
    session.add(Word(text="testword", difficulty=3, definition="A test word", image_url="http://example.com/img.png"))
    session.add(MathQuestion(text="2 + 2", answer="4", difficulty=3, topic="Mental Maths"))
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

        def commit(self):
            # We want to be able to commit in the logic, but for tests we might want to check state
            # but since we are using in-memory DB and scope=function, commits are fine.
            self.session.commit()

    # Mock the Session factory used in app.py and blueprints
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('seeder.Session', TestSessionMaker)
    monkeypatch.setattr('blueprints.mock_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_get_mock_test(client, test_db):
    rv = client.get('/mock_test')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'test_id' in data
    assert 'items' in data
    assert len(data['items']) > 0

    # Check if we have both types (since we seeded one of each)
    has_math = any(item['type'] == 'math' for item in data['items'])
    has_vocab = any(item['type'] == 'vocab' for item in data['items'])

    # Since we limit 10, and have 1 math and 1 vocab in seed, we should have both
    assert has_math
    assert has_vocab

def test_submit_mock_correct(client, test_db):
    # Fetch questions to get IDs
    word = test_db.query(Word).first()
    math = test_db.query(MathQuestion).first()

    payload = {
        "answers": [
            {
                "id": word.id,
                "type": "vocab",
                "user_answer": "testword"
            },
            {
                "id": math.id,
                "type": "math",
                "user_answer": "4"
            }
        ]
    }

    rv = client.post('/submit_mock', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['total_score'] == 20 # 10 points each
    assert data['percentage'] == 100
    assert len(data['breakdown']) == 2
    assert data['breakdown'][0]['correct'] is True
    assert data['breakdown'][1]['correct'] is True

def test_submit_mock_incorrect(client, test_db):
    # Fetch questions to get IDs
    word = test_db.query(Word).first()
    math = test_db.query(MathQuestion).first()

    payload = {
        "answers": [
            {
                "id": word.id,
                "type": "vocab",
                "user_answer": "wrong"
            },
            {
                "id": math.id,
                "type": "math",
                "user_answer": "5"
            }
        ]
    }

    rv = client.post('/submit_mock', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['total_score'] == 0
    assert data['percentage'] == 0
    assert data['breakdown'][0]['correct'] is False
    assert data['breakdown'][1]['correct'] is False

def test_submit_mock_mixed(client, test_db):
    # Fetch questions to get IDs
    word = test_db.query(Word).first()
    math = test_db.query(MathQuestion).first()

    payload = {
        "answers": [
            {
                "id": word.id,
                "type": "vocab",
                "user_answer": "testword"
            },
            {
                "id": math.id,
                "type": "math",
                "user_answer": "5" # Wrong
            }
        ]
    }

    rv = client.post('/submit_mock', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['total_score'] == 10
    assert data['percentage'] == 50

def test_submit_mock_partial_answers(client, test_db):
    # Fetch questions to get IDs
    word = test_db.query(Word).first()
    math = test_db.query(MathQuestion).first()

    # User answers one, leaves one empty
    payload = {
        "answers": [
            {
                "id": word.id,
                "type": "vocab",
                "user_answer": "testword" # Correct, answered
            },
            {
                "id": math.id,
                "type": "math",
                "user_answer": "" # Unanswered
            }
        ]
    }

    rv = client.post('/submit_mock', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()

    # Max score should be 10 (1 question answered * 10)
    # Total score should be 10 (1 correct)
    assert data['max_score'] == 10
    assert data['total_score'] == 10
    assert data['percentage'] == 100
