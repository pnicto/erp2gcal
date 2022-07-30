from math import ceil

import requests

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
def perform_login(driver):
    try:
        # Go to CMS
        driver.get("https://cms.bits-hyderabad.ac.in/login/index.php")
        # Finding the login with google button
        login_button = driver.find_element(By.LINK_TEXT, "Google")
        login_button.click()
        # Login action waiting for user to enter details to login
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "page-my-index"))
        )
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


# Function which returns security key, session key, user id to make requests
def get_required_parameters_to_make_requests(driver):
    try:
        # Preferences page to get security key and session key
        driver.get("https://cms.bits-hyderabad.ac.in/user/preferences.php")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Security keys"))
        )
        driver.find_element(By.LINK_TEXT, "Security keys").click()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cell.c0"))
        )
        security_key = driver.find_element(By.CSS_SELECTOR, ".cell.c0").text
        session_key = driver.current_url.split("=")[1]
        # Clicking profile page to get user id
        driver.find_element(By.CLASS_NAME, "usertext").click()
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "actionmenuaction-2"))
        )
        driver.find_element(By.ID, "actionmenuaction-2").click()
        user_id = driver.current_url.split("=")[1]
        # Session token from cookies
        moodle_session = driver.get_cookie("MoodleSession")["value"]
        # Cookie
        cookie = {"MoodleSession": moodle_session}
        return (security_key, session_key, user_id, cookie)
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


# Function which unenrolls from *all* courses
def unenrol_from_all_courses(security_key, user_id, session_key, cookie):
    try:
        # Gets all enrolled courses and parses them
        enrolled_courses = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&wstoken={security_key}&userid={user_id}"
        ).json()

        print(
            f"{bcolors.WARNING}\nUnenrolling from {len(enrolled_courses)} courses{bcolors.ENDC}"
        )

        for course in enrolled_courses:
            print(f"Unenrolling from {course['shortname']}...")
            enrol_instance = requests.get(
                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_course_enrolment_methods&moodlewsrestformat=json&wstoken={security_key}&courseid={course['id']}"
            ).json()
            # For all the enrolled courses get instance id
            enrolId = enrol_instance[0]["id"]
            # Make unenrol request
            requests.get(
                f"https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?confirm=1&enrolid={enrolId}&sesskey={session_key}",
                cookies=cookie,
            )

            print(
                f"{bcolors.OKGREEN}Unenrolled from {course['shortname']}.\n{bcolors.ENDC}"
            )
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


# Function which enrolls you in *all* registered courses on ERP
# Many thanks to PyRet#4288 for the code below.
# Please do not try to understand :D
def enrol_all_registered_courses(
    security_key, cookie, courses, number_of_search_results=5, filter_by_category=-1
):
    try:
        print(f"Trying to enroll into {len(courses)} courses\n")
        for course in courses:
            print(f"Searching for {course.name} in courses...")
            course_search_term = " ".join(course.name.split("-"))

            # Normal course search
            searchRes = requests.get(
                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page=0",
                cookies=cookie,
            ).json()
            totalPages = ceil(searchRes["total"] / number_of_search_results)
            if totalPages == 0:
                print(
                    f"{bcolors.WARNING}No results found for '{course_search_term}'. Press enter to continue{bcolors.ENDC}"
                )
                input()
                continue
            keepLoading = True
            pageNum = 0
            while keepLoading:
                print(f"{bcolors.OKGREEN}[Page {pageNum + 1} of {totalPages}]")
                for resNum in range(min(searchRes["total"], number_of_search_results)):
                    if filter_by_category > 0:
                        if (
                            searchRes["courses"][resNum]["categoryid"]
                            != filter_by_category
                        ):
                            continue
                    print(f"{resNum + 1}. {searchRes['courses'][resNum]['fullname']}")
                    print(f"\tCategory: {searchRes['courses'][resNum]['categoryname']}")
                    print(
                        f"\tInstructors: {', '.join([x['fullname'] for x in searchRes['courses'][resNum]['contacts']])}"
                    )
                    print(f"CID: {searchRes['courses'][resNum]['id']}")
                    print()
                print(
                    bcolors.WARNING
                    + """
        Enter one of the above numbers to enrol into the corresponding course.
        Type in 'n' and 'p' to navigate to the next and previous pages respectively.
        To skip this course, type in 's'
                    """
                    + bcolors.ENDC
                )
                choice = input()
                if choice == "s":
                    keepLoading = False
                elif choice == "n":
                    if (pageNum + 1) >= totalPages:
                        print("You are on the last page.")
                        continue
                    pageNum += 1
                    searchRes = requests.get(
                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page={pageNum}",
                        cookies=cookie,
                    ).json()
                elif choice == "p":
                    if (pageNum - 1) < 0:
                        print("You are on the first page.")
                        continue
                    pageNum -= 1
                    searchRes = requests.get(
                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page={pageNum}",
                        cookies=cookie,
                    ).json()
                else:
                    try:
                        choice = int(choice)
                        print(choice)
                        if (
                            choice <= min(searchRes["total"], number_of_search_results)
                            and choice > 0
                        ):
                            # Enrol course
                            print("Normal Course")
                            cid = searchRes["courses"][
                                pageNum * number_of_search_results + (choice - 1)
                            ]["id"]
                            enrolRes = requests.get(
                                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={security_key}&courseid={cid}",
                                cookies=cookie,
                            ).json()
                            if enrolRes["status"]:
                                print(
                                    f"{bcolors.OKGREEN}Enrolled in course {searchRes['courses'][pageNum * number_of_search_results + (choice - 1)]['fullname']} successfully!{bcolors.ENDC}"
                                )
                                print()
                            else:
                                print(
                                    f"{bcolors.FAIL}Course enrollment in {searchRes['courses'][pageNum * number_of_search_results + (choice - 1)]['fullname']} failed{bcolors.ENDC}"
                                )
                                print()
                            keepLoading = False
                        else:
                            print("Invalid choice")

                    except Exception as err:
                        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")


