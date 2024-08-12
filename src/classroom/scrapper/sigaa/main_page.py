from selenium.webdriver.common.by import By
from ..base import *
from selenium_utils.utils import *

def open_sigaa_menu(browser, menu_class, submenu_text):
    btn_atividades = browser.find_element(By.CSS_SELECTOR, menu_class)
    try:
        btn_atividades.click()
    except:
        pass 

    for btn_item_menu in browser.find_elements(By.CSS_SELECTOR, ".itemMenu"):
        menu_texto = btn_item_menu.text.strip().lower()
        if menu_texto == submenu_text.lower():
            item_link = btn_item_menu.find_element(By.XPATH, '..')
            item_link.click()
            break
def open_grades_menu(browser):
    open_sigaa_menu(browser, ".itemMenuHeaderAlunos", "Lançar Notas")
    
    
def open_task_menu(browser):
    open_sigaa_menu(browser, ".itemMenuHeaderAtividades", "tarefas")

def open_discipline_num(browser, obj_discipline, num_discipline):
    discipline_counter = 0
    for discipline_link in browser.find_elements(By.CSS_SELECTOR, "#turmas-portal td.descricao a"):
        if discipline_link.text.startswith(obj_discipline.code):
            if num_discipline == discipline_counter:
                print(f"SIGAA DISCIPLINE: {discipline_link.text}")
                discipline_link.click()
                return True
            
            discipline_counter += 1
        else:
            print(f"Disciplina {discipline_link.text} não é igual a {obj_discipline.code}")
    return False

def login_sigaa(browser):
    
    open_new_page("https://sig.cefetmg.br/sigaa/verTelaLogin.do", browser)
    wait_for(ApareceuElemento(browser, ".usuario"), infinite_loop=True)
    if browser.current_url.endswith("vinculos.jsf"):
        open_new_page("https://sig.cefetmg.br/sigaa/escolhaVinculo.do?dispatch=escolher&vinculo=1", browser)
    

