import datetime as dt
import logging
import os.path
from random import randint

from clint.textui import colored, progress
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarActions:
    def __init__(self):
        self.service = self.__initialize_gcal_service()

    def __initialize_gcal_service(self):
        creds = None

        try:
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
        except Exception as err:
            print(colored.red(err))
            print(colored.red("Failed to initialize gcal service"))

            logging.info(type(err))
            logging.info("Failed to initialize gcal service")
            exit(1)

    def create_calendar_events(self, registered_courses):
        print(colored.yellow("Till when the events should be created?"))
        print(
            colored.yellow(
                "Enter date in YYYY/MM/DD format [date excluded] eg:2023/01/05",
                bold=True,
            )
        )

        until_date = input()
        logging.info(f"Attempting to create calendar events till {until_date}")
        until_date = "".join(until_date.split("/")) + "T000000Z"

        print(colored.green("\nCreating events"))

        for course in registered_courses:
            event_body = {
                "summary": course.name,
                "description": "Created using erp2gcal",
                "start": {"dateTime": course.start, "timeZone": "Asia/Kolkata"},
                "end": {
                    "dateTime": course.end,
                    "timeZone": "Asia/Kolkata",
                },
                "colorId": randint(1, 11),
                "recurrence": [
                    f"RRULE:FREQ=WEEKLY;UNTIL={until_date};BYDAY={','.join(course.days)}"
                ],
            }
            logging.info(f"Creating event for {course.name}")

            response = (
                self.service.events()
                .insert(calendarId="primary", body=event_body)
                .execute()
            )
            logging.info(f"Response for {course.name}")
            logging.info(response)

            if response["id"]:
                print(colored.green(f"Created event for {course.name}"))

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

        with progress.Bar(label="Clearing", expected_size=len(events)) as bar:
            for idx, event in enumerate(events):
                if (
                    "description" in event
                    and "Created using erp2gcal" in event["description"]
                ):
                    self.service.events().delete(
                        calendarId="primary", eventId=event["id"]
                    ).execute()

                    bar.show(idx + 1)

        print(colored.green("Cleared"))
