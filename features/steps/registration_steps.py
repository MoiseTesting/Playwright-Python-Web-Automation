from behave import when, then
from features.pages.registration_page import RegistrationPage
import logging

logger = logging.getLogger(__name__)

@when('I fill in the registration form with following details')
def fill_registration_form(context):
    """
    Fill in all registration form fields from data table
    """
    if not hasattr(context, 'registration_page'):
        context.registration_page = RegistrationPage(context.page)
    
    # Convert table to dictionary
    form_data = {row['field']: row['value'] for row in context.table}
    context.registration_page.fill_registration_form(form_data)

@when('I accept the terms and privacy policy')
def accept_terms(context):
    """
    Accept the terms and conditions
    """
    context.registration_page.accept_terms()

@when('I click Register Now button')
def click_register(context):
    """
    Click the register button
    """
    context.registration_page.click_register()

@then('I should be redirected to confirmation page')
def verify_confirmation_page(context):
    """
    Verify redirect to confirmation page
    """
    assert context.registration_page.is_on_confirmation_page(), \
        "Not redirected to confirmation page"

@then('I should see the error message "{expected_message}"')
def verify_error_message(context, expected_message):
    """
    Verify error message text
    """
    actual_message = context.registration_page.get_error_message()
    assert expected_message in actual_message, \
        f"Expected message '{expected_message}' not found in '{actual_message}'"