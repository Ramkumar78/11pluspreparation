import random

COMMON_WORDS = [
    "the", "at", "in", "on", "to", "of", "it", "is", "as", "be", "by", "or", "he", "do", "go", "no",
    "my", "up", "me", "so", "we", "if", "us", "an", "am", "big", "red", "run", "sit", "cat", "dog",
    "hat", "mat", "bat", "rat", "sun", "fun", "car", "bus", "van", "man", "pan", "can", "fan", "top",
    "hop", "pop", "mop", "log", "fog", "pig", "dig", "wig", "fig", "pen", "hen", "ten", "men", "bed",
    "fed", "led", "red", "net", "wet", "pet", "jet", "let", "set", "met", "get", "bet", "hot", "pot",
    "cot", "lot", "dot", "got", "not", "rot", "box", "fox", "six", "mix", "fix", "cup", "pup", "rug",
    "bug", "hug", "mug", "jug", "nut", "cut", "hut", "but", "bus", "gas", "yes", "eye", "ear", "arm",
    "leg", "toe", "cow", "owl", "ant", "bee", "fly", "ice", "ink", "jam", "jar", "key", "kite", "map",
    "pie", "pin", "tie", "toy", "zoo", "ash", "ask", "bad", "bag", "bar", "bed", "beg", "bin", "bit",
    "boo", "bow", "boy", "bun", "cab", "cap", "cob", "cod", "cog", "cop", "cow", "cry", "cub", "cup",
    "dad", "dam", "day", "den", "dew", "did", "dim", "din", "dip", "doe", "dog", "don", "dot", "dry",
    "dub", "dud", "due", "dug", "dye", "ear", "eat", "egg", "ego", "elf", "elm", "end", "era", "eve",
    "eye", "fan", "far", "fat", "fax", "fed", "fee", "fen", "few", "fib", "fig", "fin", "fit", "fix",
    "flu", "fly", "fob", "foe", "fog", "for", "fox", "fry", "fun", "fur", "gag", "gap", "gas", "gel",
    "gem", "get", "gig", "gin", "got", "gum", "gun", "gut", "guy", "gym", "had", "hag", "ham", "has",
    "hat", "hay", "hem", "hen", "her", "hew", "hey", "hid", "him", "hip", "his", "hit", "hob", "hoe",
    "hog", "hop", "hot", "how", "hub", "hue", "hug", "hum", "hut", "ice", "icy", "ill", "imp", "ink",
    "inn", "ion", "ire", "its", "ivy", "jab", "jam", "jar", "jaw", "jay", "jet", "jig", "job", "jog",
    "joy", "jug", "jut", "keg", "key", "kid", "kin", "kit", "lab", "lad", "lag", "lap", "law", "lay",
    "led", "leg", "let", "lid", "lie", "lip", "lit", "lob", "log", "loo", "lot", "low", "mad", "man",
    "map", "mat", "may", "men", "met", "mew", "mix", "mob", "mom", "moo", "mop", "mud", "mug", "mum",
    "nab", "nag", "nap", "net", "new", "nib", "nil", "nip", "nod", "nor", "not", "now", "nun", "nut",
    "oak", "oar", "oat", "odd", "off", "oil", "old", "one", "orb", "ore", "our", "out", "owl", "own",
    "pad", "pal", "pan", "par", "pat", "paw", "pay", "pea", "peg", "pen", "pet", "pew", "pie", "pig",
    "pin", "pit", "pod", "pop", "pot", "pro", "pry", "pub", "pun", "pup", "pus", "put", "rag", "ram",
    "ran", "rap", "rat", "raw", "ray", "red", "rib", "rid", "rig", "rim", "rip", "rob", "rod", "rot",
    "row", "rub", "rug", "rum", "run", "rut", "rye", "sad", "sag", "sap", "sat", "saw", "say", "sea",
    "see", "set", "sew", "she", "shy", "sin", "sip", "sir", "sit", "six", "ski", "sky", "sly", "sob",
    "sod", "son", "sop", "sow", "soy", "spa", "spy", "sub", "sum", "sun", "tab", "tag", "tan", "tap",
    "tar", "tax", "tea", "tee", "ten", "the", "thy", "tic", "tie", "tin", "tip", "toe", "tog", "ton",
    "too", "top", "tow", "toy", "try", "tub", "tug", "two", "urn", "use", "van", "vat", "vet", "via",
    "vow", "wag", "war", "wax", "way", "web", "wed", "wee", "wet", "who", "why", "wig", "win", "wit",
    "woe", "won", "woo", "wow", "wry", "yak", "yam", "yap", "yaw", "yea", "yes", "yet", "yew", "you",
    "zip", "zoo"
]

