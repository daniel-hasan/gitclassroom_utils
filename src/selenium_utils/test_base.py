import pytest




from selenium import webdriver
from .utils import abre_chrome
#de: https://dev.to/delrayo/executing-selenium-test-with-pythonpytest-using-github-actions-317c
@pytest.fixture()
def open_chrome(request):
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]


    
    request.cls.chrome = abre_chrome(options)
    yield request.cls.chrome
    request.cls.chrome.close()