from multiprocessing.connection import wait
from classroom.models import Assignment, Discipline
from selenium_utils.utils import open_new_page
from .persist_assignments import update_assignment_from_class, get_class_links
from ..base import abre_chrome_github
from .persist_student_data import eval_student
from .assignments import set_deadline, open_assignment_settings,update_assignment
from django.utils.timezone import make_aware
from selenium.common.exceptions import NoSuchElementException

def update_tasks(discipline_starts_with=""):
    browser = abre_chrome_github()

    open_new_page("https://classroom.github.com/classrooms", browser)
    arr_links = get_class_links(browser)
    
    
    for class_complete_name, class_link in arr_links:
        if class_complete_name.startswith(discipline_starts_with):
            update_assignment_from_class(browser, class_complete_name, class_link)

def update_grades(class_code, assignment_acronym, first_student_name_to_eval=None):
    browser = abre_chrome_github()
    eval_student(browser, class_code, assignment_acronym, first_student_name_to_eval)
    

def update_classroom_assignment_deadlines(discipline_name, from_date):
    browser = abre_chrome_github()

    open_new_page("https://classroom.github.com/classrooms", browser)

    discipline = Discipline.objects.get(name = discipline_name)
    for assignment in discipline.assignment_set.all():
        if assignment.deadline >= make_aware(from_date):
            open_assignment_settings(browser, assignment.assignment_url)
            try:
                set_deadline(browser, assignment.deadline)
                update_assignment(browser)
                print(f"Assignment {assignment.acronym} atualizado data para: {assignment.deadline}")
            except NoSuchElementException:
                print(f"Não encontrado: "+assignment.acronym+" aqui: "+assignment.assignment_url)

