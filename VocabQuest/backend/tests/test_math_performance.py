import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, MathQuestion

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

        def delete(self, instance):
            self.session.delete(instance)

        def add_all(self, instances):
            self.session.add_all(instances)

        def __getattr__(self, attr):
            return getattr(self.session, attr)

    # Monkeypatch the Session in blueprints to return our test_db session
    # Also patch database.Session as it might be used directly
    monkeypatch.setattr('blueprints.math_routes.Session', lambda: NoCloseSession(test_db))
    monkeypatch.setattr('database.Session', lambda: NoCloseSession(test_db))

    # Disable rate limiter for tests
    try:
        from extensions import limiter
        limiter.enabled = False
    except ImportError:
        pass

    with app.test_client() as client:
        yield client

def test_optimization_uses_offset(client, test_db):
    """
    Verifies that the math routes use rng.randint for offset-based selection
    instead of relying on database-side sorting (order_by(func.random())).
    """
    # Setup data
    q1 = MathQuestion(text="Q1", answer="1", difficulty=5, topic="Ratio", question_type="Standard Written")
    test_db.add(q1)
    # Need user level 8 to trigger Standard Written logic for Ratio
    user = test_db.query(UserStats).first()
    if not user:
         user = UserStats(current_level=8, total_score=0, streak=0)
         test_db.add(user)
    else:
         user.current_level = 8
    test_db.commit()

    # We want to trigger the "Ratio" path
    # Mock rng.random to return 0.9 (skip generator logic)
    # Mock rng.randint to verify it's called.

    # We patch the 'rng' object imported in blueprints.math_routes
    with patch('blueprints.math_routes.rng') as mock_rng:
        mock_rng.random.return_value = 0.9
        mock_rng.randint.return_value = 0

        response = client.get('/next_math?topic=Ratio')
        assert response.status_code == 200
        data = response.get_json()

        # Verify randint was called (indicating offset logic was used)
        if not mock_rng.randint.called:
             pytest.fail("rng.randint was not called, implying offset optimization is missing.")

        assert data['question'] == "Q1"
