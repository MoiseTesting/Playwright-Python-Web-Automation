from behave import when, then
from features.pages.sample_pages import SamplePagesPage
import logging

logger = logging.getLogger(__name__)

@when('I click on the Sample Pages section')
def click_sample_pages(context):
    """
    Click on Sample Pages section
    """
    if not hasattr(context, 'sample_pages'):
        context.sample_pages = SamplePagesPage(context.page)
    context.sample_pages.click_sample_pages_section()
@then('I should see "Log in" page title')
def verify_login_title(context):
    """
    Verify we're on the login page
    """
    assert context.sample_pages.is_element_visible("h2:has-text('Log in')"), \
        "Login page title not visible"

@then('I should see "Already a user? Please login." text')
def verify_login_subtitle(context):
    """
    Verify login page subtitle
    """
    assert context.sample_pages.is_element_visible("text=Already a user? Please login."), \
        "Login page subtitle not visible"
    
@then('I should see the login form elements')
def verify_login_form(context):
    """
    Verify login form elements are visible
    """
    assert context.sample_pages.are_login_form_elements_visible(), \
        "Login form elements not visible"

@then('I should see "Hint-admin" text')
def verify_hint_text(context):
    """
    Verify hint text is visible
    """
    assert context.sample_pages.is_element_visible("text=Hint: admin"), \
        "Hint text not visible"

@when('I fill in the username "{username}"')
def fill_username(context, username):
    """Fill in username"""
    context.sample_pages.fill_login_form(username=username, password=None)

@when('I fill in the password "{password}"')
def fill_password(context, password):
    """Fill in password"""
    context.sample_pages.fill_login_form(username=None, password=password)

@when('I check the Remember me option')
def check_remember_me(context):
    """Check the Remember me checkbox"""
    context.sample_pages.fill_login_form(username=None, password=None, remember_me=True)

@when('I click the Log in button')
def click_login(context):
    """Click login button"""
    context.sample_pages.click_login_button()

@then('I should be redirected to the pizza order form')
def verify_pizza_form_redirect(context):
    """Verify that we are redirected to the pizza order form"""
    logger.info("Verifying redirect to pizza form")
    assert context.sample_pages.is_pizza_form_visible(), \
        "Pizza order form is not visible"

@then('I should see "{expected_text}" in the page')
def verify_page_title(context, expected_text):
    """Verify the page title matches the expected text"""
    logger.info(f"Verifying text '{expected_text}' is visible on the page")
    actual_text = context.sample_pages.get_element_text(context.sample_pages.PIZZA_TITLE)
    assert expected_text in actual_text, \
        f"Expected text '{expected_text}' not found in '{actual_text}'"

@then('I should see pizza customization options')
def verify_pizza_customization_options(context):
    """Verify all pizza customization options are present"""
    assert context.sample_pages.verify_pizza_form_sections(), \
        "Not all pizza form sections are visible"

@when('I select "{size}" pizza size')
def select_pizza_size(context, size):
    """Select pizza size"""
    context.sample_pages.select_pizza_size(size)

@when('I select "{flavor}" from pizza flavor dropdown')
def select_pizza_flavor(context, flavor):
    """Select pizza flavor"""
    context.sample_pages.select_pizza_flavor(flavor)

@when('I select "{sauce}" sauce')
def select_sauce(context, sauce):
    """Select sauce type"""
    context.sample_pages.select_sauce(sauce)

@when('I check the following toppings')
def check_toppings(context):
    """Check specified toppings"""
    for row in context.table:
        context.sample_pages.check_topping(row['topping'])

@when('I enter "{quantity}" as the quantity')
def enter_quantity(context, quantity):
    """Enter pizza quantity"""
    context.sample_pages.enter_quantity(quantity)

@when('I click Add to Cart')
def click_add_to_cart(context):
    """Click Add to Cart button"""
    context.sample_pages.click_add_to_cart()

@then('I should see the quantity validation message "{expected_message}"')
def verify_quantity_validation(context, expected_message):
    """Verify quantity validation message"""
    actual_message = context.sample_pages.get_quantity_validation_message()
    assert expected_message in actual_message, \
        f"Expected message '{expected_message}' not found in '{actual_message}'"

@then('I should see the "{expected_message}" message')
def verify_adding_cart_message(context, expected_message):
    """Verify adding to cart message"""
    actual_message = context.sample_pages.get_adding_to_cart_message()
    assert expected_message in actual_message, \
        f"Expected message '{expected_message}' not found in '{actual_message}'"

@then('I should see "{expected_message}" confirmation')
def verify_cart_confirmation(context, expected_message):
    """Verify cart confirmation message"""
    actual_message = context.sample_pages.get_cart_status_message()
    assert expected_message in actual_message, \
        f"Expected message '{expected_message}' not found in '{actual_message}'"
    
@when('I click on "New user? Register!" link')
def click_register_link(context):
    """
    Click on the register link
    """
    if not hasattr(context, 'sample_pages'):
        context.sample_pages = SamplePagesPage(context.page)
    context.sample_pages.click_element("text=New user? Register!")

@when('I click on "{link_text}" link')
def click_link_with_text(context, link_text):
    """Click on a link with specific text"""
    context.sample_pages.click_element(f"text={link_text}")

@then('I should be on the registration page')
def verify_registration_page(context):
    """Verify that we are on the registration page"""
    registration_title = "text=Register"
    assert context.sample_pages.is_element_visible(registration_title), \
        "Not on registration page"
    
@then('I should see "Register" page title')
def verify_registration_title(context):
    """
    Verify registration page title
    """
    assert context.sample_pages.is_element_visible("h2:has-text('Register')"), \
        "Registration page title not visible"
    
@then('I should see "Create your account. It\'s free and only takes a minute." text')
def verify_registration_subtitle(context):
    """
    Verify registration page subtitle
    """
    assert context.sample_pages.is_element_visible("text=Create your account. It's free and only takes a minute."), \
        "Registration page subtitle not visible"
    
