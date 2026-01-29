import pytest
import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, ComprehensionPassage, ComprehensionQuestion

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

    passage = ComprehensionPassage(
        title="Test Passage",
        content="This is a test passage content.",
        topic="Test Topic"
    )
    session.add(passage)
    session.flush()

    question = ComprehensionQuestion(
        passage_id=passage.id,
        question_text="What is this?",
        options=json.dumps(["A test", "A joke", "A story", "Nothing"]),
        correct_answer="A test",
        explanation="It says so."
    )
    session.add(question)

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

    # Mock the Session factory used in app.py and blueprints
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('app.Session', TestSessionMaker)
    monkeypatch.setattr('blueprints.comprehension_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_next_comprehension(client):
    rv = client.get('/next_comprehension')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'id' in data
    assert 'title' in data
    assert 'content' in data
    assert 'questions' in data
    assert len(data['questions']) > 0
    assert data['title'] == "Test Passage"

def test_next_comprehension_with_topic(client):
    rv = client.get('/next_comprehension?topic=Test Topic')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['topic'] == "Test Topic"

def test_check_comprehension_correct(client, test_db):
    question = test_db.query(ComprehensionQuestion).first()

    res = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "A test"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert data['correct'] is True
    assert data['score'] == 15 # Initial 0 + 15

def test_check_comprehension_incorrect(client, test_db):
    question = test_db.query(ComprehensionQuestion).first()

    res = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Wrong Answer"
    })

    assert res.status_code == 200
    data = res.get_json()
    assert data['correct'] is False
    assert data['correct_answer'] == "A test"
