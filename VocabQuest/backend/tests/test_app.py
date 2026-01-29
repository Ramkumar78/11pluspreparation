import pytest
import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app, init_db
from database import Base, UserStats, Word

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
    monkeypatch.setattr('blueprints.vocab_routes.Session', TestSessionMaker)

    # Mock get_cartoon_image just in case
    monkeypatch.setattr('app.get_cartoon_image', lambda x: "http://mock.image/url", raising=False)

    with app.test_client() as client:
        yield client

def test_next_word(client):
    rv = client.get('/next_word')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'id' in data
    assert 'image' in data
    assert 'tts_text' in data
    assert data['streak'] == 0

def test_check_answer_correct(client, test_db):
    word = test_db.query(Word).filter_by(text="testword").first()
    word_id = word.id

    # In our seed, word is "testword"
    correct_text = "testword"

    # Submit correct answer
    res = client.post('/check_answer', json={
        'id': word_id,
        'spelling': correct_text
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is True
    assert res_data['score'] > 0

def test_check_answer_incorrect(client, test_db):
    # Get a word
    word = test_db.query(Word).first()
    word_id = word.id

    # Submit wrong answer
    res = client.post('/check_answer', json={
        'id': word_id,
        'spelling': 'wronganswerxyz'
    })
    assert res.status_code == 200
    res_data = res.get_json()
    assert res_data['correct'] is False
    assert res_data['score'] == 0

def test_streak_logic(client, test_db):
    # 1. Get word
    word = test_db.query(Word).first()
    word_id = word.id
    text = "testword"

    # 2. Correct Answer
    client.post('/check_answer', json={'id': word_id, 'spelling': text})

    # 3. Get next word -> Check streak
    rv2 = client.get('/next_word')
    data2 = rv2.get_json()
    assert data2['streak'] == 1

def test_input_validation(client):
    res = client.post('/check_answer', json={'id': 'not-an-int', 'spelling': 'test'})
    assert res.status_code == 400

    res = client.post('/check_answer', json={'id': 1, 'spelling': 123})
    assert res.status_code == 400
