import random

# Use geometric shapes for display
FILLED = "■"
EMPTY = "□"

# Labelled nets for Opposite Face questions
# Each entry is (matrix, opposites_list)
# Matrix: 0=empty, string=face label
# Opposites: list of tuples (face1, face2)
OPPOSITE_FACE_NETS = [
    # Cross shape (1-4-1)
    #   1
    # 2 3 4 5
    #   6
    (
        [[0, "1", 0, 0],
         ["2", "3", "4", "5"],
         [0, "6", 0, 0]],
        [("1", "6"), ("2", "4"), ("3", "5")]
    ),
    # T-shape (aligned for easy display)
    #   1
    # 2 3 4
    #   5
    #   6
    (
        [[0, "1", 0],
         ["2", "3", "4"],
         [0, "5", 0],
         [0, "6", 0]],
        [("1", "5"), ("2", "4"), ("3", "6")]
    )
]

# The 11 Valid Nets of a Cube
# Represented as lists of lists (1=filled, 0=empty)
VALID_NETS = [
    # Group 1: 1-4-1 (6 nets)
    # 1. Cross
    [[0,1,0,0],
     [1,1,1,1],
     [0,1,0,0]],
    # 2.
    [[0,1,0,0],
     [1,1,1,1],
     [0,0,1,0]],
    # 3.
    [[0,1,0,0],
     [1,1,1,1],
     [0,0,0,1]],
    # 4.
    [[1,0,0,0],
     [1,1,1,1],
     [0,1,0,0]],
    # 5.
    [[1,0,0,0],
     [1,1,1,1],
     [0,0,1,0]],
    # 6.
    [[1,0,0,0],
     [1,1,1,1],
     [0,0,0,1]],

    # Group 2: 1-3-2 (3 nets)
    # 7.
    [[1,0,0],
     [1,1,1],
     [0,1,1]],
    # 8.
    [[0,1,0],
     [1,1,1],
     [0,1,1]],
    # 9.
    [[0,0,1],
     [1,1,1],
     [1,1,0]],

    # Group 3: 2-2-2 (1 net)
    # 10. Staircase
    [[1,1,0,0],
     [0,1,1,0],
     [0,0,1,1]],

    # Group 4: 2-3-1 (1 net)
    # 11.
    [[1,1,0,0],
     [0,1,1,1],
     [0,0,1,0]]
]

# Invalid Nets (Distractors)
INVALID_NETS = [
    # Long Strip (1x6)
    [[1,1,1,1,1,1]],

    # 2x3 Block
    [[1,1,1],
     [1,1,1]],

    # 5-1
    [[1,1,1,1,1],
     [0,0,1,0,0]],

    # C-Shape (Open box)
    [[1,1,1,1],
     [1,0,0,1]],

    # L-Shape (Long)
    [[1,0,0,0,0],
     [1,1,1,1,1]],

    # P-Shape? (6 squares)
    [[1,1],
     [1,1],
     [1,0],
     [1,0]],

    # Cross with extra arm (T shape but wrong) - No, T shape is valid.
    # Distorted Cross
    [[0,1,0],
     [1,1,1],
     [0,1,0],
     [0,0,1]], # 6 squares. T shape with one shifted.
               # This is actually valid? No.
               # Let's check:
               #   X
               # XXX
               #   X
               #    X
               # Folds to cube?
               # Center 3: F, B, R. Top: U. Bottom: D. The last one on R? No.
               # This is likely invalid.

    # A generic blob that fails (6 squares)
    [[1,1,1],
     [0,1,0],
     [1,1,0]],

     # Another failing one
     [[1,1,0],
     [0,1,1],
     [0,1,1]],

     # 2-2-2 aligned wrong
     [[1,1,0],
      [1,1,0],
      [0,1,1]]
]

def render_net(matrix):
    """
    Converts a matrix (list of lists) into a string representation using
    geometric characters for display.
    """
    rows = []
    # Find max width for padding
    if not matrix:
        return ""
    width = max(len(r) for r in matrix)

    for row in matrix:
        line = ""
        for i in range(width):
            val = row[i] if i < len(row) else 0
            if isinstance(val, str):
                # Ensure spacing is somewhat preserved if using digits
                # Using fullwidth digits might be better but let's stick to simple logic
                line += val
            else:
                line += FILLED if val else EMPTY
        rows.append(line)
    return "\n".join(rows)

def generate_opposite_face_questions(num_questions=1):
    """
    Generates 'Opposite Face' questions using labelled nets.
    """
    questions = []
    for _ in range(num_questions):
        matrix, opposites = random.choice(OPPOSITE_FACE_NETS)

        # Select a target pair
        target_pair = random.choice(opposites)
        face1, face2 = target_pair

        # Decide which one to ask about
        if random.random() < 0.5:
            given, answer = face1, face2
        else:
            given, answer = face2, face1

        net_str = render_net(matrix)

        question_text = f"The diagram below shows a net of a cube with faces numbered.\n\n{net_str}\n\nWhich face is OPPOSITE to face {given}?"

        # Distractors: other faces
        all_faces = set()
        for row in matrix:
            for cell in row:
                if isinstance(cell, str):
                    all_faces.add(cell)

        distractors = list(all_faces - {answer, given})
        random.shuffle(distractors)

        # Select 3 distractors if possible (usually 4 others exist)
        opts = [answer] + distractors[:3]
        random.shuffle(opts)

        questions.append({
            "text": question_text,
            "answer": answer,
            "topic": "Geometry",
            "diff": 8,
            "explanation": f"In this specific net configuration, face {given} is opposite to face {answer} when folded.",
            "question_type": "Multiple Choice",
            "options": opts
        })
    return questions

def generate_nets_of_cubes(num_questions=1):
    """
    Generates 'Identify the valid net' questions.
    Returns a list of question dictionaries.
    """
    questions = []

    for _ in range(num_questions):
        # 50% chance for Opposite Face question if num_questions is large,
        # but for single question generation (n=1), flip a coin.
        if random.random() < 0.5:
             # Task 2: Opposite Faces
             qs = generate_opposite_face_questions(1)
             if qs:
                 questions.extend(qs)
                 continue

        # Task 1: Identify Valid Net
        valid_matrix = random.choice(VALID_NETS)

        # Select 3 unique invalid nets
        # Ensure we have enough distractors
        num_distractors = min(3, len(INVALID_NETS))
        distractors_matrices = random.sample(INVALID_NETS, num_distractors)

        valid_str = render_net(valid_matrix)
        distractors_str = [render_net(m) for m in distractors_matrices]

        options = [valid_str] + distractors_str
        random.shuffle(options)

        questions.append({
            "text": "Which of the following shapes is a VALID net of a cube? (Can be folded to make a cube)",
            "answer": valid_str,
            "topic": "Geometry",
            "diff": 6,
            "explanation": "A cube has 11 valid nets. The selected shape is one of them. The others cannot be folded into a closed cube without overlapping or leaving a gap.",
            "question_type": "Multiple Choice",
            "options": options
        })

    return questions
