import inspect
from functools import wraps
from .exceptions import OverLimit, NotAllowed, NotCompatible
from weakref import WeakSet
from util.time import TimeUnit

def process_track_change(f):
    @wraps(f)
    def wrapper(self, *args, **kw):
        self.before(*args, **kw, f=f)
        result = f(self, *args, **kw)
        self.after(*args, **kw, f=f)
        return result

    return wrapper

import traceback

class Tracked:
    def __init__(self, value, tracker):
        self.value = value
        self.tracker = tracker
        self.additional = []

    def __del__(self):
        if self.value != 0:
            self.revert()

    def use(self, value=1):
        if value > self.value:
            raise OverLimit(f'This {self.__class__} does not have {value} in it. Maximum is {self.value}')
        self.value -= value
        self.tracker.change_value(-self.value)
        if self.value == 0:
            self.tracker.free(self)

    def revert(self):  # this is used for stuff like returning accumulated Zeon
        self.tracker.free(self)

    def check_merge(self, other):
        if self.tracker.character != other.tracker.character:
            raise NotAllowed('You cannot combine stuffs of different characters')
        if self.__class__ != other.__class__:
            raise NotAllowed('Cannot merge different stuffs')

    def merge(self, trc):
        self.check_merge(trc)

        self.value += trc.value


class Tracker:
    pts = Tracked
    RESTORE_EACH = TimeUnit.ROUND
    RESTORE_EMIT_EACH = TimeUnit.ROUND

    def __init__(self, max_value_f, character, min_value_f=None, emit_limit={}):
        self.get_maximum = max_value_f
        self.value = max_value_f()
        if min_value_f is None:
            min_value_f = lambda: 0
        self.get_minimum = min_value_f
        self.character = character
        self.reserved = WeakSet()
        self.__emit_limit_f = emit_limit
        self.emit_limit = {}
        for k in emit_limit:
            self.emit_limit[k] = emit_limit[k]()

    def __get_emit_limit(self):
        return self.__emit_limit_f

    def get_reserved(self):
        return sum([q.value for q in self.reserved])

    def free(self, pts):
        self.reserved.remove(pts)  # this can raise a ValueError, shouldn't if all is tracked okay

    def emit(self, value, pts: None) -> Tracked:
        if self.value - value < self.get_minimum():
            raise OverLimit(f'You don\'t have {value} {self.pts.__class__} to give :(')
        if pts is not None:
            if pts in self.__get_emit_limit():
                if self.emit_limit[pts] < value:
                    raise OverLimit(f'You can\'t emit more than {self.__get_emit_limit()[pts]()} '
                                    f'{pts} per {self.RESTORE_EACH}')
                self.emit_limit[pts] -= value
        pts = self.pts(value, self)
        self.reserved.add(pts)
        return pts

    def get_restore(self):
        return self.get_maximum()

    def get_emit_restore(self):
        return self.__get_emit_limit()

    def tick(self):
        self.change_value(self.get_restore())

    def tick_emit(self):
        for k in self.emit_limit:
            self.emit_limit[k] = self.get_emit_restore()[k]()
        return

    def get_tick(self):
        return self.tick, self.RESTORE_EACH

    def get_tick_emit(self):
        return self.tick_emit, self.RESTORE_EMIT_EACH

    def gain(self, pts):
        if not isinstance(pts, self.pts) and not issubclass(pts.__class__, self.pts):
            raise NotCompatible(f'{pts.__class__} can\'t be used to replenish {self.pts}')
        pts.use()
        self.change_value(pts.value)

    @process_track_change
    def change_value(self, update, **kwargs):
        self.value += update
        self.value = min(self.value, self.get_maximum())

    @process_track_change
    def set_value(self, update, **kwargs):
        self.value = min(self.get_maximum(), update)

    def before(self, *args, f=None, **kwargs):
        pass

    def after(self, *args, f=None, **kwargs):
        pass
