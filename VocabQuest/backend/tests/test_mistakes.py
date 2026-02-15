import pytest
import json
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, Mistakes

@pytest.fixture(scope='function')
def test_db():
    # Create an in-memory SQLite database for testing
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)

    # Create a configured "Session" class
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

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

        def add(self, obj):
            self.session.add(obj)

        def commit(self):
            self.session.commit()

        def rollback(self):
            self.session.rollback()

        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)

        def __getattr__(self, attr):
            return getattr(self.session, attr)

    # Mock the Session factory used in core_routes
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.core_routes.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_record_mistake_success(client, test_db):
    data = {
        "user_id": 1,
        "question_type": "Maths-Algebra",
        "question_text": "Solve for x: 2x = 4",
        "user_answer": "3",
        "correct_answer": "2"
    }

    response = client.post('/api/record_mistake', json=data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Mistake recorded successfully"}

    # Verify DB
    mistake = test_db.query(Mistakes).first()
    assert mistake is not None
    assert mistake.question_text == "Solve for x: 2x = 4"
    assert mistake.user_answer == "3"

def test_record_mistake_missing_fields(client):
    data = {
        "user_id": 1,
        # Missing question_type
        "question_text": "Solve for x: 2x = 4",
        "user_answer": "3",
        "correct_answer": "2"
    }

    response = client.post('/api/record_mistake', json=data)
    assert response.status_code == 400
    assert "Missing field" in response.get_json()["error"]

def test_record_mistake_no_data(client):
    # Depending on flask version and client implementation, sending json={} might parse as empty dict
    # sending no data might parse as None
    response = client.post('/api/record_mistake', data=None, content_type='application/json')
    # If using json={} in post, it sends {}, request.json is {}
    # The code checks `if not data`. Empty dict is False in python.
    # Wait, request.json returns None if body is empty or not json.
    # If I send json={}, request.json is {}.

    # My code:
    # data = request.json
    # if not data: return ...

    # If I send {}, `if not {}` is True. So it returns 400.

    response = client.post('/api/record_mistake', json={})
    assert response.status_code == 400
