# # Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Colors for terminal output
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Function which goes to login page
def navigation_and_login(driver):
    # Goes to this specific url which is the Student Center Section of ERP
    try:
        driver.get(
            "https://sis.erp.bits-pilani.ac.in/psc/sisprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?NavColl=true&ICAGTarget=start"
        )

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PATRANSACTIONTITLE"))
        )
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


# Function which returns the registered courses data from ERP
def get_schedule(driver):
    try:
        schedule = driver.execute_script(
            "return document.querySelector('.PSLEVEL1GRIDWBO')"
        )
        rawTableData = schedule.text
        # Removes the 2 unecessary items after splitting and returns it as a list
        return rawTableData.split("\n")[2:]
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
