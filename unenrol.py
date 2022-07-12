import requests


def unenrol(securityKey, userId, sessionKey, cookie):
    enrolledCourses = requests.get(
        f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_users_courses&moodlewsrestformat=json&wstoken={securityKey}&userid={userId}"
    ).json()

    print(f"Enrolling from {len(enrolledCourses)} courses\n")

    for course in enrolledCourses:
        print(f"Unenrolling from {course['shortname']}...")
        enrolInstance = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_enrol_get_course_enrolment_methods&moodlewsrestformat=json&wstoken={securityKey}&courseid={course['id']}").json()

        enrolId = enrolInstance[0]['id']

        res = requests.get(
            f"https://cms.bits-hyderabad.ac.in/enrol/self/unenrolself.php?confirm=1&enrolid={enrolId}&sesskey={sessionKey}", cookies=cookie)

    print("Done unenrolling!\n")
