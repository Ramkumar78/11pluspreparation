import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats

@pytest.fixture(scope='function')
def test_db():
    # Create an in-memory SQLite database for testing
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)

    # Create a configured "Session" class
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Seed initial data
    user = UserStats(current_level=3, total_score=0, streak=0)
    session.add(user)
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

        def commit(self):
            self.session.commit()

        def add(self, instance):
            self.session.add(instance)

        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)

        def __getattr__(self, attr):
            return getattr(self.session, attr)

    # Monkeypatch the Session in blueprints to return our test_db session
    TestSessionMaker = lambda: NoCloseSession(test_db)

    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)
    monkeypatch.setattr('database.Session', TestSessionMaker)

    # Disable limiter for testing
    from extensions import limiter
    limiter.enabled = False

    with app.test_client() as client:
        yield client

def test_math_challenge_endpoint(client):
    """Verify the challenge endpoint returns a valid question structure."""
    response = client.get('/api/math/challenge')
    assert response.status_code == 200
    data = response.get_json()

    # Verify structure
    assert 'question' in data
    assert 'generated_answer_check' in data
    assert 'explanation_text' in data
    assert 'topic' in data
    assert data['type'] == 'math'
    assert data['question_type'] == 'Challenge'
    assert data['id'] == -1

    # Verify content is from the seeded list
    assert isinstance(data['question'], str)
    assert len(data['question']) > 0
    assert isinstance(data['explanation_text'], str)
    assert len(data['explanation_text']) > 0
