import sys
import os
import pytest
import re

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generate_arithmetic, sanitize_filename

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

def test_sanitize_filename():
    test_cases = [
        ("Hello World", "hello_world"),
        ("  Hello   World  ", "hello_world"),
        ("Hello-World", "hello_world"),
        ("Hello!@#World", "helloworld"),
        ("Mixed CASE", "mixed_case"),
        ("Multiple     Spaces", "multiple_spaces"),
        ("---Hyphens---", "_hyphens_"), # Matches implementation where separators become underscores
        ("", ""),
        ("!@#$%", "")
    ]
    for input_str, expected in test_cases:
        assert sanitize_filename(input_str) == expected

def test_generate_arithmetic_ranges():
    # Level 1-3: a, b in [1, 20]
    for _ in range(50):
        q, a = generate_arithmetic(3)
        parts = re.split(r' \+ | - ', q)
        if len(parts) == 2:
            x, y = map(int, parts)
            # Both numbers should be <= 20.
            # Note: subtraction ensures x >= y, but originally both are <= 20.
            assert 1 <= x <= 20
            assert 1 <= y <= 20

    # Level 4-7: a in [10, 100], b in [2, 12]
    for _ in range(50):
        q, ans = generate_arithmetic(7)
        if ' x ' in q:
            x, y = map(int, q.split(' x '))
            assert 10 <= x <= 100
            assert 2 <= y <= 12
        elif ' + ' in q:
             x, y = map(int, q.split(' + '))
             assert 10 <= x <= 100
             assert 2 <= y <= 12

def test_generate_arithmetic_division_integrity():
    for _ in range(50):
        q, a = generate_arithmetic(10) # Level > 7
        if '÷' in q:
             parts = q.split(' ÷ ')
             dividend = int(parts[0])
             divisor = int(parts[1])
             answer = int(a)

             assert dividend == divisor * answer
             # Constraints check based on code logic:
             # ans = 2 + randbelow(11) -> [2, 12]
             # b = 5 + randbelow(16) -> [5, 20]
             assert 2 <= answer <= 12
             assert 5 <= divisor <= 20
