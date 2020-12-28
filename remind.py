#!/usr/bin/env python3

import argparse
import readline  # to enable navigating through entered text
from datetime import datetime
from typing import Optional

import dateparser

from reminder import Reminder, gen_id
from reminders_client import RemindersClient

# format is  "Fri, May 23 2019, 19:30"
DATE_FORMAT = '%a, %b %d %Y, %H:%M'


def read_yes_no(prompt) -> bool:
    """
    read yes/no answer from the user
    """
    ans = input(f'{prompt} [Y/n] ')
    return ans.lower() in ['', 'y', 'yes']


def parse_time_str(time_str: str) -> Optional[datetime]:
    dt = dateparser.parse(time_str)
    if dt is None:
        print('Unrecognizable time text. See help menu for legal formats')
        return None
    return dt


def read_reminder_params() -> Optional[Reminder]:
    """
    read parameters from the user and build a Reminder object.
    return a Reminder object, or None, meaning no action required (e.g. wrong
    user parameters, or user aborted the action)
    """
    title = input('What\'s the reminder: ')
    dt = parse_time_str(input('When do you want to be reminded: '))
    if dt is not None:
        print(f'\n"{title}" on {dt.strftime(DATE_FORMAT)}\n')
        save = read_yes_no('Do you want to save this?')
        if save:
            return Reminder(id=gen_id(), title=title, dt=dt)


def invoke_operation(args):
    """
    inspect the program arguments and invoke the appropriate operation
    """
    client = RemindersClient()
    
    if args.interactive or args.create:
        # prepare the reminder to create
        if args.interactive:
            reminder = read_reminder_params()
        else:
            title, time_str = args.create
            dt = parse_time_str(time_str)
            if dt is None:
                return
            reminder = Reminder(id=gen_id(), title=title, dt=dt)
        
        # execute creation if applicable
        if reminder is not None:
            if client.create_reminder(reminder):
                print('Reminder set successfully:')
                print(reminder)
    
    elif args.get:
        id = args.get
        reminder = client.get_reminder(reminder_id=id)
        if reminder is not None:
            print(reminder)
    
    elif args.delete:
        id = args.delete
        if client.delete_reminder(reminder_id=id):
            print('Reminder deleted successfully')
    
    elif args.list:
        num_reminders = args.list
        if num_reminders < 0:
            print('argument to list command must be positive')
            return
        reminders = client.list_reminders(num_reminders=num_reminders)
        reminders = filter(None, reminders)
        if reminders is not None:
            for r in sorted(reminders):
                print(r)
    
    else:
        print('Wrong usage: no valid action was specified\n'
              'please read help menu (-h) to see correct usage')


time_string_explain = '''
The TIME argument string can be in many formats such as
    * "In 2 days at 14:56"
    * "in 5 days at 9am"
    * "Mar 6 at 7pm"
    * "Sunday the 17th, 2:30pm"
    * "tomorrow"
    * "today at 19:00"
    * "2019-05-25 10:42"
'''


def parse_args():
    """
    parse and return the program arguments
    """
    parser = argparse.ArgumentParser(description='Google reminders cli',
                                     epilog=time_string_explain,
                                     formatter_class=argparse.RawTextHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', action='store_true', dest='interactive',
                       help='create a reminder by entering details interactively')
    group.add_argument('-c', nargs=2, metavar=('TITLE', 'TIME'), dest='create',
                       help='create a reminder with the given title and time')
    group.add_argument('-g', metavar='<id>', dest='get',
                       help='get reminder information by ID')
    group.add_argument('-d', metavar='<id>', dest='delete',
                       help='delete reminder by ID')
    group.add_argument('-l', type=int, metavar='N', dest='list',
                       help='list the last N created reminders, for a positive integer N')
    
    return parser.parse_args()


def main():
    args = parse_args()
    invoke_operation(args)


if __name__ == '__main__':
    main()
