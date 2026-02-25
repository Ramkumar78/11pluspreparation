import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app import app, init_db
from database import Session, UserStats

# Load scenarios
scenarios('../../features/profiles.feature')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
            yield client
    
    # Cleanup
    session = Session()
    session.query(UserStats).delete()
    session.commit()
    session.close()

# --- GIVEN STEPS ---

@given(parsers.parse('no user named "{name}" exists'))
def ensure_no_user(client, name):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()

@given(parsers.parse('a user "{name}" already exists'))
def ensure_user_exists(client, name):
    session = Session()
    if not session.query(UserStats).filter_by(name=name).first():
        session.add(UserStats(name=name))
        session.commit()
    session.close()
    
@given(parsers.parse('a user "{name}" exists'))
def ensure_user_exists_generic(client, name):
    ensure_user_exists(client, name)

# --- WHEN STEPS ---

@when(parsers.parse('I request to create a profile named "{name}"'))
def request_create_profile(client, name):
    response = client.post('/profiles', json={'name': name})
    client.last_response = response

@when(parsers.parse('I request to delete profile "{name}"'))
def request_delete_profile(client, name):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    session.close()
    
    if user:
        response = client.delete(f'/profiles/{user.id}')
    else:
        # Should rely on ID, but for test simplicity via name logic
        response = client.delete('/profiles/99999') 
        
    client.last_response = response

# --- THEN STEPS ---

@then(parsers.parse('the profile "{name}" should be created'))
def check_profile_created(client, name):
    assert client.last_response.status_code == 200
    assert client.last_response.json['name'] == name
    
    session = Session()
    assert session.query(UserStats).filter_by(name=name).first() is not None
    session.close()

@then(parsers.parse('"{name}" should have level {level:d} and score {score:d}'))
def check_profile_stats(client, name, level, score):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    assert user.current_level == level
    assert user.total_score == score
    session.close()

@then('the creation should fail with an error')
def check_creation_fail(client):
    assert client.last_response.status_code == 400
    assert 'error' in client.last_response.json

@then(parsers.parse('the profile "{name}" should no longer exist'))
def check_profile_deleted(client, name):
    assert client.last_response.status_code == 200
    
    session = Session()
    assert session.query(UserStats).filter_by(name=name).first() is None
    session.close()
