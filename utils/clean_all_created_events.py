import os.path
from typing import List
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CleanService:
    def __init__(self):
        self.__SCOPES: List[str] = ["https://www.googleapis.com/auth/calendar"]

    def perform_auth(self):
        creds = None
        if os.path.exists(("token.json")):
            creds = Credentials.from_authorized_user_file("token.json", self.__SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.__SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        self.__SERVICE = build("calendar", "v3", credentials=creds)

    def get_events(self):
        today = dt.datetime(
            dt.datetime.now().year,
            dt.datetime.now().month,
            dt.datetime.now().day,
            tzinfo=dt.timezone.utc,
        ).isoformat()

        events_list = (
            self.__SERVICE.events()
            .list(
                calendarId="primary",
                singleEvents=True,
                orderBy="startTime",
                timeMin=today,
            )
            .execute()
        )
        events = events_list.get("items", [])
        return events

    def remove_events(self):
        self.perform_auth()
        events = self.get_events()
        for event in events:
            if ("description" in event) and (
                "Created using erp2gcal" in event["description"]
            ):
                response = (
                    self.__SERVICE.events()
                    .delete(calendarId="primary", eventId=event["id"])
                    .execute()
                )


auth: CleanService = CleanService()

auth.remove_events()
