import datetime as dt

# Do not try to understand :D

# Course class
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

# Function which takes the list format courses and creates "Course" class instance for them
def coursesGen(erp_registered_courses):
    courses = []
    for i in range(0, len(erp_registered_courses), 4):
        # Assign starting and ending time of a course to start,end in RFC3399 format using timeGen function
        start, end = timeGen(
            erp_registered_courses[i + 2].split()[1], erp_registered_courses[i + 1].split()[0]
        )
        # Course (name,typ,room,days,start,end)
        courses.append(
            Course(
                erp_registered_courses[i],
                erp_registered_courses[i + 1].split()[0],
                erp_registered_courses[i + 3].split()[1],
                erp_registered_courses[i + 2].split()[0],
                start,
                end,
            )
        )
    return courses

# Function which creates corresponsing time intervals depending on the type of course
# TODO: Workshop Lab is 3hrs but this still takes it as 2 hours
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

