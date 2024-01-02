import pytest

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver

#de: https://dev.to/delrayo/executing-selenium-test-with-pythonpytest-using-github-actions-317c
@pytest.fixture()
def open_chrome(request):
    chrome_service = Service(ChromeDriverManager().install())

    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)

    
    request.cls.chrome = webdriver.Chrome(service=chrome_service, options=chrome_options)
    yield request.cls.chrome
    request.cls.chrome.close()