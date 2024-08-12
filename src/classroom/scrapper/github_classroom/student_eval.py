from selenium.webdriver.common.by import By
from selenium_utils.utils import *
from github_app_viewer.app_viewer import AppViewer
from github_app_viewer.git_utils import Git
from decimal import Decimal
import time

def get_students_from_assignment(browser):
    students_from_assignment = []
    for student_assignment in browser.find_elements(By.CSS_SELECTOR, 
                                        ".assignment-repo-list-item"):
        student_name_id = student_assignment.find_element(By.CSS_SELECTOR, 
                                                        "span.h5")\
                                        .text
        student_name, student_id = student_name_id.split("-")
        student_name = student_name.strip()
        student_id = student_id.strip()

        student_repo = student_assignment.find_element(By.CSS_SELECTOR, 
                                                        "a[id^='view-repository-tooltip']")\
                                        .get_attribute("href")

        try:
            student_repo_feedback = student_assignment.find_element(By.CSS_SELECTOR, 
                                                        "a[id^='review-feedback-tooltip']")\
                                                    .get_attribute("href")
        except NoSuchElementException:
            student_repo_feedback = None
        try:
            student_grades  = student_assignment.find_element(By.CSS_SELECTOR, 
                                                        "span.Counter")\
                                                    .get_attribute("title")
        except NoSuchElementException:
            student_grades = None

        students_from_assignment.append({"name":student_name,
         "id":student_id,
          "repo_url":student_repo,
        "feedback_url":student_repo_feedback,
         "auto_grade":student_grades})

    return students_from_assignment

def write_pull_request_eval(browser, student, total_grade):
    comment_text = browser.find_element(By.ID, 
                                        "new_comment_field")
    str_value_comment = comment_text.get_attribute("value")
    if len(str_value_comment)==0:
        str_avaliacao = "## Avaliação Geral\n"
        if student["auto_grade"]:
            value_given, total = student['auto_grade'].split("/")
            perc_value = Decimal(value_given)/Decimal(total)
            final_grade = total_grade*perc_value
            student["auto_grade"] = Decimal(value_given)

            str_avaliacao += f"Notas exercícios (automático): {final_grade}\n"
        else: 
            final_grade = total_grade

        str_avaliacao += "Nota final: "+str(final_grade)+"\n"
        str_avaliacao += "Atividades complementares: 0"
        comment_text.send_keys(str_avaliacao)
    return comment_text

def create_changes_and_view_tabs(browser):
    feedback_tab = browser.current_window_handle

    browser.switch_to.new_window('tab')
    changes_tab = browser.current_window_handle

    browser.switch_to.new_window('tab')
    view_tab = browser.current_window_handle

    browser.switch_to.window(feedback_tab)

    return changes_tab, view_tab 
def open_github_view(git_app, repo_url):
    git_repo = Git(repo_url)
    if not git_app:
        git_app = AppViewer(git_repo)
    else:
        git_app.kill_server()

    
    git_app.github = git_repo
    
    git_app.download_app()
    return git_app.execute_app()
    
def browse_student_assignment(browser, change_tab, views_tab, git_app): 
    feedback_url = browser.current_url
    repo_url = "/".join(feedback_url.split("/")[:-2])
    repo_name = repo_url.split("/")[-1]
    repo_user = repo_url.split("/")[-2]
    
    #github_page = f"https://{repo_user}.github.io/{repo_name}"
    

    feedback_tab = browser.current_window_handle


    browser.switch_to.window(change_tab)
    browser.get(feedback_url+"/files")
    #open_new_page(feedback_url+"/files", browser)

    
    
    browser.switch_to.window(views_tab)

    github_view_url = open_github_view(git_app, repo_url)
    browser.get(github_view_url)
    
    browser.switch_to.window(feedback_tab)
    return git_app
    
def find_comment_eval(browser):
    comments_el = browser.find_elements(By.CSS_SELECTOR, ".current-user")

    for comment_el in comments_el:
        if comment_el.text.find("Avaliação Geral")>=0:
            return comment_el
    return None

