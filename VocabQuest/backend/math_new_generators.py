import random

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
