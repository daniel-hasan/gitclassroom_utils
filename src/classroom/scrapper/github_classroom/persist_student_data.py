
from classroom.models import Assignment

from classroom.models import *
from selenium_utils.utils import *
from .student_eval import eval_students_assignment
def eval_student(browser, class_code, assignment_acronym):
    obj_assignment = Assignment.objects.get(discipline_fk__code__iexact = class_code,
                                acronym__iexact = assignment_acronym)
    open_new_page(obj_assignment.assignment_url, browser)

    
    for student_data in eval_students_assignment(browser, obj_assignment.total_grade):
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