# Selenium imports
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

from cms import CmsActions
from course_parse import CourseParser
from erp import ErpActions
from erp2gcal import Erp2Gcal
from utils.bcolors import bcolors


def select_preferred_browser():
    print(
        f"\n{bcolors.OKCYAN}Choose an installed browser among the list:{bcolors.ENDC}\n"
    )
    print(f"{bcolors.OKCYAN}1. Edge\n2. Chrome\n3. Firefox\n{bcolors.ENDC}")

    browser_choice = int(
        input(f"\n{bcolors.HEADER}Enter your choice(1-3):{bcolors.ENDC}\n")
    )
    if browser_choice == 1:
        # Welp I tried turning the webdriver messages off let's see how well it does
        options = edge_options()
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install())
        )
    elif browser_choice == 2:
        options = chrome_options()
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
    elif browser_choice == 3:
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install())
        )
    else:
        print(f"{bcolors.FAIL}Choose from the given options{bcolors.ENDC}")
    return driver


if __name__ == "__main__":
    try:
        driver = select_preferred_browser()
        # CMS Login
        CmsActions.perfrom_cms_login(driver)
        # Get params
        (
            security_key,
            session_key,
            user_id,
            cookie,
        ) = CmsActions.get_required_parameters_to_make_requests(driver)
        # ERP Login
        ErpActions.navigation_and_login(driver)
        erp_registered_courses = ErpActions.get_schedule(driver)
        # Create "Course" class instances
        courses = CourseParser.course_instance_generator(erp_registered_courses)
        driver.quit()

        print(
            f"\n{bcolors.HEADER}1. Unenrol from prev courses, Enrol in new courses, Create calendar events\n2. Unenrol from prev courses, Enrol in new courses\n3. Enrol\n4. Unenrol\n5. Create calendar events{bcolors.ENDC}"
        )

        choice = int(
            input(f"\n{bcolors.HEADER}Enter your choice(1-5):{bcolors.ENDC}\n")
        )

        if choice == 1:
            # Unenrol
            CmsActions.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )
            # Enrol
            CmsActions.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )
            CmsActions.enrol_main_sections(
                courses=courses, cookie=cookie, security_key=security_key
            )

            # Calendar events
            # Google calenda auth
            gcal_service = Erp2Gcal.perform_google_auth()
            # Creating events
            Erp2Gcal.create_gcal_events(
                courses=courses,
                service=gcal_service,
            )
            # Remove the side effect
            Erp2Gcal.clean_the_unnecessary_events(service=gcal_service)

        elif choice == 2:
            # Unenrol
            CmsActions.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )
            # Enrol
            CmsActions.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )

            CmsActions.enrol_main_sections(
                courses=courses, cookie=cookie, security_key=security_key
            )

        elif choice == 3:
            # Enrol
            CmsActions.enrol_all_registered_courses(
                courses=courses,
                cookie=cookie,
                security_key=security_key,
            )

            CmsActions.enrol_main_sections(
                courses=courses, cookie=cookie, security_key=security_key
            )

        elif choice == 4:
            # Unenrol
            CmsActions.unenrol_from_all_courses(
                user_id=user_id,
                session_key=session_key,
                security_key=security_key,
                cookie=cookie,
            )

        elif choice == 5:
            # Calendar events
            # Google calenda auth
            gcal_service = Erp2Gcal.perform_google_auth()
            # Creating events
            Erp2Gcal.create_gcal_events(
                courses=courses,
                service=gcal_service,
            )
            # Remove the side effect
            Erp2Gcal.clean_the_unnecessary_events(service=gcal_service)

    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
