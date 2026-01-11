
import pytest
from app import app, init_db
from database import Session, ComprehensionPassage
import os
import shutil

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_next_comprehension_includes_image(client):
    """Test that /next_comprehension returns an image_url."""
    rv = client.get('/next_comprehension')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'image_url' in data
    assert data['image_url'].startswith('/images/comprehension/')
    assert data['image_url'].endswith('.jpg')

def test_mock_test_english_includes_image(client):
    """Test that english mock test includes passage_image."""
    rv = client.get('/mock_test?type=english')
    assert rv.status_code == 200
    data = rv.get_json()
    items = data['items']
    comprehension_items = [i for i in items if i['type'] == 'comprehension']
    # There should be comprehension items in english mock test
    if comprehension_items:
        assert 'passage_image' in comprehension_items[0]
        assert comprehension_items[0]['passage_image'].startswith('/images/comprehension/')
