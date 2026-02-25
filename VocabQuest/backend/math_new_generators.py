from utils import rng
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
        q_type = rng.choice(['reflection_x', 'reflection_y', 'rotation_90', 'rotation_180', 'translation'])
        x = rng.randint(-15, 15)
        y = rng.randint(-15, 15)

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
            direction = rng.choice(['clockwise', 'anticlockwise'])
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
            dx = rng.randint(-8, 8)
            dy = rng.randint(-8, 8)
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
    # Improve angle randomness step=5
    angle = rng.choice([x for x in range(5, 360, 5)])

    # Text templates
    templates = [
        ("The bearing of B from A is {angle:03d}°. What is the bearing of A from B?", "reciprocal"),
        ("A ship sails on a bearing of {angle:03d}°. What is the opposite bearing?", "reciprocal"),
        ("Town A is on a bearing of {angle:03d}° from Town B. What is the bearing of Town B from Town A?", "reciprocal")
    ]

    text_template, q_type = rng.choice(templates)

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
        distractor = rng.choice([x for x in range(10, 360, 10)])
        if distractor != ans:
            options.add(f"{distractor:03d}")

    # Fallback
    while len(options) < 5:
        distractor = rng.randint(10, 350)
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

    total = rng.choice([24, 30, 36, 40, 48, 50, 60, 72, 80, 90, 100, 120, 180, 200, 360])
    # Choose an amount that results in a clean angle (factor of 360)
    # 360 degrees represents Total.
    deg_per_unit = 360 / total

    # Choose a random amount
    amount = rng.randint(1, total // 2)
    angle = int(amount * deg_per_unit) # Should be int if total is well chosen for factors of 360, but let's be safe

    # Recalculate angle to be sure it's integer for display if possible, or simple float
    if abs(angle - (amount * deg_per_unit)) > 0.01:
        # If not clean, pick a better total/amount pair
        total = 360
        amount = rng.randint(1, 180)
        angle = amount
        deg_per_unit = 1

    q_type = rng.choice(["calc_amount", "calc_angle"])

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
        offset = rng.choice([-10, -5, 5, 10, 15, 20])
        val = int(float(answer_str)) + offset
        if val > 0:
            options.add(str(val))

    # Fallback
    while len(options) < 5:
        offset = rng.randint(-20, 20)
        if offset == 0: offset = 1
        val = int(float(answer_str)) + offset
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
        "options": sorted(list(options), key=lambda x: int(float(x)))
    }

