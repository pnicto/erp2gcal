import os.path
from random import randint
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function which takes care of auth
# Directly taken from the docs
def google_auth():
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
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return build("calendar", "v3", credentials=creds)
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

# Function which creates the calendar events
def create_gcal_events(courses,service):
    # variable where user's end date is stored
    until = input(
        "\nTill when the events should be added? (Enter date in YYYY/MM/DD format)\n"
    )
    until = "".join(until.split("/")) + "T000000Z"

    try:
        for course in courses:
            event_body = {
                "summary": course.name,  # Title
                "description":f"{course.room}\nCreated using erp2gcal",  # Room
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
                service.events().insert(calendarId="primary", body=event_body).execute()
            )
            # print(response)
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")

# Function for known issue #1
# clean the events created as a side effect
def clean_the_unnecessary_events(service):
    # today in the format asked in docs :p
    try:
        today = dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day,tzinfo=dt.timezone.utc).isoformat()
        # Gets all events for scheduled on today
        events_list = service.events().list(calendarId='primary',singleEvents=True,orderBy='startTime',timeMin= today).execute()
        events = events_list.get('items', [])
        # Filter events with description "Created using erp2gcal"
        events_to_remove = filter(lambda x: x['description'] == 'Created using erp2gcal',events)
        # Make delete request
        for event in events_to_remove:
            response = (
                    service.events().delete(calendarId="primary", eventId = event['id']).execute()
                )
            print(response)
    except Exception as err:
        print(f"{bcolors.FAIL}{err}{bcolors.ENDC}")