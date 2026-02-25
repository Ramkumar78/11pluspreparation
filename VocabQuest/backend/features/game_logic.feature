Feature: Game Logic
    As a user
    I want to earn points and level up by spelling words correctly
    So that I can track my vocabulary progress

    Scenario: Correct Answer Increases Score and Streak
        Given a user "Alice" exists with score 0 and streak 0
        And the current word is "lion"
        When "Alice" submits the spelling "lion"
        Then the answer should be marked correct
        And "Alice" score should be greater than 0
        And "Alice" streak should be 1

    Scenario: Wrong Answer Resets Streak
        Given a user "Bob" exists with score 0 and streak 5
        And the current word is "tiger"
        When "Bob" submits the spelling "tyger"
        Then the answer should be marked incorrect
        And "Bob" streak should be 0

    Scenario: Level Up after 2 Consecutive Correct Answers
        Given a user "Charlie" exists with level 3 and streak 1
        And the current word is "bear"
        When "Charlie" submits the spelling "bear"
        Then "Charlie" streak should be 2
        And "Charlie" level should be 4
