import random

def generate_hidden_words(num_questions=10):
    """
    Generates 'Hidden Word' verbal reasoning questions.
    Find a 4-letter word hidden across the boundary of two words.
    """
    common_words = [
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

    targets = [
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

    questions = []

    attempts = 0
    while len(questions) < num_questions and attempts < 1000:
        attempts += 1
        target = random.choice(targets)
        split = random.randint(1, 3)

        part1 = target[:split].lower()
        part2 = target[split:].lower()

        left_candidates = [w for w in common_words if w.endswith(part1)]
        right_candidates = [w for w in common_words if w.startswith(part2)]

        if left_candidates and right_candidates:
            left = random.choice(left_candidates)
            right = random.choice(right_candidates)

            # Avoid overly simple cases where the word is just the two words joined (e.g. KEY + PAD = KEYPAD)
            # But here target is 4 letters, so usually it's fine.
            # Avoid cases where left == part1 or right == part2 if we want to ensure it's "hidden"
            # But for 11+ level, finding "THE CAT" -> "THECAT" -> "HECA" no.
            # Example: Target CATS. Split 1: C, ATS. Left ending in C: MUSIC? No common words ending in C are rare in list.
            # Split 2: CA, TS. Left ending in CA: AFRICA. Right starting TS: TSHIRT.
            # With short common words, finding matches might be hard.
            # Let's trust the loop to find valid ones.

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