TARGETS = [
    "CATS", "RATS", "BATS", "HATS", "MATS", "PANS", "CANS", "FANS", "POTS", "COTS", "LOTS", "DOTS",
    "NETS", "PETS", "JETS", "SETS", "BETS", "PIGS", "WIGS", "FIGS", "DOGS", "LOGS", "FOGS", "TOPS",
    "HOPS", "POPS", "MOPS", "CUPS", "PUPS", "RUGS", "BUGS", "HUGS", "MUGS", "JUGS", "NUTS", "CUTS",
    "HUTS", "BUSY", "EASY", "LATE", "GATE", "DATE", "MATE", "HATE", "RATE", "FATE", "HOPE", "ROPE",
    "COPE", "POPE", "MOPE", "RIDE", "SIDE", "HIDE", "WIDE", "TIDE", "RICE", "MICE", "DICE", "NICE",
    "VICE", "FACE", "RACE", "LACE", "PACE", "CAGE", "PAGE", "RAGE", "WAGE", "SAGE", "ROSE", "NOSE",
    "HOSE", "POSE", "LIME", "TIME", "DIME", "MIME", "PIPE", "WIPE", "RIPE", "TAPE", "CAPE", "TEAM",
    "BEAM", "SEAM", "MEAT", "BEAT", "SEAT", "HEAT", "NEAT", "FEAT", "BOAT", "COAT", "GOAT", "MOAT",
    "ROAD", "TOAD", "LOAD", "SOAP", "FOAM", "LOAM", "ROAM", "SOIL", "BOIL", "COIL", "FOIL", "TOIL",
    "COIN", "JOIN", "LOIN", "PAIN", "RAIN", "GAIN", "MAIN", "VAIN", "HAIL", "TAIL", "NAIL", "RAIL",
    "SAIL", "MAIL", "PAIL", "FAIL", "JAIL", "BAIL", "WAIL", "DEAL", "MEAL", "SEAL", "REAL", "HEAL",
    "PEAL", "TEAL", "VEAL", "FEEL", "HEEL", "PEEL", "REEL", "KEEL", "DEEP", "KEEP", "PEEP", "WEEP",
    "JEEP", "BEEP", "SEEP", "MEET", "FEET", "BEET", "SHEET", "SEED", "FEED", "NEED", "WEED", "DEED",
    "REED", "SEEN", "KEEN", "BEEN", "TEEN", "DOOR", "POOR", "MOOR", "FLOOR", "BOOK", "COOK", "LOOK",
    "HOOK", "NOOK", "TOOK", "ROOK", "GOOD", "WOOD", "HOOD", "FOOD", "MOOD", "FOOT", "BOOT", "ROOT",
    "HOOT", "TOOT", "SOOT", "COOL", "POOL", "TOOL", "FOOL", "WOOL", "MOON", "SOON", "NOON", "BOON",
    "LOON", "ROOM", "BOOM", "DOOM", "LOOM", "ZOOM", "LOOP", "HOOP"
]

