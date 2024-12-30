from features.pages.base_page import BasePage
import os
import logging

logger = logging.getLogger(__name__)

class FormsPage(BasePage):
    """
    Forms page object containing elements and methods for form interactions
    """
    
    # Basic Form Controls
    FORMS_LINK = "a[href='forms.html']"
    EXPERIENCE_INPUT = "#exp"
    EXPERIENCE_VALIDATION = "#exp_help"
    
    # Checkboxes
    PYTHON_CHECKBOX = "#check_python"
    JAVASCRIPT_CHECKBOX = "#check_javascript"
    CHECKBOX_VALIDATION = "#check_validate"
    
    # Radio Buttons
    SELENIUM_RADIO = "#rad_selenium"
    PROTRACTOR_RADIO = "#rad_protractor"
    RADIO_VALIDATION = "#rad_validate"
    
    # Dropdowns
    PRIMARY_SKILL_DROPDOWN = "#select_tool"
    LANGUAGE_MULTISELECT = "#select_lang"
    SKILL_VALIDATION = "#select_tool_validate"
    LANGUAGE_VALIDATION = "#select_lang_validate"
    
    # Text Area
    NOTES_AREA = "#notes"
    NOTES_VALIDATION = "#area_notes_validate"
    
    # German Options
    GERMAN_SWITCH = ".custom-control-label[for='german']"
    GERMAN_FLUENCY = "#fluency"
    GERMAN_VALIDATION = "#german_validate"
    FLUENCY_VALIDATION = "#fluency_validate"
    
    # Read-only Fields
    COMMON_SENSE_INPUT = "#common_sense"
    SALARY_INPUT = "#salary"
    
    # Form Validation Elements
    CITY_INPUT = "#validationCustom03"
    STATE_INPUT = "#validationCustom04"
    ZIP_INPUT = "#validationCustom05"
    TERMS_CHECKBOX = "#invalidCheck"
    SUBMIT_BUTTON = "button[type='submit']"
    
    # Validation Messages
    CITY_VALIDATION = "#invalid_city"
    STATE_VALIDATION = "#invalid_state"
    ZIP_VALIDATION = "#invalid_zip"
    TERMS_VALIDATION = "#invalid_terms"
    
    # File Upload
    SINGLE_FILE_UPLOAD = "#upload_cv"
    MULTIPLE_FILES_UPLOAD = "#upload_files"
    SINGLE_FILE_VALIDATION = "#validate_cv"
    MULTIPLE_FILES_VALIDATION = "#validate_files"
    
    # Non-English Elements
    NON_ENGLISH_NAME = "input#नाव"  # Using ID directly
    MARATHI_CHECKBOX = "input#मराठी"
    GUJARATI_CHECKBOX = "input#ગુજરાતી"
    PUNJABI_CHECKBOX = "input#ਪੰਜਾਬੀ"
    NON_ENGLISH_NAME_VALIDATION = "#नाव_तपासा"
    
    def click_forms_section(self):
        """
        Click on the Forms section link
        """
        self.logger.info("Clicking on Forms section")
        self.click_element(self.FORMS_LINK)
        
    def enter_experience(self, years: str):
        """
        Enter years of automation experience
        """
        self.logger.info(f"Entering {years} years of experience")
        self.fill_text(self.EXPERIENCE_INPUT, years)
        
    def select_programming_languages(self, languages: list):
        """
        Select programming language checkboxes using double-click if needed
        """
        self.logger.info(f"Starting to select languages: {languages}")
        
        checkbox_info = {
            "Python": {
                "checkbox": "#check_python",
                "validation_text": "PYTHON"
            },
            "JavaScript": {
                "checkbox": "#check_javascript",
                "validation_text": "JAVASCRIPT"
            }
        }
        
        for lang in languages:
            if lang in checkbox_info:
                self.logger.info(f"Attempting to select {lang}")
                checkbox = self.page.locator(checkbox_info[lang]["checkbox"])
                
                # Check current state
                current_state = checkbox.is_checked()
                self.logger.info(f"{lang} initial state: {current_state}")
                
                # First click
                self.page.click(checkbox_info[lang]["checkbox"], force=True)
                self.page.wait_for_timeout(500)  # Short wait after click
                
                # Check if state changed to desired state
                new_state = checkbox.is_checked()
                self.logger.info(f"{lang} state after first click: {new_state}")
                
                # If not in desired state, click again
                if not new_state:
                    self.logger.info(f"First click didn't set {lang}, trying second click")
                    self.page.click(checkbox_info[lang]["checkbox"], force=True)
                    self.page.wait_for_timeout(500)
                    final_state = checkbox.is_checked()
                    self.logger.info(f"{lang} state after second click: {final_state}")
                    
                    if not final_state:
                        screenshot_path = f"checkbox_failure_{lang.lower()}.png"
                        self.page.screenshot(path=screenshot_path)
                        raise AssertionError(f"Could not select {lang} checkbox after two attempts")
        
        # Final verification of all selections
        for lang in languages:
            checkbox = self.page.locator(checkbox_info[lang]["checkbox"])
            if not checkbox.is_checked():
                raise AssertionError(f"{lang} checkbox lost its selection")
                
        # Verify validation text
        final_validation = self.get_element_text("#check_validate")
        self.logger.info(f"Final validation text: {final_validation}")
        
        # Verify all selected languages appear in validation text
        missing_languages = []
        for lang in languages:
            if checkbox_info[lang]["validation_text"] not in final_validation:
                missing_languages.append(lang)
        
        if missing_languages:
            self.page.screenshot(path="validation_text_failure.png")
            raise AssertionError(f"Languages not showing in validation text: {missing_languages}")
                
    def select_automation_tool(self, tool: str):
        """
        Select automation tool radio button
        """
        self.logger.info(f"Selecting automation tool: {tool}")
        if tool == "Selenium":
            self.click_element(self.SELENIUM_RADIO)
        elif tool == "Protractor":
            self.click_element(self.PROTRACTOR_RADIO)

    def verify_successful_submission(self) -> bool:
        """
        Verify form was submitted successfully
        """
        self.logger.info("Verifying successful form submission")
        try:
            # Wait for URL to change or confirmation element to appear
            return (
                self.page.url.endswith('confirmation.html') or
                self.is_element_visible("text=Form submitted successfully")  # Add appropriate selector
            )
        except Exception as e:
            self.logger.error(f"Error verifying form submission: {str(e)}")
            return False        
            
    def select_primary_skill(self, skill: str):
        """
        Select primary skill from dropdown
        """
        self.logger.info(f"Selecting primary skill: {skill}")
        self.page.select_option(self.PRIMARY_SKILL_DROPDOWN, label=skill)
        
    def select_languages(self, languages: list):
        """
        Select languages from multi-select dropdown
        """
        self.logger.info(f"Selecting languages: {languages}")
        # Use value option instead of values for multi-select
        self.page.select_option(self.LANGUAGE_MULTISELECT, value=[lang.lower() for lang in languages])

