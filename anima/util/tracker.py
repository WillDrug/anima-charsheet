from math import floor
from enum import Enum
from anima.util.exceptions import ClassMistmatch

class TimeType(Enum):
    day = 4
    hour = 3
    minute = 2
    round = 1
    second = 0

    @staticmethod
    def convert(time_from, time_to, value):
        if time_from.value == time_to.value:
            return value
        converter = {
            TimeType.day: {'down': 24},
            TimeType.hour: {'up': 24, 'down': 60},
            TimeType.minute: {'up': 60, 'down': 20},
            TimeType.round: {'up': 20, 'down': 3},
            TimeType.second: {'up': 3},
        }
        while time_from.value != time_to.value:
            if time_from.value < time_to.value:
                value = floor(value / converter[time_from]['up'])
                time_from = TimeType(time_from.value + 1)
            else:
                value = converter[time_from]['down'] * value
                time_from = TimeType(time_from.value - 1)
        return value


class Time:
    def __init__(self, t: TimeType, v: int = 1):
        self.time_type = t
        self.time_value = v

    def convert(self, new_type):
        val = TimeType.convert(self.time_type, new_type, self.time_value)
        return Time(new_type, val)

    @staticmethod
    def sync_types(first, second):
        if first.time_type.value != second.time_type.value:
            if first.time_type.value > second.time_type.value:
                first = first.convert(second.time_type)
            else:
                second = second.convert(first.time_type)
        return first, second

    def __gt__(self, other):
        if not isinstance(other, Time):
            return self.time_value > other
        first, second = Time.sync_types(self, other)
        return first.time_value > second.time_value

    def __eq__(self, other):
        if not isinstance(other, Time):
            return self.time_value == other
        first, second = Time.sync_types(self, other)
        return first.time_value == second.time_value

    def __add__(self, other):
        if not isinstance(other, Time):
            return Time(self.time_type, self.time_value + other)
        first, second = Time.sync_types(self, other)
        return Time(first.time_type, first.time_value + second.time_value)

    def __radd__(self, other):
        if not isinstance(other, Time):
            return Time(self.time_type, self.time_value + other)
        first, second = Time.sync_types(self, other)
        return Time(first.time_type, first.time_value + second.time_value)

    def __sub__(self, other):
        if not isinstance(other, Time):
            return Time(self.time_type, self.time_value - other)
        first, second = Time.sync_types(self, other)
        return Time(first.time_type, first.time_value - second.time_value)

    def __repr__(self):
        return f'<Time({self.time_type}: {self.time_value})>'

    def __rsub__(self, other):
        if not isinstance(other, Time):
            raise ClassMistmatch(f'Tried subtracting time from something else ({other} - {self})')
        first, second = self.sync_types(self, other)
        return Time(first.time_type, second.time_value-first.time_value)

    def __truediv__(self, other):
        first, second = self.sync_types(self, other)
        return first.time_value/second.time_value

    def __floordiv__(self, other):
        first, second = self.sync_types(self, other)
        return first.time_value // second.time_value


class Tracker:
    def __init__(self, max_f, regen_f, min_f=None, buffered=True, name=''):
        self.name = name
        self._max_f = max_f
        if min_f is None:
            self._min_f = lambda: 0
        else:
            self._min_f = min_f
        self._regen_f = regen_f
        self.current = self.maximum
        self.buffer = Time(TimeType.second, 0)

    @property
    def maximum(self):  # can override to give a bonus
        if callable(self._max_f):
            return self._max_f()
        else:
            return self._max_f

    @property
    def minimum(self):
        if callable(self._min_f):
            return self._min_f()
        else:
            return self._min_f


    def update(self, value):
        self.current = max(self.minimum, min(self.maximum, self.current+value))

    def tick(self, time: Time, resting=False):
        value, regen_window = self._regen_f(resting)
        # calculate if able to currently regen
        time = time+self.buffer
        while time / regen_window >= 1:
            self.current = max(self.minimum, min(self.maximum, self.current + value))
            time = time - regen_window
        self.buffer = time

    def __repr__(self):
        return f'<Tracker {"of "+self.name if self.name != "" else ""}({self.current}/{self.maximum}) ({self.buffer})>'

if __name__ == '__main__':
    def max_f():
        return 5
    def regen_f(resting):
        return 2 if resting else 1, Time(TimeType.minute, 1)

    fake_tracker = Tracker(max_f, regen_f)
    fake_tracker.update(-10)
    print(fake_tracker)
    for _ in range(59):
        fake_tracker.tick(Time(TimeType.second))
    print(fake_tracker)
    fake_tracker.tick(Time(TimeType.second))
    print(fake_tracker)