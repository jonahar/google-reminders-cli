import time

from datetime import datetime
import functools


@functools.total_ordering
class Reminder:
    def __init__(self, title: str, dt: datetime, id: str = None):
        """
        :param title:
        :param dt:
        :param id: the remind time
        """
        #  if id was not given we set it according to the current unix time
        self.id = id if id is not None else f'cli-reminder-{time.time()}'
        self.title = title
        self.dt = dt
    
    def __lt__(self, other):
        return self.dt < other.dt
