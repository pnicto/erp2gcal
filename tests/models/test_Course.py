from models.Course import Course
import pytest


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
