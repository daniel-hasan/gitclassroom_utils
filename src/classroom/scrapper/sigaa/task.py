import re
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import Select
from classroom.models import Assignment
from .main_page import open_task_menu
from datetime import datetime
from django.utils.timezone import make_aware
def get_deadline(str_text):
    pattern_deadline = "a ([0-9]{2}/[0-9]{2}/[0-9]{4}) às ([0-9]{2}h[0-9]{2})"
    match = re.search(pattern_deadline,str_text)
    str_date = match.group(1)
    str_hour = match.group(2)
    return datetime.strptime(str_date+" "+str_hour, "%d/%m/%Y %Hh%M")

def open_update_or_create_task_by_prefix(browser, prefix, current_deadline):
    for task_line in browser.find_elements(By.CSS_SELECTOR, ".listing tr"):
        tarefa_sigaa_name = task_line.text.strip().upper()
        if tarefa_sigaa_name.startswith(prefix):
            deadline_sigaa = get_deadline(task_line.text)

            print(f"achou! {prefix} {deadline_sigaa} {current_deadline}")
            
            if current_deadline != deadline_sigaa:
                print("Dead diferente, alterar")
                btn_alterar = task_line.find_element(By.CSS_SELECTOR, "a[title^='Alterar']")
                btn_alterar.click()
                return True
            else:
                print("ignorar")
                return False
    print(f"Criando novo... {prefix}")
    btn_nova_tarefa = browser.find_element(By.CSS_SELECTOR, ".menu-interno li[class*='novaTarefa']")
    btn_nova_tarefa.click()
    return True

def iframe_update(browser, iframe, texto):
    browser.switch_to.frame(iframe)
    browser.execute_script(f"document.querySelector('body').innerHTML = '{texto}'")
    browser.switch_to.default_content()
    
def update_or_create_task(browser, assignment):
    title_el = browser.find_element(By.ID, "formAva:titulo")
    iframe_text_el =  browser.find_element(By.ID, "formAva:texto_ifr")
    task_type_select = Select(browser.find_element(By.ID, "formAva:tipo"))
    topic_el = browser.find_element(By.ID, "formAva:aula")
    topic_select = Select(browser.find_element(By.ID, "formAva:aula"))
    
    deadline_date_candidates = browser.find_elements(By.CSS_SELECTOR, ".formAva input[title*='Data Final']")
    deadline_date_el = None
    for dead_date_candidate in deadline_date_candidates:
        if dead_date_candidate.is_displayed():
            deadline_date_el = dead_date_candidate
            break
    deadline_hour_select = Select(browser.find_element(By.ID, "formAva:horaFim"))
    deadline_min_select = Select(browser.find_element(By.ID, "formAva:minutoFim"))
    
    has_grade_select = Select(browser.find_element(By.ID, "formAva:possuiNota"))
    acronym_el = browser.find_element(By.ID, "formAva:abreviacao")
    unid_el =  browser.find_element(By.ID, "formAva:unidade")
    unid_select =  Select(unid_el)
    max_grade_el =  browser.find_element(By.ID, "formAva:notaMaxima")
    
    #valores padrao
    has_grade_select.select_by_value("true")
    task_type_select.select_by_value("3")
    
    
    #unit: se for "NB" substituir por N by value caso contrario, pimeiro
    options_select = unid_el.find_elements(By.CSS_SELECTOR, "option")
    if len(options_select)>2 and re.match("[1-4][bB].*", assignment.topic_fk.acronym):
        num_bimestre = assignment.topic_fk.acronym[0]
        unid_select.select_by_value(num_bimestre)
    else:
        unid_select.select_by_index(1)
    
    #inputs 
    title_el.clear()
    title_el.send_keys(f"[{assignment.acronym.upper()}] {assignment.name}")
    assignment_text = f'<p>Entrega acessivel pelo Github Classroom <a href="{assignment.invitation_url}">por meio deste link</a>.<p>'
    iframe_update(browser, iframe_text_el, assignment_text)
    
    max_grade_el.clear()
    max_grade_el.send_keys(str(assignment.total_grade))
    
    acronym_el.clear()
    acronym_el.send_keys(assignment.acronym.upper())
    
    #topic
    topic_value = None
    for topic_option in topic_el.find_elements(By.CSS_SELECTOR, "option")[1:]:
        topic_complete_name = topic_option.text
        topic_name = topic_complete_name.split(")")[1].strip()
        if f"[{assignment.topic_fk.acronym}]" in topic_name:
            topic_value = topic_option.get_attribute("value")
            break
    if topic_value:
        topic_select.select_by_value(topic_value)
    else:
        topic_select.select_by_index(1)
        
    #deadline
    deadline_date_el.clear()
    deadline_date_el.send_keys(assignment.deadline.strftime("%d/%m/%Y"))
    deadline_hour_select.select_by_value(str(assignment.deadline.hour))
    deadline_min_select.select_by_value(str(assignment.deadline.minute))
    
    #botao de atualizar/inserir
    inputAtualizar = browser.find_element(By.CSS_SELECTOR, ".form-actions input[value*='Atualizar'],.botoes input[value*='Cadastrar']")
    inputAtualizar.click()

def update_assignments_data(browser, obj_discipline):
    #abre o menu e atualiza os dados (se necessario)
    assignments = Assignment.objects.filter(discipline_fk = obj_discipline)
    for assignment in assignments:
        if assignment.deadline and assignment.deadline > make_aware(datetime.now()):
            open_task_menu(browser)
            to_update = open_update_or_create_task_by_prefix(browser, 
                                                            f"[{assignment.acronym.upper()}]", 
                                                            assignment.deadline)
            if to_update:
                update_or_create_task(browser, assignment)