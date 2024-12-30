from features.pages.base_page import BasePage

import logging

logger = logging.getLogger(__name__)

class RegistrationPage(BasePage):
    """
    Registration page object model class containing all registration page elements and methods
    """
    
    # Page elements/locators
    FIRST_NAME_INPUT = "input[name='first_name']"
    LAST_NAME_INPUT = "input[name='last_name']"
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "#pwd1"
    CONFIRM_PASSWORD_INPUT = "#pwd2"
    TERMS_CHECKBOX = "input[name='terms']"
    REGISTER_BUTTON = "#submit_button"
    PAGE_TITLE = "h2"
    HINT_TEXT = ".hint-text"
    ERROR_MESSAGE = "#message"
    
    def __init__(self, page):
        """
        Initialize the registration page with Playwright page object
        """
        super().__init__(page)
        
    def fill_first_name(self, first_name: str):
        """
        Fill in the first name field
        """
        self.logger.info(f"Filling first name: {first_name}")
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
        
    def fill_last_name(self, last_name: str):
        """
        Fill in the last name field
        """
        self.logger.info(f"Filling last name: {last_name}")
        self.fill_text(self.LAST_NAME_INPUT, last_name)
        
    def fill_email(self, email: str):
        """
        Fill in the email field
        """
        self.logger.info(f"Filling email: {email}")
        self.fill_text(self.EMAIL_INPUT, email)
        
    def fill_password(self, password: str):
        """
        Fill in the password field
        """
        self.logger.info("Filling password field")
        self.fill_text(self.PASSWORD_INPUT, password)
        
    def fill_confirm_password(self, password: str):
        """
        Fill in the confirm password field
        """
        self.logger.info("Filling confirm password field")
        self.fill_text(self.CONFIRM_PASSWORD_INPUT, password)
        
    def accept_terms(self):
        """
        Check the terms checkbox
        """
        self.logger.info("Accepting terms and conditions")
        self.click_element(self.TERMS_CHECKBOX)
        
    def click_register(self):
        """
        Click the register button
        """
        self.logger.info("Clicking register button")
        self.click_element(self.REGISTER_BUTTON)
        
    def get_error_message(self) -> str:
        """
        Get the error message text
        """
        self.logger.info("Getting error message")
        return self.get_element_text(self.ERROR_MESSAGE)
        
    def fill_registration_form(self, form_data: dict):
        """
        Fill in all registration form fields
        """
        self.logger.info("Filling registration form")
        field_mapping = {
            'First Name': self.fill_first_name,
            'Last Name': self.fill_last_name,
            'Email': self.fill_email,
            'Password': self.fill_password,
            'Confirm Password': self.fill_confirm_password
        }
        
        for field, value in form_data.items():
            if field in field_mapping:
                field_mapping[field](value)

    def is_on_confirmation_page(self) -> bool:
        """
        Check if we're on the confirmation page
        """
        return self.page.url.endswith('confirmation.html')