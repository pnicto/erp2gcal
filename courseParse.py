import datetime as dt
from pprint import pprint


def fileParse(text):
    contents = []
    sentences_to_miss = [
        "This Week's Schedule",
        "    Class   Schedule",
        " \tClass\tSchedule",
        "Academic Calendar Deadlines",
        "",
    ]
    with open(text, "r") as f:
        for item in f.read().split("\n"):
            if item not in sentences_to_miss:
                contents.append(item)
    return contents


class Course:
    def __init__(self, name, typ, room, days, start, end):
        self.name = name
        self.typ = typ  # LAB,LEC,TUT
        self.days = days
        self.start = start
        self.room = room
        self.end = end

    def day(self):
        # Function to return days when the course happens in a week in capital letters.
        days = []
        for i in range(0, len(self.days), 2):
            days.append(self.days[i : i + 2].upper())
        return days


def coursesGen(courses_info):
    courses = []
    for i in range(0, len(courses_info), 4):
        # Assign starting and ending time of a course to start,end in RFC3399 format using timeGen function
        start, end = timeGen(
            courses_info[i + 2].split()[1], courses_info[i + 1].split()[0]
        )
        # Course (name,typ,room,days,start,end)
        courses.append(
            Course(
                courses_info[i],
                courses_info[i + 1].split()[0],
                courses_info[i + 3].split()[1],
                courses_info[i + 2].split()[0],
                start,
                end,
            )
        )
    return courses


def timeGen(inpt, typ):
    hour = int(float(inpt.split(":")[0]))  # ['2', '00PM']
    meridian = inpt.split(":")[1][2:]  #'00PM' -> PM
    # Dict with time deltas accordingly
    tdelta = {
        "TUT": dt.timedelta(hours=1),
        "LAB": dt.timedelta(hours=2),
        "TUT": dt.timedelta(hours=1),
        "LEC": dt.timedelta(hours=1),
    }
    if "PM" in meridian and hour < 12:
        hour += 12
    start = dt.datetime(
        dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day, hour
    ).isoformat()

    end = (
        dt.datetime(
            dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day, hour
        )
        + tdelta[typ]
    ).isoformat()
    return start, end


def main():
    try:
        filecont = fileParse("courses.txt")
        courses = coursesGen(filecont)
        return courses
    except ValueError:
        pprint(filecont)
        print(
            "\nLook for items like ' Class \\tSchedule' or similar and add them in line 7 of courseParse.py"
        )


main()
