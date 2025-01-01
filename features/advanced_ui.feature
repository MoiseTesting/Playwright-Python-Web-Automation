Feature: Advanced UI Features
    As a user
    I want to interact with advanced UI elements
    So that I can complete challenging automation scenarios

    Background:
        Given I navigate to the automation playground
        When I click on Advanced UI Features section

    @challenge @p1
    Scenario: Successfully Complete Book Rating Challenge
        Then I should see "Challenge 1" as the title
        And I should see book rating instructions
        When I get the star rating for "Sapiens: A Brief History of the Humankind"
        And I enter the star rating in the text box
        And I click Check Rating button
        Then I should see "Well done!" message

    @challenge @negative
    Scenario: Verify Incorrect Rating Validation
        When I get the star rating for "Sapiens: A Brief History of the Humankind"
        And I enter an incorrect star rating "****"
        And I click Check Rating button
        Then I should see "Try Again!" message