def generate_hidden_word(num_questions=10):
    """
    Generates 'Hidden Word' verbal reasoning questions.
    Find a 4-letter word hidden across the boundary of two words.
    Algorithm:
    1. Load a dictionary of common 4-letter nouns/verbs (TARGETS).
    2. Generate pairs of words (W1, W2) from COMMON_WORDS.
    3. Check if W1 ends with and W2 starts with parts of a target word.
    4. Filter for uniqueness (ensure no other 4-letter word exists in the boundary).
    """
    questions = []
    attempts = 0
    max_attempts = num_questions * 100  # Allow plenty of retries for uniqueness constraint

    while len(questions) < num_questions and attempts < max_attempts:
        attempts += 1
        target = random.choice(TARGETS)
        split = random.randint(1, 3)

        part1 = target[:split].lower()
        part2 = target[split:].lower()

        left_candidates = [w for w in COMMON_WORDS if w.endswith(part1)]
        right_candidates = [w for w in COMMON_WORDS if w.startswith(part2)]

        if left_candidates and right_candidates:
            left = random.choice(left_candidates)
            right = random.choice(right_candidates)

            # --- Uniqueness Check ---
            # Construct the combined phrase (uppercase for checking against TARGETS)
            # Example: Left="MUSIC", Right="ATLAS". Phrase="MUSICATLAS".
            # Target="CATS". Boundary is between C and A.
            # We must ensure that only ONE 4-letter word from TARGETS exists
            # across the boundary (crossing from Left to Right).

            phrase = (left + right).upper()
            L = len(left)

            # A word crossing the boundary must start at index `i` such that:
            # i < L (starts in Left)
            # i + 4 > L (ends in Right)
            # So `i` can be L-3, L-2, L-1.

            valid_hidden_words = set()
            possible_starts = [L-3, L-2, L-1]

            for start in possible_starts:
                if start >= 0 and start + 4 <= len(phrase):
                    candidate = phrase[start : start+4]
                    if candidate in TARGETS:
                        valid_hidden_words.add(candidate)

            # We strictly want exactly one valid hidden word (which should be our target)
            if len(valid_hidden_words) == 1 and target in valid_hidden_words:
                text = "Find the 4-letter word hidden between the two words."
                content = f"{left.upper()} {right.upper()}"
                answer = target
                explanation = f"The end of '{left.upper()}' ({part1.upper()}) and the start of '{right.upper()}' ({part2.upper()}) make '{target}'."

                # Check if this question is already added
                if any(q['content'] == content for q in questions):
                    continue

                questions.append({
                    "type": "hidden_word",
                    "text": text,
                    "content": content,
                    "answer": answer,
                    "difficulty": random.randint(3, 6),
                    "explanation": explanation
                })

    return questions

def generate_hidden_words(num_questions=10):
    """
    Wrapper for generate_hidden_word to maintain backward compatibility.
    """
    return generate_hidden_word(num_questions)


def generate_logical_deduction(num_questions=10):
    """
    Generates Syllogism / Logical Deduction puzzles.
    """
    entities = ["Zogs", "Pogs", "Bloops", "Glorps", "Dristles", "Flings", "Plinks", "Mips", "Snargs", "Wimbles"]
    questions = []

    for _ in range(num_questions):
        X, Y, Z = random.sample(entities, 3)

        template = random.choice([1, 2, 3])

        if template == 1:
            # All X are Y. All Y are Z. -> All X are Z.
            stmt1 = f"All {X} are {Y}."
            stmt2 = f"All {Y} are {Z}."
            correct = f"All {X} are {Z}"
            distractors = [
                f"No {X} are {Z}",
                f"No {Y} are {X}",
                f"All {Z} are {X}",
                f"No {Y} are {Z}"
            ]
            explanation = f"If all {X} are inside the group {Y}, and all {Y} are inside the group {Z}, then all {X} must be inside {Z}."

        elif template == 2:
            # All X are Y. No Y are Z. -> No X are Z.
            stmt1 = f"All {X} are {Y}."
            stmt2 = f"No {Y} are {Z}."
            correct = f"No {X} are {Z}"
            distractors = [
                f"All {X} are {Z}",
                f"Some {X} are {Z}",
                f"All {Z} are {X}",
                f"Some {Z} are {Y}"
            ]
            explanation = f"If all {X} are {Y}, but no {Y} can be {Z}, then no {X} can be {Z} either."

        elif template == 3:
            # No X are Y. All Z are Y. -> No Z are X.
            stmt1 = f"No {X} are {Y}."
            stmt2 = f"All {Z} are {Y}."
            correct = f"No {Z} are {X}"
            distractors = [
                f"All {Z} are {X}",
                f"Some {Z} are {X}",
                f"All {X} are {Z}",
                f"Some {Y} are {X}" # False because No X are Y implies No Y are X (usually)
            ]
            explanation = f"If {Z} is entirely inside {Y}, and {Y} does not overlap with {X}, then {Z} cannot overlap with {X}."

        # Select 3 random distractors
        opts = random.sample(distractors, 3)
        opts.append(correct)
        random.shuffle(opts)

        questions.append({
            "type": "logic_deduction",
            "text": "Based on the statements, which conclusion is definitely true?",
            "content": f"{stmt1} {stmt2}",
            "answer": correct,
            "difficulty": random.randint(5, 8),
            "explanation": explanation,
            "options": opts
        })

    return questions

