from util.resources import Resource, ResourceTracker
from util.exceptions import OverLimit
from math import ceil

class CreationPointTracker(ResourceTracker):
    def get_total(self, only_stat=False, only_advantage=False):
        if only_stat == only_advantage: # truetrue or falsefalse, which are both bs
            return super().get_total()
        if only_stat:
            return sum([q.value for q in self.track if q.used_stat == True])
        if only_advantage:
            return sum([q.value for q in self.track if q.used_advantage == True])

    def emit_resource(self, value=1, limit=None):  # todo: rewrite to use get_limit
        lock_stat = False
        lock_advantage = False
        if limit is not None:
            # check over full limit
            if self.get_total() + value > limit:
                raise OverLimit(f'There is no {self.resource_cls} left')
            # check over specific limit
            if self.get_total(only_stat=True) + value > ceil(limit / 2):
                lock_stat = True
            if self.get_total(only_advantage=True) + value > ceil(limit / 2):
                lock_advantage = True
            # check edge case last points
            if not lock_stat and not lock_advantage:
                if self.get_total(only_stat=True) + value > limit/2 and self.get_total(only_advantage=True) + value > limit/2:
                    if self.track.__len__() > 0:
                        if self.track[-1].used_stat:
                            lock_stat = True
                        else:
                            lock_advantage = True
            if lock_advantage and lock_stat:
                raise OverLimit(f'Too much {self.resource_cls} requested for single use')
        res = self.resource_cls(value=value, lock_stat=lock_stat, lock_advantage=lock_advantage)
        self.track.append(res)
        return res

class CreationPoint(Resource):
    def __init__(self, lock_stat=False, lock_advantage=False, **kwargs):
        super().__init__(**kwargs)
        self.lock_stat = lock_stat
        self.lock_advantage = lock_advantage
        self.used_stat = None
        self.used_advantage = None

    def set_usage(self, usage, stat=False):
        if (stat and self.lock_stat) or (not stat and self.lock_advantage):
            raise OverLimit(f'This {self.__class__.__name__} can\'t be used for {"a stat" if not stat else "an advantage"}')
        self.used_stat = stat
        self.used_advantage = not stat
        super().set_usage(usage)


class DevelopmentPoint(Resource):
    pass