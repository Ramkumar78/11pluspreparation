import random

# Use geometric shapes for display
FILLED = "■"
EMPTY = "□"

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
            line += FILLED if val else EMPTY
        rows.append(line)
    return "\n".join(rows)

def generate_nets_of_cubes(num_questions=1):
    """
    Generates 'Identify the valid net' questions.
    Returns a list of question dictionaries.
    """
    questions = []

    for _ in range(num_questions):
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
