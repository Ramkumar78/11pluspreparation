import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, ScoreHistory

@pytest.fixture(scope='function')
def test_db():
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    session.add(UserStats(current_level=3, total_score=0, streak=0))
    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(monkeypatch, test_db):
    app.config['TESTING'] = True

    class NoCloseSession:
        def __init__(self, session):
            self.session = session
        def close(self): pass
        def __getattr__(self, attr): return getattr(self.session, attr)
        def commit(self): self.session.commit() # Allow commit

    TestSessionMaker = lambda: NoCloseSession(test_db)

    # Patch database.Session!
    monkeypatch.setattr('database.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_score_history_recording(client):
    # 1. Check initial
    rv = client.get('/get_score_history')
    initial_count = len(rv.get_json())

    # 2. Submit correct math
    client.get('/next_math')

    res = client.post('/check_math', json={
        'id': -1,
        'answer': '10',
        'correct_answer': '10'
    })
    assert res.get_json()['correct'] == True

    # 3. Check history
    rv = client.get('/get_score_history')
    new_data = rv.get_json()
    assert len(new_data) == initial_count + 1
    assert new_data[-1]['mode'] == 'math'
