import requests

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.bcolors import bcolors


class CmsActions:
    # Function which goes to login page
    def perfrom_cms_login(driver):
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

            # Since firefox was having issue clicking that context menu this is a workaround for that
            driver.get("https://cms.bits-hyderabad.ac.in/user/preferences.php")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Edit profile"))
            )
            # Goes to the edit profile menu to get user id
            driver.find_element(By.LINK_TEXT, "Edit profile").click()
            user_id = driver.current_url.split("&")[0].split("=")[1]

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
    # Please do not try to understand :D
    def enrol_all_registered_courses(
        security_key,
        cookie,
        courses,
    ):
        try:
            print(f"Trying to enroll into {len(courses)} courses\n")
            for course in courses:
                print(f"Searching for {course.name} in courses...")
                course_search_term = " ".join(course.name.split("-"))

                # Normal course search
                cms_api_search_results = requests.get(
                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}",
                    cookies=cookie,
                ).json()

                if cms_api_search_results["total"] == 0:
                    print(
                        f"{bcolors.WARNING}No results found for '{course_search_term}'. Press enter to continue{bcolors.ENDC}"
                    )
                    input()
                    continue

                while True:
                    for idx in range(cms_api_search_results["total"]):
                        print(
                            f"{idx + 1}. {cms_api_search_results['courses'][idx]['fullname']}"
                        )
                        print(
                            f"\tCategory: {cms_api_search_results['courses'][idx]['categoryname']}"
                        )
                        print(
                            f"\tInstructors: {', '.join([x['fullname'] for x in cms_api_search_results['courses'][idx]['contacts']])}"
                        )
                        print()

                    print(
                        bcolors.WARNING
                        + "Enter one of the above numbers to enrol into the corresponding course.\nType in 'n' and 'p' to navigate to the next and previous pages respectively.\nTo skip this course, type in 's'\n"
                        + bcolors.ENDC
                    )

                    user_choice = input()

                    if user_choice == "s":
                        break
                    else:
                        try:
                            user_choice = int(user_choice)
                            if (
                                user_choice <= cms_api_search_results["total"]
                                and user_choice > 0
                            ):
                                # Enrol course
                                course_id = cms_api_search_results["courses"][
                                    (user_choice - 1)
                                ]["id"]
                                enrol_result = requests.get(
                                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={security_key}&courseid={course_id}",
                                    cookies=cookie,
                                ).json()
                                if enrol_result["status"]:
                                    print(
                                        f"{bcolors.OKGREEN}Enrolled in course {cms_api_search_results['courses'][(user_choice - 1)]['fullname']} successfully!{bcolors.ENDC}"
                                    )
                                    print()
                                else:
                                    print(
                                        f"{bcolors.FAIL}Course enrollment in {cms_api_search_results['courses'][(user_choice - 1)]['fullname']} failed{bcolors.ENDC}"
                                    )
                                    print()
                                break
                            else:
                                print("Invalid choice")

                        except Exception as err:
                            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    def enrol_into_main_sections(
        security_key,
        cookie,
        courses,
    ):
        try:
            print(f"{bcolors.HEADER}Enrolling into L/P sections\n{bcolors.ENDC}")
            for course in courses:
                course_search_term = " ".join(course.name.split("-"))[:-1]
                if (
                    course_search_term.endswith("P") or course_search_term.endswith("L")
                ) and (course_search_term != "ME F111 P"):
                    print(f"\nSearching for {course_search_term}")

                    cms_api_search_results = requests.get(
                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={security_key}&criterianame=search&criteriavalue={course_search_term}",
                        cookies=cookie,
                    ).json()

                    if cms_api_search_results["total"] == 0:
                        print(
                            f"{bcolors.WARNING}No results found for '{course_search_term}'. Press enter to continue{bcolors.ENDC}"
                        )
                        input()
                        continue

                    while True:
                        for idx in range(cms_api_search_results["total"]):
                            print(
                                f"{idx + 1}. {cms_api_search_results['courses'][idx]['fullname']}"
                            )
                            print(
                                f"\tCategory: {cms_api_search_results['courses'][idx]['categoryname']}"
                            )
                            print(
                                f"\tInstructors: {', '.join([x['fullname'] for x in cms_api_search_results['courses'][idx]['contacts']])}"
                            )
                            print()
                        print(
                            bcolors.WARNING
                            + "Enter one of the above numbers to enrol into the corresponding course.\nType in 'n' and 'p' to navigate to the next and previous pages respectively.\nTo skip this course, type in 's'\n"
                            + bcolors.ENDC
                        )
                        user_choice = input()
                        if user_choice == "s":
                            break
                        else:
                            try:
                                user_choice = int(user_choice)
                                if (
                                    user_choice <= cms_api_search_results["total"]
                                    and user_choice > 0
                                ):
                                    # Enrol course
                                    course_id = cms_api_search_results["courses"][
                                        (user_choice - 1)
                                    ]["id"]
                                    enrolRes = requests.get(
                                        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={security_key}&courseid={course_id}",
                                        cookies=cookie,
                                    ).json()
                                    if enrolRes["status"]:
                                        print(
                                            f"{bcolors.OKGREEN}Enrolled in course {cms_api_search_results['courses'][ (user_choice - 1)]['fullname']} successfully!{bcolors.ENDC}"
                                        )
                                        print()
                                    else:
                                        print(
                                            f"{bcolors.FAIL}Course enrollment in {cms_api_search_results['courses'][ (user_choice - 1)]['fullname']} failed{bcolors.ENDC}"
                                        )
                                        print()
                                    break
                                else:
                                    print("Invalid choice")

                            except Exception as err:
                                print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
