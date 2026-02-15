import pytest
import sys
import os
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from database import Base, UserStats, MathQuestion, TopicProgress

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

def test_math_standard_written_logic(client, test_db):
    """
    Test that 'Standard Written' questions are prioritized when
    mastery_level > 7 and topic is 'Ratio' or 'Algebra'.
    """
    # 1. Seed Questions
    # Q1: High Difficulty, Multiple Choice (Should NOT be picked if logic works)
    q_mc = MathQuestion(
        text="Hard MC Question",
        answer="100",
        difficulty=9,
        topic="Ratio",
        explanation="Test",
        question_type="Multiple Choice"
    )
    # Q2: High Difficulty, Standard Written (Should BE picked)
    q_sw = MathQuestion(
        text="Hard SW Question",
        answer="200",
        difficulty=9,
        topic="Ratio",
        explanation="Test",
        question_type="Standard Written"
    )
    test_db.add_all([q_mc, q_sw])
    test_db.commit()

    # 2. Set User Level to 8 (High)
    user = test_db.query(UserStats).first()
    user.current_level = 8
    test_db.commit()

    # 3. Request 'Ratio'
    response = client.get('/next_math?topic=Ratio')
    assert response.status_code == 200
    data = response.get_json()

    # Should be the Standard Written question
    assert data['question'] == "Hard SW Question"
    assert data['question_type'] == "Standard Written"

    # 4. Verify Lower Level Behavior
    # Set User Level to 5
    user.current_level = 5
    test_db.commit()

    # Now logic: min_diff=4, max_diff=7.
    # But our questions are diff 9. So neither should be picked by difficulty filter.
    # We need questions in range 4-7 to test lower level behavior.

    q_mc_easy = MathQuestion(text="Easy MC", answer="1", difficulty=5, topic="Ratio", question_type="Multiple Choice")
    q_sw_easy = MathQuestion(text="Easy SW", answer="1", difficulty=5, topic="Ratio", question_type="Standard Written")
    test_db.add_all([q_mc_easy, q_sw_easy])
    test_db.commit()

    response = client.get('/next_math?topic=Ratio')
    data = response.get_json()
    assert data['question'] in ["Easy MC", "Easy SW"]

def test_math_algebra_standard_written(client, test_db):
    """Test specific logic for Algebra as well."""
    q_sw = MathQuestion(
        text="Algebra SW",
        answer="X",
        difficulty=10,
        topic="Algebra",
        question_type="Standard Written"
    )
    test_db.add(q_sw)
    user = test_db.query(UserStats).first()
    user.current_level = 9
    test_db.commit()

    response = client.get('/next_math?topic=Algebra')
    data = response.get_json()
    assert data['question'] == "Algebra SW"
    assert data['question_type'] == "Standard Written"
