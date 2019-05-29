import readline

import argparse
import dateparser

from reminder import Reminder
from reminders_client import RemindersClient


def read_yes_no(prompt) -> bool:
    """
    read yes no answer from the user. default (empty answer) is yes
    """
    ans = input(f'{prompt} [Y/n] ').lower()
    if ans in ['', 'y', 'yes']:
        return True
    else:
        return False


def read_reminder_params() -> Reminder:
    """
    :return: Reminder object or None (meaning user aborted the action)
    """
    title = input('What\'s the reminder: ')
    dt = dateparser.parse(input('When do you want to be reminded: '))
    if dt is None:
        print('Unrecognizable time text')
        return None

    # format is  "Fri, May 23 2019, 19:30"
    date_str = dt.strftime('%a, %b %d %Y, %H:%M')
    print(f'\n"{title}" on {date_str}\n')

    save = read_yes_no('Do you want to save this?')
    if save:
        return Reminder(title=title, dt=dt)


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
    args = parse_args()  # handles the help menu
    client = RemindersClient()
    reminder = read_reminder_params()
    if reminder:
        if client.create_reminder(reminder):
            print('Reminder set successfully')
    else:
        print('Reminder was not saved')


if __name__ == '__main__':
    main()
