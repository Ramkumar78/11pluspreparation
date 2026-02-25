import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock seeder before importing app
sys.modules['seeder'] = MagicMock()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, VerbalReasoningQuestion, TopicProgress

@pytest.fixture(scope='function')
def test_db():
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()
    user = UserStats(current_level=3, total_score=0, streak=0)
    session.add(user)
    session.commit()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def client(monkeypatch, test_db):
    app.config['TESTING'] = True
    app.config['RATELIMIT_ENABLED'] = False

    def get_test_session():
        return test_db

    monkeypatch.setattr('blueprints.verbal_reasoning_routes.Session', get_test_session)
    monkeypatch.setattr('database.Session', get_test_session)

    with app.test_client() as client:
        yield client

def test_check_verbal_empty_json(client):
    # This should fail if `request.json` is None, but the existing code handles `if not data`.
    # However, if we send Content-Type: application/json but empty body, `request.json` might be None.
    response = client.post('/check_verbal', data='', content_type='application/json')
    # Depending on flask version, this might be 400 (Bad Request) automatically or None
    assert response.status_code == 400

def test_check_verbal_list_json(client):
    # Sending a JSON list instead of a dict
    # This should cause AttributeError: 'list' object has no attribute 'get'
    try:
        response = client.post('/check_verbal', json=["some", "list"])
    except AttributeError:
        pytest.fail("AttributeError raised: input validation missing for list type")

    assert response.status_code == 400

def test_check_verbal_no_id(client):
    # Sending a JSON dict without 'id'
    # q_id = data.get('id') -> None
    # filter_by(id=None)
    response = client.post('/check_verbal', json={"answer": "something"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is False
    assert data['explanation'] == "Question not found."

def test_check_verbal_malformed_json(client):
    response = client.post('/check_verbal', data='{invalid_json', content_type='application/json')
    assert response.status_code == 400

def test_check_verbal_id_is_list(client):
    # Sending a JSON dict with list ID should return 400
    response = client.post('/check_verbal', json={"answer": "something", "id": [1, 2]})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Invalid ID format"

def test_check_verbal_invalid_id_type(client):
    # Sending a JSON dict with invalid string ID should return 400
    response = client.post('/check_verbal', json={"answer": "something", "id": "invalid"})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Invalid ID format"
