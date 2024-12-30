from features.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class AdvancedUIPage(BasePage):
    """
    Advanced UI Features page object containing elements and methods
    for advanced UI interactions
    """
    
    # Locators
    ADVANCED_UI_BUTTON = "a[href='advanced.html']"
    CHALLENGE_TITLE = "h2:text('Challenge 1')"
    BOOK_TITLE = "text=Sapiens: A Brief History of the Humankind"
    STAR_RATING = "label.star-rating"
    RATING_INPUT = "#txt_rating"
    CHECK_RATING_BUTTON = "#check_rating"
    RATING_RESULT = "#validate_rating"
    
    def __init__(self, page):
        """
        Initialize the advanced UI page
        """
        super().__init__(page)
        
    def click_advanced_ui_section(self):
        """
        Click on Advanced UI Features section
        """
        self.logger.info("Clicking on Advanced UI Features section")
        self.click_element(self.ADVANCED_UI_BUTTON)
        
    def get_book_rating(self) -> str:
        """
        Get the star rating for the book
        """
        self.logger.info("Getting book star rating")
        # Get the content of the pseudo-element
        rating = self.page.evaluate("""() => {
            const style = window.getComputedStyle(document.querySelector('label.star-rating'), ':after');
            return style.getPropertyValue('content');
        }""")
        self.logger.info(f"Found rating: {rating}")
        return rating.strip('"')  # Remove quotes from the content value
        
    def enter_rating(self, rating: str):
        """
        Enter rating in the text box
        """
        self.logger.info(f"Entering rating: {rating}")
        self.fill_text(self.RATING_INPUT, rating)
        
    def click_check_rating(self):
        """
        Click the Check Rating button
        """
        self.logger.info("Clicking Check Rating button")
        self.click_element(self.CHECK_RATING_BUTTON)
        
    def get_rating_result(self) -> str:
        """
        Get the rating validation message
        """
        self.logger.info("Getting rating result message")
        return self.get_element_text(self.RATING_RESULT)