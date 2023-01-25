import requests
from clint.textui import colored


class CmsActions:
    def __init__(self, cms_driver):
        (
            self.session_key,
            self.security_key,
            self.user_id,
            self.cookie,
        ) = cms_driver.get_required_parameters_for_cms_api()

    def unenrol_from_all_courses(self):
        enrolled_courses = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&wstoken={self.security_key}&userid={self.user_id}"
        ).json()

        print(
            colored.yellow(
                f"Unenroling from {len(enrolled_courses)} courses\n", bold=True
            )
        )

        for course in enrolled_courses:
            print(f"Unenrolling from {course['shortname']}...")
            enrol_instance = requests.get(
                f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_course_enrolment_methods&moodlewsrestformat=json&wstoken={self.security_key}&courseid={course['id']}"
            ).json()
            course_id = enrol_instance[0]["id"]
            requests.get(
                f"https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?confirm=1&enrolid={course_id}&sesskey={self.session_key}",
                cookies=self.cookie,
            )
            print(colored.green("Ok\n"))

    def __get_enrolment_choice(self, search_term):
        search_result = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={self.security_key}&criterianame=search&criteriavalue={search_term}",
            cookies=self.cookie,
        ).json()
        total_search_results = search_result["total"]
        for num in range(total_search_results):
            print(f"{num + 1}. {search_result['courses'][num]['fullname']}")
            print(f"\tCategory: {search_result['courses'][num]['categoryname']}")
            print(
                f"\tInstructors: {', '.join([x['fullname'] for x in search_result['courses'][num]['contacts']])}"
            )
            print()

        print(
            colored.yellow(
                "Enter a number to enrol into that course or press 's' to skip"
            )
        )

        choice = input("> ")

        return (choice, search_result)

    def __enrol_into_course(self, choice, search_result):
        if choice < 0 or choice > search_result["total"]:
            raise ValueError("Enter a valid course number")

        course = search_result["courses"][choice - 1]
        enrol_response = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={self.security_key}&courseid={course['id']}",
            cookies=self.cookie,
        ).json()

        if enrol_response["status"]:
            print(
                colored.green(
                    f"Enrolment in course {course['fullname']} is successful\n"
                )
            )
        else:
            print(colored.red(f"Enrolment in course {course['fullname']} failed\n"))

    def enrol_into_registered_courses(self, registered_courses):
        print(
            colored.green(
                f"Trying to enrol into {len(registered_courses)} courses", bold=True
            )
        )

        for course in registered_courses:
            print(colored.cyan(f"\nSearching for {course.name} in courses"))

            search_term = " ".join(course.name.split("-"))

            (choice, search_result) = self.__get_enrolment_choice(search_term)

            if choice == "s":
                continue
            else:
                self.__enrol_into_course(int(choice), search_result)

            search_term = " ".join(course.name.split("-"))[:-1]
            if search_term.endswith("P") or search_term.endswith("L"):
                print(colored.yellow("Trying to enrol into respective L/P section"))

                (choice, search_result) = self.__get_enrolment_choice(search_term)

                if choice == "s":
                    continue
                else:
                    self.__enrol_into_course(int(choice), search_result)
