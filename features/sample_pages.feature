Feature: Sample Pages Login and Registration
    As a user
    I want to access the sample pages section
    So that I can interact with login and registration functionality

    Background:
        Given I navigate to the automation playground
        When I click on the Sample Pages section
        
    @smoke @p1
    Scenario: Navigate to Login Page via Sample Pages
        Then I should see "Log in" page title
        And I should see "Already a user? Please login." text
        And I should see the login form elements
        And I should see "Hint-admin" text
    
    @regression
    Scenario: Navigate to Registration Page
        When I click on "New user? Register!" link
        Then I should be on the registration page
    
    @regression @registration @p1
    Scenario: Successfully Register New User
        When I click on "New user? Register!" link
        Then I should see "Register" page title
        And I should see "Create your account. It's free and only takes a minute." text
        When I fill in the registration form with following details
            | field             | value            |
            | First Name       | John             |
            | Last Name        | Doe              |
            | Email            | john@example.com  |
            | Password         | SecurePass123    |
            | Confirm Password | SecurePass123    |
        And I accept the terms and privacy policy
        And I click Register Now button
        Then I should be redirected to confirmation page

    @regression @registration @validation
    Scenario: Verify Password Mismatch Validation
        When I click on "New user? Register!" link
        And I fill in the registration form with following details
            | field             | value            |
            | First Name       | John             |
            | Last Name        | Doe              |
            | Email            | john@example.com  |
            | Password         | SecurePass123    |
            | Confirm Password | DifferentPass123 |
        And I accept the terms and privacy policy
        And I click Register Now button
        Then I should see the error message "Passwords don't match. Try again!!"