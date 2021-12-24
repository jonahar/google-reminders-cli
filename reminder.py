import functools
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


def gen_id() -> str:
    """generate a fresh reminder id"""
    # id is set according to the current unix time
    return f"cli-reminder-{time.time()}"


@dataclass
@functools.total_ordering
class Reminder:
    id: str
    title: str
    dt: datetime
    creation_timestamp_msec: Optional[int] = None
    done: bool = False

    def __repr_title(self):
        """
        if reminder is not done return its title as is. otherwise return
        a strikethrough title
        """
        return self.title if not self.done else "̶".join(c for c in self.title)

    def __lt__(self, other):
        return self.dt < other.dt

    def __repr__(self):
        format = "%Y-%m-%d %H:%M"
        return f'{self.dt.strftime(format)}: {self.__repr_title()} ; id="{self.id}"'
