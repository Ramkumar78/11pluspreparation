Feature: Profile UI
    As a user
    I want to see and manage profiles
    So that I can select who is playing

    Scenario: Displaying Existing Profiles
        Given the following profiles exist:
            | name   | level | score |
            | Alice  | 5     | 100   |
            | Bob    | 3     | 0     |
        When I load the profile selection screen
        Then I should see a profile for "Alice"
        And I should see a profile for "Bob"

    Scenario: Creating a New Profile
        Given no profiles exist
        When I load the profile selection screen
        And I enter "Charlie" into the new profile input
        And I click the create button
        Then I should see a profile for "Charlie"
