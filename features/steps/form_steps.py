
from behave import when, then
from features.pages.forms_page import FormsPage
from config.logging_config import logger
import os
import logging

logger = logging.getLogger(__name__)

@when('I click on Forms section')
def click_forms_section(context):
    """
    Click on Forms section
    """
    context.forms_page = FormsPage(context.page)
    context.forms_page.click_forms_section()

@when('I enter "{years}" years of automation experience')
def enter_experience(context, years):
    """
    Enter years of experience
    """
    context.forms_page.enter_experience(years)

@when('I select the following programming languages')
def select_languages(context):
    """
    Select programming languages
    """
    languages = [row['language'] for row in context.table]
    context.forms_page.select_programming_languages(languages)

@when('I select "{tool}" as the automation tool')
def select_automation_tool(context, tool):
    """
    Select automation tool
    """
    context.forms_page.select_automation_tool(tool)

@when('I select "{skill}" as primary skill')
def select_primary_skill(context, skill):
    """
    Select primary skill
    """
    context.forms_page.select_primary_skill(skill)

@when('I select the following languages from multi-select')
def select_multiple_languages(context):
    """
    Select multiple languages from the multi-select dropdown
    """
    languages = [row['language'] for row in context.table]
    logger.info(f"Selecting languages: {languages}")
    context.forms_page.select_languages(languages)

@when('I enter "{text}" in the notes area')
def enter_notes(context, text):
    """
    Enter notes
    """
    context.forms_page.enter_notes(text)

@when('I toggle "Speaks German" switch to "{state}"')
def toggle_german(context, state):
    """
    Toggle German switch
    """
    context.forms_page.toggle_german_switch(state)

@when('I set German fluency level to "{level}"')
def set_fluency(context, level):
    """
    Set German fluency level
    """
    context.forms_page.set_german_fluency(level)

@when('I click Submit Form')
def submit_empty_form(context):
    """
    Submit form 
    """
    context.forms_page.submit_form()

@when('I enter "{city}" as city')
def enter_city(context, city):
    """
    Enter city
    """
    context.forms_page.fill_validation_form(city=city)

@when('I enter "{state}" as state')
def enter_state(context, state):
    """
    Enter state
    """
    context.forms_page.fill_validation_form(state=state)

@when('I enter "{zip_code}" as zip')
def enter_zip(context, zip_code):
    """
    Enter zip code
    """
    context.forms_page.fill_validation_form(zip_code=zip_code)

@when('I accept the terms and conditions')
def accept_terms(context):
    """
    Accept terms and conditions
    """
    context.forms_page.accept_terms()


@then('I should see "{message}" validation for {field}')
def verify_validation_message(context, message, field):
    """
    Verify validation message for a specific field
    """
    # Clean up expected message
    expected_message = message.strip('"').strip().strip('.')
    
    # Get actual message
    actual_message = context.forms_page.get_validation_message(field.lower())
    actual_message = actual_message.strip().strip('.')
    
    # Log both messages for debugging
    logger.info(f"Expected message: '{expected_message}'")
    logger.info(f"Actual message: '{actual_message}'")
    
    # Compare core message content
    assert expected_message.lower() in actual_message.lower(), \
        f"Expected validation message containing '{expected_message}' for {field} but got '{actual_message}'"

@then('the "{field}" field should be read-only with value "{value}"')
def verify_readonly_field(context, field, value):
    """
    Verify read-only field
    """
    field_map = {
        "Common Sense": context.forms_page.COMMON_SENSE_INPUT,
        "Current Salary": context.forms_page.SALARY_INPUT
    }
    element = context.page.locator(field_map[field])
    assert element.is_enabled() is False, f"Field {field} should be disabled"
    assert element.get_attribute('placeholder') == value, \
        f"Expected value '{value}' but got '{element.get_attribute('placeholder')}'"
    
@then('I should see the entered experience "{years}" displayed')
def verify_experience_displayed(context, years):
    """
    Verify displayed experience years
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.EXPERIENCE_VALIDATION)
    assert actual_text == years, f"Expected {years} but got {actual_text}"

@when('I click the download link')
def click_download_link(context):
    """
    Click the download link and handle the download
    """
    with context.page.expect_download() as download_info:
        context.page.click('#download_file')
    download = download_info.value
    
    # Save to downloads directory
    context.download_path = os.path.join(context.downloads_dir, download.suggested_filename)
    download.save_as(context.download_path)
    logger.info(f"File downloaded to: {context.download_path}")

@then('the file should be downloaded successfully')
def verify_file_downloaded(context):
    """
    Verify file was downloaded successfully and clean up
    """
    try:
        # Verify file exists
        assert os.path.exists(context.download_path), \
            f"Downloaded file not found at {context.download_path}"
        
        # Verify file is not empty
        assert os.path.getsize(context.download_path) > 0, \
            f"Downloaded file is empty: {context.download_path}"
        
        logger.info(f"Successfully verified download: {context.download_path}")
        
    finally:
        # Clean up downloaded file
        if os.path.exists(context.download_path):
            os.remove(context.download_path)
            logger.info(f"Cleaned up downloaded file: {context.download_path}")

def after_scenario(context, scenario):
    """
    Clean up after each scenario
    """
    # Clean up downloads directory
    if hasattr(context, 'downloads_dir') and os.path.exists(context.downloads_dir):
        for file in os.listdir(context.downloads_dir):
            file_path = os.path.join(context.downloads_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up file {file_path}: {e}")

@then('the file should be downloaded to downloads directory')
def verify_file_downloaded(context):
    """
    Verify file was downloaded successfully
    """
    assert os.path.exists(context.download_path), \
        f"Downloaded file not found at {context.download_path}"

@then('I should see selected languages "{expected_languages}" displayed')
def verify_selected_languages(context, expected_languages):
    """
    Verify selected languages display
    Handles case-insensitive comparison
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.CHECKBOX_VALIDATION)
    # Convert both strings to uppercase for comparison
    assert expected_languages.upper() == actual_text.upper(), \
        f"Expected {expected_languages} but got {actual_text}"
