
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
    def __init__(self, init_per_level, life_points_per_level, **kwargs):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[StatPoint] = self.__parse_stat_point

    def get_value_cap(self):
        return self.DEFAULT_VALUE_CAP + (1 if self.PHYSICAL else 3)

    # todo: limit inhuman\zen to appropriate caps depending on mental\physical
    @property
    def cost(self):
        return self.value + (self.value - 9 if self.value >= 10 else 0)

    @property
    def modifier(self):
        return (self.value - 5) * 5 if self.value >= 5 else -10 * (5 - self.value)  # kill me

    def __parse_stat_point(self, boost):
        """
        This silly function is because point buy is WEEEEIRD
        :return:
        """
        return boost['boost'].value if boost['boost'].value < 10 else floor(9 + ((boost['boost'].value - 9) / 2))

    # todo: see if this can be refactored into :pass
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
            #print(f'{self.__class__}, {self.value}')
            if self.value < 11:
                return self.value
            elif self.value < 20:
                return (self.value-10)*2+10
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

    def secondary_bonus(self):
        def bonus_append(skill):
            return self.modifier*skill.innate
        return self, bonus_append

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
            return 10 * self.value

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

    def pp_bonus(self):
        def bonus_append(mpp):
            return self.value/5
        return self.__class__, bonus_append

    def magic_level_bonus(self):
        def bonus_append(ml):
            levels = 0
            if self.value <= 5:
                levels = 0
            elif self.value == 6:
                levels = 10
            elif self.value == 7:
                levels = 20
            elif self.value == 8:
                levels = 30
            elif self.value == 9:
                levels = 40
            elif self.value == 10:
                levels = 50
            elif self.value == 11:
                levels = 75
            elif self.value == 12:
                levels = 100
            elif self.value == 13:
                levels = 125
            elif self.value == 14:
                levels = 150
            elif self.value == 15:
                levels = 175
            elif self.value == 16:
                levels = 200
            elif self.value == 17:
                levels = 250
            elif self.value == 18:
                levels = 300
            elif self.value == 19:
                levels = 350
            elif self.value >= 20:
                levels = 400
            return levels
        return self.__class__, bonus_append

class POW(Stat):
    PHYSICAL = False

    def magic_accum_bonus(self):
        def bonus_append(maa):
            accum = 0
            if self.value <= 7:
                accum = 5
            elif 8 <= self.value <= 11:
                accum = 10
            elif 12 <= self.value <= 14:
                accum = 15
            elif self.value == 15:
                accum = 20
            elif 16 <= self.value <= 17:
                accum = 25
            elif 18 <= self.value <= 19:
                accum = 30
            elif self.value >= 20:
                accum = 35
            return accum  #*(1+sum([floor(q['boost'].value/q['cost']) for q in maa.boosts
                          #         if isinstance(q['boost'], maa.BASE_RESOURCE)]))

        return self.__class__, bonus_append

    def zeon_bonus(self):
        def bonus_append(mz):
            return 10*self.value+self.modifier
        return self.__class__.__name__, bonus_append

class WIL(Stat):
    PHYSICAL = False
    def psy_potential_bonus(self):
        def bonus_append(pot):
            if self.value <= 4:
                return 0
            elif self.value == 5:
                return 10
            elif self.value == 6:
                return 20
            elif self.value == 7:
                return 30
            elif self.value == 8:
                return 40
            elif self.value == 9:
                return 50
            elif self.value == 10:
                return 60
            elif self.value == 11:
                return 65
            elif self.value == 12:
                return 70
            elif self.value == 13:
                return 75
            elif self.value == 14:
                return 80
            elif self.value == 15:
                return 85
            elif self.value == 16:
                return 90
            elif self.value == 17:
                return 100
            elif self.value == 18:
                return 110
            elif self.value == 19:
                return 120
            elif self.value == 20:
                return 130
            else:
                raise NotEnoughData(f'How is your stat > 20?!')

        return self.__class__, bonus_append

class PER(Stat):
    PHYSICAL = False


class MaximumLifePoints(Attribute):
    BASE_VALUE = 20


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

        self.maximum_life_points = MaximumLifePoints()
        self.maximum_life_points.add_bonus(self.config.__class__, lambda x: self.config.get_level() * self.config.LP_per_level)
        self.maximum_life_points.add_bonus(*self.stats.get('CON').health_bonus())
        self.maximum_life_points.add_bonus(*self.stats.get('STR').mod_bonus())

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
        cp = self.cp_tracker.emit_resource(value=value)
        try:
            return self.boost_stat(stat_name, cp)
        except Exception as e:  # fixme: wide exception net, poor Resource tracking
            self.cp_tracker.free_resource(cp)
            raise e


if __name__ == '__main__':
    a = Stat('STR', 1)
    b = Stat('STR', 1)
    print(a.full_cost(1))
    del b
    print(a.full_cost(1))
