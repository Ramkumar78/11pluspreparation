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
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)
    monkeypatch.setattr('database.Session', TestSessionMaker)

    # Disable rate limiter for tests
    from extensions import limiter
    limiter.enabled = False

    with app.test_client() as client:
        yield client

def test_optimization_uses_offset(client, test_db):
    """
    Verifies that the math routes use random.randint for offset-based selection
    instead of relying on database-side sorting (order_by(func.random())).
    """
    # Setup data
    q1 = MathQuestion(text="Q1", answer="1", difficulty=5, topic="Ratio", question_type="Standard Written")
    test_db.add(q1)
    user = test_db.query(UserStats).first()
    # Level 8 triggers the Standard Written logic if topic is Ratio
    user.current_level = 8
    test_db.commit()

    # We want to trigger the "Ratio" path
    # Mock random.random to return 0.9 (skip generator logic)
    # Mock random.randint to verify it's called.
    # Note: random.randint is used by the proposed offset logic.

    with patch('blueprints.math_routes.random.random', return_value=0.9), \
         patch('blueprints.math_routes.random.randint', return_value=0) as mock_randint:

        response = client.get('/next_math?topic=Ratio')
        assert response.status_code == 200
        data = response.get_json()

        # Verify randint was called (indicating offset logic was used)
        # If the code uses order_by(func.random()), randint won't be called.
        if not mock_randint.called:
             pytest.fail("random.randint was not called, implying offset optimization is missing.")

        assert data['question'] == "Q1"
