import time

from datetime import datetime


class Reminder:
    def __init__(self, title: str, dt: datetime):
        # the reminder id is the unix time at which it was created
        self.id = f'cli-reminder-{time.time()}'
        self.title = title
        self.dt = dt
