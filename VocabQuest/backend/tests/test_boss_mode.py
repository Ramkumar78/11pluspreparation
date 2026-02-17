import pytest
import sys
import os
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, MathQuestion

@pytest.fixture(scope='function')
def test_db():
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)
    TestSession = sessionmaker(bind=test_engine)
    session = TestSession()

    # Initial user with streak 4 (so next correct makes it 5)
    # But wait, next_math checks existing streak.
    # If user has streak 5, next question should be boss.
    user = UserStats(current_level=3, total_score=0, streak=5)
    session.add(user)
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
        def close(self):
            pass
        def commit(self):
            self.session.commit()
        def add(self, instance):
            self.session.add(instance)
        def query(self, *args, **kwargs):
            return self.session.query(*args, **kwargs)
        def delete(self, instance):
            self.session.delete(instance)
        def __getattr__(self, attr):
            return getattr(self.session, attr)

    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)
    monkeypatch.setattr('database.Session', TestSessionMaker)

    with app.test_client() as client:
        yield client

def test_boss_trigger(client, test_db):
    """Test that a streak of 5 triggers a boss battle."""
    # Ensure streak is 5 (set in fixture)
    user = test_db.query(UserStats).first()
    assert user.streak == 5

    # Call next_math
    response = client.get('/next_math')
    assert response.status_code == 200
    data = response.get_json()

    # Assert is_boss is True (This will fail until implemented)
    # For now, I'm writing the test to fail if feature not present
    if 'is_boss' in data:
        assert data['is_boss'] is True
        assert data['boss_name'] is not None
    else:
        # Expected failure before implementation
        pytest.fail("is_boss field missing in response")

def test_boss_scoring(client, test_db):
    """Test that defeating a boss awards bonus points."""
    # Create a question
    q = MathQuestion(text="2+2", answer="4", difficulty=3, topic="Addition", explanation="Add 2 and 2")
    test_db.add(q)
    test_db.commit()

    # User score starts at 0
    user = test_db.query(UserStats).first()
    initial_score = user.total_score

    # Submit correct answer with is_boss=True
    response = client.post('/check_math', json={
        'id': q.id,
        'answer': '4',
        'is_boss': True
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['correct'] is True

    # Reload user
    test_db.expire_all()
    user = test_db.query(UserStats).first()

    # Should be +50 points (standard 10 + bonus)
    # Wait, plan said 50 total.
    if 'BOSS DEFEATED' in data['explanation']:
         assert user.total_score == initial_score + 50
    else:
         # Expected failure
         pytest.fail("Explanation does not contain BOSS DEFEATED")
