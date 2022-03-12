import datetime as dt


def fileParse(text):
    contents = []
    sentences_to_miss = [
        "This Week's Schedule",
        "    Class   Schedule",
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
        self.typ = typ
        self.days = days
        self.start = start
        self.room = room
        self.end = end

    def day(self):
        days = []
        # dayDict = {
        #     "Mo": "Monday",
        #     "Tu": "Tuesday",
        #     "We": "Wednesday",
        #     "Th": "Thursday",
        #     "Fr": "Friday",
        #     "Sa": "Saturday",
        # }

        for i in range(0, len(self.days), 2):
            # days.append(dayDict[self.days[i : i + 2]])
            days.append(self.days[i : i + 2].upper())
        return days


def coursesGen(courses_info):
    courses = []

    for i in range(0, len(courses_info), 4):
        start, end = timeGen(
            courses_info[i + 2].split()[1], courses_info[i + 1].split()[0]
        )
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
    filecont = fileParse("courses.txt")
    courses = coursesGen(filecont)
    return courses


main()
