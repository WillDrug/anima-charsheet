import inspect
from functools import wraps
from .exceptions import OverLimit, NotAllowed, NotCompatible
from weakref import WeakSet

def process_track_change(f):
    @wraps(f)
    def wrapper(self, *args, **kw):
        self.before(*args, **kw, f=f)
        result = f(self, *args, **kw)
        self.after(*args, **kw, f=f)
        return result

    return wrapper


class Tracked:
    def __init__(self, value, tracker):
        self.value = value
        self.tracker = tracker
        self.additional = []

    def __del__(self):
        if self.value != 0:
            self.revert()

    def use(self, value):
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
    def __init__(self, max_value_f, min_value_f, character, emit_limit=None):
        self.get_maximum = max_value_f
        self.value = max_value_f()
        self.get_minimum = min_value_f
        self.character = character
        self.reserved = WeakSet()
        if emit_limit is not None:
            self.__get_emit_limit = emit_limit
            self.emit_limit = emit_limit()

    def __get_emit_limit(self):
        raise NotImplementedError()

    def get_reserved(self):
        return sum([q.value for q in self.reserved])

    def free(self, pts):
        self.reserved.remove(pts)  # this can raise a ValueError, shouldn't if all is tracked okay

    def emit(self, value) -> Tracked:
        if self.value - value < self.get_minimum():
            raise OverLimit(f'You don\'t have {value} {self.pts.__class__} to give :(')
        pts = self.pts(value, self)
        self.reserved.add(pts)
        return pts

    def gain(self, pts):
        if not isinstance(pts, self.pts):
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
