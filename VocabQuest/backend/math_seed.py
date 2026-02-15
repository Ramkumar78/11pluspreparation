import random
import math

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
    },

    # --- SUTTON SET: Advanced Ratio & Percentage ---
    {
        "text": "In a school of 1200 students, 45% are boys. 20% of the boys play cricket. How many boys play cricket?",
        "answer": "108",
        "topic": "Percentages",
        "diff": 8,
        "explanation": "First, find the number of boys: 45% of 1200. 10% is 120, so 40% is 480, 5% is 60. Total boys = 540. Now find 20% of 540. 10% is 54, so 20% is 108."
    },
    {
        "text": "The ratio of apples to oranges in a box is 3:5. If there are 12 more oranges than apples, how many fruit are there in total?",
        "answer": "48",
        "topic": "Ratio",
        "diff": 9,
        "explanation": "Difference in parts is 5 - 3 = 2 parts. We know 2 parts = 12 fruit. So 1 part = 6 fruit. Total parts = 3 + 5 = 8 parts. Total fruit = 8 * 6 = 48."
    },
    {
        "text": "A car travels 90km in 1 hour 15 minutes. At the same speed, how far will it travel in 2 hours?",
        "answer": "144",
        "topic": "Speed/Distance",
        "diff": 8,
        "explanation": "1 hr 15 mins = 75 mins. Speed = 90km / 75mins = 1.2 km/min. In 2 hours (120 mins), distance = 1.2 * 120 = 144km."
    },
    {
        "text": "Three friends share a prize. Alice gets 1/3, Bob gets 2/5, and Charlie gets the rest. If Charlie gets £24, what was the total prize?",
        "answer": "90",
        "topic": "Fractions",
        "diff": 9,
        "explanation": "Alice + Bob = 1/3 + 2/5 = 5/15 + 6/15 = 11/15. Charlie gets the remainder: 1 - 11/15 = 4/15. If 4/15 = £24, then 1/15 = £6. Total (15/15) = 15 * 6 = £90."
    },
    {
        "text": "Product A costs £40 and is reduced by 20%. Product B costs £50 and is reduced by £15. Which is cheaper now, and by how much?",
        "answer": "A by 3",
        "topic": "Percentages",
        "diff": 8,
        "explanation": "Product A: 20% of 40 is 8. Price = 32. Product B: 50 - 15 = 35. Product A (£32) is cheaper than B (£35) by £3. Enter '3' or 'A by 3'."
    }
]

# SUTTON CHALLENGE QUESTIONS
sutton_challenge_questions = [
    {
        "text": "If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch 100 mice in 100 minutes?",
        "answer": "3",
        "topic": "Logic",
        "diff": 10,
        "explanation_text": "Don't be tricked! 3 cats take 3 mins for 3 mice. This means 1 cat takes 3 mins to catch 1 mouse. In 100 minutes, 1 cat could catch (100÷3) = 33 mice. But simpler: The RATE is the same. The cats work in parallel. 3 cats catch 1 mouse per minute (combined). So in 100 minutes, the SAME 3 cats catch 100 mice."
    },
    {
        "text": "A train leaves Station A at 60 mph. Another train leaves Station B towards A at 40 mph. The stations are 100 miles apart. How long until they meet?",
        "answer": "1 hour",
        "topic": "Speed/Distance",
        "diff": 9,
        "explanation_text": "They are moving towards each other, so add their speeds: 60 + 40 = 100 mph. Distance is 100 miles. Time = Distance / Speed = 100 / 100 = 1 hour."
    },
    {
        "text": "It takes 5 machines 5 minutes to make 5 widgets. How long does it take 100 machines to make 100 widgets?",
        "answer": "5 minutes",
        "topic": "Work/Time",
        "diff": 9,
        "explanation_text": "Each machine takes 5 minutes to make 1 widget (since 5 machines make 5 widgets in 5 minutes). So 100 machines working simultaneously will make 100 widgets in 5 minutes."
    },
    {
        "text": "When I was 6 years old, my sister was half my age. Now I am 70. How old is my sister?",
        "answer": "67",
        "topic": "Age Problem",
        "diff": 8,
        "explanation_text": "When you were 6, your sister was 3 (half of 6). The age difference is 3 years. When you are 70, she is still 3 years younger, so 70 - 3 = 67."
    },
    {
        "text": "A snail is at the bottom of a 20-foot well. Each day, it climbs up 3 feet, but at night it slips back 2 feet. How many days will it take to reach the top?",
        "answer": "18",
        "topic": "Logic",
        "diff": 10,
        "explanation_text": "Net gain per day is 1 foot. After 17 days, it has climbed 17 feet. On the 18th day, it climbs 3 feet, reaching 20 feet (top) and climbs out before slipping back."
    }
]