@then('I should see "{tool}" as selected tool')
def verify_selected_tool(context, tool):
    """
    Verify selected automation tool
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.RADIO_VALIDATION)
    assert actual_text == tool, f"Expected {tool} but got {actual_text}"

@then('I should see "{skill}" as selected primary skill')
def verify_primary_skill(context, skill):
    """
    Verify selected primary skill
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.SKILL_VALIDATION)
    assert actual_text == skill, f"Expected {skill} but got {actual_text}"

@then('I should see "{languages}" in selected languages')
def verify_multiselect_languages(context, languages):
    """
    Verify selected languages in multi-select
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.LANGUAGE_VALIDATION)
    assert actual_text == languages, f"Expected {languages} but got {actual_text}"

@then('I should see "{text}" in notes validation')
def verify_notes_text(context, text):
    """
    Verify notes text
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.NOTES_VALIDATION)
    assert actual_text == text, f"Expected {text} but got {actual_text}"

@then('I should see "{status}" for German speaking status')
def verify_german_status(context, status):
    """
    Verify German speaking status
    """
    actual_status = context.forms_page.get_german_status()
    # Convert both to lowercase strings for comparison
    assert str(status).lower() == actual_status.lower(), \
        f"Expected German speaking status to be '{status}' but got '{actual_status}'"

@then('I should see "{level}" as German fluency level')
def verify_fluency_level(context, level):
    """
    Verify German fluency level
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.FLUENCY_VALIDATION)
    assert actual_text == level, f"Expected {level} but got {actual_text}"

@then('the form should be submitted successfully')
def verify_form_submission(context):
    """
    Verify form was submitted successfully
    """
    assert context.forms_page.verify_successful_submission(), \
        "Form was not submitted successfully"

@when('I select "{filename}" for single file upload')
def select_single_file(context, filename):
    """
    Select file for single file upload
    """
    context.forms_page.upload_single_file(filename)

@when('I select multiple files for upload')
def select_multiple_files(context):
    """
    Select multiple files for upload
    """
    filenames = [row['filename'] for row in context.table]
    context.forms_page.upload_multiple_files(filenames)

@then('I should see "{filename}" as the uploaded file name')
def verify_uploaded_filename(context, filename):
    """
    Verify uploaded file name
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.SINGLE_FILE_VALIDATION)
    assert actual_text == filename, f"Expected {filename} but got {actual_text}"

@then('I should see "{filenames}" as the uploaded files')
def verify_uploaded_filenames(context, filenames):
    """
    Verify uploaded files names
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.MULTIPLE_FILES_VALIDATION)
    assert actual_text.strip() == filenames.strip(), f"Expected {filenames} but got {actual_text}"

@when('I enter "{name}" in the non-English name field')
def enter_non_english_name(context, name):
    """
    Enter name in non-English name field
    """
    context.forms_page.enter_non_english_name(name)

@when('I select the following non-English options')
def select_non_english_options(context):
    """
    Select non-English language options
    Note: Use simple ASCII characters in the feature file table
    and map them to actual Unicode characters here
    """
    # Create a mapping for safer handling of non-English characters
    language_mapping = {
        "Marathi": "मराठी",
        "Gujarati": "ગુજરાતી",
        "Punjabi": "ਪੰਜਾਬੀ"
    }
    
    selected_languages = []
    for row in context.table:
        lang = row['language']
        if lang in language_mapping:
            selected_languages.append(language_mapping[lang])
    
    context.forms_page.select_non_english_languages(selected_languages)

@then('I should see "{text}" in the non-English name validation')
def verify_non_english_name(context, text):
    """
    Verify non-English name validation
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.NON_ENGLISH_NAME_VALIDATION)
    assert actual_text == text, f"Expected {text} but got {actual_text}"

@then('I should see "{text}" in non-English validation')
def verify_non_english_options(context, text):
    """
    Verify non-English options validation
    """
    actual_text = context.forms_page.get_element_text(context.forms_page.NON_ENGLISH_CHECKBOX_VALIDATION)
    assert actual_text == text, f"Expected {text} but got {actual_text}"

@then('the "Current Salary" field should be disabled')
def verify_salary_field_disabled(context):
    """
    Verify salary field is disabled
    """
    salary_field = context.page.locator(context.forms_page.SALARY_INPUT)
    assert salary_field.is_disabled(), "Salary field should be disabled"
    assert salary_field.get_attribute('placeholder') == "You should not provide this", \
        "Salary field placeholder text is incorrect"

@then('I should see "You must agree before submitting." for terms checkbox')
def verify_terms_validation(context):
    """
    Verify terms checkbox validation message
    """
    actual_message = context.forms_page.get_element_text(context.forms_page.TERMS_VALIDATION)
    assert actual_message == "You must agree before submitting.", \
        f"Expected 'You must agree before submitting.' but got '{actual_message}'"
