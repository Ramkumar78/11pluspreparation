Feature: Game UI
    As a player
    I want to interact with the game interface
    So that I can play the vocabulary game

    Scenario: Typing in the Custom Input
        Given the game is loaded with the word "lion"
        When I wait for the reading phase to complete
        And I type "lion" into the input box
        Then the input box should display "LION"

    Scenario: Submitting a Correct Answer
        Given the game is loaded with the word "lion"
        When I wait for the reading phase to complete
        And I type "lion" into the input box
        And I click the "GO!" button
        Then the answer should be submitted to the backend
