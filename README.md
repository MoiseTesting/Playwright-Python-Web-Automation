# Web Automation Framework with Playwright and Behave

## Overview
This project is a web automation testing framework built using Python, Playwright, and Behave (BDD). It demonstrates automated testing capabilities for https://play1.automationcamp.ir/, a sample website designed for automation practice. The framework implements the Page Object Model design pattern and supports cross-browser testing.

## Key Features
- Behavior Driven Development (BDD) using Behave
- Page Object Model implementation
- Cross-browser testing support
- Screenshot capture on test failure
- Detailed logging system
- File upload and download handling
- Support for non-English characters and locators
- CI/CD integration with GitHub Actions
- Multiple environment support (Dev/Prod)

## Test Scenarios Covered
1. **Basic Navigation**
   - Homepage loading and verification
   - Navigation between different sections

2. **Form Interactions**
   - Basic form controls
   - Form validations
   - File upload/download
   - Non-English form elements

3. **Sample Pages**
   - Login functionality
   - Registration process
   - Pizza order form

4. **Advanced UI Features**
   - Dynamic content handling
   - Book rating challenge
   - UI element interactions

## Project Structure
```plaintext
playwright_behave_framework/
├── .github/
│   └── workflows/              # GitHub Actions workflow files
│       └── main.yml           # Main workflow configuration
│
├── config/
│   ├── __init__.py            # Makes config directory a Python package
│   ├── dev_config.json        # Development environment settings
│   ├── logging_config.py      # Logging configuration
│   └── prod_config.json       # Production environment settings
│
├── features/
│   ├── environment.py         # Behave hooks for setup/teardown
│   │
│   ├── pages/                 # Page Object Model implementations
│   │   ├── __init__.py       # Makes pages directory a Python package
│   │   ├── advanced_ui.py    # Advanced UI features page objects
│   │   ├── base_page.py      # Base class with common methods
│   │   ├── home_page.py      # Homepage elements and interactions
│   │   └── sample_pages.py   # Sample pages elements and interactions
│   │
│   ├── steps/                 # Step definitions for Behave
│   │   ├── __init__.py       # Makes steps directory a Python package
│   │   ├── advanced_ui_steps.py    # Advanced UI feature steps
│   │   ├── form_steps.py     # Form interaction steps
│   │   ├── home_steps.py     # Homepage related steps
│   │   ├── registration_steps.py    # Registration steps
│   │   └── sample_page_steps.py     # Sample pages steps
│   │
│   ├── advanced_ui.feature   # Advanced UI test scenarios
│   ├── forms.feature         # Forms test scenarios
│   ├── home.feature         # Homepage test scenarios
│   ├── pizza_order.feature  # Pizza ordering test scenarios
│   └── sample_pages.feature # Sample pages test scenarios
│
├── logs/                      # Directory for test execution logs
├── reports/                   # Directory for test reports
├── screenshots/               # Directory for failure screenshots
│
├── test_data/
│   ├── downloads/            # Directory for downloaded files
│   └── uploads/              # Test files for upload testing
│       ├── github-pages.zip  # Sample zip file
│       ├── index.html        # Sample HTML file
│       └── sample_text.txt   # Sample text file
│
├── utils/
│   ├── __init__.py          # Makes utils directory a Python package
│   ├── helper.py            # Helper functions
│   └── verify_setup.py      # Setup verification utilities
│
├── .gitignore               # Git ignore file
├── behave.ini              # Behave configuration
├── pytest.ini              # PyTest configuration
└── requirements.txt        # Project dependencies
```

## Setup and Installation
1. Clone the repository
```bash
git clone <repository-url>
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

## Running Tests
Run all tests:
```bash
behave
```

Run specific feature:
```bash
behave features/home.feature
```

Run tests with specific tags:
```bash
behave --tags=@smoke
```

## Environment Configuration
- Dev environment: Uses settings from `config/dev_config.json`
- Prod environment: Uses settings from `config/prod_config.json`

To switch environments:
```bash
ENV=prod behave
```

## Logging
- Test execution logs are stored in the `logs` directory
- Screenshots of failures are stored in the `screenshots` directory
- Test reports are generated in the `reports` directory

## CI/CD Integration
The project includes GitHub Actions workflows for:
- Running tests on push/pull request
- Generating and publishing test reports
- Cross-browser testing

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Author
Moise Dore

