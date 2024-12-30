from features.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """
    Home page object model class containing all home page elements and methods
    """
    
    # Page elements/locators
    PAGE_TITLE = "h1"
    PAGE_SUBTITLE = "h3"
    
    def __init__(self, page):
        """
        Initialize the home page with Playwright page object
        """
        super().__init__(page)
        self.url = f"{self.config['base_url']}/index.html"
    
    def navigate(self):
        """
        Navigate to the home page
        """
        self.logger.info(f"Navigating to home page: {self.url}")
        self.navigate_to(self.url)
    
    def get_page_title(self) -> str:
        """
        Get the main page title text
        """
        self.logger.info("Getting page title text")
        return self.get_element_text(self.PAGE_TITLE)
    
    def get_page_subtitle(self) -> str:
        """
        Get the page subtitle text
        """
        self.logger.info("Getting page subtitle text")
        return self.get_element_text(self.PAGE_SUBTITLE)