from util.resources import Resource, ResourceTracker
from util.exceptions import OverLimit
from math import ceil, floor

class CreationPointTracker(ResourceTracker):
    def get_total(self, only_stat=False, only_advantage=False):
        if only_stat == only_advantage: # truetrue or falsefalse, which are both bs
            return super().get_total()
        if only_stat:
            return sum([q.value for q in self.track if q.used_stat == True])
        if only_advantage:
            return sum([q.value for q in self.track if q.used_advantage == True])

    def emit_resource(self, value=1):
        lock_stat = False
        lock_advantage = False
        if self.get_limit() is not None:
            # check over full limit
            if self.get_total() + value > self.get_limit():
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

class DevelopmentPointTracker(ResourceTracker):
    def __init__(self, *args, **kwargs):
        self.local_limits = {}
        super().__init__(*args, **kwargs)

    def add_local_limit(self, k, limit_f=None, limit_pct=None):
        if limit_f is None and limit_pct is None:
            raise NotEnoughData('Provide either a lim function or lim percentage')
        if limit_pct is not None:
            lim_f = lambda: floor(self.get_limit()*limit_pct)
        self.local_limits[k] = lim_f

    def get_local_limit(self, module):
        if self.local_limits.get(module) is not None:
            return self.local_limits.get(module)()
        else:
            raise NotEnoughData('Local limit called with no local limit function set')  # fixme this should not be happening

    def get_local(self, usage):
        return sum([q.value for q in self.track if q.usage == usage])

    def emit_resource(self, value, module):
        if module in self.local_limits:
            if self.get_local(module)+value > self.get_local_limit(module):
                raise OverLimit(f'Local DP limit for {module} exceeded')
        return super().emit_resource(value)

class DevelopmentPoint(Resource):
    pass