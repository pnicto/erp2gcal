# erp2gcal

## Features

* Enroll/unenroll batch from cms.
* Create google calendar events with ease.

## Usage

1. [Download](https://github.com/pnicto/erp2gcal/archive/refs/heads/master.zip) the repo.
2. [Visit](https://developers.google.com/calendar/api/quickstart/python) and follow the prerequisites or read more below.
   <details>
   <summary>Click to read more</summary>

   1. <a href="https://console.cloud.google.com/">Visit</a> in the side bar choose APIs & Services -> Library Search for google calendar and enable it.
   2. Now go to APIs & Services -> Credentials, Create a project and then Create Credentials -> Oauth client ID -> Desktop app as application type after creating download it as json.
   </details>
3. Rename the downloaded file as `credentials.json` and place it along with the downloaded files from step 1.
4. In the directory, run the following commands.
   ```
   pip install -r requirements.txt
   ```
   ```py
    python main.py
    ```
5. Choose the options shown on terminal and login when propmpted.

## Troubleshooting

1. Problem: `Authorization Error Error 403: Access_denied`<br/>
   Solution: [Visit](https://console.cloud.google.com/), goto APIs & Services -> OAuth consent screen, select the app you created in step 3 of `Usage` and add your email under `Test Users`.
2. Problem: `Unauthenticated`<br/>Solution: Delete the token.json and rerun the script with `Create calendar events`.
