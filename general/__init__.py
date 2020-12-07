
from util.exceptions import NotFound, NotEnoughData, Panik, OverLimit, MergedResource
from util.resources import Resource, ResourceTracker
from util.parameters import Attribute, MultipartAttributeMixin, ChoiceAttributeMixin
from util.config import ModuleConfig, Module
from util.abilities import Ability
from common.resources import CreationPoint, CreationPointTracker
from .resources import StatPoint
from math import floor, inf
import traceback


class GeneralConfig(ModuleConfig):
    def __init__(self, LPM_cost, init_per_level, life_points_per_level, **kwargs):
        self.LPM_cost = LPM_cost
        self.init_per_level = init_per_level
        self.LP_per_level = life_points_per_level
        super(GeneralConfig, self).__init__(**kwargs)


class Stat(Attribute, MultipartAttributeMixin):
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
        return min(self.base_value() +
                   self.__stat_point_value() +
                   sum([
                       floor(q['boost'].value / q['cost']) for q in self.boosts
                       if q['limited'] and not isinstance(q['boost'], self.BASE_RESOURCE)
                   ]) +
                   sum([self.bonuses[q]['f'](self) for q in self.bonuses if self.bonuses[q]['limited']]),
                   self.get_value_cap()) + \
               sum([floor(q['boost'].value / q['cost']) for q in self.boosts if not q['limited']]) + \
               sum([self.bonuses[q]['f'](self) for q in self.bonuses if not self.bonuses[q]['limited']])

    def boost(self, res: Resource, cost=None,
              limited=True):  # limited is VALUE LIMIT. COST limit always applies for base_resource
        if isinstance(res, self.BASE_RESOURCE):
            self.check_cost(res.value)
            if any([isinstance(q, self.BASE_RESOURCE) for q in self.boosts]):
                cr = [q for q in self.boosts if isinstance(q, self.BASE_RESOURCE)].pop()
                cr.set_value(cr.get_value() + res.value)
                raise MergedResource()
            cost = self.get_base_resource_cost()  # fixme
        if isinstance(res, CreationPoint):
            res.set_usage(f'Plus {res.value} to {self.__class__.__class__}', stat=True)
        else:
            res.set_usage(f'Plus {res.value} to {self.__class__}')
        if cost is None:
            cost = 1
        self.boosts.append({'boost': res, 'limited': limited, 'cost': cost})

    def mod_bonus(self):
        def bonus_append(calling_attribute):
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0
            return self.modifier

        return self.__class__, bonus_append

    def domine_bonus(self):
        def bonus_append(calling_attribute):
            if self.value < 11:
                return self.value
            elif self.value < 20:
                return (self.value-10)*2+self.value
            else:
                return (self.value-10)*3

        return self.__class__, bonus_append

    def domine_accum_bonus(self):
        def bonus_append(calling_attribute):  # fixme is this a formula?
            if self.value < 10:
                return 1
            elif self.value < 13:
                return 2
            elif self.value < 16:
                return 3
            else:
                return 4

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
            return 10 * self.value + self.modifier

        return self.__class__, bonus_append

    def regen_bonus(self):
        def bonus_append(calling_attribute):
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0
            if self.value >= 1 and self.value <= 2:
                return 0
            elif self.value >= 3 and self.value <= 7:
                return 1
            elif self.value >= 8 and self.value <= 9:
                return 2
            elif self.value == 10:
                return 3
            elif self.value == 11:
                return 4
            elif self.value == 12:
                return 5
            elif self.value == 13:
                return 6
            elif self.value == 14:
                return 7
            elif self.value == 15:
                return 8
            elif self.value == 16:
                return 9
            elif self.value == 17:
                return 10
            elif self.value == 18:
                return 11
            elif self.value == 19:
                return 12
            elif self.value == 20:
                return 12

        return self.__class__, bonus_append


class INT(Stat):
    PHYSICAL = False


class POW(Stat):
    PHYSICAL = False

    def magic_accum_bonus(self):
        def bonus_append(maa):
            return self.value*(1+sum([floor(q['boost'].value/q['cost']) for q in maa.boosts if isinstance(q['boost'], maa.BASE_RESOURCE)]))

        return self, bonus_append


