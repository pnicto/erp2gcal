from clint.textui import colored
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .utils import parse_string_to_courses


class ErpDriver:
    def __init__(self, driver):
        self.driver = driver

    def __navigate_to_login_page(self):
        try:
            logging.info("Attempting to go to the ERP student center")
            self.driver.get(
                "https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?NavColl=true&ICAGTarget=start"
            )
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PATRANSACTIONTITLE"))
            )
        except Exception as err:
            self.driver.quit()

            logging.info(type(err))
            logging.info(err)
            logging.info("Failed to go to the ERP student center")

            print(colored.red(err))
            print(colored.red("Did not login into ERP in time"))

    def get_courses_from_student_center(self):
        try:
            self.__navigate_to_login_page()
            logging.info("Attempting to get the registered courses from ERP")
            schedule_element = self.driver.execute_script(
                "return document.querySelector('.PSLEVEL1GRIDWBO')"
            )
            logging.info("Query selector returned")
            logging.info(schedule_element)

            schedule = schedule_element.text.split("\n")[2:]
            logging.info("User Schedule")
            logging.info(schedule_element.text)

            logging.info(f"Got {len(schedule)} courses from ERP schedule text")
            logging.info(schedule)

            courses = parse_string_to_courses(schedule)

            logging.info(f"Parsed {len(courses)} courses")
            for course in courses:
                logging.info(
                    f"Course,{course.name}, {course.start}, {course.component},{course.end},{course.days}"
                )

            return courses
        except Exception as err:
            print(colored.red(err))
            print("Failed getting courses from ERP")

            logging.info(type(err))
            logging.info(err)
            logging.info("Failed getting courses from ERP")
            self.driver.quit()