def generate_algebra_substitution(level):
    """Generates 'Sutton SET' style algebra substitution questions."""
    # Variables and simple positive integer values
    vars = ['a', 'b', 'x', 'y', 'n', 'p']
    v1_name, v2_name = random.sample(vars, 2)
    v1_val = random.randint(2, 8)
    v2_val = random.randint(2, 8)

    # Ensure distinct values to make it interesting, but not strictly required
    while v2_val == v1_val:
        v2_val = random.randint(2, 8)

    # Patterns:
    # 1. c1*v1 + c2*v2
    # 2. c1*v1 - c2*v2 (ensure positive)
    # 3. v1^2 + v2
    # 4. 2(v1 + v2)
    pattern = random.choice([1, 2, 3, 4])

    question_text = f"If ${v1_name} = {v1_val}$ and ${v2_name} = {v2_val}$, what is the value of "
    expr_str = ""
    ans_val = 0
    explanation = ""

    if pattern == 1:
        c1 = random.randint(2, 5)
        c2 = random.randint(2, 5)
        expr_str = f"${c1}{v1_name} + {c2}{v2_name}$?"
        ans_val = c1 * v1_val + c2 * v2_val
        explanation = f"Substitute values: {c1}({v1_val}) + {c2}({v2_val}) = {c1*v1_val} + {c2*v2_val} = {ans_val}."

    elif pattern == 2:
        c1 = random.randint(3, 6)
        c2 = random.randint(1, 2)
        # Ensure positive
        while (c1 * v1_val) <= (c2 * v2_val):
             c1 += 1
        expr_str = f"${c1}{v1_name} - {c2}{v2_name}$?"
        ans_val = c1 * v1_val - c2 * v2_val
        explanation = f"Substitute values: {c1}({v1_val}) - {c2}({v2_val}) = {c1*v1_val} - {c2*v2_val} = {ans_val}."

    elif pattern == 3:
        expr_str = f"${v1_name}^2 + {v2_name}$?"
        ans_val = v1_val**2 + v2_val
        explanation = f"Substitute values: {v1_val}² + {v2_val} = {v1_val**2} + {v2_val} = {ans_val}."

    elif pattern == 4:
        expr_str = f"$2({v1_name} + {v2_name})$?"
        ans_val = 2 * (v1_val + v2_val)
        explanation = f"Brackets first: ({v1_val} + {v2_val}) = {v1_val+v2_val}. Then multiply by 2: 2 x {v1_val+v2_val} = {ans_val}."

    question_text += expr_str

    # Generate Distractors
    options = set()
    options.add(ans_val)
    while len(options) < 5:
        # Generate close numbers
        diff = random.randint(-5, 5)
        if diff == 0: continue
        opt = ans_val + diff
        if opt > 0:
            options.add(opt)

    options_list = list(options)
    random.shuffle(options_list)

    return {
        "question": question_text,
        "options": [str(x) for x in options_list],
        "answer": str(ans_val),
        "explanation": explanation
    }


def generate_ratio_proportion(level):
    """Generates word problems for Ratio & Proportion."""
    # Pattern 1: Sharing a total
    # Pattern 2: Scaling a recipe (Proportion)

    pattern = random.choice([1, 2])

    question_text = ""
    ans_val = 0
    explanation = ""

    if pattern == 1:
        # Share Total
        ratio_a = random.randint(2, 5)
        ratio_b = random.randint(2, 5)
        total_parts = ratio_a + ratio_b
        multiplier = random.randint(2, 12) * 5 # Multiples of 5 are nice numbers usually
        total_amount = total_parts * multiplier

        # Determine question target
        target = random.choice(['larger', 'smaller', 'specific'])

        question_text = f"Share {total_amount} sweets in the ratio {ratio_a}:{ratio_b}. "

        val_a = ratio_a * multiplier
        val_b = ratio_b * multiplier

        if target == 'larger':
            question_text += "How many does the larger share get?"
            ans_val = max(val_a, val_b)
            explanation = f"Total parts = {ratio_a}+{ratio_b}={total_parts}. 1 part = {total_amount}/{total_parts}={multiplier}. Larger share is {max(ratio_a, ratio_b)} parts x {multiplier} = {ans_val}."
        elif target == 'smaller':
            question_text += "How many does the smaller share get?"
            ans_val = min(val_a, val_b)
            explanation = f"Total parts = {total_parts}. 1 part = {multiplier}. Smaller share is {min(ratio_a, ratio_b)} parts x {multiplier} = {ans_val}."
        else: # specific (first one)
            question_text += f"How many sweets correspond to the '{ratio_a}' part?"
            ans_val = val_a
            explanation = f"Total parts = {total_parts}. 1 part = {multiplier}. The share for {ratio_a} is {ratio_a} x {multiplier} = {ans_val}."

    elif pattern == 2:
        # Recipe / Proportion
        # "If 4 cakes cost 20, how much for 6?"
        item_count_1 = random.randint(2, 5)
        cost_1 = item_count_1 * random.randint(3, 8) # Ensure divisible
        item_count_2 = item_count_1 + random.randint(1, 5)

        question_text = f"If {item_count_1} toy cars cost £{cost_1}, how much do {item_count_2} cars cost?"
        unit_cost = cost_1 // item_count_1
        ans_val = unit_cost * item_count_2
        explanation = f"Find the cost of 1 car: £{cost_1} / {item_count_1} = £{unit_cost}. Then for {item_count_2} cars: {item_count_2} x £{unit_cost} = £{ans_val}."

    # Generate Distractors
    options = set()
    options.add(ans_val)
    while len(options) < 5:
        diff = random.choice([-10, -5, -2, -1, 1, 2, 5, 10, 20])
        opt = ans_val + diff
        if opt > 0:
            options.add(opt)

    options_list = list(options)
    random.shuffle(options_list)

    return {
        "question": question_text,
        "options": [str(x) for x in options_list],
        "answer": str(ans_val),
        "explanation": explanation
    }