def generate_pictograms(level=1):
    """
    Generates text-based Pictogram questions.
    """
    # Use even numbers to avoid .5 issues with int math
    symbol_val = rng.choice([2, 4, 5, 8, 10, 20, 25, 50, 100])

    contexts = [
        ("Monday", "Tuesday", "Wednesday", "days"),
        ("Apples", "Bananas", "Oranges", "fruits"),
        ("Red", "Blue", "Green", "colors"),
        ("Cars", "Bikes", "Buses", "vehicles"),
        ("Dogs", "Cats", "Fish", "pets")
    ]

    c1, c2, c3, context_type = rng.choice(contexts)

    rows = [
        (c1, rng.randint(1, 6), rng.choice([0, 0.5])),
        (c2, rng.randint(1, 6), rng.choice([0, 0.5])),
        (c3, rng.randint(1, 6), rng.choice([0, 0.5]))
    ]

    target_day, whole, half = rng.choice(rows)

    question_text = f"A pictogram uses a symbol '*' to represent {symbol_val} {context_type}. For '{target_day}', there are {whole} full symbols"
    if half:
        question_text += " and one half symbol."
    else:
        question_text += "."

    question_text += f" How many {context_type} does this represent?"

    val = int(whole * symbol_val + (half * symbol_val))
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
        offset = rng.choice([-symbol_val, -symbol_val//2, symbol_val//2, symbol_val])
        if offset == 0: offset = 1
        opt = int(answer_str) + offset
        if opt > 0:
            options.add(str(opt))

    # Fallback
    while len(options) < 5:
        offset = rng.randint(-symbol_val, symbol_val)
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
    category_sets = [
        ["A", "B", "C", "D"],
        ["Red", "Blue", "Green", "Yellow"],
        ["Football", "Rugby", "Tennis", "Cricket"],
        ["Apple", "Banana", "Orange", "Grape"],
        ["Spring", "Summer", "Autumn", "Winter"]
    ]
    categories = rng.choice(category_sets)
    vals = {k: rng.randint(5, 50) for k in categories}

    q_type = rng.choice(["difference", "sum", "read"])

    c1, c2 = rng.sample(categories, 2)

    intro = f"In a bar chart, the values are: " + ", ".join([f"{k}: {v}" for k,v in vals.items()]) + "."

    if q_type == "difference":
        question_text = f"{intro} How much more is {c1} than {c2}? (If smaller, ignore sign)"
        ans = abs(vals[c1] - vals[c2])
        explanation = f"{c1} is {vals[c1]}. {c2} is {vals[c2]}. Difference is {vals[c1]} - {vals[c2]} = {ans}."
        if vals[c2] > vals[c1]:
             explanation = f"{c2} is {vals[c2]}. {c1} is {vals[c1]}. Difference is {vals[c2]} - {vals[c1]} = {ans}."

    elif q_type == "sum":
        question_text = f"{intro} What is the total of {c1} and {c2}?"
        ans = vals[c1] + vals[c2]
        explanation = f"{vals[c1]} + {vals[c2]} = {ans}."

    else: # read
        question_text = f"{intro} What is the value of {c1}?"
        ans = vals[c1]
        explanation = f"The value is explicitly stated as {ans}."

    answer_str = str(ans)

    options = {answer_str}
    attempts = 0
    while len(options) < 5 and attempts < 20:
        attempts += 1
        offset = rng.randint(-5, 5)
        if offset == 0: offset = 1
        opt = ans + offset
        if opt >= 0:
            options.add(str(opt))

    # Fallback
    while len(options) < 5:
        offset = rng.randint(-10, 10)
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

    scenarios = [
        {
            "context": "temperature in a garden",
            "x_label": "Time",
            "y_label": "Temperature (°C)",
            "x_vals": ["9am", "10am", "11am", "12pm", "1pm", "2pm"],
            "start_range": (10, 25),
            "change_range": [-2, -1, 0, 1, 2, 3, 4]
        },
        {
            "context": "distance walked",
            "x_label": "Time",
            "y_label": "Distance (km)",
            "x_vals": ["1pm", "2pm", "3pm", "4pm", "5pm"],
            "start_range": (0, 0),
            "change_range": [2, 3, 4, 5] # Always increasing
        },
        {
            "context": "height of a plant",
            "x_label": "Day",
            "y_label": "Height (cm)",
            "x_vals": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "start_range": (5, 10),
            "change_range": [0, 1, 2, 3] # Increasing or static
        },
        {
            "context": "rainfall",
            "x_label": "Month",
            "y_label": "Rainfall (mm)",
            "x_vals": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "start_range": (20, 80),
            "change_range": [-10, -5, 0, 5, 10, 20]
        }
    ]

    for _ in range(num_questions):
        scenario = rng.choice(scenarios)

        times = scenario["x_vals"]
        start_val = rng.randint(*scenario["start_range"])
        vals = [start_val]

        for _ in range(len(times)-1):
            change = rng.choice(scenario["change_range"])
            new_val = vals[-1] + change
            if new_val < 0: new_val = 0 # Prevent negative values for things like distance/rainfall
            vals.append(new_val)

        unit = ""
        if "°C" in scenario["y_label"]: unit = "°C"
        elif "km" in scenario["y_label"]: unit = "km"
        elif "cm" in scenario["y_label"]: unit = "cm"
        elif "mm" in scenario["y_label"]: unit = "mm"

        data_str = " | ".join([f"{t}: {v}{unit}" for t, v in zip(times, vals)])
        intro = f"A line graph shows the {scenario['context']}. The points are:\n{data_str}"

        q_type = rng.choice(["read_value", "find_time", "difference", "max_min"])

        ans = ""
        explanation = ""
        question_text = ""

        if q_type == "read_value":
            idx = rng.randint(0, len(times)-1)
            target_time = times[idx]
            ans = vals[idx]
            question_text = f"{intro}\nWhat was the value at {target_time}?"
            explanation = f"At {target_time}, the graph shows {ans}{unit}."

        elif q_type == "find_time":
            # Pick a unique val if possible, or just one instance
            unique_vals = [v for v in vals if vals.count(v) == 1]
            if unique_vals:
                ans_val = rng.choice(unique_vals)
                ans_time = times[vals.index(ans_val)]
                question_text = f"{intro}\nAt what time/day was the value {ans_val}{unit}?"
                ans = ans_time # Expected string
                explanation = f"The value was {ans_val}{unit} at {ans_time}."
            else:
                # Fallback to read_value
                idx = rng.randint(0, len(times)-1)
                target_time = times[idx]
                ans = vals[idx]
                question_text = f"{intro}\nWhat was the value at {target_time}?"
                explanation = f"At {target_time}, the graph shows {ans}{unit}."

        elif q_type == "difference":
            idx1, idx2 = rng.sample(range(len(times)), 2)
            # Ensure idx1 < idx2 for logical flow
            if idx1 > idx2: idx1, idx2 = idx2, idx1

            t1, t2 = times[idx1], times[idx2]
            v1, v2 = vals[idx1], vals[idx2]
            diff = abs(v1 - v2)

            question_text = f"{intro}\nWhat is the difference between {t1} and {t2}?"
            ans = diff
            explanation = f"At {t1}, it was {v1}{unit}. At {t2}, it was {v2}{unit}. Difference is |{v1} - {v2}| = {diff}{unit}."

        elif q_type == "max_min":
            sub_type = rng.choice(["max", "min"])
            if sub_type == "max":
                val = max(vals)
                question_text = f"{intro}\nWhat was the highest value recorded?"
                ans = val
                explanation = f"The values are {vals}. The highest value is {val}{unit}."
            else:
                val = min(vals)
                question_text = f"{intro}\nWhat was the lowest value recorded?"
                ans = val
                explanation = f"The values are {vals}. The lowest value is {val}{unit}."

        # Options generation
        options = set()
        options.add(str(ans))

        # Distractors
        attempts = 0
        while len(options) < 5 and attempts < 20:
            attempts += 1
            if isinstance(ans, int) or (isinstance(ans, str) and ans.isdigit()):
                val = int(ans)
                offset = rng.randint(-5, 5)
                if offset != 0:
                    options.add(str(val + offset))
            elif isinstance(ans, str) and (ans in times):
                # Time distractors
                options.add(rng.choice(times))
            else:
                 # Generic fallback
                 options.add(str(rng.randint(10, 25)))

        # Ensure fallback if loops fail
        while len(options) < 5:
             options.add(str(rng.randint(100, 999)))

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
