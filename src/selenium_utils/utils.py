from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from pathlib import Path

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

def abre_firefox():
    #profile = webdriver.FirefoxProfile()
    #profile.accept_untrusted_certs = True

    options=Options()
    options.set_preference('accept_untrusted_certs', True)
    ff = webdriver.Firefox(options=options)
    ff.implicitly_wait(10) 
    return ff
def wait_for(condition_function, infinite_loop = True):
    start_time = time.time()
    while time.time() < start_time + 1000 or infinite_loop:
        
        if condition_function():
            return True
        else:
            print("Aguardando...")
            time.sleep(1)
    raise Exception(
        'Timeout waiting'
        )

def open_new_page(url, browser):
    any_element = browser.find_element(By.CSS_SELECTOR, "*")
    browser.get(url)
    
    def link_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            any_element.find_element(By.ID, "doesnotmatter")
            return False
        except StaleElementReferenceException:
            return True
        except NoSuchElementException:
            return False
    wait_for(link_has_gone_stale)
def click_through_to_new_page_by_css(css_selector, browser):
    link = browser.find_element(By.CSS_SELECTOR, css_selector)
    link.click()
    def link_has_gone_stale():
        try:
          # poll the link with an arbitrary call
            link.find_element(By.ID, "doesnotmatter")
            return False
        except StaleElementReferenceException:
            return True
        except NoSuchElementException:
            return False
    wait_for(link_has_gone_stale)
def click_through_to_new_page(link_id, browser):
    click_through_to_new_page_by_css("#"+link_id, browser)

class ApareceuElemento:
    def __init__(self, browser, css_elemento):
        self.browser = browser
        self.css_elemento = css_elemento
        
    def __call__(self):
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.css_elemento)
            return True
        except NoSuchElementException:
            return False

class MudaElemento:
    def __init__(self, elemento, valor):
        self.elemento = elemento
        self.valor = valor
    def __call__(self):
        self.elemento.send_keys(self.valor)


        return self.elemento.get_attribute("value") == self.valor
