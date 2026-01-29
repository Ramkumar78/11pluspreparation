import re
import random

def sanitize_filename(title):
    s = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[-\s]+', '_', s)

def generate_arithmetic(level):
    """Generates arithmetic questions suitable for the level."""
    ops = ['+', '-', '*', '/']
    if level <= 3:
        op = random.choice(['+', '-'])
        a = random.randint(1, 20)
        b = random.randint(1, 20)
    elif level <= 7:
        op = random.choice(['+', '-', '*'])
        a = random.randint(10, 100)
        b = random.randint(2, 12)
    else:
        op = random.choice(['+', '-', '*', '/'])
        a = random.randint(50, 500)
        b = random.randint(5, 20)

    if op == '+':
        return f"{a} + {b}", str(a + b)
    elif op == '-':
        if a < b: a, b = b, a
        return f"{a} - {b}", str(a - b)
    elif op == '*':
        return f"{a} x {b}", str(a * b)
    elif op == '/':
        ans = random.randint(2, 12)
        a = b * ans
        return f"{a} ÷ {b}", str(ans)
    return f"{a} + {b}", str(a+b)