def generate_fdp_conversion(level):
    """Generates rapid-fire FDP conversion questions."""
    # Types: Frac->Dec, Frac->Perc, Dec->Frac, Dec->Perc, Perc->Frac, Perc->Dec
    # We focus on common equivalents as per 11+ requirements

    equivalents = [
        {"frac": "1/2", "dec": "0.5", "perc": "50%"},
        {"frac": "1/4", "dec": "0.25", "perc": "25%"},
        {"frac": "3/4", "dec": "0.75", "perc": "75%"},
        {"frac": "1/5", "dec": "0.2", "perc": "20%"},
        {"frac": "2/5", "dec": "0.4", "perc": "40%"},
        {"frac": "3/5", "dec": "0.6", "perc": "60%"},
        {"frac": "4/5", "dec": "0.8", "perc": "80%"},
        {"frac": "1/10", "dec": "0.1", "perc": "10%"},
        {"frac": "3/10", "dec": "0.3", "perc": "30%"},
        {"frac": "7/10", "dec": "0.7", "perc": "70%"},
        {"frac": "9/10", "dec": "0.9", "perc": "90%"},
        {"frac": "1/8", "dec": "0.125", "perc": "12.5%"},
        {"frac": "1/3", "dec": "0.33...", "perc": "33.3%"},
        {"frac": "2/3", "dec": "0.66...", "perc": "66.7%"},
    ]

    item = random.choice(equivalents)
    type_q = random.choice(["F2D", "F2P", "D2F", "D2P", "P2F", "P2D"])

    question_text = ""
    ans_val = ""
    distractors = []
    explanation = ""

    if type_q == "F2D":
        question_text = f"What is {item['frac']} as a decimal?"
        ans_val = item['dec']
        # Distractors: pick other decimals
        others = [x['dec'] for x in equivalents if x['dec'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"To convert to a decimal, divide the top by the bottom: {item['frac']} = {item['dec']}."

    elif type_q == "F2P":
        question_text = f"What is {item['frac']} as a percentage?"
        ans_val = item['perc']
        others = [x['perc'] for x in equivalents if x['perc'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"To convert to a percentage, multiply by 100: {item['frac']} = {item['perc']}."

    elif type_q == "D2F":
        question_text = f"What is {item['dec']} as a fraction?"
        ans_val = item['frac']
        others = [x['frac'] for x in equivalents if x['frac'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"The decimal {item['dec']} is equivalent to the fraction {item['frac']}."

    elif type_q == "D2P":
        question_text = f"What is {item['dec']} as a percentage?"
        ans_val = item['perc']
        others = [x['perc'] for x in equivalents if x['perc'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"To convert decimal to percentage, multiply by 100: {item['dec']} = {item['perc']}."

    elif type_q == "P2F":
        question_text = f"What is {item['perc']} as a fraction?"
        ans_val = item['frac']
        others = [x['frac'] for x in equivalents if x['frac'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"{item['perc']} means {item['perc'].replace('%','')} per 100. As a fraction, this simplifies to {item['frac']}."

    elif type_q == "P2D":
        question_text = f"What is {item['perc']} as a decimal?"
        ans_val = item['dec']
        others = [x['dec'] for x in equivalents if x['dec'] != ans_val]
        distractors = random.sample(others, 4)
        explanation = f"To convert percentage to decimal, divide by 100: {item['perc']} = {item['dec']}."

    options = [ans_val] + distractors
    random.shuffle(options)

    return {
        "question": question_text,
        "options": options,
        "answer": ans_val,
        "explanation": explanation
    }
