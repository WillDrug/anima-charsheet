from util.resources import Resource, ResourceTracker, IterativePointTracker, IterativePoint, LocalLimitedPointTracker
from util.exceptions import OverLimit
from math import ceil, floor


class CreationPointTracker(IterativePointTracker):
    def get_total(self, only_stat=False, only_advantage=False, **kwargs):
        if 'only_one' in kwargs:
            only_stat = kwargs.pop('only_one')
        if 'only_two' in kwargs:
            only_advantage = kwargs.pop('only_two')
        return super().get_total(only_one=only_stat, only_two=only_advantage)

class CreationPoint(IterativePoint):
    def __init__(self, lock_stat=False, lock_advantage=False, **kwargs):
        if 'lock_one' in kwargs:
            lock_stat = kwargs.pop('lock_one')
        if 'lock_two' in kwargs:
            lock_advantage = kwargs.pop('lock_two')
        super().__init__(lock_one=lock_stat, lock_two=lock_advantage, **kwargs)

    def set_usage(self, usage, stat=False):
        super().set_usage(usage, one=stat)


class DevelopmentPointTracker(LocalLimitedPointTracker):
    pass

class DevelopmentPoint(Resource):
    pass