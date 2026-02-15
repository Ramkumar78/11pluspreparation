import pytest
import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, Word, MathQuestion, ScoreHistory, ComprehensionPassage, ComprehensionQuestion

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

    # Seed enough data for SET simulation (needs 20 Math, 15 Vocab)
    for i in range(25):
        session.add(Word(text=f"word{i}", difficulty=3, definition=f"def{i}", image_url="img.jpg"))
        session.add(MathQuestion(text=f"{i}+{i}", answer=f"{i+i}", difficulty=3, topic="Mental Maths"))

    # Seed Comprehension
    passage = ComprehensionPassage(title="Test Passage", content="Content", topic="Fiction", image_url="img.jpg")
    session.add(passage)
    session.commit() # Commit to generate ID

    session.add(ComprehensionQuestion(passage_id=passage.id, question_text="Q1", options='["A", "B"]', correct_answer="A", explanation="Exp"))
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
            self.session.commit()

    # Mock the Session factory used in app.py and blueprints
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('seeder.Session', TestSessionMaker)
    monkeypatch.setattr('blueprints.mock_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_get_set_simulation_mock_test(client, test_db):
    rv = client.get('/mock_test?type=set_simulation')
    assert rv.status_code == 200
    data = rv.get_json()

    assert data['duration_minutes'] == 45
    assert len(data['items']) > 0

    # Check composition
    math_count = len([x for x in data['items'] if x['type'] == 'math'])
    vocab_count = len([x for x in data['items'] if x['type'] == 'vocab'])
    comp_count = len([x for x in data['items'] if x['type'] == 'comprehension'])

    # Should be 20 Math, 15 Vocab, 1 Comp (from seeded data)
    assert math_count == 20
    assert vocab_count == 15
    assert comp_count == 1

def test_submit_mock_with_timing(client, test_db):
    # Fetch questions to get IDs
    word = test_db.query(Word).first()
    math = test_db.query(MathQuestion).first()

    payload = {
        "answers": [
            {
                "id": word.id,
                "type": "vocab",
                "user_answer": word.text,
                "time_taken": 5.5
            },
            {
                "id": math.id,
                "type": "math",
                "user_answer": math.answer,
                "time_taken": 10.2
            }
        ]
    }

    rv = client.post('/submit_mock', json=payload)
    assert rv.status_code == 200

    # Verify DB
    history = test_db.query(ScoreHistory).order_by(ScoreHistory.id.desc()).first()
    assert history is not None

    details = json.loads(history.details)
    assert 'breakdown' in details
    assert len(details['breakdown']) == 2

    vocab_res = next(x for x in details['breakdown'] if x['type'] == 'vocab')
    math_res = next(x for x in details['breakdown'] if x['type'] == 'math')

    assert vocab_res['time_taken'] == 5.5
    assert vocab_res['topic'] == 'Vocabulary'

    assert math_res['time_taken'] == 10.2
    assert math_res['topic'] == 'Mental Maths'
