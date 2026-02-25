from utils import rng

# Use geometric shapes for display
FILLED = "■"
EMPTY = "□"

# Helper functions for matrix manipulation
def rotate_matrix(matrix):
    """Rotates a matrix 90 degrees clockwise."""
    if not matrix:
        return matrix
    # Transpose and reverse rows
    return [list(row) for row in zip(*matrix[::-1])]

def flip_matrix(matrix):
    """Flips a matrix horizontally."""
    return [row[::-1] for row in matrix]

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
                line += val
            else:
                line += FILLED if val else EMPTY
        rows.append(line)
    return "\n".join(rows)

# Labelled nets for Opposite Face questions
# Each entry is (matrix, opposites_list)
# Matrix: 0=empty, string=face label
# Opposites: list of tuples (face1, face2)
OPPOSITE_FACE_NETS = [
    # 1. Cross shape (1-4-1)
    #   1
    # 2 3 4 5
    #   6
    (
        [[0, "1", 0, 0],
         ["2", "3", "4", "5"],
         [0, "6", 0, 0]],
        [("1", "6"), ("2", "4"), ("3", "5")]
    ),
    # 2. T-shape (1-4-1)
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
    ),
    # 3. 1-3-2 (Step like)
    #   1
    # 2 3 4
    #     5 6
    (
        [[0, "1", 0, 0],
         ["2", "3", "4", 0],
         [0, 0, "5", "6"]],
        [("1", "5"), ("2", "4"), ("3", "6")]
    ),
    # 4. Staircase (2-2-2)
    # 1 2
    #   3 4
    #     5 6
    (
        [["1", "2", 0, 0],
         [0, "3", "4", 0],
         [0, 0, "5", "6"]],
        [("1", "4"), ("2", "5"), ("3", "6")]
    ),
    # 5. 3-3 (Parallel) - Wait, this is not a valid net?
    # No, 2-3-1
    # 1 2
    #   3 4 5
    #     6
    (
        [["1", "2", 0, 0],
         [0, "3", "4", "5"],
         [0, 0, "6", 0]],
        [("1", "4"), ("2", "6"), ("3", "5")]
    )
]

# The 11 Valid Nets of a Cube
VALID_NETS = [
    # Group 1: 1-4-1 (6 nets)
    [[0,1,0,0], [1,1,1,1], [0,1,0,0]],
    [[0,1,0,0], [1,1,1,1], [0,0,1,0]],
    [[0,1,0,0], [1,1,1,1], [0,0,0,1]],
    [[1,0,0,0], [1,1,1,1], [0,1,0,0]],
    [[1,0,0,0], [1,1,1,1], [0,0,1,0]],
    [[1,0,0,0], [1,1,1,1], [0,0,0,1]],
    # Group 2: 1-3-2 (3 nets)
    [[1,0,0], [1,1,1], [0,1,1]],
    [[0,1,0], [1,1,1], [0,1,1]],
    [[0,0,1], [1,1,1], [1,1,0]],
    # Group 3: 2-2-2 (1 net)
    [[1,1,0,0], [0,1,1,0], [0,0,1,1]],
    # Group 4: 2-3-1 (1 net)
    [[1,1,0,0], [0,1,1,1], [0,0,1,0]]
]

# Invalid Nets (Distractors)
INVALID_NETS = [
    # Long Strip (1x6)
    [[1,1,1,1,1,1]],
    # 2x3 Block
    [[1,1,1], [1,1,1]],
    # 5-1
    [[1,1,1,1,1], [0,0,1,0,0]],
    # C-Shape (Open box)
    [[1,1,1,1], [1,0,0,1]],
    # L-Shape (Long)
    [[1,0,0,0,0], [1,1,1,1,1]],
    # P-Shape (6 squares)
    [[1,1], [1,1], [1,0], [1,0]],
    # Distorted Cross (Invalid)
    [[0,1,0], [1,1,1], [0,1,0], [0,0,1]],
    # Generic blob
    [[1,1,1], [0,1,0], [1,1,0]],
    # Another failing one
    [[1,1,0], [0,1,1], [0,1,1]],
    # 2-2-2 aligned wrong
    [[1,1,0], [1,1,0], [0,1,1]],
    # L with too many (3x3 corner)
    [[1,1,1], [1,0,0], [1,0,0]], # 5 squares? No
    # 2x2 plus tails
    [[1,1,0], [1,1,1], [0,1,0]] # 6 squares
]

def generate_opposite_face_questions(num_questions=1):
    """
    Generates 'Opposite Face' questions using labelled nets.
    """
    questions = []
    for _ in range(num_questions):
        matrix, opposites = rng.choice(OPPOSITE_FACE_NETS)

        # Apply random transformation to the matrix
        # 1. Rotate 0, 90, 180, 270
        rotations = rng.choice([0, 1, 2, 3])
        for _ in range(rotations):
            matrix = rotate_matrix(matrix)

        # 2. Flip
        if rng.choice([True, False]):
            matrix = flip_matrix(matrix)

        # Select a target pair
        target_pair = rng.choice(opposites)
        face1, face2 = target_pair

        # Decide which one to ask about
        if rng.random() < 0.5:
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
        rng.shuffle(distractors)

        # Select 3 distractors if possible (usually 4 others exist)
        opts = [answer] + distractors[:3]
        rng.shuffle(opts)

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
        if rng.random() < 0.5:
             qs = generate_opposite_face_questions(1)
             if qs:
                 questions.extend(qs)
                 continue

        # Task 1: Identify Valid Net
        valid_matrix = rng.choice(VALID_NETS)

        # Apply random transformation to valid net
        rotations = rng.choice([0, 1, 2, 3])
        for _ in range(rotations):
            valid_matrix = rotate_matrix(valid_matrix)
        if rng.choice([True, False]):
            valid_matrix = flip_matrix(valid_matrix)

        # Select 3 unique invalid nets
        num_distractors = min(3, len(INVALID_NETS))
        distractors_matrices = rng.sample(INVALID_NETS, num_distractors)

        # Apply transformations to distractors too
        transformed_distractors = []
        for dm in distractors_matrices:
            rot = rng.choice([0, 1, 2, 3])
            for _ in range(rot):
                dm = rotate_matrix(dm)
            if rng.choice([True, False]):
                dm = flip_matrix(dm)
            transformed_distractors.append(dm)

        valid_str = render_net(valid_matrix)
        distractors_str = [render_net(m) for m in transformed_distractors]

        options = [valid_str] + distractors_str
        rng.shuffle(options)

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
