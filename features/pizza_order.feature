Feature: Pizza Order Functionality
    As a logged-in user
    I want to customize and order pizzas
    So that I can place my order successfully

    Background:
        Given I navigate to the automation playground
        When I click on the Sample Pages section
        And I fill in the username "admin"
        And I fill in the password "admin"
        And I click the Log in button

    @regression
    Scenario: Successful Login Redirects to Pizza Form
        Then I should be redirected to the pizza order form
        And I should see "Dinesh's Pizza House" in the page
        And I should see pizza customization options

    @regression @happy-path
    Scenario: Successfully Add Pizza to Cart
        When I select "Small" pizza size
        And I select "Pepperoni" from pizza flavor dropdown
        And I select "Buffalo" sauce
        And I check the following toppings
            | topping      |
            | Onions      |
            | Green Olive |
        And I enter "2" as the quantity
        And I click Add to Cart
        Then I should see the "Adding to the cart..." message
        And I should see "Pizza added to the cart!" confirmation

    @regression @validation
    Scenario: Verify Quantity Validation Message
        When I select "Medium" pizza size
        And I select "Supreme" from pizza flavor dropdown
        And I select "Barbeque" sauce
        And I enter "0" as the quantity
        And I click Add to Cart
        Then I should see the quantity validation message "Quantity must be 1 or more!"