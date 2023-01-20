class Course:
    def __init__(self, name, component, room, days, start):
        self.name = name
        self.component = component
        self.room = room
        self.days = self.__parse_days(days)
        self.start = start

    def __parse_days(self, days_str):
        days = [days_str[i : i + 2].upper() for i in range(0, len(days_str), 2)]
        return days
