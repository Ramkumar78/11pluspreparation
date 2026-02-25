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
from database import Base, ScoreHistory

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

    # Mock session factory for core_routes
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

    # Patch where Session is imported in core_routes
    monkeypatch.setattr('blueprints.core_routes.Session', MockSession)

    with app.test_client() as client:
        yield client

def test_leaderboard_empty(client):
    """Verifies that the endpoint returns an empty list when no scores are present."""
    resp = client.get('/leaderboard')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_leaderboard_with_data(client, test_db):
    """Verifies that the endpoint returns the scores in descending order."""
    # Add some scores
    s1 = ScoreHistory(score=100, max_score=100, mode='math')
    s2 = ScoreHistory(score=200, max_score=200, mode='vocab')
    s3 = ScoreHistory(score=150, max_score=150, mode='spag')
    test_db.add_all([s1, s2, s3])
    test_db.commit()

    resp = client.get('/leaderboard')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 3
    # Sorted by score descending: 200, 150, 100
    assert data[0]['score'] == 200
    assert data[1]['score'] == 150
    assert data[2]['score'] == 100

def test_leaderboard_limit(client, test_db):
    """Verifies that the endpoint returns at most 10 scores."""
    # Add 12 scores
    for i in range(12):
        test_db.add(ScoreHistory(score=i*10, max_score=100, mode='math'))
    test_db.commit()

    resp = client.get('/leaderboard')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 10
    # Top score should be 110 (11*10)
    assert data[0]['score'] == 110

def test_leaderboard_data_format(client, test_db):
    """Verifies that the returned data contains the expected fields."""
    s1 = ScoreHistory(score=100, max_score=120, mode='verbal')
    test_db.add(s1)
    test_db.commit()

    resp = client.get('/leaderboard')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    item = data[0]
    assert 'score' in item
    assert 'max_score' in item
    assert 'mode' in item
    assert 'date' in item
    assert item['score'] == 100
    assert item['max_score'] == 120
    assert item['mode'] == 'verbal'
    # Date format check (YYYY-MM-DD HH:MM)
    import re
    assert re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', item['date'])
