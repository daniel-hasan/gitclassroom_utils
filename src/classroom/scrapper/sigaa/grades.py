from classroom.models import Handin
from .main_page import open_grades_menu
from selenium.webdriver.common.by import By
from selenium_utils.utils import *
class GradesTable:
    
    def __init__(self, browser):
        self.acronyms_not_found = set()
        self.students_not_found = set()

        self.browser = browser
        self.col_per_assignment_acronym = {}
        arr_ths = browser.find_elements(By.CSS_SELECTOR, '#notas-turma tr:nth-child(2) th')
        for j, table_col_header in enumerate(arr_ths):
            self.col_per_assignment_acronym[table_col_header.text.strip()] = j
        
        self.student_line_per_id = {}
        student_lines = browser.find_elements(By.CSS_SELECTOR, '#notas-turma tr')
        for student_line in student_lines[2:]:
            current_student_id  = student_line.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text.strip()
            self.student_line_per_id[current_student_id] = student_line.find_elements(By.CSS_SELECTOR, "td")
            
        
    def set_student_grade(self, student_id, assignment_acronym, grade):
        if assignment_acronym not in self.col_per_assignment_acronym:
            self.acronyms_not_found.add(assignment_acronym)
            return False
        if student_id not in self.student_line_per_id:
            self.students_not_found.add(student_id)
            return False

        col_number = self.col_per_assignment_acronym[assignment_acronym]
        student_line =  self.student_line_per_id[student_id]
        
        formated_num = "{:.2f}".format( grade )
        if len(formated_num) == 4:
            formated_num = "0"+formated_num

        input_student = student_line[col_number].find_element(By.CSS_SELECTOR , "input")
        input_student.clear()
        input_student.send_keys(formated_num)
        return True
def update_grades_data(browser, discipline):
    open_grades_menu(browser)
    """
    script_js = "let tabela = document.querySelector('.listagem');\n"
    script_js += "let linhas = tabela.querySelectorAll('tr');\n"

    script_js += "for(let i = 2 ; i<linhas.length; i++){\n"
    script_js += "  let cols = linhas[i].querySelectorAll('td');\n"
    script_js += "  for(let j = 3; j<cols.length; j++){\n"
    script_js += "      cols[j].innerHTML = \"<input type='text' size=2>\";\n"
    script_js += "  }\n"
    script_js += "}"
    browser.execute_script(script_js)
    """
    grades_table = GradesTable(browser)
    assignment_acronym_not_found = set()
    for handin in Handin.objects.filter(assignment_fk__discipline_fk = discipline)\
                                .select_related("student_fk","assignment_fk"):
        assignment_acronym = handin.assignment_fk.acronym
        student_id = handin.student_fk.class_id
        found = grades_table.set_student_grade(student_id, assignment_acronym, handin.final_grade)
        if not found:
            assignment_acronym_not_found.add(assignment_acronym)
    click_through_to_new_page_by_css("input[alt$='Salvar']", browser)

    print(f"Acronyms not found: {grades_table.acronyms_not_found}")