import time

from datetime import datetime


class Reminder:
    def __init__(self, title: str, dt: datetime, id: str = None):
        #  if id was not given we set it according to the current unix time
        self.id = id if id is not None else f'cli-reminder-{time.time()}'
        self.title = title
        self.dt = dt
