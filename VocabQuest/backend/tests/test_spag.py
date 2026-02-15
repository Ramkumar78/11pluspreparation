import pytest
import sys
import os
import json
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app
from spag_seed import SPAG_QUESTIONS

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_spag_generate(client):
    """Test that the SPaG endpoint returns a valid question structure."""
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

    # Verify the question is one of the seed questions
    assert any(q['id'] == data['id'] for q in SPAG_QUESTIONS)

def test_spag_new_questions_availability():
    """
    Test that new questions (IDs 101-105) can be retrieved.
    Since SPAG_QUESTIONS is imported, we can check it directly.
    """
    # Force reload of the module if needed, but in this context SPAG_QUESTIONS is imported from spag_seed

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
