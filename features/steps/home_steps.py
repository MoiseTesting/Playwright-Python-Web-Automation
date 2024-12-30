from behave import given, when, then
from features.pages.home_page import HomePage
from config.logging_config import logger

@given('I navigate to the automation playground')
def navigate_to_home(context):
    """
    Navigate to the automation playground home page
    """
    logger.info("Navigating to automation playground home page")
    context.home_page = HomePage(context.page)
    context.home_page.navigate()

@then('I should see the page title "{expected_title}"')
def verify_page_title(context, expected_title):
    """
    Verify the page title matches the expected text
    """
    logger.info(f"Verifying page title matches: {expected_title}")
    actual_title = context.home_page.get_page_title()
    assert actual_title == expected_title, \
        f"Expected title '{expected_title}' but got '{actual_title}'"

@then('I should see the subtitle "{expected_subtitle}"')
def verify_page_subtitle(context, expected_subtitle):
    """
    Verify the page subtitle matches the expected text
    """
    logger.info(f"Verifying page subtitle matches: {expected_subtitle}")
    actual_subtitle = context.home_page.get_page_subtitle()
    assert actual_subtitle == expected_subtitle, \
        f"Expected subtitle '{expected_subtitle}' but got '{actual_subtitle}'"