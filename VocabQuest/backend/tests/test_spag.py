import pytest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder to prevent heavy initialization/migration
sys.modules['seeder'] = MagicMock()

from app import app
from spag_seed import SPAG_QUESTIONS

# Mock UserStats for spec if needed, or just use MagicMock
# We avoid importing UserStats from database to avoid DB init if possible,
# but spag_routes imports it, so it's likely already imported.
# Let's import it but mock Session interactions.

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('blueprints.spag_routes.Session')
def test_spag_generate(mock_session_cls, client):
    """Test that the SPaG endpoint returns a valid question structure."""
    # Setup mock session and user
    mock_session = mock_session_cls.return_value
    mock_user = MagicMock()
    mock_user.current_level = 5
    mock_user.total_score = 100
    mock_user.streak = 3

    # Configure query return
    mock_session.query.return_value.first.return_value = mock_user

    response = client.get('/api/spag/generate')
    assert response.status_code == 200
    data = response.get_json()

    # Verify structure
    assert 'id' in data
    assert 'type' in data
    assert 'question' in data
    assert 'options' in data
    assert 'answer' in data
    assert 'explanation' in data

    # Verify User Stats
    assert data['user_level'] == 5
    assert data['score'] == 100
    assert data['streak'] == 3

    # Check types
    assert isinstance(data['user_level'], int)
    assert isinstance(data['score'], int)
    assert isinstance(data['streak'], int)

    # Verify the question is one of the seed questions
    assert any(q['id'] == data['id'] for q in SPAG_QUESTIONS)

def test_spag_new_questions_availability():
    """
    Test that new questions (IDs 101-105) can be retrieved.
    Since SPAG_QUESTIONS is imported, we can check it directly.
    """
    new_ids = {101, 102, 103, 104, 105}
    present_ids = {q['id'] for q in SPAG_QUESTIONS}

    # Check if all new_ids are in present_ids
    missing_ids = new_ids - present_ids
    assert not missing_ids, f"Missing new SPaG question IDs: {missing_ids}"

def test_spag_new_questions_200_series_availability():
    """
    Test that new questions (IDs 200-204) can be retrieved.
    """
    new_ids = {200, 201, 202, 203, 204}
    present_ids = {q['id'] for q in SPAG_QUESTIONS}

    # Check if all new_ids are in present_ids
    missing_ids = new_ids - present_ids
    assert not missing_ids, f"Missing new SPaG question IDs: {missing_ids}"