def generate_letter_sequences(num_questions=10):
    """
    Generates Letter Sequence questions.
    Example: A, C, E, G, ? -> I (Pattern: +2)
    """
    questions = []

    # 0=A, 1=B, ..., 25=Z
    # Convert index to char: chr(ord('A') + idx)
    # Convert char to index: ord(char) - ord('A')

    for _ in range(num_questions):
        pattern_type = random.choice(['add', 'sub', 'alternating_add', 'alternating_sub_add', 'pairs'])

        sequence = []
        answer = ""
        explanation = ""

        if pattern_type == 'add':
            step = random.randint(1, 4)
            start = random.randint(0, 25 - (step * 5)) # Ensure we don't go out of bounds easily
            current = start
            for _ in range(5):
                sequence.append(chr(ord('A') + current))
                current = (current + step) % 26 # Wrap around if needed, though restricted start helps

            # The last one added is the 5th element. The question asks for the next one?
            # Let's show 4, ask for 5th.
            sequence_str = ", ".join(sequence[:4])
            answer = sequence[4]
            explanation = f"The pattern is +{step} letters. {sequence[3]} + {step} -> {answer}."

        elif pattern_type == 'sub':
            step = random.randint(1, 3)
            start = random.randint(step * 5, 25)
            current = start
            for _ in range(5):
                sequence.append(chr(ord('A') + current))
                current = (current - step) % 26

            sequence_str = ", ".join(sequence[:4])
            answer = sequence[4]
            explanation = f"The pattern is -{step} letters (backwards). {sequence[3]} - {step} -> {answer}."

        elif pattern_type == 'alternating_add':
            step1 = random.randint(1, 2)
            step2 = random.randint(3, 4)
            start = random.randint(0, 15)
            current = start
            seq_indices = []

            # A, C (+2), F (+3), H (+2), K (+3)
            for i in range(5):
                seq_indices.append(current)
                sequence.append(chr(ord('A') + current))
                if i % 2 == 0:
                    current = (current + step1) % 26
                else:
                    current = (current + step2) % 26

            sequence_str = ", ".join(sequence[:4])
            answer = sequence[4]
            explanation = f"The pattern alternates +{step1} and +{step2}."

        elif pattern_type == 'alternating_sub_add':
            # +X, -Y
            step1 = random.randint(2, 4) # Add
            step2 = random.randint(1, 2) # Sub
            start = random.randint(5, 20)
            current = start

            for i in range(5):
                sequence.append(chr(ord('A') + current))
                if i % 2 == 0:
                    current = (current + step1) % 26
                else:
                    current = (current - step2) % 26

            sequence_str = ", ".join(sequence[:4])
            answer = sequence[4]
            explanation = f"The pattern is +{step1}, -{step2}."

        elif pattern_type == 'pairs':
            # AZ, BY, CX, DW...
            # Forward index, Backward index
            # A (0), Z (25) -> sum 25
            # B (1), Y (24) -> sum 25
            start = random.randint(0, 5)
            sequence = []
            for i in range(3): # 3 pairs = 6 letters
                fwd = start + i
                bwd = 25 - (start + i)
                sequence.append(chr(ord('A') + fwd))
                sequence.append(chr(ord('A') + bwd))

            # Show 5, ask 6th
            sequence_str = ", ".join(sequence[:5])
            answer = sequence[5]
            explanation = f"The sequence consists of opposite pairs in the alphabet (A-Z, B-Y, etc.)."

        questions.append({
            "type": "letter_sequence",
            "text": "What is the next letter in the sequence?",
            "content": sequence_str,
            "answer": answer,
            "difficulty": random.randint(4, 7),
            "explanation": explanation
        })

    return questions

