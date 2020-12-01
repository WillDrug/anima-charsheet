from util.exceptions import NotFound, NotEnoughData, Panik, OverLimit, MergedResource
from util.resources import CreationPointTracker, CreationPoint, Resource, ResourceTracker
from util.parameters import ModuleConfig, Attribute, MultipartAttribute
from .resources import Willpower, Fatigue, StatPoint
from math import floor, inf
import traceback


class GeneralConfig(ModuleConfig):
    def __init__(self, LPM_cost, init_per_level, life_points_per_level):
        self.LPM_cost = LPM_cost
        self.init_per_level = init_per_level
        self.LP_per_level = life_points_per_level
        super(GeneralConfig, self).__init__()


class Stat(MultipartAttribute):
    INSTANCE_LIST = {}  # important!
    # 11 physical 13 mental WOW MENTAL
    DEFAULT_VALUE_CAP = 10  # fixme
    DEFAULT_BASE_RESOURCE_CAP = 11
    DEFAULT_SUM_BASE_RESOURCE_CAP = 65  # this is redundant
    BASE_RESOURCE = StatPoint
    PHYSICAL = True

    def get_value_cap(self):
        return self.DEFAULT_VALUE_CAP + (1 if self.PHYSICAL else 3)

    # todo: limit inhuman\zen to appropriate caps depending on mental\physical
    @property
    def cost(self):
        return self.value + (self.value - 9 if self.value >= 10 else 0)

    @property
    def modifier(self):
        return (self.value - 5) * 5 if self.value >= 5 else -10 * (5 - self.value)  # kill me

    def __stat_point_value(self):
        """
        This silly function is because point buy is WEEEEIRD
        :return:
        """
        return sum(
            [
                q['boost'].value if q['boost'].value < 10 else floor(9 + ((q['boost'].value - 9) / 2))
                for q in self.boosts if isinstance(q['boost'], StatPoint)
            ]
        )

    @property
    def value(self):
        return min(self.base_value +
                   self.__stat_point_value() +
                   sum([
                       floor(q['boost'].value / q['cost']) for q in self.boosts
                       if q['limited'] and not isinstance(q['boost'], self.base_resource)
                   ]) +
                   sum([self.bonuses[q]['f'](self) for q in self.bonuses if self.bonuses[q]['limited']]),
                   self.get_value_cap()) + \
               sum([floor(q['boost'].value / q['cost']) for q in self.boosts if not q['limited']]) + \
               sum([self.bonuses[q]['f'](self) for q in self.bonuses if not self.bonuses[q]['limited']])

    def boost(self, res: Resource, cost=None,
              limited=True):  # limited is VALUE LIMIT. COST limit always applies for base_resource
        if isinstance(res, self.base_resource):
            self.check_cost(res.value)
            if any([isinstance(q, self.base_resource) for q in self.boosts]):
                cr = [q for q in self.boosts if isinstance(q, self.base_resource)].pop()
                cr.set_value(cr.get_value() + res.value)
                raise MergedResource()
            cost = self.get_base_resource_cost()  # fixme
        if isinstance(res, CreationPoint):
            res.set_usage(f'Plus {res.value} to {self.__class__.__class__}', stat=True)
        else:
            res.set_usage(f'Plus {res.value} to {self.__class__}')
        if cost is None:
            cost = 1
        res.set_usage(f'Plus {res.value} to {self.__class__}')
        self.boosts.append({'boost': res, 'limited': limited, 'cost': cost})

    def mod_bonus(self):
        def bonus_append(calling_attribute):
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0
            return self.modifier

        return self.__class__, bonus_append


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
            return 20 + 10 * self.value + self.modifier

        return self.__class__, bonus_append


class INT(Stat):
    PHYSICAL = False


class POW(Stat):
    PHYSICAL = False


class WIL(Stat):
    PHYSICAL = False


class PER(Stat):
    PHYSICAL = False


class LifePoints(Attribute):
    def __init__(self, LPM_cost):
        self.LPM_cost = LPM_cost  # this can be and is used by bonuses
        super().__init__()
    #  LifePoints take no resources in and should be unboostable. Leaving the method open nonetheless.


class Initiative(Attribute):  # fixme: separation of boint-buy and resource boosts are kinda dumb
    BASE_VALUE = 20
    DEFAULT_BASE_RESOURCE_CAP = 0  # can't update


class Weight(Attribute):
    BASE_VALUE = 0
    DEFAULT_BASE_RESOURCE_CAP = 0  # can't update

    # fixme: kf should be the *modifier* function

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
    BASE_VALUE = 0
    DEFAULT_BASE_RESOURCE_CAP = 0

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
            return self.level * self.config.LP_per_level

        return class_lp

    def max_stat_points(self):
        return 65

    def __init__(self, config: GeneralConfig):
        self.stat_points_tracker = ResourceTracker(StatPoint, self.max_stat_points)
        self.config = config
        self.stats = {k: Stat(k, self, base=StatPoint) for k in
                      Stat.impl_list()}  # fixme: possibly change to clear set attributes
        self.maximum_life_points = LifePoints(self.config.LPM_cost)
        self.maximum_life_points.add_bonus(self.config.__class__, lambda x: self.level * self.config.LP_per_level)
        self.maximum_life_points.add_bonus(*self.stats.get('CON').health_bonus())
        self.initiative = Initiative()
        self.initiative.add_bonus(self.config.__class__, lambda x: self.level * self.config.init_per_level)
        self.initiative.add_bonus(*self.stats.get('DEX').mod_bonus())  # todo: think about this
        self.initiative.add_bonus(*self.stats.get('AGI').mod_bonus())
        self.cp_tracker = CreationPointTracker(CreationPoint)
        self.movement = Movement()
        self.movement.add_bonus(*self.stats.get('AGI').bonus())
        self.weight = Weight()
        self.weight.add_bonus(*self.stats.get('STR').bonus())
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
                stp = self.stat_points_tracker.emit_resource(stats[k])  # possible exception 1
                self.stats[k].boost(stp)  # possible exception 2
            except MergedResource:  # nonblocking exception
                self.stat_points_tracker.free_resource(stp)

    @property
    def level(self) -> int:
        return floor(self.config.get_dp() / 100)

    @property
    def presence(self):
        return self.level * 5

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
