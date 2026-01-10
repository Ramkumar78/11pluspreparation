# Comprehensive 11+ Maths Questions targeting Wilson's, Wallington, Sutton, Nonsuch
# Topics: Number, Algebra, Geometry, Ratio, Data, Measurement, BIDMAS

MATH_LIST = [
    # --- BIDMAS / Order of Operations ---
    {
        "text": "Calculate: 10 + 4 x 2",
        "answer": "18",
        "topic": "BIDMAS",
        "diff": 3,
        "explanation": "Using BIDMAS, we multiply before we add. 4 x 2 = 8. Then 10 + 8 = 18."
    },
    {
        "text": "Calculate: (5 + 7) ÷ 3",
        "answer": "4",
        "topic": "BIDMAS",
        "diff": 3,
        "explanation": "Brackets first! 5 + 7 = 12. Then divide: 12 ÷ 3 = 4."
    },
    {
        "text": "Calculate: 20 - 5 x 3 + 2",
        "answer": "7",
        "topic": "BIDMAS",
        "diff": 5,
        "explanation": "Multiplication first: 5 x 3 = 15. The sum becomes 20 - 15 + 2. Subtraction and Addition happen left to right: 20 - 15 = 5. Then 5 + 2 = 7."
    },
    {
        "text": "What is 3² + 4 x 5?",
        "answer": "29",
        "topic": "BIDMAS",
        "diff": 5,
        "explanation": "Indices (powers) first: 3² = 9. Then Multiplication: 4 x 5 = 20. Finally Add: 9 + 20 = 29."
    },

    # --- FRACTIONS, DECIMALS, PERCENTAGES ---
    {
        "text": "What is 2/5 of 40?",
        "answer": "16",
        "topic": "Fractions",
        "diff": 2,
        "explanation": "Find 1/5 first: 40 ÷ 5 = 8. Then find 2/5: 8 x 2 = 16."
    },
    {
        "text": "Which fraction is equivalent to 0.75? (Write as a/b)",
        "answer": "3/4",
        "topic": "Fractions",
        "diff": 3,
        "explanation": "0.75 is 75/100. Divide top and bottom by 25: 75÷25=3, 100÷25=4. The answer is 3/4."
    },
    {
        "text": "Calculate 15% of 200.",
        "answer": "30",
        "topic": "Percentages",
        "diff": 4,
        "explanation": "10% of 200 is 20. 5% is half of that (10). So 15% = 20 + 10 = 30."
    },
    {
        "text": "What is 1/3 + 1/4? (Write as a/b)",
        "answer": "7/12",
        "topic": "Fractions",
        "diff": 6,
        "explanation": "Find a common denominator (12). 1/3 is 4/12. 1/4 is 3/12. Add them: 4/12 + 3/12 = 7/12."
    },
    {
        "text": "A jacket costs £80. It is reduced by 20%. What is the new price?",
        "answer": "64",
        "topic": "Percentages",
        "diff": 5,
        "explanation": "10% of £80 is £8. 20% is £16. Subtract this from the original price: 80 - 16 = 64."
    },

    # --- RATIO & PROPORTION ---
    {
        "text": "Share 20 sweets in the ratio 2:3.",
        "answer": "8:12",
        "topic": "Ratio",
        "diff": 4,
        "explanation": "Total parts = 2 + 3 = 5. Value of one part = 20 ÷ 5 = 4. Part 1: 2 x 4 = 8. Part 2: 3 x 4 = 12."
    },
    {
        "text": "A recipe needs 300g flour for 4 people. How much flour for 6 people?",
        "answer": "450",
        "topic": "Proportion",
        "diff": 5,
        "explanation": "For 2 people (half of 4), you need 150g. So for 6 people (4 + 2), you need 300 + 150 = 450g."
    },
    {
        "text": "The ratio of boys to girls is 4:5. There are 20 boys. How many girls are there?",
        "answer": "25",
        "topic": "Ratio",
        "diff": 5,
        "explanation": "4 parts = 20 boys. So 1 part = 20 ÷ 4 = 5. Girls have 5 parts, so 5 x 5 = 25 girls."
    },

    # --- ALGEBRA ---
    {
        "text": "If x = 5, what is 3x + 2?",
        "answer": "17",
        "topic": "Algebra",
        "diff": 3,
        "explanation": "3x means 3 times x. 3 x 5 = 15. Then add 2: 15 + 2 = 17."
    },
    {
        "text": "Solve for y: 2y - 4 = 10",
        "answer": "7",
        "topic": "Algebra",
        "diff": 5,
        "explanation": "Add 4 to both sides: 2y = 14. Divide by 2: y = 7."
    },
    {
        "text": "Find the next number: 5, 9, 13, 17, ...",
        "answer": "21",
        "topic": "Sequences",
        "diff": 3,
        "explanation": "The rule is add 4 each time. 17 + 4 = 21."
    },
    {
        "text": "If a = 3 and b = 4, what is a² + b?",
        "answer": "13",
        "topic": "Algebra",
        "diff": 6,
        "explanation": "a² is 3 x 3 = 9. b is 4. 9 + 4 = 13."
    },

    # --- GEOMETRY ---
    {
        "text": "How many degrees in a right angle?",
        "answer": "90",
        "topic": "Geometry",
        "diff": 1,
        "explanation": "A right angle is exactly 90 degrees."
    },
    {
        "text": "What is the perimeter of a rectangle with length 8cm and width 3cm?",
        "answer": "22",
        "topic": "Perimeter",
        "diff": 3,
        "explanation": "Perimeter is distance around. 8 + 3 + 8 + 3 = 22cm."
    },
    {
        "text": "What is the area of a square with side length 6cm?",
        "answer": "36",
        "topic": "Area",
        "diff": 3,
        "explanation": "Area = side x side. 6 x 6 = 36cm²."
    },
    {
        "text": "A triangle has angles 50° and 60°. What is the third angle?",
        "answer": "70",
        "topic": "Angles",
        "diff": 4,
        "explanation": "Angles in a triangle add to 180°. 50 + 60 = 110. 180 - 110 = 70°."
    },
    {
        "text": "How many edges does a cube have?",
        "answer": "12",
        "topic": "3D Shapes",
        "diff": 4,
        "explanation": "A cube has 12 edges, 6 faces, and 8 vertices (corners)."
    },

    # --- MEASUREMENT & TIME ---
    {
        "text": "How many minutes in 1.5 hours?",
        "answer": "90",
        "topic": "Time",
        "diff": 2,
        "explanation": "1 hour = 60 mins. 0.5 hours = 30 mins. 60 + 30 = 90 mins."
    },
    {
        "text": "A film starts at 14:20 and lasts 110 minutes. What time does it finish? (HH:MM)",
        "answer": "16:10",
        "topic": "Time",
        "diff": 5,
        "explanation": "110 minutes is 1 hour and 50 mins. 14:20 + 1 hour = 15:20. 15:20 + 50 mins = 15:70... which is 16:10."
    },
    {
        "text": "Convert 2.5kg into grams.",
        "answer": "2500",
        "topic": "Measurement",
        "diff": 3,
        "explanation": "There are 1000g in 1kg. So 2.5 x 1000 = 2500g."
    },

    # --- DATA & STATISTICS ---
    {
        "text": "What is the mean of 2, 5, and 8?",
        "answer": "5",
        "topic": "Statistics",
        "diff": 4,
        "explanation": "Add them up: 2 + 5 + 8 = 15. Divide by how many numbers there are (3). 15 ÷ 3 = 5."
    },
    {
        "text": "What is the range of: 10, 3, 8, 2, 9?",
        "answer": "8",
        "topic": "Statistics",
        "diff": 4,
        "explanation": "Range is the difference between the biggest and smallest number. Biggest is 10, smallest is 2. 10 - 2 = 8."
    }
]