def generate_compound_words(num_questions=10):
    """
    Generates Compound Word questions.
    Find the word that completes the compound word.
    """
    compounds = [
        ("foot", "ball"), ("sun", "flower"), ("rain", "coat"), ("pan", "cake"),
        ("fire", "man"), ("super", "man"), ("grand", "mother"), ("week", "end"),
        ("sea", "side"), ("tooth", "brush"), ("key", "board"), ("note", "book"),
        ("door", "step"), ("black", "bird"), ("blue", "berry"), ("straw", "berry"),
        ("star", "fish"), ("jelly", "fish"), ("cow", "boy"), ("milk", "man"),
        ("snow", "ball"), ("basket", "ball"), ("butter", "fly"), ("dragon", "fly"),
        ("post", "man"), ("po", "lice"), ("sun", "light"), ("moon", "light")
    ]

    # Pre-compute valid completions for each first word to avoid ambiguous distractors
    valid_completions = {}
    for w1, w2 in compounds:
        if w1 not in valid_completions:
            valid_completions[w1] = set()
        valid_completions[w1].add(w2)

    distractors_pool = ["ball", "man", "fly", "fish", "berry", "light", "stone", "water", "land", "house", "room", "top", "box"]

    questions = []
    attempts = 0

    while len(questions) < num_questions and attempts < 1000:
        attempts += 1
        word1, word2 = random.choice(compounds)

        correct = word2

        # Generate distractors
        opts = [correct]
        while len(opts) < 4:
            d = random.choice(distractors_pool)
            # Ensure distractor is not the correct answer AND not another valid completion for this word
            if d != correct and d not in opts:
                if d in valid_completions[word1]:
                    continue # Skip if this distractor makes another valid compound word (e.g. SUN + LIGHT when target is FLOWER)
                opts.append(d)
        random.shuffle(opts)

        content = f"{word1.upper()} + [ ? ]"
        text = f"Select the word that can be added to the end of '{word1.upper()}' to form a new compound word."
        explanation = f"'{word1.title()}' + '{word2}' makes '{word1.title()}{word2}'."

        # Check dupe
        if any(q['content'] == content for q in questions):
            continue

        questions.append({
            "type": "compound_word",
            "text": text,
            "content": content,
            "answer": correct,
            "difficulty": 3,
            "explanation": explanation,
            "options": opts
        })

    return questions

def generate_statement_logic(num_questions=10):
    """
    Generates Statement Logic (Comparison) questions.
    """
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
    properties = [
        ("taller", "shorter", "tallest"),
        ("older", "younger", "oldest"),
        ("faster", "slower", "fastest"),
        ("stronger", "weaker", "strongest"),
        ("richer", "poorer", "richest")
    ]

    questions = []

    for _ in range(num_questions):
        A, B, C = random.sample(names, 3)
        prop_adj, prop_opp, prop_sup = random.choice(properties)

        # Scenario: A > B, B > C => A is most 'prop'
        # Statements:
        # 1. A is taller than B.
        # 2. B is taller than C.
        # Question: Who is the tallest?

        stmt1 = f"{A} is {prop_adj} than {B}."
        stmt2 = f"{B} is {prop_adj} than {C}."

        question_text = f"Based on the statements, who is the {prop_sup}?"
        answer = A
        options = [A, B, C]
        random.shuffle(options)

        explanation = f"{A} is {prop_adj} than {B}, and {B} is {prop_adj} than {C}, so {A} is the {prop_sup}."

        # Variation: Mix adjectives? "A is taller than B. C is shorter than B."
        # => A > B, C < B => A > B > C. Tallest? A.

        variation = random.choice([1, 2])
        if variation == 2:
            stmt1 = f"{A} is {prop_adj} than {B}."
            stmt2 = f"{C} is {prop_opp} than {B}." # C < B
            explanation = f"{A} is {prop_adj} than {B}. {C} is {prop_opp} than {B} means {B} is {prop_adj} than {C}. So {A} > {B} > {C}."

        content = f"{stmt1} {stmt2}"

        questions.append({
            "type": "statement_logic",
            "text": question_text,
            "content": content,
            "answer": answer,
            "difficulty": random.randint(4, 6),
            "explanation": explanation,
            "options": options
        })

    return questions