# Alternative method if the above doesn't work:
    def select_languages_alternative(self, languages: list):
        """
        Alternative method to select languages from multi-select dropdown
        """
        self.logger.info(f"Selecting languages: {languages}")
        for lang in languages:
            self.page.select_option(self.LANGUAGE_MULTISELECT, value=lang.lower())
        
    def enter_notes(self, text: str):
        """
        Enter text in notes area
        """
        self.logger.info(f"Entering notes: {text}")
        self.fill_text(self.NOTES_AREA, text)
        
    def toggle_german_switch(self, state: str):
        """
        Toggle German switch to specified state using double-click if needed
        """
        self.logger.info(f"Setting German switch to: {state}")
        desired_state = state.lower() == "on"
        
        checkbox = self.page.locator(self.GERMAN_SWITCH)
        current_state = checkbox.is_checked()
        
        if current_state != desired_state:
            # First click
            self.click_element(self.GERMAN_SWITCH)
            self.page.wait_for_timeout(500)
            
            # Check if we got desired state
            new_state = checkbox.is_checked()
            if new_state != desired_state:
                # Try second click if needed
                self.click_element(self.GERMAN_SWITCH)
                self.page.wait_for_timeout(500)

    def get_german_status(self) -> str:
        """
        Get the German speaking status text
        """
        return self.get_element_text(self.GERMAN_VALIDATION)
            
    def set_german_fluency(self, level: str):
        """
        Set German fluency level
        """
        self.logger.info(f"Setting German fluency to: {level}")
        self.page.fill(self.GERMAN_FLUENCY, level)
        
    def fill_validation_form(self, city: str = None, state: str = None, zip_code: str = None):
        """
        Fill validation form fields
        """
        if city:
            self.fill_text(self.CITY_INPUT, city)
        if state:
            self.fill_text(self.STATE_INPUT, state)
        if zip_code:
            self.fill_text(self.ZIP_INPUT, zip_code)
            
    def accept_terms(self):
        """
        Accept terms and conditions
        """
        self.logger.info("Accepting terms and conditions")
        self.click_element(self.TERMS_CHECKBOX)
        
    def submit_form(self):
        """
        Click the submit form button
        """
        self.logger.info("Submitting form")
        self.click_element(self.SUBMIT_BUTTON)
        # Wait for validations to appear
        self.page.wait_for_timeout(500)

    def get_validation_message(self, field: str) -> str:
        """
        Get validation message for specific field and clean it
        """
        validation_selectors = {
            'city': "#invalid_city",
            'state': "#invalid_state",
            'zip': "#invalid_zip",
            'terms': "#invalid_terms"
        }
        
        if field not in validation_selectors:
            raise ValueError(f"Unknown field: {field}")
            
        self.logger.info(f"Getting validation message for {field}")
        # Add wait for validation message to appear
        self.wait_for_element(validation_selectors[field])
        # Get text and clean it
        message = self.get_element_text(validation_selectors[field])
        return message.strip() if message else ""
    
    def get_field_validation_state(self, field: str) -> dict:
        """
        Get detailed validation information for debugging
        """
        selector = f"#{field}"
        element = self.page.locator(selector)
        return {
            'value': element.input_value(),
            'valid': element.get_attribute('aria-invalid') != 'true',
            'validation_message': self.get_validation_message(field)
        }
    
    def upload_single_file(self, filename: str):
        """
        Upload a single file
        """
        file_path = os.path.join(os.getcwd(), 'test_data', 'uploads', filename)
        self.logger.info(f"Uploading file: {file_path}")
        self.page.set_input_files(self.SINGLE_FILE_UPLOAD, file_path)

    def upload_multiple_files(self, filenames: list):
        """
        Upload multiple files
        """
        file_paths = [os.path.join(os.getcwd(), 'test_data', 'uploads', f) for f in filenames]
        self.logger.info(f"Uploading files: {file_paths}")
        self.page.set_input_files(self.MULTIPLE_FILES_UPLOAD, file_paths)

    def enter_non_english_name(self, name: str):
        """
        Enter name in the non-English name field
        """
        self.logger.info(f"Entering name in non-English field: {name}")
        self.fill_text(self.NON_ENGLISH_NAME, name)
        
    def select_non_english_languages(self, languages: list):
        """
        Select non-English language options
        """
        self.logger.info(f"Selecting non-English languages: {languages}")
        language_map = {
            "मराठी": self.MARATHI_CHECKBOX,
            "ગુજરાતી": self.GUJARATI_CHECKBOX,
            "ਪੰਜਾਬੀ": self.PUNJABI_CHECKBOX
        }
        
        for lang in languages:
            if lang in language_map:
                self.click_element(language_map[lang])    

    async def download_file(self):
        """
        Handle file download
        """
        with self.page.expect_download() as download_info:
            self.click_element(self.DOWNLOAD_LINK)
        download = download_info.value
        
        # Wait for download to complete
        download_path = os.path.join(self.context.downloads_dir, download.suggested_filename)
        download.save_as(download_path)
        return download_path