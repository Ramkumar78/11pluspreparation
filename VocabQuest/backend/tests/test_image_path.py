import pytest
from app import app
from seeder import seed_database as init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_next_word_image_path(client):
    response = client.get('/next_word')
    assert response.status_code == 200
    data = response.get_json()

    assert "image" in data
    image_path = data["image"]
    assert image_path.startswith("/images/")
    assert image_path.endswith(".jpg")

    # Check that the word text is part of the image path
    # Note: The response doesn't explicitly return the word text (it returns tts_text),
    # but the image path is derived from it.
    # We can verify the structure: /images/{word}.jpg

    word_part = image_path.split("/images/")[1].split(".jpg")[0]
    assert len(word_part) > 0
