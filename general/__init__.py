from util.exceptions import NotFound, NotEnoughData, Panik, OverLimit
from util.resources import CreationPointTracker, CreationPoint, Resource, ResourceTracker
from util.parameters import ModuleConfig, Attribute, MultipartAttribute
from .resources import Willpower, Fatigue
from math import floor, inf
import traceback

class GeneralConfig(ModuleConfig):
    def __init__(self, LPM_cost, init_per_level, life_points_per_level):
        self.LPM_cost = LPM_cost
        self.init_per_level = init_per_level
        self.LP_per_level = life_points_per_level
        super(GeneralConfig, self).__init__()

class Stat(MultipartAttribute):
    COST_LIMIT = 10
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

    def mod_bonus(self):
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

class CON(Stat):
   def health_bonus(self):
       def bonus_append(calling_attribute):
           if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
               return 0
           return 20+10*self.value+self.modifier
       return self.__name__, bonus_append

class INT(Stat):
    pass

class POW(Stat):
    pass

class WIL(Stat):
    pass

class PER(Stat):
    pass

class LifePoints(Attribute):
    def __init__(self, LPM_cost):
        self.LPM_cost = LPM_cost  # this can be and is used by bonuses
        super().__init__()
    #  LifePoints take no resources in and should be unboostable. Leaving the method open nonetheless.

class Initiative(Attribute):  # fixme: separation of boint-buy and resource boosts are kinda dumb
    STARTING_VALUE = 20
    COST_LIMIT = 20  # cannot be updated by itself

class Weight(Attribute):
    STARTING_VALUE = 0
    COST_LIMIT = 0  # cannot be updated by itself

    def kg(self):
        """
        :return: light and heavy load by something
        """
        if self.value == 1:
            return 1, 1
        elif self.value == 2:
            return 5, 10
        elif self.value == 3:
            return 10, 20
        elif self.value == 4:
            return 15, 40
        elif self.value == 5:
            return 25, 60
        elif self.value == 6:
            return 40, 120
        elif self.value == 7:
            return 60, 180
        elif self.value == 8:
            return 80, 260
        elif self.value == 9:
            return 100, 350
        elif self.value == 10:
            return 150, 420
        elif self.value == 11:
            return 200, 600
        elif self.value == 12:
            return 350, 1000
        elif self.value == 13:
            return 1000, 3000
        elif self.value == 14:
            return 5000, 25000
        elif self.value == 15:
            return 15000, 100000
        elif self.value == 16:
            return 100000, 500000
        elif self.value == 17:
            return 500000, 2500000
        elif self.value == 18:
            return 1000000, 10000000
        elif self.value == 19:
            return 10000000, 150000000
        elif self.value >= 20:
            return inf, inf
        else:
            raise NotFound('This bs does not work with your values')


class Movement(Attribute):
    STARTING_VALUE = 0

    def meters(self):  # fixme this is some rpg bullshit right there
        if self.value == 1:
            return 1
        elif self.value == 2:
            return 4
        elif self.value == 3:
            return 8
        elif self.value == 4:
            return 15
        elif self.value == 5:
            return 20
        elif self.value == 6:
            return 22
        elif self.value == 7:
            return 25
        elif self.value == 8:
            return 28
        elif self.value == 9:
            return 32
        elif self.value == 10:
            return 35
        elif self.value == 11:
            return 40
        elif self.value == 12:
            return 50
        elif self.value == 13:
            return 80
        elif self.value == 14:
            return 150
        elif self.value == 15:
            return 250
        elif self.value == 16:
            return 500
        elif self.value == 17:
            return 1000
        elif self.value == 18:
            return 5000
        elif self.value == 19:
            return 25000
        elif self.value >= 20:
            return inf
        else:
            raise NotFound('This bs does not work with your values')


class General:
    def get_class_lp(self):
        def class_lp(inst):
            return self.level*self.config.LP_per_level
        return class_lp

    def __init__(self, config: GeneralConfig):
        self.config = config
        self.stats = {k: Stat(k, self) for k in Stat.impl_list()}  # fixme: possibly change to clear set attributes
        self.maximum_life_points = LifePoints(self.config.LPM_cost)
        self.maximum_life_points.add_bonus(self.config.__class__, lambda x: self.level*self.config.LP_per_level)
        self.maximum_life_points.add_bonus(self.stats.get('CON').health_bonus())
        self.initiative = Initiative()
        self.initiative.add_bonus(self.config.__class__, lambda x: self.level*self.config.init_per_level)
        self.initiative.add_bonus(self.stats.get('DEX').mod_bonus())  # todo: think about this
        self.initiative.add_bonus(self.stats.get('AGI').mod_bonus())
        self.cp_tracker = CreationPointTracker(CreationPoint)
        self.movement = Movement()
        self.movement.add_bonus(self.stats.get('AGI').bonus())
        self.weight = Weight()
        self.weight.add_bonus(self.stats.get('STR').bonus())
        self.fatigue_tracker = ResourceTracker(Fatigue, limit_f=lambda: self.stats.get('CON').value)
        self.willpower_tracker = ResourceTracker(Willpower, limit_f=lambda: self.stats.get('WIL').value)

    @property
    def stat_costs(self):
        return Stat.cls_full_cost(self)

    def set_stats(self, stats: dict):
        for k in stats:
            if k not in Stat.impl_list():
                raise NotFound(f'{k} is not a stat')
        try:
            for k in stats:
                aff = []
                try:
                    self.stats[k].change_base_value(stats[k])
                    aff.append(k)
                except OverLimit as e:
                    for k in aff:
                        self.stats[k].rollback_base_value()
                    raise e  # reraise because I'm a shithead

    @property
    def level(self) -> int:
        return floor(self.config.get_dp()/100)

    @property
    def presence(self):
        return self.level*5


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