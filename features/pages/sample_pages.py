from features.pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class SamplePagesPage(BasePage):
    """
    Sample Pages section object model class containing all sample pages elements and methods
    """
    
    # Page elements/locators
    SAMPLE_PAGES_BUTTON = "a[href='login.html'].btn-success"
    
    # Login page elements
    LOGIN_PAGE_TITLE = "text=Log in"  # The "Log in" text at the top
    ALREADY_USER_TEXT = "text=Already a user? Please login."
    USERNAME_FIELD = "input[placeholder='Username']"  # More specific than just #username
    PASSWORD_FIELD = "input[placeholder='Password']"  # More specific than just #password
    LOGIN_BUTTON = "button:has-text('Log in')"  # Button with exact text "Log in"
    REMEMBER_ME_CHECKBOX = "input[type='checkbox']"
    REGISTER_LINK = "text=New user? Register!"
    HINT_ADMIN_TEXT = "text=Hint-admin"  # The hint text shown
    # Pizza form elements - updated with correct locators from HTML source
    PIZZA_TITLE = "h3"
    
    # Size radio buttons
    PIZZA_SIZE_LARGE = "#rad_large"
    PIZZA_SIZE_MEDIUM = "#rad_medium"
    PIZZA_SIZE_SMALL = "#rad_small"
    PIZZA_SIZE_MAP = {
        "Large": "#rad_large",
        "Medium": "#rad_medium",
        "Small": "#rad_small"
    }
    
    # Pizza flavor dropdown
    PIZZA_FLAVOR_DROPDOWN = "#select_flavor"
    
    # Sauce radio buttons
    SAUCE_MARINARA = "#rad_marinara"
    SAUCE_BUFFALO = "#rad_buffalo"
    SAUCE_BARBEQUE = "#rad_barbeque"
    SAUCE_MAP = {
        "Marinara": "#rad_marinara",
        "Buffalo": "#rad_buffalo",
        "Barbeque": "#rad_barbeque"
    }
    
    # Toppings checkboxes
    TOPPINGS_ONIONS = "#onions"
    TOPPINGS_GREEN_OLIVE = "#green_olive"
    TOPPINGS_TOMATOES = "#tomoto"
    TOPPINGS_MAP = {
        "Onions": "#onions",
        "Green Olive": "#green_olive",
        "Tomatoes": "#tomoto"
    }
    
    
    # Other elements
    QUANTITY_INPUT = "#quantity"
    ADD_TO_CART_BUTTON = "#submit_button"
    PIZZA_FORM = "#pizza_order_form"
    
   
    
    
    # Modal and message locators
    QUANTITY_VALIDATION_MODAL = "#quantity_modal"
    QUANTITY_VALIDATION_MESSAGE = ".modal-body"
    ADDING_TO_CART_MODAL = "#success_modal"
    ADDING_TO_CART_MESSAGE = ".modal-title"
    CART_CONFIRMATION_MESSAGE = "#added_message"
    
 
    
    def __init__(self, page):
        """
        Initialize the sample pages with Playwright page object
        """
        super().__init__(page)
        
    def click_sample_pages_section(self):
        """
        Click on the Sample Pages section
        """
        self.logger.info("Clicking on Sample Pages section")
        try:
            # Wait for element to be visible
            self.wait_for_element(self.SAMPLE_PAGES_BUTTON)
            self.click_element(self.SAMPLE_PAGES_BUTTON)
            self.logger.info("Successfully clicked Sample Pages section")
        except Exception as e:
            self.logger.error(f"Failed to click Sample Pages section: {str(e)}")
            raise
        
    def is_login_page_visible(self) -> bool:
        """
        Check if Login page elements are visible
        """
        self.logger.info("Checking if Login page is visible")
        return self.is_element_visible(self.LOGIN_PAGE_TITLE) and \
               self.is_element_visible(self.ALREADY_USER_TEXT)
        
    def are_login_form_elements_visible(self) -> bool:
        """
        Check if all login form elements are visible
        """
        self.logger.info("Checking visibility of login form elements")
        username_visible = self.is_element_visible(self.USERNAME_FIELD)
        password_visible = self.is_element_visible(self.PASSWORD_FIELD)
        login_button_visible = self.is_element_visible(self.LOGIN_BUTTON)
        remember_me_visible = self.is_element_visible(self.REMEMBER_ME_CHECKBOX)
        register_link_visible = self.is_element_visible(self.REGISTER_LINK)
        
        return all([
            username_visible, 
            password_visible, 
            login_button_visible,
            remember_me_visible,
            register_link_visible
        ])
    
    def fill_login_form(self, username: str = None, password: str = None, remember_me: bool = False):
        """
        Fill in the login form
        """
        try:
            if username:
                self.logger.info(f"Filling username: {username}")
                self.page.fill("input[placeholder='Username']", username)
                
            if password:
                self.logger.info("Filling password")
                self.page.fill("input[placeholder='Password']", password)
                
            if remember_me:
                self.logger.info("Checking remember me checkbox")
                self.click_element(self.REMEMBER_ME_CHECKBOX)
                
        except Exception as e:
            self.logger.error(f"Failed to fill login form: {str(e)}")
            raise
    
    def click_login_button(self):
        """
        Click the login button
        """
        self.logger.info("Clicking login button")
        self.click_element(self.LOGIN_BUTTON)

    def is_pizza_form_visible(self) -> bool:
        """
        Check if pizza order form is visible
        """
        self.logger.info("Checking if pizza order form is visible")
        try:
            # Wait for the form to be visible
            self.wait_for_element(self.PIZZA_FORM)
            # Check for critical elements that indicate the form is loaded
            return all([
                self.is_element_visible(self.PIZZA_FORM),
                self.is_element_visible(self.PIZZA_SIZE_LARGE),
                self.is_element_visible(self.ADD_TO_CART_BUTTON)
            ])
        except Exception as e:
            self.logger.error(f"Error checking pizza form visibility: {str(e)}")
            return False

    def verify_pizza_form_sections(self) -> bool:
        """
        Verify all pizza form sections are present
        """
        self.logger.info("Verifying pizza form sections")
        sections = [
            "Pizza Size",
            "Pizza Flavor",
            "Sauce",
            "Toppings",
            "Quantity"
        ]
        
        for section in sections:
            if not self.is_element_visible(f"text={section}"):
                self.logger.error(f"Section not found: {section}")
                return False
        return True

    def are_pizza_customization_options_visible(self) -> bool:
        """
        Verify that all pizza customization options are visible
        """
        self.logger.info("Checking visibility of pizza customization options")
        elements = [
            self.PIZZA_SIZE_LARGE,
            self.PIZZA_SIZE_MEDIUM,
            self.PIZZA_SIZE_SMALL,
            self.PIZZA_FLAVOR_DROPDOWN,
            self.SAUCE_MARINARA,
            self.SAUCE_BUFFALO,
            self.SAUCE_BARBEQUE,
            self.TOPPINGS_ONIONS,
            self.TOPPINGS_GREEN_OLIVE,
            self.TOPPINGS_TOMATOES,
            self.QUANTITY_INPUT,
            self.ADD_TO_CART_BUTTON
        ]
    def select_pizza_size(self, size: str):
        """
        Select the pizza size
        """
        self.logger.info(f"Selecting pizza size: {size}")
        selector = self.PIZZA_SIZE_MAP.get(size)
        if not selector:
            raise ValueError(f"Invalid pizza size: {size}")
        self.click_element(selector)
    
    def select_pizza_flavor(self, flavor: str):
        """
        Select pizza flavor from dropdown
        """
        self.logger.info(f"Selecting pizza flavor: {flavor}")
        self.page.select_option(self.PIZZA_FLAVOR_DROPDOWN, label=flavor)
    
    def select_sauce(self, sauce: str):
        """
        Select the sauce type
        """
        self.logger.info(f"Selecting sauce: {sauce}")
        selector = self.SAUCE_MAP.get(sauce)
        if not selector:
            raise ValueError(f"Invalid sauce type: {sauce}")
        self.click_element(selector)
    
    def check_topping(self, topping: str):
        """
        Check a specific topping
        """
        self.logger.info(f"Checking topping: {topping}")
        selector = self.TOPPINGS_MAP.get(topping)
        if not selector:
            raise ValueError(f"Invalid topping: {topping}")
        self.click_element(selector)
    
    def enter_quantity(self, quantity: str):
        """
        Enter pizza quantity
        """
        self.logger.info(f"Entering quantity: {quantity}")
        self.fill_text(self.QUANTITY_INPUT, quantity)
    
    def click_add_to_cart(self):
        """
        Click the Add to Cart button
        """
        self.logger.info("Clicking Add to Cart button")
        self.click_element(self.ADD_TO_CART_BUTTON)
    
    def get_quantity_validation_message(self) -> str:
        """
        Get the quantity validation message from modal
        """
        self.wait_for_element(self.QUANTITY_VALIDATION_MODAL)
        return self.get_element_text(self.QUANTITY_VALIDATION_MESSAGE)
    
    def get_cart_status_message(self) -> str:
        """
        Get the cart status message
        """
        self.wait_for_element(self.CART_CONFIRMATION_MESSAGE)
        return self.get_element_text(self.CART_CONFIRMATION_MESSAGE)
    
    def get_adding_to_cart_message(self) -> str:
        """
        Get the "Adding to cart..." message
        """
        self.wait_for_element(self.ADDING_TO_CART_MODAL)
        return self.get_element_text(self.ADDING_TO_CART_MESSAGE)
    def click_register_link(self):
        """
        Click the register link
        """
        self.logger.info("Clicking register link")
        self.click_element(self.REGISTER_LINK)

    