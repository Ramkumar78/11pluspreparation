import pytest
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import sanitize_filename, generate_arithmetic

def test_sanitize_filename():
    assert sanitize_filename("Test File") == "test_file"
    assert sanitize_filename("Test  File") == "test_file"
    assert sanitize_filename("Test - File") == "test_file"
    assert sanitize_filename("Test File!") == "test_file"
    assert sanitize_filename("  Test File  ") == "test_file"
    assert sanitize_filename("MixedCASE") == "mixedcase"
    assert sanitize_filename("Special@#$%^&*Chars") == "specialchars"
    assert sanitize_filename("Dash-Separated") == "dash_separated"

def test_generate_arithmetic_level_low():
    """Test levels <= 3"""
    for _ in range(20):
        question, answer = generate_arithmetic(3)
        # Parse question
        parts = question.split()
        assert len(parts) == 3
        a, op, b = int(parts[0]), parts[1], int(parts[2])

        assert op in ['+', '-']
        assert 1 <= a <= 40  # Sum/diff could be up to 40 if a,b are 20
        # Actually a and b are randint(1, 20)
        # If op is '+', result is a+b
        # If op is '-', logic ensures a >= b

        # Verify calculation
        if op == '+':
            assert int(answer) == a + b
        elif op == '-':
            assert int(answer) == a - b
            assert int(answer) >= 0

def test_generate_arithmetic_level_medium():
    """Test levels 4-7"""
    for _ in range(20):
        question, answer = generate_arithmetic(5)
        parts = question.split()
        assert len(parts) == 3
        a, op, b = int(parts[0]), parts[1], int(parts[2])

        assert op in ['+', '-', 'x'] # Wait, generate_arithmetic returns 'x' for multiplication

        # Verify calculation
        if op == '+':
            assert int(answer) == a + b
        elif op == '-':
            assert int(answer) == a - b
            assert int(answer) >= 0
        elif op == 'x':
            assert int(answer) == a * b

def test_generate_arithmetic_level_high():
    """Test levels > 7"""
    for _ in range(20):
        question, answer = generate_arithmetic(8)
        parts = question.split()
        assert len(parts) == 3
        a, op, b = int(parts[0]), parts[1], int(parts[2])

        assert op in ['+', '-', 'x', '÷'] # '÷' for division

        # Verify calculation
        if op == '+':
            assert int(answer) == a + b
        elif op == '-':
            assert int(answer) == a - b
        elif op == 'x':
            assert int(answer) == a * b
        elif op == '÷':
            assert int(answer) == a // b # Integer division result check
            assert a % b == 0 # Should be divisible
