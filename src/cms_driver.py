from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CmsDriver:
    def __init__(self, driver) -> None:
        self.driver = driver

    def __navigate_to_login_page(self):
        self.driver.get("https://cms.bits-hyderabad.ac.in/login/index.php")
        login_button = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Google"))
        )
        login_button.click()

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

        return session_key

    def __get_security_key(self, session_key):
        self.driver.get(
            f"https://cms.bits-hyderabad.ac.in/user/managetoken.php?sesskey={session_key}"
        )
        security_key_cell = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cell.c0"))
        )
        security_key = security_key_cell.text
        return security_key

    def __get_user_id(self):
        self.driver.get("https://cms.bits-hyderabad.ac.in/user/preferences.php")
        edit_profile_link = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Edit profile"))
        )
        edit_profile_link.click()
        user_id = self.driver.current_url.split("&")[0].split("=")[1]
        return user_id

    def get_required_parameters_for_cms_api(self):
        self.__navigate_to_login_page()
        session_key = self.__get_session_key()
        security_key = self.__get_security_key(session_key)
        user_id = self.__get_user_id()

        moodle_session = self.driver.get_cookie("MoodleSession")["value"]
        cookie = {"MoodleSession": moodle_session}

        return (session_key, security_key, user_id, cookie)
