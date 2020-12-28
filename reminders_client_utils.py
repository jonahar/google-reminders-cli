import json
import os
from datetime import datetime, timedelta
from typing import Optional

import httplib2
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from reminder import Reminder

APP_KEYS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app_keys.json')
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
            flow=OAuth2WebServerFlow(
                client_id=app_keys['APP_CLIENT_ID'],
                client_secret=app_keys['APP_CLIENT_SECRET'],
                scope=['https://www.googleapis.com/auth/reminders'],
                user_agent='google reminders cli tool',
            ),
            storage=storage,
            flags=tools.argparser.parse_args([]),
        )
    auth_http = credentials.authorize(httplib2.Http())
    return auth_http


def create_req_body(reminder: Reminder) -> str:
    """
    returns the body of a create-reminder request
    """
    body = {
        '2': {
            '1': 7
        },
        '3': {
            '2': reminder.id
        },
        '4': {
            '1': {
                '2': reminder.id
            },
            '3': reminder.title,
            '5': {
                '1': reminder.dt.year,
                '2': reminder.dt.month,
                '3': reminder.dt.day,
                '4': {
                    '1': reminder.dt.hour,
                    '2': reminder.dt.minute,
                    '3': reminder.dt.second,
                }
            },
            '8': 0
        }
    }
    return json.dumps(body)


def update_req_body(reminder: Reminder) -> str:
    """
    returns the body of a update-reminder request
    """
    body = {
        '2': {
            '2': reminder.id
        },
        '4': {
            '1': {
                '2': reminder.id
            },
            '3': reminder.title,
            '5': {
                '1': reminder.dt.year,
                '2': reminder.dt.month,
                '3': reminder.dt.day,
                '4': {
                    '1': reminder.dt.hour,
                    '2': reminder.dt.minute,
                    '3': reminder.dt.second,
                },
                '9': 1 if reminder.all_day else 0,
            },
            '8': 1 if reminder.done else 0,
            '11': str(int(datetime.utcnow().timestamp() * 1000)),
            '18': str(reminder.creation_timestamp_msec)
        },
        '7': {
            '1': [
                0,
                1,
                3,
                10,
            ]},
    }
    return json.dumps(body)


def get_req_body(reminder_id: str) -> str:
    """
    returns the body of a get-reminder request
    """
    body = {'2': [{'2': reminder_id}]}
    return json.dumps(body)


def delete_req_body(reminder_id: str) -> str:
    """
    returns the body of a delete-reminder request
    """
    body = {'2': [{'2': reminder_id}]}
    return json.dumps(body)


def list_req_body(num_reminders: int, max_timestamp_msec: int = 0) -> str:
    """
    returns the body of a list-reminders request.

    The body corresponds to a request that retrieves a maximum of num_reminders
    reminders, whose creation timestamp is less than max_timestamp_msec.
    max_timestamp_msec is a unix timestamp in milliseconds. if its value is 0, treat
    it as current time.
    """
    body = {
        '5': 1,  # boolean field: 0 or 1. 0 doesn't work ¯\_(ツ)_/¯
        '6': num_reminders,  # number number of reminders to retrieve
    }
    
    if max_timestamp_msec:
        max_timestamp_msec += int(timedelta(hours=15).total_seconds() * 1000)
        body['16'] = max_timestamp_msec
        # Empirically, when requesting with a certain timestamp, reminders with the given
        # timestamp or even a bit smaller timestamp are not returned. Therefore we increase
        # the timestamp by 15 hours, which seems to solve this...  ~~voodoo~~
        # (I wish Google had a normal API for reminders)
    
    return json.dumps(body)


def build_reminder(reminder_dict: dict) -> Optional[Reminder]:
    r = reminder_dict
    try:
        id = r['1']['2']
        title = r['3']
        if '5' in r:
            year = r['5']['1']
            month = r['5']['2']
            day = r['5']['3']
            if '4' in r['5']:
                hour = r['5']['4']['1']
                minute = r['5']['4']['2']
                second = r['5']['4']['3']
            else:
                hour = 0
                minute = 0
                second = 0
            all_day = '9' in r['5'] and r['5']['9'] == 1
        else:
            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day
            hour = 0
            minute = 0
            second = 0

        creation_timestamp_msec = int(r['18'])
        done_timestamp_msec = int(r['11']) if '11' in r else None
        done = '8' in r and r['8'] == 1

        return Reminder(
            id=id,
            title=title,
            dt=datetime(year, month, day, hour, minute, second),
            creation_timestamp_msec=creation_timestamp_msec,
            done_timestamp_msec=done_timestamp_msec,
            done=done,
            all_day = all_day
        )

    except KeyError:
        print('build_reminder failed: unrecognized reminder dictionary format')
        return None
