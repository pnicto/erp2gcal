import datetime as dt
import os.path
from random import randint

from clint.textui import colored
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class GoogleCalendarActions:
    def __init__(self):
        self.service = self.__initialize_gcal_service()

    def __initialize_gcal_service(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    def create_calendar_events(self, registered_courses):
        print(colored.yellow("Till when the events should be created?"))
        print(
            colored.yellow(
                "Enter date in YYYY/MM/DD format [date excluded] eg:2023/01/05",
                bold=True,
            )
        )
        until_date = input()
        until_date = "".join(until_date.split("/")) + "T000000Z"

        print(colored.green("\nCreating events"))

        for course in registered_courses:
            event_body = {
                "summary": course.name,
                "description": f"{course.room}\nCreated using erp2gcal",
                "start": {"dateTime": course.start, "timeZone": "Asia/Kolkata"},
                "end": {
                    "dateTime": course.end,
                    "timeZone": "Asia/Kolkata",
                },
                "colorId": randint(1, 11),
                "recurrence": [
                    f"RRULE:FREQ=WEEKLY;UNTIL={until_date};BYDAY={','.join(course.day())}"
                ],
            }

            response = (
                self.service.events()
                .insert(calendarId="primary", body=event_body)
                .execute()
            )
            print(response)

        print(colored.green("Created"))

        self.delete_all_created_events(clean_up=True)

    def delete_all_created_events(self, clean_up=False):
        TODAY = dt.datetime.now()
        today_in_iso = dt.datetime(
            TODAY.year, TODAY.month, TODAY.day, tzinfo=dt.timezone.utc
        ).isoformat()

        if not clean_up:
            print(colored.yellow("Till when the events should be deleted?"))
            print(
                colored.yellow(
                    "Enter date in YYYY/MM/DD format [date excluded] eg:2023/01/05",
                    bold=True,
                )
            )
            until_date = input()
            year, month, day = map(int, until_date.split("/"))
            until_date_iso = dt.datetime(
                year, month, day, tzinfo=dt.timezone.utc
            ).isoformat()
        else:
            until_date_iso = dt.datetime(
                TODAY.year, TODAY.month, TODAY.day + 1, tzinfo=dt.timezone.utc
            ).isoformat()

        event_list = (
            self.service.events()
            .list(
                calendarId="primary",
                singleEvents=True,
                orderBy="startTime",
                timeMin=today_in_iso,
                timeMax=until_date_iso,
            )
            .execute()
        )

        events = event_list.get("items", [])
        for event in events:
            if (
                "description" in event
                and "Created using erp2gcal" in event["description"]
            ):
                response = (
                    self.service.events()
                    .delete(calendarId="primary", eventId=event["id"])
                    .execute()
                )
                print(response)

        print(colored.green("Cleared"))
