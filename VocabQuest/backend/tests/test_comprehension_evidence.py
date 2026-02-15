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
        title="Evidence Test Passage",
        content="The quick brown fox jumps over the lazy dog.",
        topic="Testing",
        image_url=None
    )
    session.add(passage)
    session.flush()

    question = ComprehensionQuestion(
        passage_id=passage.id,
        question_text="What does the fox do?",
        options=json.dumps(["Jumps", "Sleeps"]),
        correct_answer="Jumps",
        explanation="It jumps.",
        evidence_text="The quick brown fox jumps over the lazy dog."
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

    # Mock the Session factory used in blueprints
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.comprehension_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_evidence_bonus_logic(client, test_db):
    """Verify that check_comprehension awards bonus points for correct evidence."""
    question = test_db.query(ComprehensionQuestion).first()

    # 1. Correct Answer + Correct Evidence (Exact Match)
    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Jumps",
        'evidence': "The quick brown fox jumps over the lazy dog."
    })
    data = rv.get_json()
    assert data['correct'] is True
    assert data['evidence_bonus'] is True
    # Score: 0 -> 15 (base) + 5 (bonus) = 20
    user = test_db.query(UserStats).first()
    assert user.total_score == 20

    # Reset score for next check
    user.total_score = 0
    test_db.commit()

    # 2. Correct Answer + Partial Evidence (User selects sub-phrase)
    # Evidence text: "The quick brown fox jumps over the lazy dog."
    # User selects: "fox jumps over"
    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Jumps",
        'evidence': "fox jumps over"
    })
    data = rv.get_json()
    assert data['correct'] is True
    assert data['evidence_bonus'] is True
    assert user.total_score == 20

    # Reset
    user.total_score = 0
    test_db.commit()

    # 3. Correct Answer + Wrong Evidence
    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Jumps",
        'evidence': "lazy dog sleeps"
    })
    data = rv.get_json()
    assert data['correct'] is True
    assert data['evidence_bonus'] is False
    assert user.total_score == 15 # Only base score

    # Reset
    user.total_score = 0
    test_db.commit()

    # 4. Wrong Answer + Correct Evidence
    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Sleeps",
        'evidence': "The quick brown fox jumps over the lazy dog."
    })
    data = rv.get_json()
    assert data['correct'] is False
    assert data.get('evidence_bonus', False) is False
    assert user.total_score == 0

    # 5. Evidence too short
    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "Jumps",
        'evidence': "The" # Too short (< 5 chars)
    })
    data = rv.get_json()
    assert data['correct'] is True
    assert data['evidence_bonus'] is False
    assert user.total_score == 15
