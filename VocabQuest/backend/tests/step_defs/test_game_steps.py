import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app import app, init_db
from database import Session, UserStats, Word

# Load scenarios
scenarios('../../features/game_logic.feature')

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
    session.query(Word).delete()
    session.commit()
    session.close()

# --- GIVEN STEPS ---

@given(parsers.parse('a user "{name}" exists with score {score:d} and streak {streak:d}'))
def create_user(client, name, score, streak):
    session = Session()
    # Ensure word 'lion' exists for testing
    if not session.query(Word).filter_by(text='lion').first():
        session.add(Word(text='lion', definition='Cat', difficulty=3, word_type='noun'))
    if not session.query(Word).filter_by(text='bear').first():
        session.add(Word(text='bear', definition='Animal', difficulty=3, word_type='noun'))
    if not session.query(Word).filter_by(text='tiger').first():
        session.add(Word(text='tiger', definition='Big Cat', difficulty=3, word_type='noun'))
        
    user = UserStats(name=name, total_score=score, streak=streak, current_level=3)
    session.add(user)
    session.commit()
    session.close()

@given(parsers.parse('a user "{name}" exists with level {level:d} and streak {streak:d}'))
def create_user_level(client, name, level, streak):
    session = Session()
    # Add word 'bear'
    if not session.query(Word).filter_by(text='bear').first():
        session.add(Word(text='bear', definition='Animal', difficulty=3, word_type='noun'))
        
    user = UserStats(name=name, total_score=0, streak=streak, current_level=level)
    session.add(user)
    session.commit()
    session.close()

@given(parsers.parse('the current word is "{word}"'))
def set_current_word(client, word):
    # In a real integration test, we might force the word. 
    # Here we assume the word exists in DB and we pass its ID in the request.
    pass

# --- WHEN STEPS ---

@when(parsers.parse('"{name}" submits the spelling "{spelling}"'))
def submit_spelling(client, name, spelling):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    # Find word ID based on spelling (or the expected word from GIVEN)
    # This is a simplification; in real game we'd use the ID from next_word.
    # We'll just look up the word "lion" or "bear" or "tiger" from the scenario context if relevant,
    # but here we rely on the spelling matching a known word in DB.
    
    # Heuristic: Find the word that corresponds to the test scenario
    # If spelling is "tyger" (wrong), we need to find "tiger" ID.
    target_word_text = spelling if spelling in ['lion', 'bear'] else 'tiger' 
    word = session.query(Word).filter_by(text=target_word_text).first()
    
    response = client.post('/check_answer', json={
        'id': word.id,
        'spelling': spelling,
        'user_id': user.id
    })
    
    # Store response in client options for THEN steps
    client.last_response = response
    session.close()

# --- THEN STEPS ---

@then('the answer should be marked correct')
def check_correct(client):
    assert client.last_response.json['correct'] == True

@then('the answer should be marked incorrect')
def check_incorrect(client):
    assert client.last_response.json['correct'] == False

@then(parsers.parse('"{name}" score should be greater than {score:d}'))
def check_score(client, name, score):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    assert user.total_score > score
    session.close()

@then(parsers.parse('"{name}" streak should be {streak:d}'))
def check_streak(client, name, streak):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    assert user.streak == streak
    session.close()

@then(parsers.parse('"{name}" level should be {level:d}'))
def check_level(client, name, level):
    session = Session()
    user = session.query(UserStats).filter_by(name=name).first()
    assert user.current_level == level
    session.close()