# Laziness got the best of me so instead of coming up with something new I just changed few lines in the normal one 💀
def enrol_main_sections(
    security_key, cookie, courses, number_of_search_results=5, filter_by_category=-1
):
    try:
        for course in courses:
            course_search_term = " ".join(course.name.split("-"))[:-1]
            print(f"{bcolors.HEADER}Enrolling into L/P sections{bcolors.ENDC}")
            if (
                course_search_term.endswith("P") or course_search_term.endswith("L")
            ) and course_search_term != "ME F111 P":
                print(
                    f"{bcolors.OKGREEN}Searching for {course_search_term}{bcolors.ENDC}\n"
                )

                # Normal course search
                searchRes = requests.get(
                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page=0",
                    cookies=cookie,
                ).json()
                totalPages = ceil(searchRes["total"] / number_of_search_results)
                if totalPages == 0:
                    print(
                        f"{bcolors.WARNING}No results found for '{course_search_term}'. Press enter to continue{bcolors.ENDC}"
                    )
                    input()
                    continue
                keepLoading = True
                pageNum = 0
                while keepLoading:
                    print(f"{bcolors.OKGREEN}[Page {pageNum + 1} of {totalPages}]")
                    for resNum in range(
                        min(searchRes["total"], number_of_search_results)
                    ):
                        if filter_by_category > 0:
                            if (
                                searchRes["courses"][resNum]["categoryid"]
                                != filter_by_category
                            ):
                                continue
                        print(
                            f"{resNum + 1}. {searchRes['courses'][resNum]['fullname']}"
                        )
                        print(
                            f"\tCategory: {searchRes['courses'][resNum]['categoryname']}"
                        )
                        print(
                            f"\tInstructors: {', '.join([x['fullname'] for x in searchRes['courses'][resNum]['contacts']])}"
                        )
                        print(f"CID: {searchRes['courses'][resNum]['id']}")
                        print()
                    print(
                        bcolors.WARNING
                        + """
            Enter one of the above numbers to enrol into the corresponding course.
            Type in 'n' and 'p' to navigate to the next and previous pages respectively.
            To skip this course, type in 's'
                        """
                        + bcolors.ENDC
                    )
                    choice = input()
                    if choice == "s":
                        keepLoading = False
                    elif choice == "n":
                        if (pageNum + 1) >= totalPages:
                            print("You are on the last page.")
                            continue
                        pageNum += 1
                        searchRes = requests.get(
                            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page={pageNum}",
                            cookies=cookie,
                        ).json()
                    elif choice == "p":
                        if (pageNum - 1) < 0:
                            print("You are on the first page.")
                            continue
                        pageNum -= 1
                        searchRes = requests.get(
                            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}&perpage={number_of_search_results}&page={pageNum}",
                            cookies=cookie,
                        ).json()
                    else:
                        try:
                            choice = int(choice)
                            print(choice)
                            if (
                                choice
                                <= min(searchRes["total"], number_of_search_results)
                                and choice > 0
                            ):
                                # Enrol course
                                print("MAIN COURSE Course")
                                cid = searchRes["courses"][
                                    pageNum * number_of_search_results + (choice - 1)
                                ]["id"]
                                enrolRes = requests.get(
                                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={security_key}&courseid={cid}",
                                    cookies=cookie,
                                ).json()
                                if enrolRes["status"]:
                                    print(
                                        f"{bcolors.OKGREEN}Enrolled in course {searchRes['courses'][pageNum * number_of_search_results + (choice - 1)]['fullname']} successfully!{bcolors.ENDC}"
                                    )
                                    print()
                                else:
                                    print(
                                        f"{bcolors.FAIL}Course enrollment in {searchRes['courses'][pageNum * number_of_search_results + (choice - 1)]['fullname']} failed{bcolors.ENDC}"
                                    )
                                    print()
                                keepLoading = False
                            else:
                                print("Invalid choice")

                        except Exception as err:
                            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
