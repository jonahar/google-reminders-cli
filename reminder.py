import functools
import time
from datetime import datetime


@functools.total_ordering
class Reminder:
    def __init__(
        self,
        title: str,
        dt: datetime,
        creation_timestamp_msec: int = None,
        id: str = None
    ):
        self.title = title
        self.dt = dt
        self.creation_timestamp_msec = creation_timestamp_msec
        #  if id was not given we set it according to the current unix time
        self.id = id if id is not None else f'cli-reminder-{time.time()}'
    
    def __lt__(self, other):
        return self.dt < other.dt
    
    def __repr__(self):
        format = '%Y-%m-%d %H:%M'
        return f'{self.dt.strftime(format)}: {self.title} ; id="{self.id}"'
