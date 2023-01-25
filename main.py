from clize import run

from src.cms_actions import CmsActions
from src.cms_driver import CmsDriver
from src.erp_driver import ErpDriver
from src.gcal_actions import GoogleCalendarActions
from src.utils import initialize_driver_for_preferred_browser


def main(actions="abc", browser="firefox"):
    """
    Erp2gcal is a program to create google calendar events for your registered courses along with some functionality for cms.

    :param browser: Headless browser of your choice (choose an installed one)

    Acceptable browser params are 'edge', 'firefox', 'chrome'

    :param actions: Actions to perform. Refer below for the acceptable values eg: ac

        a : Unenrol from all courses\n
        b : Enrol into registered courses on cms\n
        c : Create gcal events\n
        d : Delete created gcal events

    For more information visit https://github.com/pnicto/erp2gcal
    """

    driver = initialize_driver_for_preferred_browser(browser)

    registered_courses = None
    cms_actions = None
    gcal_actions = None

    try:
        cms_driver = CmsDriver(driver)
        erp_driver = ErpDriver(driver)

        if "a" in actions:
            cms_actions = CmsActions(cms_driver)
            cms_actions.unenrol_from_all_courses()

        if "b" in actions:
            if not cms_actions:
                cms_actions = CmsActions(cms_driver)

            registered_courses = erp_driver.get_courses_from_student_center()
            cms_actions.enrol_into_registered_courses(registered_courses)

        if "c" in actions:
            if not registered_courses:
                registered_courses = erp_driver.get_courses_from_student_center()

            gcal_actions = GoogleCalendarActions()
            gcal_actions.create_calendar_events(registered_courses)

        if "d" in actions:
            if not gcal_actions:
                gcal_actions = GoogleCalendarActions()

            gcal_actions.delete_all_created_events()

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    run(main)