class WIL(Stat):
    PHYSICAL = False


class PER(Stat):
    PHYSICAL = False


class MaximumLifePoints(Attribute):
    BASE_VALUE = 20

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
    @property
    def modifier(self):
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
    @property
    def modifier(self):
        """
        :return: Movement in meters
        """
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


class Regeneration(Attribute):
    @property
    def modifier(self):
        # regen, regen rest, penalty reduction
        # fixme: change this to be usable by character controller
        if self.value == 1:
            return "10d", "5d", "-5d"
        elif self.value == 2:
            return "20d", "10d", "-5d"
        elif self.value == 3:
            return "30d", "15d", "-5d"
        elif self.value == 4:
            return "40d", "20d", "-10d"
        elif self.value == 5:
            return "50d", "25d", "-10d"
        elif self.value == 6:
            return "75d", "30", "-15d"
        elif self.value == 7:
            return "100d", "100d", "-20d"
        elif self.value == 8:
            return "250d", "200d", "-25d"
        elif self.value == 9:
            return "500d", "NA", "-30d"
        elif self.value == 10:
            return "1m", "NA", "-40d"
        elif self.value == 11:
            return "2m", "NA", "-50d"
        elif self.value == 12:
            return "5m", "NA", "-5h"
        elif self.value == 13:
            return "10m", "NA", "-10h"
        elif self.value == 14:
            return "1t", "NA", "-15h"
        elif self.value == 15:
            return "5t", "NA", "-20h"
        elif self.value == 16:
            return "10t", "NA", "-10m"
        elif self.value == 17:
            return "25t", "NA", "-10m"
        elif self.value == 18:
            return "50t", "NA", "-25m"
        elif self.value == 19:
            return "100t", "NA", "ALL"
        elif self.value == 20:
            return "250t", "NA", "ALL"


class MaximumMentalHealth(Attribute):
    iwp = None

    def pass_iwp(self, int, wil, pow):
        self.iwp = lambda: int.value + wil.value + pow.value

    def stat_bonus(self):
        if self.iwp is None:
            raise NotFound('Use pass_iwp first')

        # self bonus
        def bonus_append(calling_instance):
            if self.iwp() >= 3 >= self.iwp():
                return None
            elif self.iwp() >= 9 >= self.iwp():
                return 20
            elif self.iwp() >= 13 >= self.iwp():
                return 30
            elif self.iwp() >= 16 >= self.iwp():
                return 50
            elif self.iwp() >= 19 >= self.iwp():
                return 80
            elif self.iwp() >= 21 >= self.iwp():
                return 120
            elif self.iwp() >= 25 >= self.iwp():
                return 150
            elif self.iwp() >= 29 >= self.iwp():
                return 200
            elif self.iwp() >= 32 >= self.iwp():
                return 350
            elif self.iwp() >= 36 >= self.iwp():
                return 500

        return self.__class__, bonus_append
    @property
    def modifier(self):
        """
        Returns mental health threshold.
        :return:
        """
        if self.iwp() >= 3 >= self.iwp():
            return None
        elif self.iwp() >= 9 >= self.iwp():
            return 5
        elif self.iwp() >= 13 >= self.iwp():
            return 10
        elif self.iwp() >= 16 >= self.iwp():
            return 15
        elif self.iwp() >= 19 >= self.iwp():
            return 20
        elif self.iwp() >= 21 >= self.iwp():
            return 25
        elif self.iwp() >= 25 >= self.iwp():
            return 30
        elif self.iwp() >= 29 >= self.iwp():
            return 40
        elif self.iwp() >= 32 >= self.iwp():
            return 50
        elif self.iwp() >= 36 >= self.iwp():
            return 60

class Resistance(Ability, ChoiceAttributeMixin):
    IGNORE = ['STAT']
    GNOSIS = False


class Physical(Resistance):
    STAT = 'CON'


class Magic(Resistance):
    STAT = 'POW'


class Psychic(Resistance):
    STAT = 'WIL'


class Critical(Resistance):
    STAT = 'CON'


