import pytest
import sys
import os
import random
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder before importing app to prevent heavy initialization
sys.modules['seeder'] = MagicMock()

from app import app
from database import Base, UserStats, MathQuestion, TopicProgress
from math_seed import generate_algebra_substitution, generate_ratio_proportion, generate_fdp_conversion
from math_new_generators import generate_bearings, generate_pie_charts, generate_pictograms, generate_bar_charts, generate_transformations, generate_line_graphs

# Fixtures for Integration Tests
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
    class NoCloseSession:
        def __init__(self, session):
            self.session = session
        def close(self): pass
        def commit(self): self.session.commit()
        def add(self, instance): self.session.add(instance)
        def query(self, *args, **kwargs): return self.session.query(*args, **kwargs)
        def __getattr__(self, attr): return getattr(self.session, attr)
    TestSessionMaker = lambda: NoCloseSession(test_db)
    monkeypatch.setattr('blueprints.math_routes.Session', TestSessionMaker)
    monkeypatch.setattr('database.Session', TestSessionMaker)
    with app.test_client() as client:
        yield client

# Unit Tests for Generators

def test_generate_algebra_substitution():
    for _ in range(10): # Test multiple times for randomness
        result = generate_algebra_substitution(5)
        assert "question" in result
        assert "options" in result
        assert "answer" in result
        assert "explanation" in result
        assert len(result["options"]) == 5
        assert result["answer"] in result["options"]
        # Basic content check
        assert "If" in result["question"] or "$" in result["question"]
        # Ensure answer is positive integer string
        assert int(result["answer"]) > 0

def test_generate_ratio_proportion():
    for _ in range(10):
        result = generate_ratio_proportion(5)
        assert "question" in result
        assert "options" in result
        assert "answer" in result
        assert "explanation" in result
        assert len(result["options"]) == 5
        assert result["answer"] in result["options"]
        # Content check
        assert any(x in result["question"] for x in ["ratio", "cost", "sweets", "cars"])

def test_generate_fdp_conversion():
    for _ in range(10):
        result = generate_fdp_conversion(5)
        assert "question" in result
        assert "options" in result
        assert "answer" in result
        assert "explanation" in result
        assert len(result["options"]) == 5
        assert result["answer"] in result["options"]
        # Ensure explanation relates
        assert any(x in result["explanation"] for x in ["decimal", "fraction", "percentage", "%"])

def test_generate_bearings():
    for _ in range(5):
        result = generate_bearings()
        assert "text" in result
        assert "answer" in result
        assert "skill_tag" in result
        assert result["skill_tag"] == "Bearings"
        assert result["topic"] == "Geometry"
        assert len(result["options"]) == 5

def test_generate_pie_charts():
    for _ in range(5):
        result = generate_pie_charts()
        assert "text" in result
        assert "answer" in result
        assert result["skill_tag"] == "Pie Charts"
        assert result["topic"] == "Statistics"

def test_generate_pictograms():
    for _ in range(5):
        result = generate_pictograms()
        assert "text" in result
        assert "answer" in result
        assert result["skill_tag"] == "Pictograms"

def test_generate_bar_charts():
    for _ in range(5):
        result = generate_bar_charts()
        assert "text" in result
        assert "answer" in result
        assert result["skill_tag"] == "Bar Charts"

def test_generate_transformations():
    results = generate_transformations(5)
    assert len(results) == 5
    for q in results:
        assert "text" in q
        assert "answer" in q
        assert "topic" in q
        assert q["topic"] == "Transformations"

def test_generate_line_graphs():
    questions = generate_line_graphs(num_questions=5)
    assert len(questions) == 5
    for q in questions:
        assert "text" in q
        assert "answer" in q
        assert "options" in q
        assert "explanation" in q
        assert q["skill_tag"] == "Line Graphs"
        assert q["topic"] == "Statistics"
        assert len(q["options"]) == 5
        assert q["answer"] in q["options"]
        # Basic content check
        assert "line graph" in q["text"].lower()
        # "temperature" is not always present due to new scenarios (distance, height, etc.)

# Integration Tests for Route

def test_next_math_algebra_generator(client, monkeypatch):
    # Force random to favor generator (probability < 0.6)
    # math_routes uses random.random() < 0.6
    # We patch random.random to return 0.1
    monkeypatch.setattr('blueprints.math_routes.rng.random', lambda: 0.1)

    response = client.get('/next_math?topic=Algebra')
    assert response.status_code == 200
    data = response.get_json()

    assert data['type'] == 'math'
    assert data['topic'] == 'Algebra'
    assert data['question_type'] == 'Sutton SET Generated'
    assert len(data['options']) == 5
    assert data['generated_answer_check'] is not None
    assert data['explanation'] is not None

def test_next_math_ratio_generator(client, monkeypatch):
    monkeypatch.setattr('blueprints.math_routes.rng.random', lambda: 0.1)

    response = client.get('/next_math?topic=Ratio')
    assert response.status_code == 200
    data = response.get_json()

    assert data['topic'] == 'Ratio'
    assert data['question_type'] == 'Sutton SET Generated'
    assert len(data['options']) == 5

def test_next_math_fdp_generator(client, monkeypatch):
    monkeypatch.setattr('blueprints.math_routes.rng.random', lambda: 0.1)

    # Test for "Fractions"
    response = client.get('/next_math?topic=Fractions')
    assert response.status_code == 200
    data = response.get_json()
    assert data['question_type'] == 'Sutton SET Generated'

    # Test for "Percentages"
    response = client.get('/next_math?topic=Percentages')
    assert response.status_code == 200
    data = response.get_json()
    assert data['question_type'] == 'Sutton SET Generated'

def test_db_fallback_explanation(client, test_db, monkeypatch):
    """Test that existing DB questions also return explanation now."""
    # Force random > 0.6 to skip generator for Algebra
    monkeypatch.setattr('blueprints.math_routes.rng.random', lambda: 0.9)

    # Add a DB question with explanation
    q = MathQuestion(
        text="Solve x+1=2",
        answer="1",
        topic="Algebra",
        explanation="Subtract 1 from both sides.",
        question_type="Multiple Choice",
        options='["1", "2", "3", "4", "5"]'
    )
    test_db.add(q)
    test_db.commit()

    response = client.get('/next_math?topic=Algebra')
    assert response.status_code == 200
    data = response.get_json()

    assert data['topic'] == 'Algebra'
    assert data['question'] == "Solve x+1=2"
    # Ensure explanation is present in response
    assert data['explanation'] == "Subtract 1 from both sides."
    # Ensure options parsed
    assert data['options'] == ["1", "2", "3", "4", "5"]
