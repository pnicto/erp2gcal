from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
import courseParse
from random import randint
from datetime import datetime as dt
from datetime import timedelta as td


def auth():
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


service = auth()
courses = courseParse.main()
# colors = service.colors().get().execute()


for course in courses:
    event_body = {
        "summary": course.name,  # Title
        "description": course.room,  # Room
        "start": {"dateTime": course.start, "timeZone": "Asia/Kolkata"},
        "end": {
            "dateTime": course.end,
            "timeZone": "Asia/Kolkata",
        },
        "colorId": randint(1, 11),
        "recurrence": [
            f"RRULE:FREQ=WEEKLY;UNTIL=20220328T000000Z;BYDAY={','.join(course.day())}"
        ],  # UNTIL= , BYDAY="SU" / "MO" / "TU" / "WE" / "TH" / "FR" / "SA"
    }

    response = service.events().insert(calendarId="primary", body=event_body).execute()
    print(response)
