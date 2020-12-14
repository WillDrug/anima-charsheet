from enum import Enum
from .exceptions import NotFound, NotCompatible
class TimeUnit(Enum):
    ROUND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4

class TimeTracker:
    def __init__(self):
        self.__time_processing = {
            TimeUnit.ROUND: self.tick_round,
            TimeUnit.MINUTE: self.tick_minute,
            TimeUnit.HOUR: self.tick_hour,
            TimeUnit.DAY: self.tick_day
        }
        self.tick_functions = {
            TimeUnit.ROUND: set(),
            TimeUnit.MINUTE: set(),
            TimeUnit.HOUR: set(),
            TimeUnit.DAY: set()
        }
        self.tick_reference = {}

    def track(self, f, unit: TimeUnit, per=1):
        if not isinstance(unit, TimeUnit):
            raise NotCompatible(f'Please use {TimeUnit} specs to track time')
        self.tick_functions[unit].add(f)
        self.tick_reference[f] = {'unit': unit, 'per': per, 'cache': 0}

    def untrack(self, f):
        self.tick_functions[self.backref[f]].remove(f)
        del self.tick_reference[f]

    def tick(self, value: int, unit: TimeUnit):
        if unit not in self.__time_processing:
            raise NotFound(f'Requested to tick non implemented time unit')
        return self.__time_processing[unit](value)

    def tick_common(self, value, unit: TimeUnit):
        for f in self.tick_functions[unit]:
            per = self.tick_reference[f]['per']
            cache = self.tick_reference[f]['cache']
            cache = cache+value
            while cache >= per:
                f()
                cache = cache-per
            self.tick_reference[f]['cache'] = cache
        return

    def tick_round(self, value: int):
        self.tick_common(value, TimeUnit.ROUND)
        return

    def tick_minute(self, value: int, propagate=True):
        self.tick_common(value, TimeUnit.MINUTE)
        if propagate:
            self.tick_round(value*20)

    def tick_hour(self, value: int, propagate=True):
        self.tick_common(value, TimeUnit.HOUR)
        if propagate:
            self.tick_minute(value*60)

    def tick_day(self, value: int, propagate=True):
        self.tick_common(value, TimeUnit.DAY)
        if propagate:
            self.tick_hour(value*24)