def edit_comment_eval(comment_eval_el):
    btn_actions_el = comment_eval_el.find_element(By.CSS_SELECTOR, ".timeline-comment-actions")
    btn_actions_el.click()

    #for button in comment_eval_el.find_elements(By.CSS_SELECTOR, "button"):
    #    print(button.get_attribute("class"))
    wait_for(ApareceuElemento(comment_eval_el, ".js-comment-edit-button"))
    #for button in comment_eval_el.find_elements(By.CSS_SELECTOR, "button"):
    #    print(button.get_attribute("class"))
    
    btn_edit_el = btn_actions_el.find_element(By.CSS_SELECTOR, ".js-comment-edit-button")
    btn_edit_el.click()
    return comment_eval_el.find_element(By.CSS_SELECTOR, 
                            "textarea[name='issue_comment[body]']")

def has_finished_edit(browser, new_comment_textarea_el, 
                                edit_comment_textarea_el):
    if edit_comment_textarea_el:
        return not edit_comment_textarea_el.is_displayed()
    
    if new_comment_textarea_el and \
        new_comment_textarea_el.get_attribute("value").strip() == "":
        return find_comment_eval(browser) != None
    else:
        return False

def prepare_eval_commentfield(browser, student, total_grade):

    #verifica se é uma aba de edição ou um novo comentario
    comment_eval_saved_el = find_comment_eval(browser)
    edit_comment_textarea_el = None
    new_comment_textarea_el = None
    if comment_eval_saved_el:
        edit_comment_textarea_el = edit_comment_eval(comment_eval_saved_el)
    else:
        new_comment_textarea_el = write_pull_request_eval(browser, 
                                                        student, 
                                                        total_grade)
    return new_comment_textarea_el, edit_comment_textarea_el
def get_final_grade(browser):
    comment_eval = find_comment_eval(browser)
    dict_entries = {"nota final":None,
                    "atividades complementares":None}


    for str_line in comment_eval.text.split("\n"):
        for grade_entry in dict_entries.keys():
            if str_line.find(":") >= 0 and\
                str_line.strip().lower().startswith(grade_entry):

                grade_val = str_line.split(":")[-1].strip()
                if grade_val:
                    dict_entries[grade_entry] = Decimal(grade_val)
    return dict_entries["nota final"], dict_entries["atividades complementares"]

def eval_students_assignment(browser, total_grade, first_student_name_to_eval=None):
    print("Veio aqui")
    arr_students = get_students_from_assignment(browser)
    changes_tab, view_tab  = create_changes_and_view_tabs(browser)
    pos_student = 0
    pos_student_per_feedback_url = {}
    git_app = None
    print(f"Encontrou {len(arr_students)} estudantes")
    #caso o first_student_repo_to_eval for none
    #consideramos que jjá encontrou o primeiro aluno
    #assim, será coletado todos
    found_first_student = first_student_name_to_eval is None

    while pos_student<len(arr_students):
        student = arr_students[pos_student]
        #apenas coleta o estudante a partir do primeiro a avaliar
        if not found_first_student:
            if first_student_name_to_eval.lower() in student["name"].lower():
                found_first_student = True
            else:
                print(f"Estudante {student['name']} ignorado")
                pos_student += 1
                continue
        
        open_new_page(student["feedback_url"], browser)
        start = time.time()

        git_app = browse_student_assignment(browser, changes_tab, view_tab, git_app)
        end = time.time()
        print(f'Tempo: {end-start}')
        student["feedback_url"] = browser.current_url 
        pos_student_per_feedback_url[browser.current_url] = pos_student

        new_comment_el, edit_comment_el = prepare_eval_commentfield(browser, 
                                                            student, 
                                                            total_grade)
        student_feedback_url = browser.current_url
        current_url = student_feedback_url
        try:
            while not has_finished_edit(browser, new_comment_el, 
                                    edit_comment_el):
                time.sleep(1)
                current_url = browser.current_url
                if current_url != student_feedback_url and \
                    current_url in pos_student_per_feedback_url:
                    break
                #print("Aguardando")
        except StaleElementReferenceException:
            print("Saiu")
        current_url = browser.current_url
        if current_url != student_feedback_url:
            pos_student = pos_student_per_feedback_url[current_url]
            print(f"Voltou para o aluno {pos_student}")
        else:
            stale = True
            while stale:
                try:
                    student["final_grade"], student["complementar_grade"] = get_final_grade(browser)
                    stale = False
                except StaleElementReferenceException:
                    print("deu stale, tentando novamente")
                    stale = True

            yield student
            pos_student += 1

    