import httplib2
import json
import os
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from reminder import Reminder

APP_KEYS_FILE = 'app_keys.json'
USER_OAUTH_DATA_FILE = os.path.expanduser('~/.google-reminders-cli-oauth')


def authenticate() -> httplib2.Http:
    """
    returns an Http instance that already contains the user credentials and is
    ready to make requests to alter user data.

    On the first time, this function will open the browser so that the user can
    grant it access to his data
    """
    with open(APP_KEYS_FILE) as f:
        app_keys = json.load(f)
    storage = Storage(USER_OAUTH_DATA_FILE)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(
            OAuth2WebServerFlow(
                client_id=app_keys['APP_CLIENT_ID'],
                client_secret=app_keys['APP_CLIENT_SECRET'],
                scope=['https://www.googleapis.com/auth/reminders'],
                user_agent='google reminders cli tool'),
            storage,
        )
    auth_http = credentials.authorize(httplib2.Http())
    return auth_http


def create_req_body(reminder: Reminder) -> dict:
    """
    returns the body of a create-reminder request
    """
    body = {
        "2": {
            "1": 7
        },
        "3": {
            "2": reminder.id
        },
        "4": {
            "1": {
                "2": reminder.id
            },
            "3": reminder.title,
            "5": {
                "1": reminder.dt.year,
                "2": reminder.dt.month,
                "3": reminder.dt.day,
                "4": {
                    "1": reminder.dt.hour,
                    "2": reminder.dt.minute,
                    "3": reminder.dt.second,
                }
            },
            "8": 0
        }
    }
    return json.dumps(body)
