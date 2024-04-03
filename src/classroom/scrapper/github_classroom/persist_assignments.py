from classroom.models import *
from django.utils.timezone import make_aware
from classroom.scrapper.github_classroom.assignments import *
def get_class_links(browser):
    arr_links = []
    for class_link_el in browser.find_elements(By.CSS_SELECTOR, "#js-search-results a.d-block[href^='/classrooms/']"):
        class_link = class_link_el.get_attribute("href")
        class_name = class_link_el.find_element(By.CSS_SELECTOR, "h2").text
        arr_links.append((class_name, class_link))
    return arr_links

def update_assignment_from_class(browser, class_complete_name, class_link):
    print(class_complete_name, class_link)
    class_code, class_name = class_complete_name.split("]")
    
    class_code = class_code[1:]
    class_name = class_name.strip()
    print(f"Class link: {class_link}")
    obj_discipline, created = Discipline.objects.get_or_create(url = class_link, 
                                defaults={"name":class_name,
                                        "code":class_code})
    if not created:
        obj_discipline.name = class_name
        obj_discipline.code = class_code
        obj_discipline.save()
    
    
    for assignment_data in get_assignments_from_classroom(browser, class_link):
        print("-----------------")
        obj_assign_topic,_ = Topic.objects.get_or_create(acronym = assignment_data["topic"],
                                                    discipline_fk = obj_discipline)
        
        obj_assign, created = Assignment.objects.get_or_create(invitation_url = assignment_data["invitation_url"],
                                                        defaults={"topic_fk":obj_assign_topic,
                                                                    "discipline_fk":obj_discipline,
                                                                    "acronym":assignment_data["acronym"],
                                                                    "name":assignment_data["name"],
                                                                    "assignment_url":assignment_data["link"],
                                                                    "deadline":make_aware(assignment_data["deadline"]) if assignment_data["deadline"] else None,
                                                                    "total_grade":assignment_data["total_grade"]})

        obj_assign.topic_fk = obj_assign_topic
        obj_assign.acronym = assignment_data["acronym"]
        obj_assign.name =  assignment_data["name"]
        obj_assign.assignment_url =  assignment_data["link"]
        obj_assign.deadline =  make_aware(assignment_data["deadline"]) if assignment_data["deadline"] else None 
        obj_assign.total_grade =assignment_data["total_grade"]
        obj_assign.save()

        
