import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configure logging for the test framework
    Creates a new log file for each test run with timestamp
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a timestamp for the log file
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = f'logs/test_run_{timestamp}.log'

    # Configure logging format
    logging_format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        datefmt=date_format,
        handlers=[
            # File handler with detailed information
            logging.FileHandler(log_file),
            # Console handler with color formatting
            logging.StreamHandler()
        ]
    )

    # Create logger instance
    logger = logging.getLogger('automation_framework')
    logger.setLevel(logging.INFO)

    return logger

# Create a logger instance that can be imported by other modules
logger = setup_logging()