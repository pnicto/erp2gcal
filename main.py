# Selenium imports
from lib2to3.pgen2 import driver
from selenium import webdriver
# Edge imports
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as edge_options
# Chrome imports
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as chrome_options
# Firefox imports
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# Brave imports
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.core.utils import ChromeType
# Opera imports
from webdriver_manager.opera import OperaDriverManager

import cms
import courseParse
import erp
import erp2gcal

# Colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def select_preferred_browser():
    print(f"\n{bcolors.OKCYAN}Choose a installed browser among the list:{bcolors.ENDC}\n")
    print(f"\n{bcolors.OKCYAN}1. Edge\n2. Chrome\n3. Firefox\n4. Brave\n5. Opera{bcolors.ENDC}")

    browser_choice = int(input(f"\n{bcolors.HEADER}Enter your choice(1-5):{bcolors.ENDC}\n"))
    if browser_choice==1:
        # Welp I tried turning the webdriver messages off let's see how well
        options = edge_options()
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    elif browser_choice==2:
        options = chrome_options()
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_choice==3:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_choice==4:
        driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
    elif browser_choice==5:
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    else:
        print(f'{bcolors.FAIL}Choose from the given options{bcolors.ENDC}')
    return driver

if __name__ == "__main__":
    print(f"\n{bcolors.HEADER}1. Unenrol from prev courses, Enrol in new courses, Create calendar events\n2. Unenrol from prev courses, Enrol in new courses\n3. Enrol\n4. Unenrol\n5. Create calendar events{bcolors.ENDC}")

    choice = int(input(f"\n{bcolors.HEADER}Enter your choice(1-5):{bcolors.ENDC}\n"))

    driver = select_preferred_browser()
    if choice == 1:
        try:
            # Unenrol, Enrol, Calendar events
            # CMS Login
            cms.perform_login(driver)
            # Get params
            (
                security_key,
                session_key,
                user_id,
                cookie,
            ) = cms.get_required_parameters_to_make_requests(driver)
            # Unenrol
            cms.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )
            # ERP Login
            erp.navigation_and_login(driver)
            erp_registered_courses = erp.get_schedule(driver)
            # Create "Course" class instances
            courses = courseParse.coursesGen(erp_registered_courses)
            # Enrol
            cms.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )
            # Google calenda auth
            gcal_service = erp2gcal.google_auth()
            # Creating events
            erp2gcal.create_gcal_events(
                courses=courses,
                service=gcal_service,
            )
            # Remove the side effect
            erp2gcal.clean_the_unnecessary_events(service=gcal_service)
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    elif choice == 2:
        try:
            # Unenrol, Enrol
            cms.perform_login(driver)
            # Get params
            (
                security_key,
                session_key,
                user_id,
                cookie,
            ) = cms.get_required_parameters_to_make_requests(driver)
            # Unenrol
            cms.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )
            # ERP Login
            erp.navigation_and_login(driver)
            erp_registered_courses = erp.get_schedule(driver)
            # Create "Course" class instances
            courses = courseParse.coursesGen(erp_registered_courses)
            # Enrol
            cms.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )

        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    elif choice == 3:
        try:
            # Enrol
            cms.perform_login(driver)
            # Get params
            (
                security_key,
                session_key,
                user_id,
                cookie,
            ) = cms.get_required_parameters_to_make_requests(driver)
            # ERP Login
            erp.navigation_and_login(driver)
            erp_registered_courses = erp.get_schedule(driver)
            # Create "Course" class instances
            courses = courseParse.coursesGen(erp_registered_courses)
            # Enrol
            cms.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    elif choice == 4:
        try:
            # Unenrol
            cms.perform_login(driver)
            # Get params
            (
                security_key,
                session_key,
                user_id,
                cookie,
            ) = cms.get_required_parameters_to_make_requests(driver)
            # Unenrol
            cms.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    elif choice == 5:
        try:
            # Calendar events
            # ERP Login
            erp.navigation_and_login(driver)
            erp_registered_courses = erp.get_schedule(driver)
            # Create "Course" class instances
            courses = courseParse.coursesGen(erp_registered_courses)
            # Google calenda auth
            gcal_service = erp2gcal.google_auth()
            # Creating events
            erp2gcal.create_gcal_events(
                courses=courses,
                service=gcal_service,
            )
            # Remove the side effect
            erp2gcal.clean_the_unnecessary_events(service=gcal_service)
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")