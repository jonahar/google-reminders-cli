import functools
import time
from datetime import datetime


def gen_id() -> str:
    """generate a fresh reminder id"""
    # id is set according to the current unix time
    return f'cli-reminder-{time.time()}'


@functools.total_ordering
class Reminder:
    def __init__(
        self,
        id: str,
        title: str,
        dt: datetime,
        creation_timestamp_msec: int = None,
        done: bool = False,
    ):
        if id is None:
            raise ValueError('Reminder id must not be None')
        self.id = id
        self.title = title
        self.dt = dt
        self.creation_timestamp_msec = creation_timestamp_msec
        self.done = done
    
    def __repr_title(self):
        """
        if reminder is not done return its title as is. otherwise return
        a strikethrough title
        """
        return (
            self.title if not self.done
            else '̶'.join(c for c in self.title)
        )
    
    def __lt__(self, other):
        return self.dt < other.dt
    
    def __repr__(self):
        format = '%Y-%m-%d %H:%M'
        return f'{self.dt.strftime(format)}: {self.__repr_title()} ; id="{self.id}"'
