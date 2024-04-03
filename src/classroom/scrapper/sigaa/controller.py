from classroom.models import *
from selenium_utils.utils import open_new_page
from selenium.webdriver.common.by import By
from .task import update_assignments_data
from ..base import abre_chrome_github
from .main_page import login_sigaa, open_discipline_num
from .grades import update_grades_data
def open_portal(browser):
    open_new_page("https://sig.cefetmg.br/sigaa/portais/docente/docente.jsf", browser)

def update_assignments(browser, obj_discipline, callable_update):
    
    #se está na tela de 
    
    try:
        open_portal(browser)
        browser.current_url
    except:
        login_sigaa(browser)

    num_discipline = 0
    while open_discipline_num(browser, obj_discipline, num_discipline):
        print(obj_discipline)
        callable_update(browser, obj_discipline)

        open_portal(browser)
        #btn_portal = browser.find_element(By.CSS_SELECTOR, ".botaoPortal")
        #btn_portal.click()
        num_discipline += 1

def update_tasks(discipline_name = ""):

    chrome = abre_chrome_github()
    lstDisciplines = Discipline.objects.all()
    if discipline_name:
        lstDisciplines = lstDisciplines.filter(name = discipline_name)

    for obj_discipline in lstDisciplines:
        update_assignments(chrome, obj_discipline, update_assignments_data)

def update_grades():
    chrome = abre_chrome_github()
    for obj_discipline in Discipline.objects.all():
        update_assignments(chrome, obj_discipline, update_grades_data)