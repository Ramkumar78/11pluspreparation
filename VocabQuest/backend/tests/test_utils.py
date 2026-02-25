import sys
import os
import pytest
import re

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_arithmetic

def test_generate_arithmetic_level_low():
    # Level <= 3: +, -
    for _ in range(20):
        q, a = generate_arithmetic(3)
        assert any(op in q for op in ['+', '-'])
        assert not any(op in q for op in ['x', '÷'])
        # Check answer validity
        # q is like "a + b" or "a - b"
        # We can try to parse it or just trust the function returns valid strings
        assert isinstance(q, str)
        assert isinstance(a, str)

def test_generate_arithmetic_level_mid():
    # Level <= 7: +, -, x
    has_mul = False
    for _ in range(50):
        q, a = generate_arithmetic(7)
        assert any(op in q for op in ['+', '-', 'x'])
        assert '÷' not in q
        if 'x' in q:
            has_mul = True
    assert has_mul # statistically likely

def test_generate_arithmetic_level_high():
    # Level > 7: +, -, x, ÷
    has_div = False
    for _ in range(50):
        q, a = generate_arithmetic(10)
        assert any(op in q for op in ['+', '-', 'x', '÷'])
        if '÷' in q:
            has_div = True
            # specific check for division logic
            # q format: "a ÷ b", a = b * ans
            parts = q.split(' ÷ ')
            assert len(parts) == 2
            dividend = int(parts[0])
            divisor = int(parts[1])
            answer = int(a)
            assert dividend / divisor == answer
    assert has_div # statistically likely

def test_generate_arithmetic_validity():
    # General validity check for all operations
    for level in [2, 5, 8]:
        for _ in range(20):
            q, a = generate_arithmetic(level)

            if '+' in q:
                x, y = map(int, q.split(' + '))
                assert int(a) == x + y
            elif '-' in q:
                x, y = map(int, q.split(' - '))
                assert int(a) == x - y
            elif 'x' in q:
                x, y = map(int, q.split(' x '))
                assert int(a) == x * y
            elif '÷' in q:
                x, y = map(int, q.split(' ÷ '))
                assert int(a) == x // y
