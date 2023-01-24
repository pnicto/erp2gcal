import datetime as dt

from models.Course import Course
from utils import parse_string_to_courses

SCHEDULE = "This Week's Schedule\n  Class Schedule\nECON F212-L1\nLEC (2740)\nTuTh 6:00PM - 7:30PM\nRoom  TBA\nEEE F241-L2\nLEC (2786)\nTuThSa 11:00AM - 11:50AM\nRoom  TBA\nEEE F241-P2\nLAB (2795)\nMo 1:00PM - 2:50PM\nRoom  TBA\nEEE F241-T3\nTUT (2806)\nTu 3:00PM - 3:50PM\nRoom  TBA\nEEE F242-L1\nLEC (2813)\nTuTh 4:00PM - 4:50PM\nRoom  TBA\nFr 5:00PM - 5:50PM\nRoom  TBA\nEEE F242-T5\nTUT (2819)\nTh 8:00AM - 8:50AM\nRoom  TBA\nEEE F243-L1\nLEC (2821)\nMoWeFr 10:00AM - 10:50AM\nRoom  TBA\nEEE F243-T2\nTUT (2824)\nSa 8:00AM - 8:50AM\nRoom  TBA\nEEE F244-L1\nLEC (2829)\nMoWeFr 9:00AM - 9:50AM\nRoom  TBA\nEEE F244-T3\nTUT (2832)\nTu 8:00AM - 8:50AM\nRoom  TBA\nEEE F246-P1\nLAB (3342)\nTuTh 1:00PM - 2:50PM\nRoom  TBA\nHSS F338-L1\nLEC (3233)\nMoWeFr 11:00AM - 11:50AM\nRoom  TBA\nMGTS F211-L1\nLEC (2711)\nMoWe 5:00PM - 5:50PM\nRoom  TBA\nTh 5:00PM - 5:50PM\nRoom  TBA\nMGTS F211-T1\nTUT (2712)\nTu 5:00PM - 5:50PM\nRoom  TBA"


def create_date_time_isoformat_from_hour(hour):
    TODAY = dt.datetime.now()
    return dt.datetime(TODAY.year, TODAY.month, TODAY.day, hour).isoformat()


EXPECTED = [
    Course("ECON F212-L1", "LEC", "TBA", "TuTh", "6:00PM"),
    Course("EEE F241-L2", "LEC", "TBA", "TuThSa", "11:00AM"),
    Course("EEE F241-P2", "LAB", "TBA", "Mo", "1:00PM"),
    Course("EEE F241-T3", "TUT", "TBA", "Tu", "3:00PM"),
    Course("EEE F242-L1", "LEC", "TBA", "TuTh", "4:00PM"),
    Course("EEE F242-L1", "LEC", "TBA", "Fr", "5:00PM"),
    Course("EEE F242-T5", "TUT", "TBA", "Th", "8:00AM"),
    Course("EEE F243-L1", "LEC", "TBA", "MoWeFr", "10:00AM"),
    Course("EEE F243-T2", "TUT", "TBA", "Sa", "8:00AM"),
    Course("EEE F244-L1", "LEC", "TBA", "MoWeFr", "9:00AM"),
    Course("EEE F244-T3", "TUT", "TBA", "Tu", "8:00AM"),
    Course("EEE F246-P1", "LAB", "TBA", "TuTh", "1:00PM"),
    Course("HSS F338-L1", "LEC", "TBA", "MoWeFr", "11:00AM"),
    Course("MGTS F211-L1", "LEC", "TBA", "MoWe", "5:00PM"),
    Course("MGTS F211-L1", "LEC", "TBA", "Th", "5:00PM"),
    Course("MGTS F211-T1", "TUT", "TBA", "Tu", "5:00PM"),
]


class TestCourseParser:
    def test_course_parser(self):
        parsed_courses = parse_string_to_courses(SCHEDULE)
        for idx, course in enumerate(parsed_courses):
            assert course == EXPECTED[idx]
