import datetime as dt

import pytest

from models.Course import Course


def create_date_time_isoformat_from_hour(hour):
    TODAY = dt.datetime.now()
    return dt.datetime(TODAY.year, TODAY.month, TODAY.day, hour).isoformat()


class TestCourse:
    @pytest.mark.parametrize(
        "days,expected",
        [
            ("MoWeFr", ["MO", "WE", "FR"]),
            ("TuThSa", ["TU", "TH", "SA"]),
        ],
    )
    def test_parse_days(self, days, expected):
        course = Course("", "LEC", "", days, "2:00PM")
        assert course.days == expected

    def test_raise_error_when_day_is_missing(self):
        with pytest.raises(ValueError):
            Course("", "LEC", "", "", "2:00PM")

    @pytest.mark.parametrize(
        "time,expected",
        [
            ("12:00AM", create_date_time_isoformat_from_hour(0)),
            ("6:00AM", create_date_time_isoformat_from_hour(6)),
            ("12:00PM", create_date_time_isoformat_from_hour(12)),
            ("6:00PM", create_date_time_isoformat_from_hour(18)),
            ("6:30PM", create_date_time_isoformat_from_hour(18)),
        ],
    )
    def test_parse_start_timings(self, time, expected):
        course = Course("", "LEC", "", "MoWeFr", time)
        assert course.start == expected

    @pytest.mark.parametrize(
        "component,expected",
        [
            ("LAB", create_date_time_isoformat_from_hour(19)),
            ("LEC", create_date_time_isoformat_from_hour(18)),
            ("TUT", create_date_time_isoformat_from_hour(18)),
        ],
    )
    def test_parse_end_timings(self, component, expected):
        course = Course("", component, "", "MoWeFr", "5:00PM")
        assert course.end == expected

    def test_raise_error_when_time_is_missing(self):
        with pytest.raises(ValueError):
            Course("", "LEC", "", "MoWeFr", "")
