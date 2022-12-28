import os.path
from random import randint
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from utils import bcolors


class Erp2Gcal:
    # Function which takes care of auth
    def perform_google_auth():
        try:
            SCOPES = ["https://www.googleapis.com/auth/calendar"]
            creds = None
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                # If there are no (valid) credentials available, let the user log in.
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
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    # Function which creates the calendar events
    def create_gcal_events(courses, service):
        # variable where user's end date is stored
        until = input(
            f"{bcolors.OKCYAN}\nTill when the events should be added? (Enter date in YYYY/MM/DD format)[Excluded]{bcolors.ENDC}\n"
        )
        until = "".join(until.split("/")) + "T000000Z"

        try:
            print(f"{bcolors.OKGREEN}Creating events...\n{bcolors.ENDC}")
            for course in courses:
                event_body = {
                    "summary": course.name,  # Title
                    "description": f"{course.room}\nCreated using erp2gcal",  # Room
                    "start": {"dateTime": course.start, "timeZone": "Asia/Kolkata"},
                    "end": {
                        "dateTime": course.end,
                        "timeZone": "Asia/Kolkata",
                    },
                    # print colors to know the colorIds
                    # colors = service.colors().get().execute()
                    "colorId": randint(1, 11),
                    "recurrence": [
                        f"RRULE:FREQ=WEEKLY;UNTIL={until};BYDAY={','.join(course.day())}"
                    ],  # UNTIL= , BYDAY="SU" / "MO" / "TU" / "WE" / "TH" / "FR" / "SA"
                }

                response = (
                    service.events()
                    .insert(calendarId="primary", body=event_body)
                    .execute()
                )
                print(f"{bcolors.OKGREEN}Successfully created events!{bcolors.ENDC}")
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

    # clean the events created as a side effect
    def clean_unnecessary_events(service):
        try:
            # today in the format asked in docs :p
            today = dt.datetime(
                dt.datetime.now().year,
                dt.datetime.now().month,
                dt.datetime.now().day,
                tzinfo=dt.timezone.utc,
            ).isoformat()
            tomorrow = dt.datetime(
                dt.datetime.now().year,
                dt.datetime.now().month,
                dt.datetime.now().day + 1,
                tzinfo=dt.timezone.utc,
            ).isoformat()
            # Gets all events for scheduled on today
            events_list = (
                service.events()
                .list(
                    calendarId="primary",
                    singleEvents=True,
                    orderBy="startTime",
                    timeMin=today,
                    timeMax=tomorrow,
                )
                .execute()
            )
            events = events_list.get("items", [])
            # Make delete request
            for event in events:
                if (
                    "description" in event
                    and "Created using erp2gcal" in event["description"]
                ):

                    response = (
                        service.events()
                        .delete(calendarId="primary", eventId=event["id"])
                        .execute()
                    )

            print(f"{bcolors.OKGREEN}Removed unnecessary events!{bcolors.ENDC}")
        except Exception as err:
            print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")
