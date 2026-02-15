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
    },

    # ==========================
    # PREVIOUS QUESTIONS (Restored)
    # ==========================
    {
        "text": "What is 453 + 248?",
        "answer": "701",
        "topic": "Basic Operations",
        "diff": 1,
        "explanation": "Add the units: 3+8=11 (write 1, carry 1). Tens: 5+4+1=10 (write 0, carry 1). Hundreds: 4+2+1=7. The answer is 701."
    },
    {
        "text": "What is the value of the digit 5 in 2,560?",
        "answer": "500",
        "topic": "Place Value",
        "diff": 2,
        "explanation": "The 0 is units, 6 is tens, 5 is hundreds. So the value is 500."
    },
    {
        "text": "Round 348 to the nearest 100.",
        "answer": "300",
        "topic": "Rounding",
        "diff": 2,
        "explanation": "Look at the tens digit (4). Since it is less than 5, we round down. 348 becomes 300."
    },
    {
        "text": "How many minutes are there in 3 hours?",
        "answer": "180",
        "topic": "Time",
        "diff": 2,
        "explanation": "There are 60 minutes in 1 hour. So 3 x 60 = 180 minutes."
    },
    {
        "text": "Identify the prime number: 8, 9, 10, 11, 12.",
        "answer": "11",
        "topic": "Number Properties",
        "diff": 3,
        "explanation": "A prime number has exactly two factors: 1 and itself. 8, 9, 10, 12 all have other factors. 11 only divides by 1 and 11."
    },
    {
        "text": "What is 1/2 of 48?",
        "answer": "24",
        "topic": "Fractions",
        "diff": 2,
        "explanation": "To find half, divide by 2. 48 ÷ 2 = 24."
    },
    {
        "text": "Convert 0.75 to a percentage.",
        "answer": "75%",
        "topic": "Percentages",
        "diff": 3,
        "explanation": "To turn a decimal into a percentage, multiply by 100. 0.75 x 100 = 75%."
    },
    {
        "text": "What shape has 5 sides?",
        "answer": "Pentagon",
        "topic": "Geometry",
        "diff": 2,
        "explanation": "A 3-sided shape is a triangle, 4 is a quadrilateral, and 5 is a pentagon."
    },
    {
        "text": "Simplify the ratio 10:15.",
        "answer": "2:3",
        "topic": "Ratio",
        "diff": 3,
        "explanation": "Divide both numbers by the biggest number that fits into both (5). 10÷5=2 and 15÷5=3. The ratio is 2:3."
    },
    {
        "text": "Find the perimeter of a square with side length 5cm.",
        "answer": "20",
        "topic": "Perimeter",
        "diff": 3,
        "explanation": "Perimeter is the distance around the outside. A square has 4 equal sides. 5 + 5 + 5 + 5 = 20cm."
    },
    {
        "text": "Calculate 2/3 + 1/6. Give your answer as a simple fraction (e.g. 5/6).",
        "answer": "5/6",
        "topic": "Fractions",
        "diff": 5,
        "explanation": "Make the denominators the same. Multiply 2/3 by 2 to get 4/6. Now add 4/6 + 1/6 = 5/6."
    },
    {
        "text": "Which is larger: 0.4 or 3/5?",
        "answer": "3/5",
        "topic": "Fractions/Decimals",
        "diff": 5,
        "explanation": "Convert 3/5 to a decimal. 3 ÷ 5 = 0.6. Since 0.6 is bigger than 0.4, 3/5 is larger."
    },
    {
        "text": "Calculate 15% of 80.",
        "answer": "12",
        "topic": "Percentages",
        "diff": 5,
        "explanation": "Find 10% first: 80 ÷ 10 = 8. Find 5% (half of 10%): half of 8 is 4. Add them: 8 + 4 = 12."
    },
    {
        "text": "Calculate 5 + 3 x 4.",
        "answer": "17",
        "topic": "BODMAS",
        "diff": 4,
        "explanation": "Use BODMAS/BIDMAS. Multiply first: 3 x 4 = 12. Then add 5: 5 + 12 = 17."
    },
    {
        "text": "Solve for x: 3x - 4 = 11.",
        "answer": "5",
        "topic": "Algebra",
        "diff": 6,
        "explanation": "Add 4 to both sides: 3x = 15. Divide by 3: x = 5."
    },
    {
        "text": "I think of a number, multiply it by 2 and add 7. The answer is 19. What is the number?",
        "answer": "6",
        "topic": "Algebra Word Problem",
        "diff": 5,
        "explanation": "Work backwards. Start with 19. Subtract 7 to get 12. Divide by 2 to get 6."
    },
    {
        "text": "If a = 5 and b = 3, what is the value of 2a + b²?",
        "answer": "19",
        "topic": "Algebra Substitution",
        "diff": 6,
        "explanation": "First, 2a means 2 x 5 = 10. Second, b² means 3 x 3 = 9. Finally add them: 10 + 9 = 19."
    },
    {
        "text": "A map scale is 1:1000. How many metres in real life is 5cm on the map?",
        "answer": "50",
        "topic": "Ratio/Scale",
        "diff": 6,
        "explanation": "5cm on map = 5000cm in real life. Convert to metres: 5000 ÷ 100 = 50m."
    },
    {
        "text": "Share £60 in the ratio 2:3. What is the smaller share?",
        "answer": "24",
        "topic": "Ratio",
        "diff": 5,
        "explanation": "Add the parts: 2 + 3 = 5 parts. Value of one part: £60 ÷ 5 = £12. Smaller share is 2 parts: 2 x £12 = £24."
    },
    {
        "text": "What is the area of a triangle with base 8cm and height 5cm?",
        "answer": "20",
        "topic": "Area",
        "diff": 4,
        "explanation": "Area of triangle = (base x height) ÷ 2. 8 x 5 = 40. 40 ÷ 2 = 20."
    },
    {
        "text": "Angles on a straight line add up to what?",
        "answer": "180",
        "topic": "Angles",
        "diff": 4,
        "explanation": "Angles on a straight line always add up to 180 degrees. Angles around a point add to 360."
    },
    {
        "text": "Calculate the volume of a cuboid with length 10cm, width 3cm, and height 4cm.",
        "answer": "120",
        "topic": "Volume",
        "diff": 5,
        "explanation": "Volume = Length x Width x Height. 10 x 3 = 30. 30 x 4 = 120cm³."
    },
    {
        "text": "The price of a coat is reduced by 20% in a sale. The sale price is £40. What was the original price?",
        "answer": "50",
        "topic": "Reverse Percentages",
        "diff": 9,
        "explanation": "If reduced by 20%, the coat is worth 80% of the original price. So £40 is 80%. Divide by 8 to find 10% (£5). Multiply by 10 to find 100% (£50)."
    },
    {
        "text": "A train travels 120km in 1 hour 30 minutes. What is its average speed in km/h?",
        "answer": "80",
        "topic": "Speed Distance Time",
        "diff": 8,
        "explanation": "1 hour 30 mins is 1.5 hours. Speed = Distance ÷ Time. 120 ÷ 1.5 is the same as 1200 ÷ 15, which is 80km/h."
    },
    {
        "text": "The mean of 5 numbers is 12. A sixth number is added and the new mean is 13. What is the sixth number?",
        "answer": "18",
        "topic": "Averages (Mean)",
        "diff": 8,
        "explanation": "Total of first 5 numbers = 5 x 12 = 60. Total of 6 numbers = 6 x 13 = 78. The difference is the new number: 78 - 60 = 18."
    },
    {
        "text": "Find the next number in the sequence: 2, 6, 12, 20, 30...",
        "answer": "42",
        "topic": "Sequences",
        "diff": 8,
        "explanation": "Look at the gaps: +4, +6, +8, +10. The next gap must be +12. 30 + 12 = 42."
    },
    {
        "text": "Solve for y: 2(y + 3) = 18",
        "answer": "6",
        "topic": "Advanced Algebra",
        "diff": 8,
        "explanation": "Expand the bracket: 2y + 6 = 18. Subtract 6: 2y = 12. Divide by 2: y = 6. (Or divide by 2 first: y+3=9, so y=6)."
    },
    {
        "text": "A garden is 10m long and 8m wide. A path 1m wide runs all around the outside edge. What is the area of the path?",
        "answer": "40",
        "topic": "Area Problem Solving",
        "diff": 9,
        "explanation": "Inner Area = 10 x 8 = 80m². Outer dimensions = 10+1+1 (12m) by 8+1+1 (10m). Outer Area = 12 x 10 = 120m². Path Area = Outer - Inner = 120 - 80 = 40m²."
    },
    {
        "text": "If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch 100 mice in 100 minutes?",
        "answer": "3",
        "topic": "Logic",
        "diff": 10,
        "explanation": "Don't be tricked! 3 cats take 3 mins for 3 mice. This means 1 cat takes 3 mins to catch 1 mouse. In 100 minutes, 1 cat could catch (100÷3) = 33 mice. 3 cats can catch 3 x 33 = 99... wait. Simpler way: The RATE is the same. The cats work in parallel. 3 cats catch 1 mouse per minute (combined). So in 100 minutes, the SAME 3 cats catch 100 mice."
    },
    {
        "text": "What is the surface area of a cube with volume 27cm³?",
        "answer": "54",
        "topic": "Surface Area",
        "diff": 9,
        "explanation": "First find the side length. ? x ? x ? = 27. The side is 3cm. A cube has 6 faces. Area of one face = 3 x 3 = 9. Total surface area = 9 x 6 = 54cm²."
    },
    {
        "text": "Simplify completely: (12a⁵b²) / (4a²b)",
        "answer": "3a³b",
        "topic": "Algebra Indices",
        "diff": 9,
        "explanation": "Divide numbers: 12÷4 = 3. Subtract powers for a: a⁵ ÷ a² = a³. Subtract powers for b: b² ÷ b = b. Result: 3a³b."
    },

    # --- STANDARD WRITTEN (High Level) ---
    {
        "text": "A recipe for 4 people uses 200g of flour and 150ml of milk. How much flour is needed for 6 people?",
        "answer": "300",
        "topic": "Ratio",
        "diff": 8,
        "explanation": "Ratio is 4 people : 200g. 1 person : 50g. 6 people : 300g.",
        "question_type": "Standard Written"
    },
    {
        "text": "Solve for x: 3(2x + 4) = 30",
        "answer": "3",
        "topic": "Algebra",
        "diff": 8,
        "explanation": "Expand: 6x + 12 = 30. Subtract 12: 6x = 18. Divide by 6: x = 3.",
        "question_type": "Standard Written"
    },
    {
        "text": "The ratio of red to blue marbles is 3:5. If there are 24 red marbles, how many blue marbles are there?",
        "answer": "40",
        "topic": "Ratio",
        "diff": 8,
        "explanation": "3 parts = 24. 1 part = 8. Blue is 5 parts. 5 * 8 = 40.",
        "question_type": "Standard Written"
    },
    {
        "text": "Alice is 3 times as old as Bob. In 10 years, Alice will be twice as old as Bob. How old is Bob now?",
        "answer": "10",
        "topic": "Algebra",
        "diff": 9,
        "explanation": "Let Bob = b, Alice = 3b. (3b + 10) = 2(b + 10). 3b + 10 = 2b + 20. b = 10.",
        "question_type": "Standard Written"
    },
    {
        "text": "Share £80 between Ann and Ben in the ratio 3:5. How much does Ben get?",
        "answer": "50",
        "topic": "Ratio",
        "diff": 8,
        "explanation": "Total parts = 8. 1 part = 10. Ben gets 5 parts = 50.",
        "question_type": "Standard Written"
    },
    {
        "text": "A rectangular garden has a perimeter of 40m. The length is 4m more than the width. Find the width.",
        "answer": "8",
        "topic": "Algebra",
        "diff": 9,
        "explanation": "2(w + w + 4) = 40. 4w + 8 = 40. 4w = 32. w = 8.",
        "question_type": "Standard Written"
    },
    # Control question to test filtering
    {
        "text": "Control Question: High Diff Multiple Choice Ratio",
        "answer": "100",
        "topic": "Ratio",
        "diff": 9,
        "explanation": "Just a test.",
        "question_type": "Multiple Choice"
    }
]
