import argparse
import json
import os
import time
from typing import Tuple

import dateparser
import httplib2
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

APP_KEYS_FILE = 'app_keys.json'
USER_OAUTH_DATA_FILE = os.path.expanduser('~/.google-reminders-cli-oauth')

HTTP_OK = 200
WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}


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


def build_request_params(
    title: str, year: int, month: int, day: int, hour: int, minute: int,
) -> Tuple[dict, dict]:
    """
    get the headers and data needed for the request

    :return: (headers, data)
    """
    second = 00  # we always use 0 seconds
    headers = {
        'content-type': 'application/json+protobuf',
    }

    id = time.time()  # the reminder id is the unix time at which it was created
    reminder_id = f'cli-reminder-{id}'

    # The structure of the dictionary was extracted from a browser request to
    # create a new reminder. I didn't find any official documentation
    # for the request parameters.
    data = {
        "2": {
            "1": 7
        },
        "3": {
            "2": reminder_id
        },
        "4": {
            "1": {
                "2": reminder_id
            },
            "3": title,
            "5": {
                "1": year,
                "2": month,
                "3": day,
                "4": {
                    "1": hour,
                    "2": minute,
                    "3": second,
                }
            },
            "8": 0
        }
    }
    return headers, data


def read_yes_no(prompt) -> bool:
    """
    read yes no answer from the user. default (empty answer) is yes
    """
    ans = input(f'{prompt} [Y/n] ').lower()
    if ans in ['', 'y', 'yes']:
        return True
    else:
        return False


def read_reminder_params():
    """
    :return: (headers, data), or None (meaning to action required)
    """
    title = input('What\'s the reminder: ')
    date_str = input('When do you want to be reminded: ')
    dt = dateparser.parse(date_str)
    if dt is None:
        print('Unrecognizable time text')
        return
    weekday = WEEKDAYS[dt.weekday()]

    print(
        f'\n"{title}" on {weekday}, {dt.year}-{dt.month}-{dt.day} '
        f'at {str(dt.hour).zfill(2)}:{str(dt.minute).zfill(2)}\n'
    )
    save = read_yes_no('Do you want to save this?')
    if save:
        return build_request_params(title, dt.year, dt.month, dt.day, dt.hour, dt.minute)


usage = '''
Simply enter your reminder and the time at which you want to be reminded:
    $ remind
    What's the reminder: Pay bills
    When do you want to be reminded: tomorrow at 4pm
    
The time text can be in many formats such as
    * In 2 days at 14:56
    * in 5 days at 9am
    * Mar 6 at 7pm
    * Sunday the 17th, 2:30pm
    * tomorrow
    * today at 19:00
    * 2019-05-25 10:42
'''


def parse_args():
    """
    parse and return the program arguments
    """
    parser = argparse.ArgumentParser(description='Google reminders cli',
                                     epilog=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    return parser.parse_args()


def main():
    parse_args()  # handles the help menu
    auth_http = authenticate()
    params = read_reminder_params()
    if params:
        headers, data = params
        response, content = auth_http.request(
            uri='https://reminders-pa.clients6.google.com/v1internalOP/reminders/create',
            method='POST',
            body=json.dumps(data),
            headers=headers,
        )
        if response.status == HTTP_OK:
            print('Reminder set successfully')
        else:
            print('Error while trying to set a reminder:')
            print(f'    status code - {response.status}')
            print(f'    {content}')
    else:
        print('Reminder was not saved')


if __name__ == '__main__':
    main()
