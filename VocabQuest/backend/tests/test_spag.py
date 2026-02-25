import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder to prevent heavy initialization/migration
sys.modules['seeder'] = MagicMock()

from app import app
from spag_seed import SPAG_QUESTIONS

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('blueprints.spag_routes.Session')
@patch('random.random')
def test_spag_generate_static(mock_random, mock_session_cls, client):
    """Test that the SPaG endpoint returns a valid static question."""
    mock_random.return_value = 0.1 # Force static question (< 0.6)

    mock_session = mock_session_cls.return_value
    mock_user = MagicMock()
    mock_user.current_level = 5
    mock_user.total_score = 100
    mock_user.streak = 3
    mock_session.query.return_value.first.return_value = mock_user

    response = client.get('/api/spag/generate')
    assert response.status_code == 200
    data = response.get_json()

    # Structure Check
    assert data['id'] != -1
    assert data['type'] == 'spag'
    assert 'topic' in data
    assert 'question' in data
    assert 'options' in data
    assert 'answer' in data
    assert 'explanation' in data

    # User Stats Check
    assert data['user_level'] == 5
    assert data['score'] == 100
    assert data['streak'] == 3

    # Verify ID exists in seed list
    assert any(q['id'] == data['id'] for q in SPAG_QUESTIONS)

@patch('blueprints.spag_routes.Session')
@patch('random.random')
def test_spag_generate_shuffled(mock_random, mock_session_cls, client):
    """Test that the SPaG endpoint returns a shuffled sentence question."""
    mock_random.return_value = 0.7 # Force shuffled sentence (0.6 <= x < 0.8)

    mock_session = mock_session_cls.return_value
    mock_user = MagicMock()
    mock_user.current_level = 5
    mock_user.total_score = 100
    mock_user.streak = 3
    mock_session.query.return_value.first.return_value = mock_user

    response = client.get('/api/spag/generate')
    assert response.status_code == 200
    data = response.get_json()

    assert data['id'] == -1
    assert data['type'] == 'spag'
    assert data['topic'] == 'Syntax' # Defined in generator
    assert data['question'] == "Rearrange the words to form a correct sentence."
    assert len(data['options']) > 0
    assert data['user_level'] == 5

@patch('blueprints.spag_routes.Session')
@patch('random.random')
def test_spag_generate_word_families(mock_random, mock_session_cls, client):
    """Test that the SPaG endpoint returns a word family question."""
    mock_random.return_value = 0.9 # Force word families (>= 0.8)

    mock_session = mock_session_cls.return_value
    mock_user = MagicMock()
    mock_user.current_level = 5
    mock_user.total_score = 100
    mock_user.streak = 3
    mock_session.query.return_value.first.return_value = mock_user

    response = client.get('/api/spag/generate')
    assert response.status_code == 200
    data = response.get_json()

    assert data['id'] == -1
    assert data['type'] == 'spag'
    assert data['topic'] == 'Morphology' # Defined in generator
    assert 'root' in data['explanation'] or 'comes from' in data['explanation']
    assert data['user_level'] == 5

def test_spag_new_questions_availability():
    """Test that new questions (IDs 101-105) can be retrieved."""
    new_ids = {101, 102, 103, 104, 105}
    present_ids = {q['id'] for q in SPAG_QUESTIONS}
    missing_ids = new_ids - present_ids
    assert not missing_ids

def test_spag_new_questions_200_series_availability():
    """Test that new questions (IDs 200-204) can be retrieved."""
    new_ids = {200, 201, 202, 203, 204}
    present_ids = {q['id'] for q in SPAG_QUESTIONS}
    missing_ids = new_ids - present_ids
    assert not missing_ids
