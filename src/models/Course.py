import datetime as dt

COMPONENT_DURATION_TIMEDELTAS = {
    "LAB": dt.timedelta(hours=2),
    "LEC": dt.timedelta(hours=1),
    "TUT": dt.timedelta(hours=1),
}


class Course:
    def __init__(self, name, component, room, days, start):
        self.name = name
        self.component = component
        self.room = room
        self.days = self.__parse_days(days)
        self.start, self.end = self.__generate_start_and_end_timings_isoformat(start)

    def __parse_days(self, days_str):
        if not days_str:
            raise ValueError("days_str cannot be empty")

        days = [days_str[i : i + 2].upper() for i in range(0, len(days_str), 2)]

        return days

    def __generate_start_and_end_timings_isoformat(self, start_str):
        if len(start_str) == 0:
            raise ValueError("Start timing cannot be empty")

        hour = self.__get_hour_from_string(start_str)
        today = dt.datetime.now()

        start = dt.datetime(today.year, today.month, today.day, hour)
        end = (
            dt.datetime(today.year, today.month, today.day, hour)
            + COMPONENT_DURATION_TIMEDELTAS[self.component]
        )

        return start.isoformat(), end.isoformat()

    def __get_hour_from_string(self, str):
        split_str = str.split(":")

        hour = int(split_str[0])
        meridian = split_str[1][2:]

        if "PM" in meridian and hour < 12:
            hour += 12

        if "AM" in meridian and hour == 12:
            hour = 0

        return hour
