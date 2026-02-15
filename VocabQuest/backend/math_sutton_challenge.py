# High-level logic and worded maths problems for "Sutton SET" / Wilson's School

SUTTON_CHALLENGE_LIST = [
    # 1. Advanced Algebra (Forming equations from word scenarios)
    {
        "text": "A father is 4 times as old as his son. In 20 years, he will be twice as old. How old is the father now?",
        "answer": "40",
        "topic": "Algebra",
        "diff": 9,
        "explanation": "Let the son's age be s. Father is 4s. In 20 years: (4s + 20) = 2(s + 20). 4s + 20 = 2s + 40. Subtract 2s from both sides: 2s + 20 = 40. Subtract 20: 2s = 20. So s = 10. Father is 4 x 10 = 40.",
        "question_type": "Standard Written"
    },

    # 2. Complex Ratios (Combining two different ratios)
    {
        "text": "The ratio of cats to dogs is 2:3. The ratio of dogs to rabbits is 4:5. If there are 45 rabbits, how many cats are there?",
        "answer": "24",
        "topic": "Ratio",
        "diff": 9,
        "explanation": "Make the 'dogs' part the same in both ratios. LCM of 3 and 4 is 12. Cats:Dogs becomes 8:12 (multiplying by 4). Dogs:Rabbits becomes 12:15 (multiplying by 3). Combined ratio C:D:R is 8:12:15. Rabbits correspond to 15 parts. 15 parts = 45 rabbits, so 1 part = 3. Cats have 8 parts, so 8 x 3 = 24 cats.",
        "question_type": "Standard Written"
    },

    # 3. Logic/Number puzzles
    {
        "text": "I think of a number. I multiply it by 3, add 2, divide by 5, and then subtract 4. The result is 3. What was my number?",
        "answer": "11",
        "topic": "Logic",
        "diff": 8,
        "explanation": "Work backwards from the result (3). Opposite of subtract 4 is add 4: 3 + 4 = 7. Opposite of divide by 5 is multiply by 5: 7 x 5 = 35. Opposite of add 2 is subtract 2: 35 - 2 = 33. Opposite of multiply by 3 is divide by 3: 33 / 3 = 11.",
        "question_type": "Standard Written"
    },

    # 4. Inverse operations with fractions
    {
        "text": "A bottle is 2/5 full of water. When 300ml is added, it becomes 2/3 full. What is the capacity of the bottle in ml?",
        "answer": "1125",
        "topic": "Fractions",
        "diff": 9,
        "explanation": "Find the difference in fractions. 2/3 - 2/5. Common denominator is 15. 10/15 - 6/15 = 4/15. So 4/15 of the bottle is 300ml. To find 1/15, divide 300 by 4 = 75ml. The full capacity (15/15) is 75 x 15 = 1125ml.",
        "question_type": "Standard Written"
    },

    # 5. Speed, Distance, Time (Time delay)
    {
        "text": "Train A leaves London at 09:00 traveling at 60 mph. Train B leaves London at 10:30 traveling at 90 mph on the same track. At what time will Train B catch Train A?",
        "answer": "13:30",
        "topic": "Speed/Distance",
        "diff": 10,
        "explanation": "Train A has a head start of 1.5 hours (from 09:00 to 10:30). Distance = Speed x Time = 60 x 1.5 = 90 miles. Train B travels 30 mph faster than A (90 - 60). Time to catch up = Distance / Relative Speed = 90 / 30 = 3 hours. 3 hours after 10:30 is 13:30.",
        "question_type": "Standard Written"
    },

    # 6. Advanced Algebra (Simultaneous word problem)
    {
        "text": "3 apples and 2 bananas cost £1.80. 5 apples and 4 bananas cost £3.20. What is the cost of one banana in pence?",
        "answer": "30",
        "topic": "Algebra",
        "diff": 9,
        "explanation": "Equation 1: 3a + 2b = 180. Equation 2: 5a + 4b = 320. Double the first equation: 6a + 4b = 360. Now compare with Equation 2. The difference is 1 apple (6a - 5a). Cost difference is 360 - 320 = 40p. So an apple costs 40p. Substitute into Eq 1: 3(40) + 2b = 180 -> 120 + 2b = 180 -> 2b = 60 -> b = 30p.",
        "question_type": "Standard Written"
    },

    # 7. Complex Ratios (Sharing with change)
    {
        "text": "A bag contains red and blue counters in the ratio 3:4. I add 10 red counters, and the ratio becomes 5:4. How many blue counters are there?",
        "answer": "20",
        "topic": "Ratio",
        "diff": 9,
        "explanation": "The number of blue counters hasn't changed, and the 'blue' part of the ratio is 4 in both cases. This makes it easy! The red part increased from 3 to 5, which is a change of 2 parts. We know 2 parts = 10 counters. So 1 part = 5 counters. Blue counters = 4 parts = 4 x 5 = 20.",
        "question_type": "Standard Written"
    },

    # 8. Logic/Number Properties
    {
        "text": "Find a two-digit number such that the second digit is 3 times the first, and if you add 36 to the number, the digits reverse.",
        "answer": "26",
        "topic": "Logic",
        "diff": 9,
        "explanation": "Let the first digit be x. The second is 3x. Possible numbers: 13, 26, 39. (4 would mean 12, not a digit). Check adding 36: 13 + 36 = 49 (not 31). 26 + 36 = 62 (digits reversed!). 39 + 36 = 75. The answer is 26.",
        "question_type": "Standard Written"
    },

    # 9. Inverse operations with fractions (Remainder)
    {
        "text": "Peter spends 1/3 of his money on a toy. He then spends 1/4 of the REMAINING money on sweets. He has £15 left. How much money did he start with?",
        "answer": "30",
        "topic": "Fractions",
        "diff": 10,
        "explanation": "After spending 1/3, he has 2/3 left. He spends 1/4 of this remainder. 1/4 of 2/3 is 2/12 (or 1/6) of the original total. Fraction remaining = 2/3 - 1/6 = 4/6 - 1/6 = 3/6 = 1/2. If 1/2 of his money is £15, then the total was £30.",
        "question_type": "Standard Written"
    },

    # 10. Speed, Distance, Time (Average Speed)
    {
        "text": "A cyclist travels uphill at 10 km/h and downhill at 30 km/h. If the distance up equals the distance down, what is the average speed for the whole journey?",
        "answer": "15",
        "topic": "Speed/Distance",
        "diff": 10,
        "explanation": "Don't just average 10 and 30! Pick a distance, say 30km. Time up = 30/10 = 3 hours. Time down = 30/30 = 1 hour. Total distance = 60km. Total time = 4 hours. Average Speed = 60 / 4 = 15 km/h.",
        "question_type": "Standard Written"
    }
]
