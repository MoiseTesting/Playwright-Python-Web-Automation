Feature: Form Interactions
    As a user
    I want to interact with various form elements
    So that I can test form functionality and validations

    Background:
        Given I navigate to the automation playground
        When I click on Forms section

    @forms @basic
    Scenario: Fill Basic Form Controls
        When I enter "5" years of automation experience
        And I select the following programming languages
            | language   |
            | JavaScript|
            | Python|
        And I select "Selenium" as the automation tool
        And I select "Selenium" as primary skill
        And I select the following languages from multi-select
            | language    |
            | Python     |
        And I enter "Test notes12345" in the notes area
        And I toggle "Speaks German" switch to "on"
        And I set German fluency level to "3"
        Then I should see the entered experience "5" displayed
        And I should see selected languages "Python JavaScript" displayed
        And I should see "SELENIUM" as selected tool
        And I should see "sel" as selected primary skill
        And I should see "python" in selected languages
        And I should see "Test notes12345" in notes validation
        And I should see "true" for German speaking status
        And I should see "3" as German fluency level

    @forms @readonly
    Scenario: Verify Read-Only Fields
        Then the "Common Sense" field should be read-only with value "Common Sense"
        And the "Current Salary" field should be disabled
        
    @forms @validation
    Scenario: Verify Form Validations
        When I click Submit Form
        Then I should see "provide a valid city" validation for city
        And I should see "provide a valid state" validation for state
        And I should see "provide a valid zip" validation for zip
        And I should see "must agree before submitting" validation for terms

    @forms @validation @happy-path
    Scenario: Successfully Submit Form
        When I enter "New York" as city
        And I enter "NY" as state
        And I enter "10001" as zip
        And I accept the terms and conditions
        And I click Submit Form
        

    @forms @file-upload
    Scenario: Upload Files
        When I select "index.html" for single file upload
        Then I should see "index.html" as the uploaded file name
        When I select multiple files for upload
            | filename     |
            | sample_text.txt |
            | index.html    |
        Then I should see " sample_text.txt index.html" as the uploaded files

    @forms @file-handling
Scenario: Handle File Upload and Download
    Given I navigate to the automation playground
    When I click on Forms section
    And I select "index.html" for single file upload
    Then I should see "index.html" as the uploaded file name
    When I select multiple files for upload
        | filename     |
        | sample_text.txt |
        | index.html       |
    Then I should see "sample_text.txt index.html" as the uploaded files
    When I click the download link
    Then the file should be downloaded successfully

    @forms @non-english
Scenario: Interact with Non-English Form Elements
    Given I navigate to the automation playground
    When I click on Forms section
    And I enter "Test Name" in the non-English name field
    And I select the following non-English options
        | language |
        | Marathi  |
        | Gujarati |
    Then I should see "Test Name" in the non-English name validation