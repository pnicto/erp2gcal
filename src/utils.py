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


def parse_string_to_courses(registered_course_str_list):
    parsed_courses = []
    normal_class_pattern = r"[A-Z]{2,4}\s[FG]\d{3}-[LPT]\d+\n[A-Z]{3}\s\(\d{4}\)\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}[AP]M\s-\s\d{1,2}:\d{2}[AP]M\b\nRoom\s+TBA"
    split_class_pattern = r"[A-Z]{2,4}\s[FG]\d{3}-[LPT]\d+\n[A-Z]{3}\s\(\d{4}\)\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}[AP]M\s-\s\d{1,2}:\d{2}[AP]M\b\nRoom\s+TBA\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}[AP]M\s-\s\d{1,2}:\d{2}[AP]M\b\nRoom\s+TBA"

    for idx in range(len(registered_course_str_list)):
        if idx + 4 >= len(registered_course_str_list):
            break

        normal_class_str_to_match = "\n".join(
            [
                registered_course_str_list[idx],
                registered_course_str_list[idx + 1],
                registered_course_str_list[idx + 2],
                registered_course_str_list[idx + 3],
            ]
        )

        normal_class_match = re.match(normal_class_pattern, normal_class_str_to_match)

        if normal_class_match:
            parsed_course = Course(
                registered_course_str_list[idx],
                registered_course_str_list[idx + 1].split()[0],
                registered_course_str_list[idx + 3].split()[1],
                registered_course_str_list[idx + 2].split()[0],
                registered_course_str_list[idx + 2].split()[1],
            )
            parsed_courses.append(parsed_course)

            if idx + 5 >= len(registered_course_str_list):
                break

            split_class_str_to_match = "\n".join(
                [
                    registered_course_str_list[idx],
                    registered_course_str_list[idx + 1],
                    registered_course_str_list[idx + 2],
                    registered_course_str_list[idx + 3],
                    registered_course_str_list[idx + 4],
                    registered_course_str_list[idx + 5],
                ]
            )

            split_class_match = re.match(split_class_pattern, split_class_str_to_match)

            if split_class_match:
                parsed_course = Course(
                    registered_course_str_list[idx],
                    registered_course_str_list[idx + 1].split()[0],
                    registered_course_str_list[idx + 5].split()[1],
                    registered_course_str_list[idx + 4].split()[0],
                    registered_course_str_list[idx + 4].split()[1],
                )
                parsed_courses.append(parsed_course)

    return parsed_courses
