import sys
import os
import pytest

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from verbal_new_generators import generate_hidden_word, generate_compound_words

def test_generate_hidden_word_basic():
    questions = generate_hidden_word(5)
    assert len(questions) == 5
    for q in questions:
        assert q['type'] == 'hidden_word'
        assert 'content' in q
        assert 'answer' in q
        assert 'explanation' in q

def test_generate_hidden_word_uniqueness():
    num = 20
    questions = generate_hidden_word(num)
    contents = [q['content'] for q in questions]
    assert len(set(contents)) == len(contents)

def test_generate_compound_words_basic():
    questions = generate_compound_words(5)
    assert len(questions) == 5
    for q in questions:
        assert q['type'] == 'compound_word'
        assert 'content' in q
        assert 'answer' in q
        assert 'options' in q
        assert len(q['options']) == 4
        assert q['answer'] in q['options']

def test_generate_compound_words_uniqueness():
    # Only ~28 compounds available, so don't ask for more than that
    num = 10
    questions = generate_compound_words(num)
    contents = [q['content'] for q in questions]
    assert len(set(contents)) == len(contents)
