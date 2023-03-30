import os
import re

from clint.textui import colored
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .models.Course import Course

os.environ["WDM_LOCAL"] = "1"


def initialize_driver_for_preferred_browser(browser_arg):

    try:
        if browser_arg == "chrome":
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        elif browser_arg == "firefox":
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        elif browser_arg == "edge":
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install())
            )
        else:
            raise ValueError("Invalid choice")
        return driver
    except WebDriverException as err:
        print(colored.red(err.msg))
    except Exception:
        print(
            colored.red(
                "Please connect to internet to proceed. Need to download the required webdriver."
            )
        )


def parse_string_to_courses(registered_course_str):
    registered_course_str_list = registered_course_str.split("\n")[2:]
    parsed_courses = []

    for idx in range(0, len(registered_course_str_list), 4):
        if idx == len(registered_course_str_list):
            break

        parsed_course = Course(
            registered_course_str_list[idx],
            registered_course_str_list[idx + 1].split()[0],
            registered_course_str_list[idx + 3].split()[1],
            registered_course_str_list[idx + 2].split()[0],
            registered_course_str_list[idx + 2].split()[1],
        )

        parsed_courses.append(parsed_course)

        if idx + 4 < len(registered_course_str_list) and not re.match(
            r"^[A-Z]{2,4}\s[A-Z]\d{3}-[A-Z]\d", registered_course_str_list[idx + 4]
        ):
            parsed_course = Course(
                registered_course_str_list[idx],
                registered_course_str_list[idx + 1].split()[0],
                registered_course_str_list[idx + 5].split()[1],
                registered_course_str_list[idx + 4].split()[0],
                registered_course_str_list[idx + 4].split()[1],
            )

            parsed_courses.append(parsed_course)

            registered_course_str_list.remove(registered_course_str_list[idx + 4])
            registered_course_str_list.remove(registered_course_str_list[idx + 4])

    return parsed_courses
