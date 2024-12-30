Feature: Home Page Functionality
    As a user
    I want to access the automation playground home page
    So that I can interact with various automation elements

    @smoke @p1
    Scenario: Successfully load the home page
        Given I navigate to the automation playground
        Then I should see the page title "The Playground"
        And I should see the subtitle "an Application Under Test"