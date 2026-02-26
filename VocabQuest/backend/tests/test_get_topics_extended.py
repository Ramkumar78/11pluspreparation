import pytest
import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder to prevent heavy initialization and db migrations during test collection
sys.modules['seeder'] = MagicMock()

from app import app
from database import Base, TopicProgress
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope='function')
def test_db():
    """Sets up an in-memory database for testing."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def client(monkeypatch, test_db):
    """Configures the Flask test client and mocks the database session."""
    app.config['TESTING'] = True

    # Mock session factory for core_routes
    class TestSessionProxy:
        def __init__(self, session):
            self.session = session

        def __getattr__(self, name):
            return getattr(self.session, name)

        def close(self):
            pass # Don't close the shared test session during the request

        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)

    MockSession = lambda: TestSessionProxy(test_db)

    # Patch Session in core_routes to use our test database session
    monkeypatch.setattr('blueprints.core_routes.Session', MockSession)

    with app.test_client() as client:
        yield client

def test_get_topics_empty(client):
    """Verifies /get_topics returns an empty list when no topics are present in the database."""
    resp = client.get('/get_topics')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_topics_mastery_calculation(client, test_db):
    """Verifies the mastery percentage calculation and response format for various levels."""
    topics = [
        TopicProgress(topic="Arithmetic", mastery_level=1, questions_answered=10, questions_correct=5),
        TopicProgress(topic="Algebra", mastery_level=5, questions_answered=20, questions_correct=15),
        TopicProgress(topic="Geometry", mastery_level=10, questions_answered=30, questions_correct=30),
        TopicProgress(topic="Advanced", mastery_level=12, questions_answered=5, questions_correct=5)
    ]
    test_db.add_all(topics)
    test_db.commit()

    resp = client.get('/get_topics')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 4

    # Topic mapping for easy verification
    results = {t['topic']: t for t in data}

    # Verify Arithmetic (Level 1 -> 10%)
    assert results['Arithmetic']['mastery'] == 10
    assert results['Arithmetic']['level'] == 1
    assert results['Arithmetic']['correct'] == 5
    assert results['Arithmetic']['total'] == 10

    # Verify Algebra (Level 5 -> 50%)
    assert results['Algebra']['mastery'] == 50
    assert results['Algebra']['level'] == 5

    # Verify Geometry (Level 10 -> 100%)
    assert results['Geometry']['mastery'] == 100
    assert results['Geometry']['level'] == 10

    # Verify Advanced (Level 12 -> 100% capped)
    assert results['Advanced']['mastery'] == 100
    assert results['Advanced']['level'] == 12

def test_get_topics_data_format(client, test_db):
    """Verifies that the returned items contain all expected fields."""
    tp = TopicProgress(topic="Fractions", mastery_level=3, questions_answered=10, questions_correct=8)
    test_db.add(tp)
    test_db.commit()

    resp = client.get('/get_topics')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    item = data[0]

    # Check for presence of all required keys
    expected_keys = {"topic", "level", "mastery", "correct", "total"}
    assert expected_keys.issubset(item.keys())

    assert item['topic'] == "Fractions"
    assert item['level'] == 3
    assert item['mastery'] == 30
    assert item['correct'] == 8
    assert item['total'] == 10
