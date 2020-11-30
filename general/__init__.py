from util.exceptions import NotFound, NotEnoughData, Panik, OverLimit
from util.resources import CreationPointTracker, CreationPoint, Resource
from util.parameters import ModuleConfig, Attribute, MultipartAttribute
from math import floor
import traceback

class GeneralConfig(ModuleConfig):
    def __init__(self, LPM_cost, init_per_level, life_points_per_level):
        self.LPM_cost = LPM_cost
        self.init_per_level = init_per_level
        self.LP_per_level = life_points_per_level
        super(GeneralConfig, self).__init__()

class Stat(MultipartAttribute):
    VALUE_LIMIT = 10
    SUM_COST_LIMIT = 65
    INSTANCE_LIST = {}  # important!
    STARTING_VALUE = 5

    # todo: limit inhuman\zen to appropriate caps depending on mental\physical
    @property
    def cost(self):
        return self.value + (self.value-9 if self.value >= 10 else 0)

    @property
    def modifier(self):
        return (self.value-5)*5 if self.value >= 5 else -10*(5-self.value)  # kill me

    def boost(self, res: Resource):  # todo change to function
        if isinstance(res, CreationPoint):
            res.set_usage(f'Plus {res.value} to {self.__class__.__name__}', stat=True)
        else:
            res.set_usage(f'Plus {res.value} to {self.__name__}')

        self.boosts.append(res)

    def bonus(self):
        def bonus_append(calling_attribute):
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0
            return self.modifier
        return self.__name__, bonus_append

class STR(Stat):
    pass

class DEX(Stat):
    pass

class AGI(Stat):
    pass

class LifePoints(Attribute):
    pass

class Initiative(Attribute):
    STARTING_VALUE = 20

class General:
    def get_class_lp(self):
        def class_lp(inst):
            return self.level*self.config.LP_per_level
        return class_lp

    def __init__(self, config: GeneralConfig):
        self.config = config
        self.stats = {k: Stat(k, self) for k in Stat.impl_list()}
        self.maximum_life_points = LifePoints()
        self.maximum_life_points.add_bonus(self.config.__class__, lambda x: self.level*self.config.LP_per_level)

        self.initiative = Initiative()
        self.initiative.add_bonus(self.config.__class__, lambda x: self.level*self.config.init_per_level)
        self.initiative.add_bonus(self.stats.get('dex').bonus())  # todo: think about this
        self.initiative.add_bonus(self.stats.get('agi').bonus())
        self.cp_tracker = CreationPointTracker(CreationPoint)

    @property
    def stat_costs(self):
        return Stat.cls_full_cost(self)

    def set_stats(self, stats: dict):
        for k in stats:
            if k not in Stat.impl_list():
                raise NotFound(f'{k} is not a stat')
        try:
            for k in stats:
                self.stats[k].change_base_value(stats[k])
        except OverLimit as e:
            for k in stats:
                self.stats[k].rollback_base_value()
            raise e
    @property
    def level(self) -> int:
        return floor(self.config.get_dp()/100)

    def boost_stat(self, stat_name, res: Resource):
        stat = self.stats.get(stat_name)
        if stat is None:
            raise NotFound(f'{stat_name} is not a stat')
        stat.boost(res)

    def boost_stat_with_cp(self, stat_name, value):  # todo: catch? anything?
        cp = self.cp_tracker.emit_resource(value=value, limit=self.level)
        return self.boost_stat(stat_name, cp)



if __name__ == '__main__':
    a = Stat('STR', 1)
    b = Stat('STR', 1)
    print(a.full_cost(1))
    del b
    print(a.full_cost(1))