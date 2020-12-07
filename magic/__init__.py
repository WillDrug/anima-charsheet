from util.config import ModuleConfig, Module
from util.parameters import Attribute
from util.abilities import Ability
from common.resources import DevelopmentPoint
from math import floor

class MagicConfig(ModuleConfig):
    def __init__(self, zeon_cost, ma_multiple_cost, mp_cost, summon_cost, control_cost, bind_cost, banish_cost, **kwargs):
        self.zeon_cost = zeon_cost
        self.ma_multiple_cost = ma_multiple_cost
        self.mp_cost = mp_cost
        self.summon_cost = summon_cost
        self.control_cost = control_cost
        self.bind_cost = bind_cost
        self.banish_cost = banish_cost
        super().__init__(**kwargs)

class MagicAccumulation(Attribute):
    BASE_RESOURCE = DevelopmentPoint

    @property
    def value(self):  # change to yeet DP, they are used in STAT bonus.
        limited = self.base_value() + sum([floor(q['boost'].value / q['cost']) for q in self.boosts if q['limited']
                                           and not isinstance(q['boost'], self.BASE_RESOURCE)]) + \
                  sum([self.bonuses[q]['f'](self) for q in self.bonuses if self.bonuses[q]['limited']])
        if self.get_value_cap() is not None:
            limited = min(limited, self.get_value_cap())
        return limited + \
               sum([floor(q['boost'].value / q['cost']) for q in self.boosts if not q['limited']
                    and not isinstance(q['boost'], self.BASE_RESOURCE)]) + \
               sum([self.bonuses[q]['f'](self) for q in self.bonuses if not self.bonuses[q]['limited']])

class Magic(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.magic_accumulation = MagicAccumulation(base_res_cost=self.config.ma_multiple_cost)
        self.magic_accumulation.add_bonus(*self.config.character.general.stats.get('POW').magic_accum_bonus())