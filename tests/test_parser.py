import datetime as dt

from src.models.Course import Course
from src.utils import parse_string_to_courses

SCHEDULES = [
    [
        "ECON F212-L13",
        "LEC (2740)",
        "TuTh 6:00PM - 7:30PM",
        "Room  TBA",
        "EEE F241-L2",
        "LEC (2786)",
        "TuThSa 11:00AM - 11:50AM",
        "Room TBA",
        "EEE F241-P2",
        "LAB (2795)",
        "Mo 1:00PM - 2:50PM",
        "Room  TBA",
        "EEE F241-T3",
        "TUT (2806)",
        "Tu 3:00PM - 3:50PM",
        "Room  TBA",
        "EEE F242-L1",
        "LEC (2813)",
        "TuTh 4:00PM - 4:50PM",
        "Room  TBA",
        "Fr 5:00PM - 5:50PM",
        "Room  TBA",
        "EEE F242-T5",
        "TUT (2819)",
        "Th 8:00AM - 8:50AM",
        "Room  TBA",
        "EEE F243-L1",
        "LEC (2821)",
        "MoWeFr 10:00AM - 10:50AM",
        "Room  TBA",
        "EEE F243-T2",
        "TUT (2824)",
        "Sa 8:00AM - 8:50AM",
        "Room  TBA",
        "EEE F244-L1",
        "LEC (2829)",
        "MoWeFr 9:00AM - 9:50AM",
        "Room  TBA",
        "EEE F244-T3",
        "TUT (2832)",
        "Tu 8:00AM - 8:50AM",
        "Room  TBA",
        "EEE F246-P1",
        "LAB (3342)",
        "TuTh 1:00PM - 2:50PM",
        "Room  TBA",
        "HSS F338-L1",
        "LEC (3233)",
        "MoWeFr 11:00AM - 11:50AM",
        "Room  TBA",
        "MGTS F211-L1",
        "LEC (2711)",
        "MoWe 5:00PM - 5:50PM",
        "Room  TBA",
        "Th 5:00PM - 5:50PM",
        "Room  TBA",
        "MGTS F211-T1",
        "TUT (2712)",
        "Tu 5:00PM - 5:50PM",
        "Room  TBA",
        "CS F367-P1",
        "PRO (3352)",
        "Room  TBA",
        "EEE F243-L1",
        "LEC (2821)",
        "WeFr 10:00AM - 10:50AM",
        "Room  TBA",
        "Mo 10:00AM - 10:50AM",
        "Room  TBA",
    ],
    [
        "CS F376-P1",
        "PRO (3598)",
        "Room  TBA",
        "HSS F346-L1",
        "LEC (3566)",
        "TuThSa 11:00AM - 11:50AM",
        "Room  TBA",
    ],
]


def create_date_time_isoformat_from_hour(hour):
    TODAY = dt.datetime.now()
    return dt.datetime(TODAY.year, TODAY.month, TODAY.day, hour).isoformat()


# FIX: The expected array needs to be in order for the tests to work as expected
EXPECTED = [
    [
        Course("ECON F212-L13", "LEC", "TBA", "TuTh", "6:00PM"),
        Course("EEE F241-L2", "LEC", "TBA", "TuThSa", "11:00AM"),
        Course("EEE F241-P2", "LAB", "TBA", "Mo", "1:00PM"),
        Course("EEE F241-T3", "TUT", "TBA", "Tu", "3:00PM"),
        Course("EEE F242-L1", "LEC", "TBA", "TuTh", "4:00PM"),
        Course("EEE F242-T5", "TUT", "TBA", "Th", "8:00AM"),
        Course("EEE F243-L1", "LEC", "TBA", "MoWeFr", "10:00AM"),
        Course("EEE F243-T2", "TUT", "TBA", "Sa", "8:00AM"),
        Course("EEE F244-L1", "LEC", "TBA", "MoWeFr", "9:00AM"),
        Course("EEE F244-T3", "TUT", "TBA", "Tu", "8:00AM"),
        Course("EEE F246-P1", "LAB", "TBA", "TuTh", "1:00PM"),
        Course("HSS F338-L1", "LEC", "TBA", "MoWeFr", "11:00AM"),
        Course("MGTS F211-L1", "LEC", "TBA", "MoWe", "5:00PM"),
        Course("MGTS F211-T1", "TUT", "TBA", "Tu", "5:00PM"),
        Course("EEE F243-L1", "LEC", "TBA", "WeFr", "10:00AM"),
        Course("EEE F242-L1", "LEC", "TBA", "Fr", "5:00PM"),
        Course("MGTS F211-L1", "LEC", "TBA", "Th", "5:00PM"),
        Course("EEE F243-L1", "LEC", "TBA", "Mo", "10:00AM"),
    ],
    [
        Course("HSS F346-L1", "LEC", "TBA", "TuThSa", "11:00AM"),
    ],
]


class TestCourseParser:
    def test_course_parser(self):
        for id, schedule in enumerate(SCHEDULES):
            parsed_courses = parse_string_to_courses(schedule)

            assert len(parsed_courses) == len(EXPECTED[id])

            for idx, course in enumerate(parsed_courses):
                print(course.name, EXPECTED[id][idx].name)
                assert course == EXPECTED[id][idx]
