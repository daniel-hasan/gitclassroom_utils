from datetime import datetime
from dateutil import tz
from selenium.webdriver.common.by import By
from selenium_utils.utils import *
from selenium.webdriver.common.keys import Keys

def get_assignment_data(browser):
    assignment_link = browser.find_element(By.CSS_SELECTOR, 
                                        "input[name^='assignment-invitation-link']")\
                           .get_attribute("value")
    
    #procura o deadline na pagina principal
    deadline_dates = browser.find_elements(By.CSS_SELECTOR, 
                                        "time")
    deadline = None
    for deadline_date in deadline_dates:
        deadline_parent = deadline_date.find_element(By.XPATH, '..')
        if deadline_parent.text.lower().find("due")>=0:
            str_deadline = deadline_date.get_attribute("datetime")
            deadline = datetime.strptime(str_deadline, "%Y-%m-%dT%H:%M:%Sz")
    #
    # se nao achou o deadline, procura na pagina de configuração
    if not deadline:
        #cria url de configuração
        current_assignment = browser.current_url
        open_assignment_settings(browser, current_assignment)
        
        
        
        #obtem deadline
        deadline_el = browser.find_element(By.ID, "assignment_deadline_deadline_at") 
        str_deadline = deadline_el.get_attribute("value")
        deadline = None
        if str_deadline:
            deadline = datetime.strptime(str_deadline, "%Y-%m-%dT%H:%M")

        
        open_new_page(current_assignment, browser)


    return {"invitation_url":assignment_link,
            "deadline":deadline
             }
def set_deadline(browser, deadline):
    deadline_el = browser.find_element(By.ID, "assignment_deadline_deadline_at")

    str_date_deadline = deadline.strftime("%m%d%Y")
    int_hour_deadline = int(deadline.strftime("%H"))
    int_min_deadline = deadline.strftime("%M")
    str_pm_am = "A" if int_hour_deadline <= 12 else "P"
    if int_hour_deadline > 13:
        int_hour_deadline = int_hour_deadline-12

    deadline_el.send_keys(str_date_deadline)
    deadline_el.send_keys(Keys.RIGHT)
    deadline_el.send_keys(f"{int_hour_deadline}{int_min_deadline}{str_pm_am}")
    

def update_assignment(browser):
    click_through_to_new_page_by_css("button[type='submit']", browser)

def open_assignment_settings(browser, assignment_url):
    arr_cur_assignment_parts = assignment_url.split("/")
    arr_cur_assignment_parts[-2] = "new_assignments"
    edit_assignment_url = "/".join(arr_cur_assignment_parts)+"/settings"
    open_new_page(edit_assignment_url, browser)
    return edit_assignment_url

def get_assignments_links(browser):
    new_assignment_el = browser.find_element(By.CSS_SELECTOR, "a[href$='/new-assignment']")
    
    href_new_assignment = new_assignment_el.get_attribute('href')
    classroom_link = "/".join(href_new_assignment.split("/")[:-1])
    classroom_path = "/"+"/".join(classroom_link[9:].split("/")[1:])

    links_per_class = {}
    for a_classroom_el in browser.find_elements(By.CSS_SELECTOR, f"a[href^='{classroom_path}/assignments/']"):
        link = a_classroom_el.get_attribute('href')
        
        if not link.endswith("settings") and link != classroom_link:
            class_name = a_classroom_el.text

            links_per_class[class_name] = link

    return links_per_class

def get_assignments_from_classroom(browser, classroom_url):
    
    open_new_page(classroom_url, browser)
    
    links_per_class = get_assignments_links(browser)
    for assignment_name, assignment_link in links_per_class.items():
        print(f"{assignment_name}: {assignment_link}")
        
        open_new_page(assignment_link, browser)
        topic_acronym, name_points = assignment_name.split("]")
        
        arr_name_points = name_points.split("(")
        total_points = None
        if len(arr_name_points)>1:
            name, total_points = name_points.split("(")
            total_points = total_points.replace("p)","")
        else: 
            name = name_points

        name = name.strip()
        
        topic, acronym = topic_acronym[1:].split("-")

        assignment_data = get_assignment_data(browser)
        
        assignment_data["link"] = assignment_link
        assignment_data["topic"] = topic
        assignment_data["acronym"] = acronym
        assignment_data["name"] = name
        assignment_data["total_grade"] = total_points
        
        yield assignment_data