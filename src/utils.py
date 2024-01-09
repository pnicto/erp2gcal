import os
import re
from typing import List

from clint.textui import colored
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .models.Course import Course

os.environ["WDM_LOCAL"] = "1"


def initialize_driver_for_preferred_browser(browser_arg, binary_location):
    try:
        if browser_arg == "chrome":
            chrome_options = ChromeOptions()
            if binary_location:
                chrome_options.binary_location = binary_location
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=chrome_options,
            )
        elif browser_arg == "firefox":
            firefox_options = FirefoxOptions()
            if binary_location:
                firefox_options.binary_location = binary_location
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options,
            )
        elif browser_arg == "edge":
            edge_options = EdgeOptions()
            if binary_location:
                edge_options.binary_location = binary_location
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=edge_options,
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


# TODO: It seems redundant to convert the list back to string when it is actually a string in the first place
def parse_string_to_courses(registered_course_str_list) -> List[Course]:
    parsed_courses = []
    normal_class_pattern = r"[A-Z]{2,4}\s[FG]\d{3}-[LPT]\d+\n[A-Z]{3}\s\(\d{4}\)\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}\s-\s\d{1,2}:\d{2}\b\n\w+\s+\w+"
    split_class_pattern = r"[A-Z]{2,4}\s[FG]\d{3}-[LPT]\d+\n[A-Z]{3}\s\(\d{4}\)\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}\s-\s\d{1,2}:\d{2}\b\n\w+\s+\w+\n(Mo|Tu|We|Th|Fr|Sa|Su)+\s\b\d{1,2}:\d{2}\s-\s\d{1,2}:\d{2}\b\n\w+\s+\w+"

    # just genius
    registered_course_str = "\n".join(registered_course_str_list)

    normal_courses_iter = re.finditer(normal_class_pattern, registered_course_str)
    split_courses_iter = re.finditer(split_class_pattern, registered_course_str)

    for normal_course_match in normal_courses_iter:
        normal_course_str = normal_course_match.group()
        normal_course_split = normal_course_str.split("\n")

        parsed_course = Course(
            normal_course_split[0],
            normal_course_split[1].split()[0],
            normal_course_split[2].split()[0],
            normal_course_split[2].split()[1],
        )
        parsed_courses.append(parsed_course)

    for split_course_match in split_courses_iter:
        split_course_str = split_course_match.group()
        split_course_split = split_course_str.split("\n")

        parsed_split_course = Course(
            split_course_split[0],
            split_course_split[1].split()[0],
            split_course_split[4].split()[0],
            split_course_split[4].split()[1],
        )
        parsed_courses.append(parsed_split_course)

    return parsed_courses
