from util.resources import IterativePoint, IterativePointTracker, Resource, ResourceTracker, LocalLimitedPointTracker

class InnateBonusTracker(IterativePointTracker):
    def get_total(self, only_mental=False, only_physical=False, **kwargs):
        if 'only_one' in kwargs:
            only_mental = kwargs.pop('only_one')
        if 'only_two' in kwargs:
            only_physical = kwargs.pop('only_two')
        return super().get_total(only_one=only_mental, only_two=only_physical)

class InnateBonus(IterativePoint):
    def __init__(self, lock_mental=False, lock_physical=False, **kwargs):
        if 'lock_one' in kwargs:
            lock_mental = kwargs.pop('lock_one')
        if 'lock_two' in kwargs:
            lock_physical = kwargs.pop('lock_two')
        super().__init__(lock_one=lock_mental, lock_two=lock_physical, **kwargs)

    def set_usage(self, usage, mental=False):
        super().set_usage(usage, one=mental)

class Bonus(Resource):
    pass

class BonusTracker(LocalLimitedPointTracker):
    pass

class TertiaryPoint(Resource):
    pass