import random
import math

def generate_transformations(num_questions=20):
    """
    Generates procedural math questions for Geometry Transformations:
    - Reflection (x-axis, y-axis)
    - Rotation (90°, 180°)
    - Translation

    Returns a list of dictionaries compatible with the MathQuestion schema.
    """
    questions = []

    for _ in range(num_questions):
        q_type = random.choice(['reflection_x', 'reflection_y', 'rotation_90', 'rotation_180', 'translation'])
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

        if q_type == 'reflection_x':
            new_x, new_y = x, -y
            text = f"Point A is at ({x}, {y}). It is reflected in the x-axis. What are the new coordinates?"
            explanation = f"Reflection in x-axis changes the sign of the y-coordinate. ({x}, {y}) -> ({x}, {-y})."
            diff = 6

        elif q_type == 'reflection_y':
            new_x, new_y = -x, y
            text = f"Point A is at ({x}, {y}). It is reflected in the y-axis. What are the new coordinates?"
            explanation = f"Reflection in y-axis changes the sign of the x-coordinate. ({x}, {y}) -> ({-x}, {y})."
            diff = 6

        elif q_type == 'rotation_90':
            # Clockwise 90 degrees: (x, y) -> (y, -x)
            # Counter-clockwise 90 degrees: (x, y) -> (-y, x)
            direction = random.choice(['clockwise', 'anticlockwise'])
            if direction == 'clockwise':
                new_x, new_y = y, -x
                text = f"Point A is at ({x}, {y}). It is rotated 90° clockwise about the origin (0,0). What are the new coordinates?"
                explanation = f"90° clockwise rotation: (x, y) -> (y, -x). ({x}, {y}) -> ({y}, {-x})."
            else:
                new_x, new_y = -y, x
                text = f"Point A is at ({x}, {y}). It is rotated 90° anticlockwise about the origin (0,0). What are the new coordinates?"
                explanation = f"90° anticlockwise rotation: (x, y) -> (-y, x). ({x}, {y}) -> ({-y}, {x})."
            diff = 8

        elif q_type == 'rotation_180':
            new_x, new_y = -x, -y
            text = f"Point A is at ({x}, {y}). It is rotated 180° about the origin (0,0). What are the new coordinates?"
            explanation = f"180° rotation: (x, y) -> (-x, -y). ({x}, {y}) -> ({-x}, {-y})."
            diff = 7

        elif q_type == 'translation':
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            # Ensure non-zero translation
            if dx == 0 and dy == 0:
                dx = 1

            new_x, new_y = x + dx, y + dy

            vector_str = f"({dx}, {dy})"
            text = f"Point A is at ({x}, {y}). It is translated by the vector {vector_str}. What are the new coordinates?"
            explanation = f"Translation adds the vector to the point. ({x}+{dx}, {y}+{dy}) = ({new_x}, {new_y})."
            diff = 5

        questions.append({
            "text": text,
            "answer": f"({new_x}, {new_y})",
            "topic": "Transformations",
            "diff": diff,
            "explanation": explanation,
            "question_type": "Multiple Choice"
        })

    return questions

def generate_bearings(level=1):
    """
    Generates bearing questions (e.g. Reciprocal Bearings).
    """
    # 1. Reciprocal Bearings (Back Bearing)
    # Ensure angle is a nice number ending in 0 or 5 for easier mental math
    angle = random.choice([x for x in range(10, 350, 10)])

    # Text templates
    templates = [
        ("The bearing of B from A is {angle:03d}°. What is the bearing of A from B?", "reciprocal"),
        ("A ship sails on a bearing of {angle:03d}°. What is the opposite bearing?", "reciprocal")
    ]

    text_template, q_type = random.choice(templates)

    explanation = ""
    ans = 0
    if q_type == "reciprocal":
        if angle < 180:
            ans = angle + 180
            explanation = f"Since the bearing is less than 180°, add 180°. {angle} + 180 = {ans}."
        else:
            ans = angle - 180
            explanation = f"Since the bearing is more than 180°, subtract 180°. {angle} - 180 = {ans}."

    question_text = text_template.format(angle=angle)
    answer_str = f"{ans:03d}"

    # Options
    options = {answer_str}
    attempts = 0
    while len(options) < 5 and attempts < 20:
        attempts += 1
        distractor = random.choice([x for x in range(10, 360, 10)])
        if distractor != ans:
            options.add(f"{distractor:03d}")

    # Fallback
    while len(options) < 5:
        distractor = random.randint(10, 350)
        if distractor != ans:
            options.add(f"{distractor:03d}")

    return {
        "text": question_text,
        "answer": answer_str,
        "topic": "Geometry",
        "skill_tag": "Bearings",
        "diff": 5,
        "explanation": explanation,
        "question_type": "Multiple Choice",
        "options": sorted(list(options))
    }

