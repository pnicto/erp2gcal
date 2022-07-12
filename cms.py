# Selenium imports
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests

driver = webdriver.Edge(service=EdgeService(
    EdgeChromiumDriverManager().install()))

driver = webdriver.Edge()

# Login logic
# Going to login page and clicking on google login button
driver.get('https://cms.bits-hyderabad.ac.in/login/index.php')
loginButton = driver.find_element(By.LINK_TEXT, 'Google')

loginButton.click()

# Login action waiting for user to enter details to login

WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.ID, 'page-my-index')))


# Finding required parameters to perform requests
# Preferences page to get security key and session key
driver.get('https://cms.bits-hyderabad.ac.in/user/preferences.php')
driver.find_element(By.LINK_TEXT, 'Security keys').click()
securityKey = driver.find_element(By.CSS_SELECTOR, '.cell.c0').text
sessionKey = driver.current_url.split('=')[1]

# Clicking profile page to get user id
driver.find_element(By.CLASS_NAME, 'usertext').click()
driver.find_element(By.ID, 'actionmenuaction-2').click()
userId = driver.current_url.split('=')[1]

# Session token from cookies
moodleSession = driver.get_cookie('MoodleSession')['value']

# Cookie
cookie = {
    "MoodleSession": moodleSession
}

driver.quit()

# Unenrollment
def unenrollment(securityKey, userId, sessionKey, cookie):
    enrolledCourses = requests.get(
        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&wstoken={securityKey}&userid={userId}"
    ).json()

    print(f"Enrolling from {len(enrolledCourses)} courses\n")

    for course in enrolledCourses:
        print(f"Unenrolling from {course['shortname']}...")
        enrolInstance = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_course_enrolment_methods&moodlewsrestformat=json&wstoken={securityKey}&courseid={course['id']}").json()

        enrolId = enrolInstance[0]['id']

        res = requests.get(
            f"https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?confirm=1&enrolid={enrolId}&sesskey={sessionKey}", cookies=cookie)

    print("Done unenrolling!\n")

# Giving option to perform action
print("""
      1. Unenrol from all previous courses and Enrol in new courses
      2. Enrol
      3. Unenrol
      """)

choice = int(input('Enter 1 or 2:\n'))

if choice == 1:
  unenrollment(securityKey, userId, sessionKey, cookie)
elif choice == 2:
    print('enrol')
else:
  print('unenrol')