def generate_number_sequences(num_questions=10):
    """
    Generates Number Sequence questions.
    Patterns: Arithmetic, Geometric, Alternating, Squares/Cubes.
    """
    questions = []

    for _ in range(num_questions):
        pattern_type = random.choice(['arithmetic', 'geometric', 'squares', 'alternating'])
        sequence = []
        answer = ""
        explanation = ""

        if pattern_type == 'arithmetic':
            start = random.randint(1, 50)
            diff = random.randint(1, 15) * random.choice([1, -1])
            if diff == 0: diff = 2

            for i in range(6):
                sequence.append(start + i * diff)

            # Show 5, ask 6th
            seq_display = ", ".join(map(str, sequence[:5]))
            answer = str(sequence[5])
            sign = "+" if diff > 0 else ""
            explanation = f"The pattern is {sign}{diff}. {sequence[4]} {sign}{diff} = {answer}."

        elif pattern_type == 'geometric':
            start = random.randint(1, 5)
            ratio = random.randint(2, 3)

            curr = start
            for _ in range(6):
                sequence.append(curr)
                curr *= ratio

            seq_display = ", ".join(map(str, sequence[:5]))
            answer = str(sequence[5])
            explanation = f"The pattern is multiply by {ratio}. {sequence[4]} * {ratio} = {answer}."

        elif pattern_type == 'squares':
            start_n = random.randint(1, 5)
            for i in range(6):
                n = start_n + i
                sequence.append(n*n)

            seq_display = ", ".join(map(str, sequence[:5]))
            answer = str(sequence[5])
            explanation = f"The sequence is square numbers: {start_n}^2, {start_n+1}^2... The next is {start_n+5}^2 = {answer}."

        elif pattern_type == 'alternating':
            start = random.randint(10, 50)
            op1 = random.randint(2, 5)
            op2 = random.randint(1, 3)
            # +op1, -op2

            curr = start
            for i in range(6):
                sequence.append(curr)
                if i % 2 == 0:
                    curr += op1
                else:
                    curr -= op2

            seq_display = ", ".join(map(str, sequence[:5]))
            answer = str(sequence[5])
            # The 6th term (index 5) comes after 5th term (index 4).
            # Indices: 0, 1, 2, 3, 4, 5
            # 0 -> 1 (+op1)
            # 1 -> 2 (-op2)
            # 2 -> 3 (+op1)
            # 3 -> 4 (-op2)
            # 4 -> 5 (+op1)
            explanation = f"The pattern alternates +{op1} and -{op2}. {sequence[4]} + {op1} = {answer}."

        questions.append({
            "type": "number_sequence",
            "text": "What is the next number in the sequence?",
            "content": seq_display,
            "answer": answer,
            "difficulty": random.randint(4, 7),
            "explanation": explanation
        })

    return questions