def generate_pie_charts(level=1):
    """
    Generates Pie Chart interpretation questions.
    """
    # Type 1: Calculate Amount given Angle and Total
    # Type 2: Calculate Angle given Amount and Total

    total = random.choice([60, 72, 90, 120, 180, 360])
    # Choose an amount that results in a clean angle (factor of 360)
    # 360 degrees represents Total.
    deg_per_unit = 360 // total

    # Choose a random amount
    amount = random.randint(1, total // 2)
    angle = amount * deg_per_unit

    q_type = random.choice(["calc_amount", "calc_angle"])

    if q_type == "calc_amount":
        question_text = f"In a pie chart representing {total} people, a sector has an angle of {angle}°. How many people does this represent?"
        answer_str = str(amount)
        # Simpler explanation
        frac_simp = math.gcd(angle, 360)
        explanation = f"The fraction of the circle is {angle}/360, which simplifies to {angle//frac_simp}/{360//frac_simp}. {angle//frac_simp}/{360//frac_simp} of {total} is {amount}."

    else: # calc_angle
        question_text = f"In a survey of {total} people, {amount} chose Blue. What angle would represent this on a pie chart?"
        answer_str = str(angle)
        explanation = f"Fraction of people is {amount}/{total}. Multiply by 360°. ({amount}/{total}) x 360 = {angle}°."

    # Options
    options = {answer_str}
    attempts = 0
    while len(options) < 5 and attempts < 20:
        attempts += 1
        offset = random.choice([-10, -5, 5, 10, 15, 20])
        val = int(answer_str) + offset
        if val > 0:
            options.add(str(val))

    # Fallback
    while len(options) < 5:
        offset = random.randint(-20, 20)
        if offset == 0: offset = 1
        val = int(answer_str) + offset
        if val > 0:
            options.add(str(val))

    return {
        "text": question_text,
        "answer": answer_str,
        "topic": "Statistics",
        "skill_tag": "Pie Charts",
        "diff": 6,
        "explanation": explanation,
        "question_type": "Multiple Choice",
        "options": sorted(list(options), key=lambda x: int(x))
    }

def generate_pictograms(level=1):
    """
    Generates text-based Pictogram questions.
    """
    # Use even numbers to avoid .5 issues with int math
    symbol_val = random.choice([2, 4, 10])
    rows = [
        ("Monday", random.randint(1, 5), random.choice([0, 0.5])),
        ("Tuesday", random.randint(1, 5), random.choice([0, 0.5])),
        ("Wednesday", random.randint(1, 5), random.choice([0, 0.5]))
    ]

    target_day, whole, half = random.choice(rows)

    question_text = f"A pictogram uses a symbol '*' to represent {symbol_val} items. On {target_day}, there are {whole} full symbols"
    if half:
        question_text += " and one half symbol."
    else:
        question_text += "."

    question_text += f" How many items does this represent?"

    val = whole * symbol_val + int(half * symbol_val)
    answer_str = str(val)

    explanation = f"Each full symbol is {symbol_val}. {whole} x {symbol_val} = {whole*symbol_val}. "
    if half:
        explanation += f"Half a symbol is {symbol_val//2}. Total = {whole*symbol_val} + {symbol_val//2} = {val}."
    else:
        explanation += f"Total = {val}."

    options = {answer_str}
    attempts = 0
    while len(options) < 5 and attempts < 20:
        attempts += 1
        offset = random.choice([-symbol_val, -symbol_val//2, symbol_val//2, symbol_val])
        if offset == 0: offset = 1
        opt = int(answer_str) + offset
        if opt > 0:
            options.add(str(opt))

    # Fallback
    while len(options) < 5:
        offset = random.randint(-symbol_val, symbol_val)
        if offset == 0: offset = 1
        opt = int(answer_str) + offset
        if opt > 0:
            options.add(str(opt))

    return {
        "text": question_text,
        "answer": answer_str,
        "topic": "Statistics",
        "skill_tag": "Pictograms",
        "diff": 4,
        "explanation": explanation,
        "question_type": "Multiple Choice",
        "options": sorted(list(options), key=lambda x: int(x))
    }

def generate_bar_charts(level=1):
    """
    Generates text-based Bar Chart questions.
    """
    # Compare two bars or sum them
    categories = ["A", "B", "C", "D"]
    vals = {k: random.randint(5, 20) for k in categories}

    q_type = random.choice(["difference", "sum", "read"])

    c1, c2 = random.sample(categories, 2)

    intro = f"In a bar chart, bar A is {vals['A']}, bar B is {vals['B']}, bar C is {vals['C']}, and bar D is {vals['D']}."

    if q_type == "difference":
        question_text = f"{intro} How much taller is bar {c1} than bar {c2}? (If smaller, ignore sign)"
        ans = abs(vals[c1] - vals[c2])
        explanation = f"Bar {c1} is {vals[c1]}. Bar {c2} is {vals[c2]}. Difference is {vals[c1]} - {vals[c2]} = {ans}."
        if vals[c2] > vals[c1]:
             explanation = f"Bar {c2} is {vals[c2]}. Bar {c1} is {vals[c1]}. Difference is {vals[c2]} - {vals[c1]} = {ans}."

    elif q_type == "sum":
        question_text = f"{intro} What is the total height of bars {c1} and {c2}?"
        ans = vals[c1] + vals[c2]
        explanation = f"{vals[c1]} + {vals[c2]} = {ans}."

    else: # read
        question_text = f"{intro} What is the value of bar {c1}?"
        ans = vals[c1]
        explanation = f"The value is explicitly stated as {ans}."

    answer_str = str(ans)

    options = {answer_str}
    attempts = 0
    while len(options) < 5 and attempts < 20:
        attempts += 1
        offset = random.randint(-5, 5)
        if offset == 0: offset = 1
        opt = ans + offset
        if opt >= 0:
            options.add(str(opt))

    # Fallback
    while len(options) < 5:
        offset = random.randint(-10, 10)
        if offset == 0: offset = 1
        opt = ans + offset
        if opt >= 0:
            options.add(str(opt))

    return {
        "text": question_text,
        "answer": answer_str,
        "topic": "Statistics",
        "skill_tag": "Bar Charts",
        "diff": 3,
        "explanation": explanation,
        "question_type": "Multiple Choice",
        "options": sorted(list(options), key=lambda x: int(x))
    }

def generate_line_graphs(num_questions=1):
    """
    Generates text-based Line Graph questions.
    """
    questions = []

    for _ in range(num_questions):
        # Scenario: Temperature over time
        times = ["9am", "10am", "11am", "12pm", "1pm", "2pm"]
        start_temp = random.randint(10, 20)
        temps = [start_temp]
        for _ in range(len(times)-1):
            change = random.choice([-2, -1, 0, 1, 2, 3])
            temps.append(temps[-1] + change)

        data_str = " | ".join([f"{t}: {temp}°C" for t, temp in zip(times, temps)])
        intro = f"A line graph shows the temperature in a garden from 9am to 2pm. The points are:\n{data_str}"

        q_type = random.choice(["read_value", "find_time", "difference", "max_min"])

        ans = ""
        explanation = ""
        question_text = ""

        if q_type == "read_value":
            idx = random.randint(0, len(times)-1)
            target_time = times[idx]
            ans = temps[idx]
            question_text = f"{intro}\nWhat was the temperature at {target_time}?"
            explanation = f"At {target_time}, the graph shows {ans}°C."

        elif q_type == "find_time":
            # Pick a unique temp if possible, or just one instance
            unique_temps = [t for t in temps if temps.count(t) == 1]
            if unique_temps:
                ans_temp = random.choice(unique_temps)
                ans_time = times[temps.index(ans_temp)]
                question_text = f"{intro}\nAt what time was the temperature {ans_temp}°C?"
                ans = ans_time # Expected string
                explanation = f"The temperature was {ans_temp}°C at {ans_time}."
            else:
                # Fallback to read_value
                idx = random.randint(0, len(times)-1)
                target_time = times[idx]
                ans = temps[idx]
                question_text = f"{intro}\nWhat was the temperature at {target_time}?"
                explanation = f"At {target_time}, the graph shows {ans}°C."

        elif q_type == "difference":
            idx1, idx2 = random.sample(range(len(times)), 2)
            # Ensure idx1 < idx2 for logical flow "between X and Y"
            if idx1 > idx2: idx1, idx2 = idx2, idx1

            t1, t2 = times[idx1], times[idx2]
            v1, v2 = temps[idx1], temps[idx2]
            diff = abs(v1 - v2)

            question_text = f"{intro}\nWhat is the difference in temperature between {t1} and {t2}?"
            ans = diff
            explanation = f"At {t1}, it was {v1}°C. At {t2}, it was {v2}°C. Difference is |{v1} - {v2}| = {diff}°C."

        elif q_type == "max_min":
            sub_type = random.choice(["max", "min"])
            if sub_type == "max":
                val = max(temps)
                question_text = f"{intro}\nWhat was the highest temperature recorded?"
                ans = val
                explanation = f"The temperatures are {temps}. The highest value is {val}°C."
            else:
                val = min(temps)
                question_text = f"{intro}\nWhat was the lowest temperature recorded?"
                ans = val
                explanation = f"The temperatures are {temps}. The lowest value is {val}°C."

        # Options generation
        options = set()
        options.add(str(ans))

        # Distractors
        attempts = 0
        while len(options) < 5 and attempts < 20:
            attempts += 1
            if isinstance(ans, int) or (isinstance(ans, str) and ans.isdigit()):
                val = int(ans)
                offset = random.randint(-5, 5)
                if offset != 0:
                    options.add(str(val + offset))
            elif isinstance(ans, str) and ("am" in ans or "pm" in ans):
                # Time distractors
                options.add(random.choice(times))
            else:
                 # Generic fallback
                 options.add(str(random.randint(10, 25)))

        # Ensure fallback if loops fail
        while len(options) < 5:
             options.add(str(random.randint(100, 999)))

        questions.append({
            "text": question_text,
            "answer": str(ans),
            "topic": "Statistics",
            "skill_tag": "Line Graphs",
            "diff": 5,
            "explanation": explanation,
            "question_type": "Multiple Choice",
            "options": sorted(list(options))
        })

    return questions
