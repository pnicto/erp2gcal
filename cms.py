from math import ceil

import requests
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver = webdriver.Edge()

# Function which goes to login page
def perform_login():
    try:
        # Go to CMS
        driver.get('https://cms.bits-hyderabad.ac.in/login/index.php')
        # Finding the login with google button
        login_button = driver.find_element(By.LINK_TEXT, 'Google')
        login_button.click()
        # Login action waiting for user to enter details to login
        WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, 'page-my-index')))
    except Exception as err:
        print(err)


# Function which returns security key, session key, user id to make requests
def get_required_parameters_to_make_requests():
    try:
    # Preferences page to get security key and session key
        driver.get('https://cms.bits-hyderabad.ac.in/user/preferences.php')
        driver.find_element(By.LINK_TEXT, 'Security keys').click()
        security_key = driver.find_element(By.CSS_SELECTOR, '.cell.c0').text
        session_key = driver.current_url.split('=')[1]
        # Clicking profile page to get user id
        driver.find_element(By.CLASS_NAME, 'usertext').click()
        driver.find_element(By.ID, 'actionmenuaction-2').click()
        user_id = driver.current_url.split('=')[1]
        # Session token from cookies
        moodle_session = driver.get_cookie('MoodleSession')['value']
        # Cookie
        cookie = {
            "MoodleSession": moodle_session
        }
        return (security_key, session_key, user_id, cookie)
    except Exception as err:
        print(err)

# Function which unenrolls from *all* courses
def unenrol_from_all_courses(security_key,user_id,session_key,cookie):
    try:
        # Gets all enrolled courses and parses them
        enrolled_courses = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&wstoken={security_key}&userid={user_id}"
        ).json()

        print(f"Enrolling from {len(enrolled_courses)} courses\n")

        for course in enrolled_courses:
            print(f"Unenrolling from {course['shortname']}...")
            enrol_instance = requests.get(
                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_course_enrolment_methods&moodlewsrestformat=json&wstoken={security_key}&courseid={course['id']}").json()
            # For all the enrolled courses get instance id
            enrolId = enrol_instance[0]['id']
            # Make unenrol request
            requests.get(
                f"https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?confirm=1&enrolid={enrolId}&sesskey={session_key}", cookies=cookie)

        if len(enrolled_courses) == 0:
            print("\nDone unenrolling!!!\n")
        else:
            print(enrolled_courses)
    except Exception as err:
        print(err)

# Function which enrolls you in *all* registered courses on ERP
def enrol_all_registered_courses(security_key,
cookie,erp_registered_courses, number_of_search_results=5,filter_by_category=-1):
    try:
        print(f"Trying to enroll into {len(erp_registered_courses)} courses")
        for course in erp_registered_courses:
            print(f"Searching for {course.name} in courses...")
            searchRes = requests.get(
                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course.name}&perpage={number_of_search_results}&page=0", cookies=cookie).json()
            totalPages = ceil(searchRes['total'] / number_of_search_results)
            if totalPages == 0:
                print(f"No results found for '{course.name}'. Press enter to continue")
                input()
                continue
            keepLoading = True
            pageNum = 0
            while keepLoading:
                print(f"[Page {pageNum + 1} of {totalPages}]")
                for resNum in range(min(searchRes['total'], number_of_search_results)):
                    if filter_by_category > 0:
                        if searchRes['courses'][resNum]['categoryid'] != filter_by_category:
                            continue
                    print(f"{resNum + 1}. {searchRes['courses'][resNum]['fullname']}")
                    print(
                        f"\tCategory: {searchRes['courses'][resNum]['categoryname']}")
                    print(
                        f"\tIntructors: {', '.join([x['fullname'] for x in searchRes['courses'][resNum]['contacts']])}")
                    print()
                print("""
        Enter one of the above numbers to enrol into the corresponding course.
        Type in 'n' and 'p' to navigate to the next and previous pages respectively.
        To skip this course, type in 's'
                    """)
                choice = input()
                if choice == "s":
                    keepLoading = False
                elif choice == "n":
                    if (pageNum + 1) >= totalPages:
                        print("You are on the last page.")
                        continue
                    pageNum += 1
                    searchRes = requests.get(
                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course.name}&perpage={number_of_search_results}&page={pageNum}", cookies=cookie).json()
                elif choice == "p":
                    if (pageNum - 1) < 0:
                        print("You are on the first page.")
                        continue
                    pageNum -= 1
                    searchRes = requests.get(
                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course.name}&perpage={number_of_search_results}&page={pageNum}", cookies=cookie).json()
                else:
                    try:
                        choice = int(choice)
                        if choice <= min(searchRes['total'], number_of_search_results) and choice > 0:
                            # Enrol course
                            cid = searchRes['courses'][resNum]['id']
                            enrolRes = requests.get(
                                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={security_key}&courseid={cid}", cookies=cookie).json()
                            if enrolRes['status']:
                                print(
                                    f"Enrolled in course {searchRes['courses'][resNum]['fullname']} successfully!"  )
                                print()
                            else:
                                print(
                                    f"Course enrollment in {searchRes['courses'][resNum]['fullname']} failed"  )
                                print()
                            keepLoading = False
                        else:
                            print("Invalid choice")
                    except Exception as err:
                        print("Invalid choice")
    except Exception as err:
        print(err)
