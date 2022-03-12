# erp2gcal

Script to help add classes in google calendar from erp.

## Usage

1. [Download](https://github.com/pnicto/erp2gcal/archive/refs/heads/master.zip) the repo.
2. [Visit](https://console.cloud.google.com/) in the side bar choose APIs & Services -> Library Search for google calendar and enable it
3. Now go to APIs & Services -> Credentials, Create a project and then Create Credentials -> Oauth client ID -> Desktop app as application type after creating download it as json.
4. Rename the downloaded file as `Credentials.json` and place it along with the downloaded files from step 1.
5. Run
   ```
   pip install requirements.txt
   ```
6. Go to ERP -> Student Center and copy the text as shown. ![](https://media.discordapp.net/attachments/786594878418583562/952232294544986172/unknown.png)
7. Paste it in `courses.txt` file.
8. ```py
    python erp2gcal.py
   ```
# Known Issues

The day you run the script the calendar will be filled with all classes.

# Troubleshooting

Common problem might be the `Class schedule` line in `courses.txt` you can fix that by changing line 6 in `courseParse.py`