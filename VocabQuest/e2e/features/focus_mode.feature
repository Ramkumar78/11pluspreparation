Feature: Focus Mode
  As a student
  I want to use Focus Mode
  So that I can study without distractions and track my time

  Scenario: Toggle Focus Mode and verify UI changes
    Given I am on the homepage
    Then I should see the "Focus Mode" toggle
    And I should see the session timer

    When I toggle Focus Mode on
    Then the background should be neutral
    And the bouncing lion should be hidden
    And the timer should be counting
