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
        title="Test Passage Title!",
        content="This is a test passage content.",
        topic="History",
        image_url=None # Explicitly None to test sanitization fallback
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

    # Mock the Session factory used in blueprints
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.comprehension_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_next_comprehension_structure(client):
    """Verify next_comprehension returns a passage with its associated questions as a JSON list."""
    rv = client.get('/next_comprehension')
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['title'] == "Test Passage Title!"
    assert 'questions' in data
    assert isinstance(data['questions'], list)
    assert len(data['questions']) == 1
    assert data['questions'][0]['text'] == "What is this?"

def test_check_comprehension_score(client, test_db):
    """Verify that check_comprehension awards 15 points for correct answers."""
    question = test_db.query(ComprehensionQuestion).first()

    # Initial score check
    user = test_db.query(UserStats).first()
    initial_score = user.total_score
    assert initial_score == 0

    rv = client.post('/check_comprehension', json={
        'question_id': question.id,
        'answer': "A test"
    })

    assert rv.status_code == 200
    data = rv.get_json()
    assert data['correct'] is True

    # Refresh user from DB
    test_db.expire(user)
    assert user.total_score == initial_score + 15
    assert data['score'] == 15

def test_next_comprehension_sanitization(client):
    """Ensure the sanitize_filename utility is called correctly for image URLs."""
    # The passage seeded has title "Test Passage Title!" and image_url=None
    # sanitize_filename("Test Passage Title!") should result in "test_passage_title"
    # Expected URL: /images/comprehension/test_passage_title.jpg

    rv = client.get('/next_comprehension')
    assert rv.status_code == 200
    data = rv.get_json()

    # We expect the fallback image URL since we set image_url=None
    assert data['image_url'] == "/images/comprehension/test_passage_title.jpg"

def test_next_comprehension_fallback(client):
    """Verify that if a requested topic doesn't exist, a random passage is still returned."""
    # Request a non-existent topic "Science" (seeded topic is "History")
    rv = client.get('/next_comprehension?topic=Science')

    assert rv.status_code == 200
    data = rv.get_json()

    # Should return the only available passage (History)
    assert data['title'] == "Test Passage Title!"
    # Ideally check that it is indeed the fallback, but since we only have one passage,
    # getting it proves the fallback worked (otherwise 404 or null).
