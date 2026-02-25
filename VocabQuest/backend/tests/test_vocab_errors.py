import pytest
import sys
import os
import json
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
    app.config['RATELIMIT_ENABLED'] = False
    limiter.enabled = False

    class TestSessionProxy:
        def __init__(self, session):
            self.session = session
        def __getattr__(self, name):
            return getattr(self.session, name)
        def close(self):
            pass
        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)
        def add(self, *args, **kwargs):
            return self.session.add(*args, **kwargs)
        def commit(self, *args, **kwargs):
            return self.session.commit(*args, **kwargs)

    MockSession = lambda: TestSessionProxy(test_db)
    monkeypatch.setattr('blueprints.vocab_routes.Session', MockSession)

    with app.test_client() as client:
        yield client

def test_check_answer_invalid_id_type(client):
    """Test non-integer id results in 400 Invalid ID."""
    # Scenario: ID is a string "1"
    resp = client.post('/check_answer', json={'id': "1", 'spelling': 'apple'})
    assert resp.status_code == 400
    assert resp.get_json()['error'] == "Invalid ID"

def test_check_answer_missing_id(client):
    """Test missing id results in 400 Invalid ID."""
    # Scenario: ID is missing (None)
    resp = client.post('/check_answer', json={'spelling': 'apple'})
    assert resp.status_code == 400
    assert resp.get_json()['error'] == "Invalid ID"

def test_check_answer_invalid_spelling_type(client):
    """Test non-string spelling results in 400 Invalid spelling format."""
    # Scenario: Spelling is an integer 123
    resp = client.post('/check_answer', json={'id': 1, 'spelling': 123})
    assert resp.status_code == 400
    assert resp.get_json()['error'] == "Invalid spelling format"

def test_check_answer_empty_json_body(client):
    """Test empty JSON body results in 400 No data provided."""
    # Scenario: Body is {}
    resp = client.post('/check_answer', json={})
    assert resp.status_code == 400
    assert resp.get_json()['error'] == "No data provided"

def test_check_answer_malformed_json_list(client):
    """Test list JSON body results in 400 Invalid data format (not crash)."""
    # Scenario: Body is ["invalid"]
    # Currently this would cause 500 without the fix.
    resp = client.post('/check_answer', json=["invalid"])
    assert resp.status_code == 400
    # We expect "Invalid data format" or "No data provided" depending on implementation,
    # but strictly speaking for list it should be invalid format if list is not empty.
    # Current implementation check `if not data` handles empty list, but not populated list.
    assert resp.get_json()['error'] == "Invalid data format"
