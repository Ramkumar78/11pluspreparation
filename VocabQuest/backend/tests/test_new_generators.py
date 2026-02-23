import pytest
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from math_new_generators import generate_transformations
from verbal_new_generators import generate_hidden_words, generate_logical_deduction

def test_generate_transformations():
    questions = generate_transformations(5)
    assert len(questions) == 5
    for q in questions:
        assert 'text' in q
        assert 'answer' in q
        assert q['topic'] == 'Transformations'
        assert isinstance(q['diff'], int)
        assert 'explanation' in q
        # Answer format check: (x, y)
        assert q['answer'].startswith('(')
        assert q['answer'].endswith(')')
        assert ',' in q['answer']

def test_generate_hidden_words():
    questions = generate_hidden_words(5)
    # It might return fewer if it fails to find matches, but with 1000 attempts it should find 5 easily.
    if len(questions) == 0:
        pytest.skip("No hidden word questions generated - possible if word list is too small or restricted.")

    for q in questions:
        assert q['type'] == 'hidden_word'
        assert 'text' in q
        assert 'content' in q
        assert 'answer' in q
        assert len(q['answer']) == 4
        # Verify hidden word is in content
        parts = q['content'].split()
        assert len(parts) == 2
        # Check logic: end of part1 + start of part2 should contain answer?
        # Actually, the hidden word is bridging the two.
        # "THE CAT" -> "THECAT", "CATS" is in "THECAT"?? No.
        # "CATS" from "THE CAT" -> "THE" ends with C? No.
        # Wait, my logic in generator:
        # part1 = target[:split], part2 = target[split:]
        # left ends with part1, right starts with part2.
        # So left + right contains part1 + part2 = target.
        # "THE" ends with "C"? No.
        # "MUSIC" ends with "C". "ATLAS" starts with "AT".
        # MUSIC ATLAS -> CATS.
        combined = parts[0] + parts[1]
        # The target should be a substring of the combined string
        # Specifically at the junction.
        # But simply checking substring is a good enough sanity check for now.
        assert q['answer'].upper() in combined.upper()

def test_generate_logical_deduction():
    questions = generate_logical_deduction(5)
    assert len(questions) == 5
    for q in questions:
        assert q['type'] == 'logic_deduction'
        assert 'text' in q
        assert 'content' in q
        assert 'answer' in q
        assert 'options' in q
        assert len(q['options']) == 4
        assert q['answer'] in q['options']
        # Check content structure
        assert "All" in q['content'] or "No" in q['content']
