from util.config import ModuleConfig, Module
from util.parameters import Attribute
from util.abilities import Ability
from common.resources import DevelopmentPoint
from general import POW
from math import floor

class MagicConfig(ModuleConfig):
    def __init__(self, zeon_cost, ma_multiple_cost, mp_cost, ml_per_level, summon_cost, control_cost, bind_cost, banish_cost,
                 zeon_per_level, summon_per_level, control_per_level, bind_per_level, banish_per_level, **kwargs):
        self.zeon_cost = zeon_cost
        self.ma_multiple_cost = ma_multiple_cost
        self.mp_cost = mp_cost
        self.summon_cost = summon_cost
        self.control_cost = control_cost
        self.bind_cost = bind_cost
        self.banish_cost = banish_cost
        self.summon_per_level = summon_per_level
        self.control_per_level = control_per_level
        self.bind_per_level = bind_per_level
        self.banish_per_level = banish_per_level
        self.ml_per_level = ml_per_level
        self.zeon_per_level = zeon_per_level
        super().__init__(**kwargs)

class MagicAccumulation(Attribute):
    BASE_RESOURCE = DevelopmentPoint

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[DevelopmentPoint] = self.calculate_multiples

    def calculate_multiples(self, boost):
        return floor(boost['boost'].value/boost['cost'])*self.bonuses.get(POW)['f'](self)

    def calculate_innate(self):
        if self.value < 55:
            return 10
        elif self.value < 75:
            return 20
        elif self.value < 95:
            return 30
        elif self.value < 115:
            return 40
        elif self.value < 135:
            return 50
        elif self.value < 155:
            return 60
        elif self.value < 185:
            return 70
        elif self.value < 200:
            return 80
        else:
           return 90

class MagicProjection(Ability):
    BASE_RESOURCE = DevelopmentPoint
    STAT = 'PER'

class MagicLevel(Attribute):
    BASE_RESOURCE = DevelopmentPoint
    DEFAULT_BASE_RESOURCE_COST = 5

class MaximumZeon(Attribute):
    BASE_RESOURCE = DevelopmentPoint
    BASE_VALUE = 20


class ZeonRegeneration(Attribute):
    BASE_RESOURCE = DevelopmentPoint

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[DevelopmentPoint] = self.calculate_multiple

    def calculate_multiple(self, boost):
        return floor(boost['boost'].value/boost['cost'])*self.ma_bonus(self)

class InnateMagic(Attribute):
    pass

class Summon(Ability):
    STAT = 'POW'
    BASE_RESOURCE = DevelopmentPoint

class Control(Ability):
    STAT = 'WIL'
    BASE_RESOURCE = DevelopmentPoint

class Bind(Ability):
    STAT = 'POW'
    BASE_RESOURCE = DevelopmentPoint

class Banish(Ability):
    STAT = 'POW'
    BASE_RESOURCE = DevelopmentPoint

class Magic(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic_accumulation = MagicAccumulation(base_res_cost=self.config.ma_multiple_cost)
        self.magic_accumulation.add_bonus(*self.config.character.general.stats.get('POW').magic_accum_bonus())
        self.magic_projection = MagicProjection(presence_f=self.config.get_presence,
                                                stat_dict=self.config.character.general.stats,
                                                base_res_cost=self.config.mp_cost,
                                                base_lim_f=lambda: floor(self.config.get_dp()*self.config.dp_limit/2))
        self.magic_level = MagicLevel(base_lim_f=lambda: floor(self.config.get_dp()/10))
        self.magic_level.add_bonus(self, lambda x: self.config.get_level()*self.config.ml_per_level)
        self.magic_level.add_bonus(*self.config.character.general.stats.get('INT').magic_level_bonus())
        self.maximum_zeon = MaximumZeon(base_res_cost=self.config.zeon_cost/5)
        # fixme maximum zeon is almost an ability, apart from weird stat function
        self.maximum_zeon.add_bonus(self, lambda x: self.config.get_level()*self.config.zeon_per_level+self.config.get_presence())
        self.maximum_zeon.add_bonus(*self.config.character.general.stats.get('POW').zeon_bonus())
        self.zeon_regeneration = ZeonRegeneration(base_res_cost=self.config.ma_multiple_cost/2)
        self.zeon_regeneration.set_base_value_function(lambda: self.magic_accumulation.value)
        self.zeon_regeneration.ma_bonus = self.config.character.general.stats.get('POW').magic_accum_bonus()[1]
        self.innate_magic = InnateMagic()
        self.innate_magic.set_base_value_function(self.magic_accumulation.calculate_innate)
        self.summon = Summon(presence_f=lambda: 0, base_res_cost=self.config.summon_cost,
                             stat_dict=self.config.character.general.stats)
        self.summon.add_bonus(self, lambda x: self.config.summon_per_level*self.config.get_level())
        self.control = Control(presence_f=lambda: 0, base_res_cost=self.config.control_cost,
                             stat_dict=self.config.character.general.stats)
        self.control.add_bonus(self, lambda x: self.config.control_per_level*self.config.get_level())
        self.bind = Bind(presence_f=lambda: 0, base_res_cost=self.config.bind_cost,
                             stat_dict=self.config.character.general.stats)
        self.bind.add_bonus(self, lambda x: self.config.bind_per_level*self.config.get_level())
        self.banish = Banish(presence_f=lambda: 0, base_res_cost=self.config.banish_cost,
                             stat_dict=self.config.character.general.stats)
        self.banish.add_bonus(self, lambda x: self.config.banish_per_level*self.config.get_level())
        # todo: add magic buying here? or...