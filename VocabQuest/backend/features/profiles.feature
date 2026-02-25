Feature: Profile Management
    As a user
    I want to create and manage profiles
    So that multiple people can play on the same device

    Scenario: Create a New Profile
        Given no user named "David" exists
        When I request to create a profile named "David"
        Then the profile "David" should be created
        And "David" should have level 3 and score 0

    Scenario: Prevent Duplicate Profiles
        Given a user "Eve" already exists
        When I request to create a profile named "Eve"
        Then the creation should fail with an error

    Scenario: Delete a Profile
        Given a user "Frank" exists
        When I request to delete profile "Frank"
        Then the profile "Frank" should no longer exist
