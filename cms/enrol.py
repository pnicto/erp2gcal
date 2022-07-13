from math import ceil

import requests


def enrollment(securityKey,cookie,courses,secondSemCode= 27):
    numChoices = 5
    print(f"Trying to enroll into {len(courses)} courses")
    for course in courses:
        print(f"Searching for {course.name} in courses...")
        searchRes = requests.get(
            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={securityKey}&criterianame=search&criteriavalue={course.name}&perpage={numChoices}&page=0", cookies=cookie).json()
        totalPages = ceil(searchRes['total'] / numChoices)
        if totalPages == 0:
            print(f"No results found for '{course.name}'. Press enter to continue")
            input()
            continue
        keepLoading = True
        pageNum = 0
        while keepLoading:
            print(f"[Page {pageNum + 1} of {totalPages}]")
            for resNum in range(min(searchRes['total'], numChoices)):
                if secondSemCode > 0:
                    if searchRes['courses'][resNum]['categoryid'] != secondSemCode:
                        continue
                print(f"{resNum + 1}. {searchRes['courses'][resNum]['fullname']}")
                print(
                    f"\tCategory: {searchRes['courses'][resNum]['categoryname']}")
                print(
                    f"\tIntructors: {', '.join([x['fullname'] for x in searchRes['courses'][resNum]['contacts']])}")
                print()
            print("""
    Enter one of the above numbers to enrol into the corresponding course.
    Type in 'n' and 'p' to navigate to the next and previous pages respectively.
    To skip this course, type in 's'
                """)
            choice = input()
            if choice == "s":
                keepLoading = False
            elif choice == "n":
                if (pageNum + 1) >= totalPages:
                    print("You are on the last page.")
                    continue
                pageNum += 1
                searchRes = requests.get(
                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={securityKey}&criterianame=search&criteriavalue={course.name}&perpage={numChoices}&page={pageNum}", cookies=cookie).json()
            elif choice == "p":
                if (pageNum - 1) < 0:
                    print("You are on the first page.")
                    continue
                pageNum -= 1
                searchRes = requests.get(
                    f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=core_course_search_courses&moodlewsrestformat=json&wstoken={securityKey}&criterianame=search&criteriavalue={course.name}&perpage={numChoices}&page={pageNum}", cookies=cookie).json()
            else:
                try:
                    choice = int(choice)
                    if choice <= min(searchRes['total'], numChoices) and choice > 0:
                        # Enrol course
                        cid = searchRes['courses'][resNum]['id']
                        enrolRes = requests.get(
                            f"https://cms.bits-hyderabad.ac.in/webservice/rest/server.php?wsfunction=enrol_self_enrol_user&moodlewsrestformat=json&wstoken={securityKey}&courseid={cid}", cookies=cookie).json()
                        if enrolRes['status']:
                            print(
                                f"Enrolled in course {searchRes['courses'][resNum]['fullname']} successfully!"  )
                            print()
                        else:
                            print(
                                f"Course enrollment in {searchRes['courses'][resNum]['fullname']} failed"  )
                            print()
                        keepLoading = False
                    else:
                        print("Invalid choice")
                except Exception as err:
                    print("Invalid choice")

