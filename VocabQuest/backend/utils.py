import re
import secrets
import json

def sanitize_filename(title):
    s = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[-\s]+', '_', s)

def generate_arithmetic(level):
    """Generates arithmetic questions suitable for the level."""
    ops = ['+', '-', '*', '/']
    if level <= 3:
        op = secrets.choice(['+', '-'])
        a = 1 + secrets.randbelow(20)
        b = 1 + secrets.randbelow(20)
    elif level <= 7:
        op = secrets.choice(['+', '-', '*'])
        a = 10 + secrets.randbelow(91)
        b = 2 + secrets.randbelow(11)
    else:
        op = secrets.choice(['+', '-', '*', '/'])
        a = 50 + secrets.randbelow(451)
        b = 5 + secrets.randbelow(16)

    if op == '+':
        return f"{a} + {b}", str(a + b)
    elif op == '-':
        if a < b: a, b = b, a
        return f"{a} - {b}", str(a - b)
    elif op == '*':
        return f"{a} x {b}", str(a * b)
    elif op == '/':
        ans = 2 + secrets.randbelow(11)
        a = b * ans
        return f"{a} ÷ {b}", str(ans)
    return f"{a} + {b}", str(a+b)

def check_badges(user):
    """Checks for new badges based on user stats."""
    existing_badges = []
    if user.badges:
        try:
            existing_badges = json.loads(user.badges)
        except:
            existing_badges = []

    new_badges = []

    # Score Badges
    if user.total_score >= 100 and "Novice" not in existing_badges:
        new_badges.append("Novice")
    if user.total_score >= 500 and "Apprentice" not in existing_badges:
        new_badges.append("Apprentice")
    if user.total_score >= 1000 and "High Flyer" not in existing_badges:
        new_badges.append("High Flyer")
    if user.total_score >= 5000 and "Scholar" not in existing_badges:
        new_badges.append("Scholar")

    # Streak Badges
    if user.streak >= 5 and "On Fire" not in existing_badges:
        new_badges.append("On Fire")
    if user.streak >= 10 and "Unstoppable" not in existing_badges:
        new_badges.append("Unstoppable")
    if user.streak >= 20 and "Godlike" not in existing_badges:
        new_badges.append("Godlike")

    # Level Badges
    if user.current_level >= 5 and "Level Master" not in existing_badges:
        new_badges.append("Level Master")
    if user.current_level >= 10 and "Grandmaster" not in existing_badges:
        new_badges.append("Grandmaster")

    if new_badges:
        existing_badges.extend(new_badges)
        user.badges = json.dumps(existing_badges)

    return new_badges
