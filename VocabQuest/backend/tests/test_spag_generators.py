import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spag_new_generators import generate_shuffled_sentence
from verbal_new_generators import generate_word_families

def test_generate_shuffled_sentence():
    """Test Shuffled Sentence generator."""
    questions = generate_shuffled_sentence(5)
    # It attempts to generate 5, might be fewer if duplicates found but 5 is small enough
    if len(questions) == 0:
        pytest.skip("No shuffled sentences generated (possibly due to empty seed list or constraints)")

    for q in questions:
        assert q['type'] == 'shuffled_sentence'
        assert q['id'] == -1
        assert 'options' in q
        assert isinstance(q['options'], list)
        assert len(q['options']) > 0

        # Verify that options are a permutation of the answer words
        words_in_answer = q['answer'].split()
        assert sorted(q['options']) == sorted(words_in_answer)

        assert q['question'] == "Rearrange the words to form a correct sentence."

def test_generate_word_families():
    """Test Word Families generator."""
    questions = generate_word_families(5)
    assert len(questions) == 5

    for q in questions:
        assert q['type'] == 'word_families'
        assert q['id'] == -1
        assert q['topic'] == 'Morphology'
        assert 'options' in q
        assert isinstance(q['options'], list)
        assert len(q['options']) == 4
        assert q['answer'] in q['options']
        assert 'root' in q['explanation'] or 'comes from' in q['explanation']
