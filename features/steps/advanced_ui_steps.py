from behave import when, then
from features.pages.advanced_ui_page import AdvancedUIPage
import logging

logger = logging.getLogger(__name__)

@when('I click on Advanced UI Features section')
def click_advanced_ui_section(context):
    """
    Click on Advanced UI Features section
    """
    context.advanced_ui = AdvancedUIPage(context.page)
    context.advanced_ui.click_advanced_ui_section()

@then('I should see "Challenge 1" as the title')
def verify_challenge_title(context):
    """
    Verify the challenge title is displayed
    """
    assert context.advanced_ui.is_element_visible(context.advanced_ui.CHALLENGE_TITLE), \
        "Challenge 1 title not visible"

@then('I should see book rating instructions')
def verify_instructions(context):
    """
    Verify the rating instructions are displayed
    """
    instructions = "Using Selenium (or any other tool) - read the * Rating of the book"
    assert context.advanced_ui.is_element_visible(f"text={instructions}"), \
        "Rating instructions not visible"

@when('I get the star rating for "{book_title}"')
def get_book_rating(context, book_title):
    """
    Get the star rating for the specified book
    """
    context.current_rating = context.advanced_ui.get_book_rating()

@when('I enter the star rating in the text box')
def enter_current_rating(context):
    """
    Enter the current star rating
    """
    context.advanced_ui.enter_rating(context.current_rating)

@when('I enter an incorrect star rating "{rating}"')
def enter_incorrect_rating(context, rating):
    """
    Enter an incorrect star rating
    """
    context.advanced_ui.enter_rating(rating)

@when('I enter the star rating "{rating}"')
def enter_specific_rating(context, rating):
    """
    Enter a specific star rating
    """
    context.advanced_ui.enter_rating(rating)

@when('I click Check Rating button')
def click_check_rating(context):
    """
    Click the Check Rating button
    """
    context.advanced_ui.click_check_rating()

@then('I should see "{expected_message}" message')
def verify_rating_message(context, expected_message):
    """
    Verify the rating result message
    """
    actual_message = context.advanced_ui.get_rating_result()
    assert actual_message == expected_message, \
        f"Expected message '{expected_message}' but got '{actual_message}'"
    
@then('I should see the correct validation message')
def verify_rating_validation_message(context):
    """
    Verify if the validation message is correct based on entered rating vs actual rating
    """
    actual_message = context.advanced_ui.get_rating_result()
    entered_rating = context.text_context if hasattr(context, 'text_context') else ""
    actual_rating = context.current_rating
    
    if entered_rating == actual_rating:
        expected_message = "Well done!"
    else:
        expected_message = "Try Again!"
        
    assert actual_message == expected_message, \
        f"Expected message '{expected_message}' but got '{actual_message}' for entered rating '{entered_rating}' and actual rating '{actual_rating}'"