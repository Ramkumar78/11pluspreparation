try:
    from math_new_generators import generate_transformations
except ImportError:
    try:
        from VocabQuest.backend.math_new_generators import generate_transformations
    except ImportError:
        print("Warning: Could not import generate_transformations. Skipping procedural generation.")
        def generate_transformations(n=0): return []

GEOMETRY_LIST = [
    {
        "text": "A rectangle has an area of 48cm² and a width of 4cm. What is its perimeter?",
        "answer": "32",
        "topic": "Geometry",
        "diff": 7,
        "explanation": "Area = L x W. 48 = L x 4. Length = 12cm. Perimeter = 2(L + W) = 2(12 + 4) = 2(16) = 32cm."
    },
    {
        "text": "One angle in an isosceles triangle is 40°. What is the largest possible size for one of the other angles?",
        "answer": "100",
        "topic": "Angles",
        "diff": 8,
        "explanation": "Case 1: The 40° is the unique angle. Remaining 140° is split by 2 = 70°. Largest is 70°. Case 2: The 40° is one of the base angles. Then the other base is 40°. The third angle is 180 - 40 - 40 = 100°. 100° is larger than 70°."
    },
    {
        "text": "A cube has a total surface area of 150cm². What is its volume?",
        "answer": "125",
        "topic": "Shape",
        "diff": 9,
        "explanation": "Surface area of cube = 6 * (side)². 150 / 6 = 25. side² = 25, so side = 5cm. Volume = side³ = 5 * 5 * 5 = 125cm³."
    },
    {
        "text": "Coordinates: Point A is at (2, 2), Point B is at (2, 6), Point C is at (5, 2). What is the area of triangle ABC?",
        "answer": "6",
        "topic": "Coordinates",
        "diff": 7,
        "explanation": "Base AB is along x=2, length is 6-2=4. Height AC is along y=2, length is 5-2=3. Area = 0.5 * base * height = 0.5 * 4 * 3 = 6."
    },
    {
        "text": "A rectangle has a perimeter of 24cm. The length is twice the width. What is the area?",
        "answer": "32",
        "topic": "Geometry Puzzle",
        "diff": 9,
        "explanation": "Perimeter = 2(L+W). If L=2W, then Perimeter = 2(3W) = 6W. 24 = 6W, so Width = 4cm. Length = 8cm. Area = 8 x 4 = 32cm²."
    },
    {
        "text": "The mean of four numbers is 6. Three of the numbers are 3, 5, and 9. What is the fourth number?",
        "answer": "7",
        "topic": "Statistics",
        "diff": 7,
        "explanation": "Total sum = Mean x Count. 6 x 4 = 24. Sum of known numbers = 3 + 5 + 9 = 17. Missing number = 24 - 17 = 7."
    },
    {
        "text": "A cube has a volume of 125cm³. What is the total surface area of the cube?",
        "answer": "150",
        "topic": "3D Shapes",
        "diff": 9,
        "explanation": "If Volume = 125, the side length is the cube root of 125, which is 5cm. Area of one face = 5x5 = 25cm². A cube has 6 faces. Total Surface Area = 25 x 6 = 150cm²."
    },
    {
        "text": "A train leaves Sutton at 07:45 and arrives in Victoria at 08:23. How many minutes did the journey take?",
        "answer": "38",
        "topic": "Time",
        "diff": 5,
        "explanation": "From 07:45 to 08:00 is 15 mins. From 08:00 to 08:23 is 23 mins. Total = 15 + 23 = 38 mins."
    },
    {
        "text": "Coordinates: Point A is at (2, 2). Point B is at (2, 6). If ABCD is a square, what are the coordinates of D?",
        "answer": "(6, 2)",
        "topic": "Coordinates",
        "diff": 8,
        "explanation": "Distance from A to B is 4 units (vertical). A square has equal sides, so the width must be 4. D is to the right of A. (2+4, 2) = (6, 2)."
    }
]

# Append procedural questions
GEOMETRY_LIST.extend(generate_transformations(20))