def generate_letter_connections(num_questions=10):
    """
    Generates Word Ladder questions (Start -> ? -> End).
    Uses BFS to find a path between two words.
    """
    # 1. Build Graph from COMMON_WORDS and TARGETS (only same length words)
    # Group by length
    words_by_len = {}
    all_words = set(w.lower() for w in COMMON_WORDS + TARGETS)

    for w in all_words:
        if 3 <= len(w) <= 4:
            l = len(w)
            if l not in words_by_len: words_by_len[l] = []
            words_by_len[l].append(w)

    def is_neighbor(w1, w2):
        diff = 0
        for c1, c2 in zip(w1, w2):
            if c1 != c2: diff += 1
        return diff == 1

    def get_path(start_word, length_limit=5):
        # BFS
        l = len(start_word)
        pool = words_by_len.get(l, [])
        queue = [(start_word, [start_word])]
        visited = {start_word}

        candidates = []

        while queue:
            curr, path = queue.pop(0)
            if len(path) >= length_limit:
                continue

            # Find neighbors
            for w in pool:
                if w not in visited and is_neighbor(curr, w):
                    new_path = path + [w]
                    if len(new_path) >= 3: # Minimum path length 3 (Start -> Mid -> End)
                        candidates.append(new_path)
                    visited.add(w)
                    queue.append((w, new_path))

            if len(candidates) > 20: break # Don't search too long

        return random.choice(candidates) if candidates else None

    questions = []
    attempts = 0
    while len(questions) < num_questions and attempts < 100:
        attempts += 1
        # Pick random length (3 or 4)
        l = random.choice([3, 4])
        pool = words_by_len.get(l, [])
        if not pool: continue

        start = random.choice(pool)
        path = get_path(start)

        if path and 3 <= len(path) <= 4:
            # Create question
            # Path: A -> B -> C (len 3). Missing B.
            # Path: A -> B -> C -> D (len 4). Missing B or C.

            missing_idx = random.randint(1, len(path)-2)
            missing_word = path[missing_idx]

            display_path = list(path)
            display_path[missing_idx] = "?"
            content = " -> ".join([w.upper() for w in display_path])

            text = "Complete the word ladder by changing one letter at a time."
            explanation = f"Change one letter at a time: {' -> '.join([w.upper() for w in path])}."

            # Simple distractors: random words of same length
            distractors = []
            while len(distractors) < 3:
                d = random.choice(pool)
                if d != missing_word and d not in path and d not in distractors:
                    distractors.append(d)

            options = [missing_word] + distractors
            random.shuffle(options)

            questions.append({
                "type": "word_ladder",
                "text": text,
                "content": content,
                "answer": missing_word,
                "difficulty": 5,
                "explanation": explanation,
                "options": options
            })

    return questions

def generate_seating_arrangements(num_questions=10):
    """
    Generates Logic Seating Arrangement questions.
    """
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]

    questions = []

    for _ in range(num_questions):
        # Linear Arrangement of 4 people
        people = random.sample(names, 4)
        # Arrangement: P1 P2 P3 P4 (Left to Right)

        # Generate Clues
        clues = []

        # Clue 1: Direct relation (P1 next to P2)
        p1, p2 = people[0], people[1]
        clues.append(f"{p1} is sitting to the immediate left of {p2}.")

        # Clue 2: Positional (P4 is on the far right)
        clues.append(f"{people[3]} is sitting on the far right.")

        # Clue 3: Relative (P2 is between P1 and P3)
        clues.append(f"{people[1]} is sitting between {people[0]} and {people[2]}.")

        random.shuffle(clues)
        content = " ".join(clues)

        # Question types
        q_type = random.choice(['left', 'right', 'between'])

        if q_type == 'left':
            text = "Who is sitting on the far left?"
            answer = people[0]
            explanation = f"From the clues, the order is {people[0]}, {people[1]}, {people[2]}, {people[3]}. So {people[0]} is on the far left."
        elif q_type == 'right':
            # Actually 'next to' is ambiguous, let's say 'Who is immediately to the right of X?'
            text = f"Who is immediately to the right of {people[2]}?"
            answer = people[3]
            explanation = f"The order is {people[0]}, {people[1]}, {people[2]}, {people[3]}. {people[3]} is to the right of {people[2]}."
        else:
             text = f"Who is sitting between {people[0]} and {people[2]}?"
             answer = people[1]
             explanation = f"The order is {people[0]}, {people[1]}, {people[2]}, {people[3]}."

        options = sorted(people)

        questions.append({
            "type": "seating_logic",
            "text": text,
            "content": content,
            "answer": answer,
            "difficulty": 6,
            "explanation": explanation,
            "options": options
        })

    return questions
