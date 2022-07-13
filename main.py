from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import cms
import courseParse
import erp
import erp2gcal

if __name__ == "__main__":
  print("\n1. Unenrol from prev courses, Enrol in new courses, Create calendar events\n2. Unenrol from prev courses, Enrol in new courses\n3. Enrol\n4. Unenrol\n5. Create calendar events")

  choice = int(input("\nEnter your choice(1-5):\n"))

  # TODO: Give option to choose browser
  # print("\nChoose a installed browser among the list:\n")
  # print("\n1. Edge\n2. Chrome\n3. Firefox\n4. Brave\n5. Opera")

  # browser_choice = int(input("\nEnter your choice(1-5):\n"))

  driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

  if choice == 1:
    try:
      # Unenrol, Enrol, Calendar events
      # CMS Login
      cms.perform_login(driver)
      # Get params
      security_key, session_key, user_id, cookie = cms.get_required_parameters_to_make_requests(driver)
      # Unenrol
      cms.unenrol_from_all_courses(user_id=user_id,session_key=session_key,security_key=security_key,cookie=cookie)
      # ERP Login
      erp.navigation_and_login(driver)
      erp_registered_courses = erp.get_schedule(driver)
      # Enrol
      cms.enrol_all_registered_courses(erp_registered_courses=erp_registered_courses,cookie=cookie,security_key=security_key)
      # Create "Course" class instances
      courses = courseParse.coursesGen(erp_registered_courses)
      # Google calenda auth
      gcal_service = erp2gcal.google_auth()
      # Creating events
      erp2gcal.create_gcal_events(courses=courses,service=gcal_service,)
    except Exception as err:
      print(err)

  elif choice ==2:
    try:
      # Unenrol, Enrol
      cms.perform_login(driver)
      # Get params
      security_key, session_key, user_id, cookie = cms.get_required_parameters_to_make_requests(driver)
      # Unenrol
      cms.unenrol_from_all_courses(user_id=user_id,session_key=session_key,security_key=security_key,cookie=cookie)
      # ERP Login
      erp.navigation_and_login(driver)
      erp_registered_courses = erp.get_schedule(driver)
      # Enrol
      cms.enrol_all_registered_courses(erp_registered_courses=erp_registered_courses,cookie=cookie,security_key=security_key)
    except Exception as err:
      print(err)

  elif choice ==3:
    try:
      # Enrol
      cms.perform_login(driver)
      # Get params
      security_key, session_key, user_id, cookie = cms.get_required_parameters_to_make_requests(driver)
      # ERP Login
      erp.navigation_and_login(driver)
      erp_registered_courses = erp.get_schedule(driver)
      # Enrol
      cms.enrol_all_registered_courses(erp_registered_courses=erp_registered_courses,cookie=cookie,security_key=security_key)
    except Exception as err:
      print(err)

  elif choice ==4:
    try:
      # Unenrol
      cms.perform_login(driver)
      # Get params
      security_key, session_key, user_id, cookie = cms.get_required_parameters_to_make_requests(driver)
      # Unenrol
      cms.unenrol_from_all_courses(user_id=user_id,session_key=session_key,security_key=security_key,cookie=cookie)
    except Exception as err:
      print(err)

  elif choice==5:
    try:
      # Calendar events
      # ERP Login
      erp.navigation_and_login(driver)
      erp_registered_courses = erp.get_schedule(driver)
    except Exception as err:
      print(err)
