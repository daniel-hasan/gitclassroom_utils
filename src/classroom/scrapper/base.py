from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def abre_chrome_github():
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    
    
    chrome_service = ChromeService(ChromeDriverManager().install())

    chrome_options = ChromeOptions()
    options = [
        #"--headless",
        f'user-agent={user_agent}',
        "--disable-gpu",
        "--disable-blink-features=AutomationControlled",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "user-data-dir=~/.chrome_selenium"
    ]
    for option in options:
        chrome_options.add_argument(option)


    return webdriver.Chrome(service=chrome_service, options=chrome_options)
    