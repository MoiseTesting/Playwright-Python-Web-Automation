
import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright
from config.logging_config import logger

def before_all(context):
    """
    Runs before all tests
    """
    logger.info("Starting test execution")
    
    # Create downloads directory if it doesn't exist
    downloads_dir = os.path.join(os.getcwd(), 'test_data', 'downloads')
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)

     # Create screenshots directory if it doesn't exist
    screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

     # Store screenshots path in context
    context.screenshots_dir = screenshots_dir
    
    # Store downloads path in context for use in tests
    context.downloads_dir = downloads_dir

    # Load configuration
    env = os.getenv('ENV', 'dev')
    config_path = f'config/{env}_config.json'
    
    try:
        with open(config_path, 'r') as f:
            context.config = json.load(f)
            logger.info(f"Loaded configuration for environment: {env}")
    except Exception as e:
        logger.error(f"Failed to load config file {config_path}: {str(e)}")
        raise

def before_scenario(context, scenario):
    """
    Runs before each scenario
    """
    try:
        context.playwright = sync_playwright().start()
        
        # Launch browser
        context.browser = context.playwright.chromium.launch(
            headless=context.config.get('headless', False)
        )
        
        # Create new browser context with downloads enabled
        context.browser_context = context.browser.new_context(
            accept_downloads=True,  # Enable downloads
            viewport=context.config.get('viewport', {'width': 1920, 'height': 1080})
        )
        
        # Create new page
        context.page = context.browser_context.new_page()
        
        logger.info("Browser and page initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize browser: {str(e)}")
        raise

def after_scenario(context, scenario):
    """
    Runs after each scenario
    """
    try:
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
    
        if scenario.status == "failed":
            # Create timestamp for unique screenshot name
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = os.path.join(
                context.screenshots_dir, 
                f"failure_{scenario.name.replace(' ', '_')}_{timestamp}.png"
            )
            
            # Take screenshot
            if hasattr(context, 'page'):
                context.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"Screenshot captured at: {screenshot_path}")                

        # Close browser resources
        if hasattr(context, 'page'):
            context.page.close()
        if hasattr(context, 'browser_context'):
            context.browser_context.close()
        if hasattr(context, 'browser'):
            context.browser.close()
        if hasattr(context, 'playwright'):
            context.playwright.stop()
            
        logger.info("Browser resources cleaned up")
    except Exception as e:
        logger.error(f"Error in cleanup: {str(e)}")
        raise

def after_all(context):
    """
    Runs after all tests
    """
    logger.info("Test execution completed")
