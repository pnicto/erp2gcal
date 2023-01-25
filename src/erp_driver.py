from clint.textui import colored
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .utils import parse_string_to_courses


class ErpDriver:
    def __init__(self, driver):
        self.driver = driver

    def __navigate_to_login_page(self):
        try:
            self.driver.get(
                "https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?NavColl=true&ICAGTarget=start"
            )
            WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PATRANSACTIONTITLE"))
            )
        except TimeoutException:
            self.driver.quit()
            print(colored.red("Did not login in time"))

    def get_courses_from_student_center(self):
        try:
            self.__navigate_to_login_page()
            schedule_element = self.driver.execute_script(
                "return document.querySelector('.PSLEVEL1GRIDWBO')"
            )
            schedule = schedule_element.text
            courses = parse_string_to_courses(schedule)

            return courses
        except Exception as err:
            print(err)
            self.driver.quit()
