import pytest
import sys
import os
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder to prevent heavy initialization
sys.modules['seeder'] = MagicMock()

from app import app
from database import Base, UserStats, Word
from extensions import limiter
import bleach

# Fixtures for DB and Client
@pytest.fixture(scope='function')
def test_db():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def client(monkeypatch, test_db):
    app.config['TESTING'] = True
    app.config['RATELIMIT_ENABLED'] = False # Disable rate limiting for tests
    limiter.enabled = False # Explicitly disable limiter

    # Mock session factory for blueprints
    class TestSessionProxy:
        def __init__(self, session):
            self.session = session

        def __getattr__(self, name):
            return getattr(self.session, name)

        def close(self):
            pass # Don't close the shared test session

        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)

        def add(self, *args, **kwargs):
            return self.session.add(*args, **kwargs)

        def commit(self, *args, **kwargs):
            return self.session.commit(*args, **kwargs)

    MockSession = lambda: TestSessionProxy(test_db)

    # Patch where Session is imported in vocab_routes
    monkeypatch.setattr('blueprints.vocab_routes.Session', MockSession)

    with app.test_client() as client:
        yield client

def test_adaptive_learning(client, test_db):
    """
    Test Adaptive Learning: Verify that check_answer increases current_level after 2 correct answers
    and decreases it immediately after 1 wrong answer.
    """
    # Setup user
    user = UserStats(current_level=5, streak=0, total_score=0)
    test_db.add(user)

    # Setup a word
    word = Word(text="apple", difficulty=5, definition="fruit", image_url="apple.jpg")
    test_db.add(word)
    test_db.commit()

    word_id = word.id

    # 1. First Correct Answer (Streak 1)
    # Should increase streak, score, but NOT level (streak % 2 != 0)
    resp = client.post('/check_answer', json={'id': word_id, 'spelling': 'apple'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['correct'] is True
    assert data['new_level'] == 5

    # Verify in DB
    test_db.expire_all() # Refresh
    user = test_db.query(UserStats).first()
    assert user.streak == 1
    assert user.current_level == 5

    # 2. Second Correct Answer (Streak 2)
    # Should increase streak to 2, level should increase (streak % 2 == 0)
    resp = client.post('/check_answer', json={'id': word_id, 'spelling': 'apple'})
    data = resp.get_json()
    assert data['new_level'] == 6

    test_db.expire_all()
    user = test_db.query(UserStats).first()
    assert user.streak == 2
    assert user.current_level == 6

    # 3. Wrong Answer
    # Should reset streak, decrease level immediately
    resp = client.post('/check_answer', json={'id': word_id, 'spelling': 'wrong'})
    data = resp.get_json()
    assert data['correct'] is False
    assert data['new_level'] == 5 # 6 - 1 = 5

    test_db.expire_all()
    user = test_db.query(UserStats).first()
    assert user.streak == 0
    assert user.current_level == 5

def test_filtering_logic(client, test_db):
    """
    Test Filtering: Mock the database to ensure next_word correctly filters words
    within the +/- 1 difficulty range of the user's level.
    """
    # User level 5
    user = UserStats(current_level=5)
    test_db.add(user)

    # Words
    # Level 5 +/- 1 => 4, 5, 6 are valid candidates
    w1 = Word(text="level3", difficulty=3, definition="d", image_url="img") # Too easy
    w2 = Word(text="level4", difficulty=4, definition="d", image_url="img") # OK
    w3 = Word(text="level5", difficulty=5, definition="d", image_url="img") # OK
    w4 = Word(text="level6", difficulty=6, definition="d", image_url="img") # OK
    w5 = Word(text="level7", difficulty=7, definition="d", image_url="img") # Too hard

    test_db.add_all([w1, w2, w3, w4, w5])
    test_db.commit()

    # Call next_word multiple times to verify we only get 4, 5, 6
    difficulties_seen = set()
    # 30 calls shouldn't trigger rate limit if disabled
    for _ in range(30):
        resp = client.get('/next_word')
        assert resp.status_code == 200, f"Failed with {resp.status_code}"
        data = resp.get_json()
        diff = data['difficulty']
        difficulties_seen.add(diff)
        assert diff in [4, 5, 6], f"Difficulty {diff} should not be selected for user level 5"

    # Verify we saw at least some valid ones
    assert len(difficulties_seen) > 0

def test_safety_check_empty_user(client, test_db):
    """
    Test Safety Checks: Verify the behavior when UserStats is empty (it should auto-initialize).
    """
    # Ensure DB is empty of UserStats
    test_db.query(UserStats).delete()
    test_db.commit()

    # Add a word so next_word can return something
    test_db.add(Word(text="test", difficulty=3, definition="d", image_url="img"))
    test_db.commit()

    # Call next_word
    resp = client.get('/next_word')
    assert resp.status_code == 200

    # Check that user was created
    user = test_db.query(UserStats).first()
    assert user is not None
    assert user.current_level == 3 # Default

def test_sanitization(client, test_db, monkeypatch):
    """
    Test Sanitization: Ensure bleach.clean is working by sending HTML tags in the answer.
    """
    # Setup
    word = Word(text="apple", difficulty=3, definition="d", image_url="img")
    user = UserStats(current_level=3)
    test_db.add(word)
    test_db.add(user)
    test_db.commit()

    # Spy on bleach.clean
    real_clean = bleach.clean
    mock_clean = MagicMock(side_effect=real_clean)
    monkeypatch.setattr('blueprints.vocab_routes.bleach.clean', mock_clean)

    # Send HTML: <b>apple</b>
    payload = {'id': word.id, 'spelling': '<b>apple</b>'}
    resp = client.post('/check_answer', json=payload)
    data = resp.get_json()

    # Verify bleach.clean was called
    assert mock_clean.called
    assert mock_clean.call_args[0][0] == '<b>apple</b>'

    # Note: bleach.clean by default escapes tags, so '<b>apple</b>' becomes '&lt;b&gt;apple&lt;/b&gt;'
    # This does not match 'apple', so it should be incorrect.
    # We verify that the system processed it and marked it incorrect (didn't crash).
    assert data['correct'] is False

def test_check_answer_errors(client, test_db):
    """
    Test Error Handling: Verify that check_answer returns 400 for invalid inputs.
    """
    # Test Case 1: Non-integer word_id (e.g. string "1")
    resp = client.post('/check_answer', json={'id': "1", 'spelling': 'apple'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['error'] == "Invalid ID"

    # Test Case 2: Missing word_id (word_id is None)
    # If key 'id' is missing, data.get('id') returns None, which is not int.
    resp = client.post('/check_answer', json={'spelling': 'apple'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['error'] == "Invalid ID"

    # Test Case 3: Non-string spelling (e.g. integer 123)
    resp = client.post('/check_answer', json={'id': 1, 'spelling': 123})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['error'] == "Invalid spelling format"
