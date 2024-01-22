import logging
from clint.textui import colored
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CmsDriver:
    def __init__(self, driver) -> None:
        self.driver = driver

    def __navigate_to_login_page(self):
        try:
            self.driver.get("https://cms.bits-hyderabad.ac.in/login/index.php")
            login_button = WebDriverWait(self.driver, 100).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Google"))
            )
            logging.info("Attempting to click the login with google button")
            login_button.click()
        except Exception as err:
            self.driver.quit()
            logging.info(type(err))
            logging.info(err)
            logging.info("Failed to go to the CMS login page")

            print(colored.red(err))
            print(colored.red("Did not login to into CMS in time"))

    def __get_session_key(self):
        logout_btn = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/nav/div[2]/div[5]/div/div/div/div/div/div/a[8]",
                )
            )
        )
        session_key = logout_btn.get_dom_attribute("href").split("=")[1]
        logging.info("Attempting to get the session key")

        return session_key

    def __get_security_key(self, session_key):
        self.driver.get(
            f"https://cms.bits-hyderabad.ac.in/user/managetoken.php?sesskey={session_key}"
        )
        security_key_cell = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cell.c0"))
        )
        security_key = security_key_cell.text
        logging.info("Attempting to get the security key")
        return security_key

    def __get_user_id(self):
        self.driver.get("https://cms.bits-hyderabad.ac.in/user/preferences.php")
        edit_profile_link = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Edit profile"))
        )
        edit_profile_link.click()
        user_id = self.driver.current_url.split("&")[0].split("=")[1]
        logging.info("Attempting to get the user id")
        return user_id

    def get_required_parameters_for_cms_api(self):
        logging.info("Attempting to navigate to CMS")
        self.__navigate_to_login_page()
        logging.info("Attempting to get the required parameters from CMS")
        session_key = self.__get_session_key()
        security_key = self.__get_security_key(session_key)
        user_id = self.__get_user_id()

        logging.info("Attempting to get the moodle session cookie")

        moodle_session = self.driver.get_cookie("MoodleSession")["value"]
        cookie = {"MoodleSession": moodle_session}

        logging.info("Lengths of CMS Parameters: ")
        logging.info(len(session_key))
        logging.info(len(user_id))
        logging.info(len(security_key))
        logging.info(len(cookie))

        return (session_key, security_key, user_id, cookie)
