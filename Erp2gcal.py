def fileParse(text):
    contents = []
    sentences_to_miss = ["This Week's Schedule",
                         "    Class   Schedule", "Academic Calendar Deadlines", '']
    with open(text, 'r') as f:
        for item in f.read().split('\n'):
            if item not in sentences_to_miss:
                contents.append(item)
    return contents


class Course:
    def __init__(self, name, typ, room, days=[], start=None, end=None, ):
        self.name = name
        self.typ = typ
        self.days = days
        self.start = start
        self.end = end
        self.room = room


def dayParse(self):
    pass

# BITS F112-L1
# LEC (1838)
# MoWe 11:00AM - 11:50AM
# Room  TBA

# if i % 4 == 0:  # Course Name
#             # dayTime.append(content[i].split()[0])
#             # print(content[i])
#             pass
#         elif i % 4 == 1:  # Type
#             # print(content[i])
#             pass
#         elif i % 4 == 2:  # Day and Time
#             # print(content[i])
#             pass
#         elif i % 4 == 3:  # Room
#             # print(content[i])
#             pass
#         i += 4


def coursesGen(courses_info):
    courses = []
    for i in range(0, len(courses_info), 4):

        courses.append(Course(
            courses_info[i], courses_info[i+1].split()[0], courses_info[i+3].split()[1]))

    return courses


def main():
    filecont = fileParse('text.txt')
    courses = coursesGen(filecont)

    for i in range(0, len(courses)):
        print(courses[i].typ)


main()
