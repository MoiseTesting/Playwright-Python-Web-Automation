import sys
import subprocess
from typing import Tuple, List
import pkg_resources
from config.logging_config import logger

def check_python_version() -> Tuple[bool, str]:
    """
    Check if Python version is compatible (3.7+)
    """
    current_version = sys.version_info
    required_version = (3, 7)
    
    is_compatible = current_version >= required_version
    message = f"Python version: {sys.version}"
    
    return is_compatible, message

def check_package_installation() -> List[Tuple[str, bool, str]]:
    """
    Check if all required packages are installed with correct versions
    """
    required_packages = {
        'playwright': '1.42.0',
        'behave': '1.2.6',
        'pytest': '8.0.0',
        'python-dotenv': '1.0.1',
        'behave-html-formatter': '0.9.10'
    }
    
    results = []
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    
    for package, required_version in required_packages.items():
        is_installed = package in installed_packages
        if is_installed:
            installed_version = installed_packages[package]
            is_correct_version = installed_version == required_version
            message = f"{package}: Required={required_version}, Installed={installed_version}"
        else:
            is_correct_version = False
            message = f"{package}: Not installed"
            
        results.append((package, is_correct_version, message))
    
    return results

def check_playwright_browsers() -> Tuple[bool, str]:
    """
    Check if Playwright browsers are installed
    """
    try:
        result = subprocess.run(['playwright', 'browser-versions'], 
                              capture_output=True, 
                              text=True)
        return True, f"Browsers installed: {result.stdout}"
    except Exception as e:
        return False, f"Error checking browsers: {str(e)}"

def main():
    """
    Run all verification checks and log results
    """
    logger.info("Starting setup verification...")
    
    # Check Python version
    python_ok, python_msg = check_python_version()
    logger.info(f"Python version check: {python_msg}")
    if not python_ok:
        logger.error("Python version is not compatible!")
    
    # Check package installations
    logger.info("Checking package installations...")
    package_results = check_package_installation()
    for package, is_correct, message in package_results:
        if is_correct:
            logger.info(message)
        else:
            logger.error(message)
    
    # Check Playwright browsers
    browsers_ok, browsers_msg = check_playwright_browsers()
    if browsers_ok:
        logger.info(f"Playwright browsers check: {browsers_msg}")
    else:
        logger.error(f"Playwright browsers check failed: {browsers_msg}")
    
    # Summary
    all_packages_ok = all(result[1] for result in package_results)
    if python_ok and all_packages_ok and browsers_ok:
        logger.info("✅ All setup checks passed successfully!")
    else:
        logger.error("❌ Some setup checks failed. Please review the logs above.")

if __name__ == "__main__":
    main()