class Social(Resistance):
    STAT = 'WIL'
    GNOSIS = True


class Surprise(Resistance):
    STAT = 'PER'
    GNOSIS = True

class MaximumWillpower(Attribute):
    pass

class MaximumFatigue(Attribute):
    pass

# todo: refactor, move attributes to a separate file
class General(Module):
    def get_class_lp(self):
        def class_lp(inst):
            return self.config.get_level() * self.config.LP_per_level

        return class_lp

    def get_max_stat_points(self):
        return 65

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stat_points_tracker = ResourceTracker(StatPoint, self.get_max_stat_points)
        self.stats = {k: Stat(k, self, base=StatPoint) for k in
                      Stat.impl_list()}  # fixme: possibly change to clear set attributes

        self.maximum_life_points = MaximumLifePoints(self.config.LPM_cost)
        self.maximum_life_points.add_bonus(self.config.__class__, lambda x: self.config.get_level() * self.config.LP_per_level)
        self.maximum_life_points.add_bonus(*self.stats.get('CON').health_bonus())

        self.initiative = Initiative()
        self.initiative.add_bonus(self.config.__class__, lambda x: self.config.get_level() * self.config.init_per_level)
        self.initiative.add_bonus(*self.stats.get('DEX').mod_bonus())  # todo: think about this
        self.initiative.add_bonus(*self.stats.get('AGI').mod_bonus())

        self.cp_tracker = CreationPointTracker(CreationPoint, limit_f=self.config.get_level)

        self.movement = Movement()
        self.movement.add_bonus(*self.stats.get('AGI').bonus())

        self.weight = Weight()
        self.weight.add_bonus(*self.stats.get('STR').bonus())

        # fixme: either do a tracker for every resource or turn those into Attributes
        # fixme: make low fatigue affect shit
        self.maximum_fatigue = MaximumFatigue()
        self.maximum_fatigue.add_bonus(*self.stats.get('CON').bonus())
        self.maximum_willpower = MaximumWillpower()
        self.maximum_willpower.add_bonus(*self.stats.get('WIL').bonus())

        self.regen = Regeneration()
        self.regen.add_bonus(*self.stats.get('CON').regen_bonus())

        self.maximum_mental_health = MaximumMentalHealth()
        self.maximum_mental_health.pass_iwp(self.stats.get('INT'), self.stats.get('WIL'), self.stats.get('POW'))
        self.maximum_mental_health.set_base_value_function(self.config.get_presence)

        self.resistance = Resistance(presence_f=lambda: self.config.get_presence()*2, stat_dict=self.stats)
        self.resistance.add_bonus(self, lambda x: 0 if not x.GNOSIS else floor(self.config.get_gnosis()/5)*40)

    @property
    def stat_costs(self):
        return Stat.cls_full_cost(self)

    def invest_into_stats(self, stats: dict):  # fixme better name
        for k in stats:
            if k not in Stat.impl_list():
                raise NotFound(f'{k} is not a stat')
            stp = None
            try:
                stp = self.stat_points_tracker.emit_resource(stats[k])  # possible exception 1
                self.boost_stat(k, stp)  # possible exception 2
            except MergedResource:  # nonblocking exception
                if stp is not None:
                    self.stat_points_tracker.free_resource(stp)
            except Exception as e:  # fixme: wide exception net, poor Resource tracking
                if stp is not None:
                    self.stat_points_tracker.free_resource(stp)
                raise e

    def boost_stat(self, stat_name, res: Resource):
        stat = self.stats.get(stat_name)
        if stat is None:
            raise NotFound(f'{stat_name} is not a stat')
        stat.boost(res)

    def boost_stat_with_cp(self, stat_name, value):  # todo: catch? anything?
        cp = self.cp_tracker.emit_resource(value=value, limit=self.config.get_level())
        try:
            return self.boost_stat(stat_name, cp)
        except Exception as e: # fixme: wide exception net, poor Resource tracking
            self.cp_tracker.free_resource(cp)
            raise e


if __name__ == '__main__':
    a = Stat('STR', 1)
    b = Stat('STR', 1)
    print(a.full_cost(1))
    del b
    print(a.full_cost(1))
