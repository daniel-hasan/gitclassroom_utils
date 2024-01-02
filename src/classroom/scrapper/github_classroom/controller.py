from selenium_utils.utils import open_new_page
from .persist_assignments import update_assignment_from_class, get_class_links
from ..base import abre_chrome_github
from .assignments import get_assignments_links
from .persist_student_data import eval_student

def update_tasks():
    browser = abre_chrome_github()

    open_new_page("https://classroom.github.com/classrooms", browser)
    arr_links = get_class_links(browser)
    
     
    for class_complete_name, class_link in arr_links:
        update_assignment_from_class(browser, class_complete_name, class_link)

def update_grades(class_code, assignment_acronym):
    browser = abre_chrome_github()
    eval_student(browser, class_code, assignment_acronym)
    