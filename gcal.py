from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
import Erp2gcal
from datetime import datetime as dt
from datetime import timedelta as td


def auth():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


service = auth()
courses = Erp2gcal.main()
colors = service.colors().get().execute()
# val = service.calendarList().get(calendarId='primary').execute()

# print(val['summary'])


event_body = {
    'summary': courses[1].name,  # Title
    'description': courses[0].room,  # Room
    'start': {
        'dateTime': dt(2022, 3, 9, 16).isoformat(),
        'timeZone': 'Asia/Kolkata'
    },
    'end': {
        'dateTime': (dt(2022, 3, 9, 16)+td(hours=1)).isoformat(),
        'timeZone': 'Asia/Kolkata'
    },
    'colorId': 5,
    # 'recurrence': []
}

# event = {
#     'summary': 'Google I/O 2015',
#     'location': '800 Howard St., San Francisco, CA 94103',
#     'description': 'A chance to hear more about Google\'s developer products.',
#     'start': {
#         'dateTime': '2015-05-28T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'end': {
#         'dateTime': '2015-05-28T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#     ],
#     'attendees': [
#         {'email': 'lpage@example.com'},
#         {'email': 'sbrin@example.com'},
#     ],
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#             {'method': 'email', 'minutes': 24 * 60},
#             {'method': 'popup', 'minutes': 10},
#         ],
#     },
# }

response = service.events().insert(calendarId='primary', body=event_body).execute()
print(response)
