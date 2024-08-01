# Erp2gcal

## Features

- ~~Enroll/unenroll batch from cms.~~ **Disabled currently as CMS is not functioning.**
- Create google calendar events for the registered courses with ease.

## Usage

1. [Download](https://github.com/pnicto/erp2gcal/archive/refs/heads/master.zip) the repo.
2. [Visit](https://developers.google.com/calendar/api/quickstart/python#prerequisites) and follow the prerequisites.
   <details>
   <summary>Click to read more</summary>

   1. <a href="https://developers.google.com/calendar/api/quickstart/python#enable_the_api/">Click here</a> and enable the API.
   2. Now go to APIs & Services -> Credentials, Create a project and then Create Credentials -> Oauth client ID -> Desktop app as application type (Make sure you add your BITS email to test users) after creating download it as json.
   </details>

3. Have `python` installed.
4. Rename the downloaded file as `credentials.json` and place it along with the downloaded files from step 1.
5. If you have already have `poetry` you can skip this step. Else follow along.

   Linux

   ```bash
   python -m venv .venv
   source .venv/bin/activate # Activate the virtual environment
   pip install poetry # Install poetry
   ```

6. Install the dependencies and run the script.

   ```bash
   poetry install
   python main.py -h # To show the help
   ```

### Examples

```
Arguments:
  actions      Actions to perform. Refer below for the acceptable values eg: ac (default: abc)

a : Unenrol from all courses
b : Enrol into registered courses on cms
c : Create gcal events
d : Delete created gcal events

  browser      Headless browser of your choice (choose an installed one) (default: firefox)

Acceptable browser params are 'edge', 'firefox', 'chrome'

Options:
  --binary-location=STR   Path to browser's binary

Other actions:
  -h, --help   Show the help
```

```bash
python main.py abc firefox # Refer above for what 'abc' mean
python main.py bc chrome
python main.py --binary-location=/usr/bin/microsoft-edge-dev abc edge
```
