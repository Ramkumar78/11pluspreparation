import pytest
import sys
import os
from unittest.mock import MagicMock

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Mock seeder to prevent heavy initialization/migration
sys.modules['seeder'] = MagicMock()

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_check_math_no_data(client):
    """Test /check_math with no data (content-type application/json but empty body)"""
    response = client.post('/check_math', data='null', content_type='application/json')
    assert response.status_code == 400
    assert b"No data provided" in response.data

def test_check_math_empty_body(client):
    """Test /check_math with empty body"""
    response = client.post('/check_math', data='', content_type='application/json')
    assert response.status_code == 400

def test_check_math_list_input(client):
    """Test /check_math with non-empty list input"""
    response = client.post('/check_math', data='[1, 2]', content_type='application/json')
    # This should fail with 500 if not handled
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400

def test_check_math_string_input(client):
    """Test /check_math with string input"""
    response = client.post('/check_math', data='"hello"', content_type='application/json')
    # This should fail with 500 if not handled
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400

def test_check_math_int_input(client):
    """Test /check_math with int input"""
    response = client.post('/check_math', data='123', content_type='application/json')
    # This should fail with 500 if not handled
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400
