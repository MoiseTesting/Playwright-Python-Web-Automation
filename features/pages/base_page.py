from playwright.sync_api import Page
import json
import os
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasePage:
    """
    Base page class that all page objects will inherit from.
    Contains common methods and utilities for all pages.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger  # Add logger as instance variable
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """
        Load the configuration based on the environment
        """
        env = os.getenv('ENV', 'dev')
        config_path = f'config/{env}_config.json'
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.logger.info(f"Loaded configuration for environment: {env}")
                return config
        except Exception as e:
            self.logger.error(f"Failed to load config file {config_path}: {str(e)}")
            raise
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL
        """
        try:
            self.logger.info(f"Navigating to URL: {url}")
            self.page.goto(url)
            self.logger.info(f"Successfully navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
        
    def get_element_text(self, selector: str) -> str:
        """
        Get text content of an element
        """
        try:
            self.logger.debug(f"Getting text content from element: {selector}")
            text = self.page.text_content(selector)
            self.logger.debug(f"Text content retrieved: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from element {selector}: {str(e)}")
            raise
    
    def click_element(self, selector: str) -> None:
        """
        Click on an element
        """
        try:
            self.logger.debug(f"Attempting to click element: {selector}")
            self.page.click(selector)
            self.logger.debug(f"Successfully clicked element: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {str(e)}")
            raise
    
    def fill_text(self, selector: str, text: str) -> None:
        """
        Fill text in an input field
        """
        try:
            self.logger.info(f"Filling text field {selector} with value: {text}")
            self.page.fill(selector, text)
            self.logger.debug(f"Successfully filled text field: {selector}")
        except Exception as e:
            self.logger.error(f"Failed to fill text in element {selector}: {str(e)}")
            raise
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Check if element is visible
        """
        try:
            self.logger.debug(f"Checking visibility of element: {selector}")
            is_visible = self.page.is_visible(selector)
            self.logger.debug(f"Element {selector} visibility status: {is_visible}")
            return is_visible
        except Exception as e:
            self.logger.error(f"Failed to check visibility of element {selector}: {str(e)}")
            raise
    
    def wait_for_element(self, selector: str, timeout: int = None) -> None:
        """
        Wait for element to be visible
        """
        try:
            timeout = timeout or self.config['timeout']
            self.logger.debug(f"Waiting for element {selector} with timeout {timeout}ms")
            self.page.wait_for_selector(selector, timeout=timeout)
            self.logger.debug(f"Element {selector} appeared within timeout")
        except Exception as e:
            self.logger.error(f"Timeout waiting for element {selector}: {str(e)}")
            raise