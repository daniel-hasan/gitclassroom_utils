
from classroom.models import Assignment

from classroom.models import *
from selenium_utils.utils import *
from .student_eval import eval_students_assignment
def eval_student(browser, class_code, assignment_acronym,
                first_student_name_to_eval=None):
    
    obj_assignment = Assignment.objects.get(discipline_fk__code__iexact = class_code,
                                acronym__iexact = assignment_acronym)
    open_new_page(obj_assignment.assignment_url, browser)
    #pega o link da paginação da lista dos alunos antes
    arr_url = [link_to_assign_pg.get_attribute("href") 
                    for link_to_assign_pg in  browser.find_elements(By.CSS_SELECTOR, 
                                                        "nav.pagination a.next")] 
    
    first_student_found = eval_assignment_from_page(browser, obj_assignment,
                                                    False,
                                                    first_student_name_to_eval)
    for link_to_page in arr_url:
       
        open_new_page(link_to_page, browser)
        
         #assim que encontrar o primeiro estudante, deixar o first_student_name_to_eval = None
        #para coletar todos os demais estudantes
        first_student_name_to_eval = first_student_name_to_eval if not first_student_found else None
        first_student_found = eval_assignment_from_page(browser, obj_assignment,
                                    first_student_found,
                                   first_student_name_to_eval )

def eval_assignment_from_page(browser, obj_assignment,
                            first_student_found=False,
                            first_student_name_to_eval = None):

    for student_data in eval_students_assignment(browser, 
                                            obj_assignment.total_grade,
                                            first_student_name_to_eval):
        
        student,_ = Student.objects.get_or_create(class_id = student_data["id"],
                                        defaults={"name":student_data["name"]})
        handin,_ = Handin.objects.get_or_create(assignment_fk=obj_assignment,
                                    student_fk=student)
        auto_grade = student_data["auto_grade"]
        if type(auto_grade) == str:
            auto_grade = auto_grade.split("/")[0]
        handin.feedback_url = student_data["feedback_url"]
        handin.auto_grade = auto_grade
        handin.final_grade = student_data["final_grade"]
        handin.complementar_grade = student_data["complementar_grade"] if student_data["complementar_grade"] else 0
        handin.save()
        first_student_found = True
    return first_student_found