DATA_PROBABILITY_LIST = [
    # --- PROBABILITY (Combined Events) ---
    {
        "text": "Two fair six-sided dice are rolled. What is the probability that the sum of the numbers is 7? (Answer as a fraction)",
        "answer": "1/6",
        "topic": "Probability",
        "diff": 8,
        "explanation": "There are 6x6=36 total outcomes. The pairs that sum to 7 are (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). That is 6 outcomes. Probability is 6/36 which simplifies to 1/6."
    },
    {
        "text": "A bag contains 3 red balls and 2 blue balls. A ball is picked and NOT replaced. Then a second ball is picked. What is the probability that both balls are red? (Answer as a fraction)",
        "answer": "3/10",
        "topic": "Probability",
        "diff": 9,
        "explanation": "Probability of first red = 3/5. Since it's not replaced, there are now 2 red and 2 blue (4 total). Probability of second red = 2/4 = 1/2. Combined probability = 3/5 x 1/2 = 3/10."
    },
    {
        "text": "A card is drawn from a standard deck of 52 cards. What is the probability it is a Heart or a King? (Answer as a fraction)",
        "answer": "4/13",
        "topic": "Probability",
        "diff": 9,
        "explanation": "There are 13 Hearts and 4 Kings. But the King of Hearts is counted twice. So 13 + 4 - 1 = 16 cards. Probability is 16/52. Divide top and bottom by 4: 4/13."
    },

    # --- STATISTICS (Reverse Mean) ---
    {
        "text": "The mean of 4 numbers is 8. What is the 5th number if the new mean is 9?",
        "answer": "13",
        "topic": "Statistics",
        "diff": 8,
        "explanation": "Total of 4 numbers = 4 x 8 = 32. Total of 5 numbers = 5 x 9 = 45. The difference is the 5th number: 45 - 32 = 13."
    },
    {
        "text": "The mean height of 5 children is 140cm. A 6th child joins and the mean becomes 142cm. How tall is the 6th child?",
        "answer": "152",
        "topic": "Statistics",
        "diff": 8,
        "explanation": "Total height of 5 children = 5 x 140 = 700. Total height of 6 children = 6 x 142 = 852. Difference = 852 - 700 = 152cm."
    },

    # --- TIME (Timetables) ---
    {
        "text": "A train leaves London at 14:45 and arrives in Paris at 18:10 (local time). Paris is 1 hour ahead of London. How many minutes was the journey?",
        "answer": "145",
        "topic": "Time",
        "diff": 7,
        "explanation": "Convert Paris time to London time: 18:10 - 1 hour = 17:10. Journey is from 14:45 to 17:10. 14:45 to 16:45 is 2 hours (120 mins). 16:45 to 17:10 is 25 minutes. Total: 120 + 25 = 145 mins."
    },
    {
        "text": "A bus journey takes 155 minutes. If it arrives at 11:20, what time did it depart? (Format HH:MM)",
        "answer": "08:45",
        "topic": "Time",
        "diff": 7,
        "explanation": "155 minutes is 2 hours and 35 minutes. Subtract 2 hours from 11:20 -> 09:20. Subtract 35 minutes: 09:20 - 20 mins = 09:00. 09:00 - 15 mins = 08:45."
    },

    # --- DATA & VENN DIAGRAMS ---
    {
        "text": "In a class of 30 students, 18 play Football and 15 play Cricket. 5 play neither. How many play both?",
        "answer": "8",
        "topic": "Venn Diagrams",
        "diff": 8,
        "explanation": "Total students = 30. Students playing at least one sport = 30 - 5 (neither) = 25. Sum of individual sports = 18 + 15 = 33. The overlap (both) = 33 - 25 = 8."
    },
    {
        "text": "50 people were asked about pets. 25 have a dog, 20 have a cat, and 8 have both. How many have neither?",
        "answer": "13",
        "topic": "Venn Diagrams",
        "diff": 8,
        "explanation": "Those with at least one pet = (Dog + Cat) - Both = 25 + 20 - 8 = 37. Those with neither = Total - 37 = 50 - 37 = 13."
    },
    {
        "text": "In a group of 100 people, 70 like Coffee, 60 like Tea. If everyone likes at least one, how many like ONLY Tea?",
        "answer": "30",
        "topic": "Venn Diagrams",
        "diff": 9,
        "explanation": "Everyone likes at least one, so Union = 100. Sum of individual = 70 + 60 = 130. Overlap (Both) = 130 - 100 = 30. Only Tea = Total Tea - Both = 60 - 30 = 30."
    }
]
