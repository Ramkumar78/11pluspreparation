import pytest
import json
from unittest.mock import MagicMock, patch
from flask import Flask
from database import Session, UserStats, MathQuestion, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the blueprint - assuming the app structure allows this
# We might need to adjust sys.path if not running from root, but the environment seems to handle it.
from blueprints.math_routes import math_bp

# Setup a test app
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(math_bp)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_session():
    # Create an in-memory SQLite db
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Patch the Session in the math_routes module
    with patch('blueprints.math_routes.Session', return_value=session):
        yield session

    session.close()

def test_boss_mode_alignment_geometry(client, mock_session):
    # Setup user with streak 5 (trigger boss)
    user = UserStats(current_level=5, total_score=100, streak=5)
    mock_session.add(user)

    # Add a Geometry question to DB so we can fetch it
    q = MathQuestion(topic="Geometry", text="Cube Net?", answer="Yes", difficulty=5, question_type="Multiple Choice")
    mock_session.add(q)
    mock_session.commit()

    # Request Geometry topic
    response = client.get('/next_math?topic=Geometry')
    data = response.get_json()

    assert data['is_boss'] == True
    assert data['topic'] == "Geometry"
    # The bug: Boss name is random, so it MIGHT be "The Geometry Giant" or it might not.
    # The fix requirement: It MUST be "The Geometry Giant" for Geometry.

    # We assert that it is "The Geometry Giant" to demonstrate the requirement.
    # This might fail before the fix.
    assert data['boss_name'] == "The Geometry Giant"

def test_boss_mode_alignment_mental_maths(client, mock_session):
    # Setup user with streak 5
    user = UserStats(current_level=5, total_score=100, streak=5)
    mock_session.add(user)
    mock_session.commit()

    # Request Mental Maths
    response = client.get('/next_math?topic=Mental Maths')
    data = response.get_json()

    assert data['is_boss'] == True
    assert data['topic'] == "Mental Maths"

    # Should NOT be "The Geometry Giant" or "The Algebra Alien"
    inappropriate_bosses = ["The Geometry Giant", "The Algebra Alien", "The Fraction Phantom", "Professor Percent"]
    assert data['boss_name'] not in inappropriate_bosses

def test_boss_mode_alignment_algebra(client, mock_session):
    # Setup user with streak 5
    user = UserStats(current_level=5, total_score=100, streak=5)
    mock_session.add(user)

    # Add Algebra question
    q = MathQuestion(topic="Algebra", text="x + 2 = 4", answer="2", difficulty=5)
    mock_session.add(q)
    mock_session.commit()

    # Request Algebra
    response = client.get('/next_math?topic=Algebra')
    data = response.get_json()

    assert data['is_boss'] == True
    assert data['topic'] == "Algebra"
    assert data['boss_name'] == "The Algebra Alien"
