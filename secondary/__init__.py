from util.exceptions import NotFound
from util.config import ModuleConfig, Module
from util.parameters import MultipartAttributeMixin
from util.abilities import Ability
from .resources import InnateBonusTracker, InnateBonus, Bonus, BonusTracker
from math import floor

class SecondaryConfig(ModuleConfig):
    def check_ability(self, skilllist):
        for skill in skilllist:
            if skill not in Skill.impl_list():
                raise NotFound(f'{skill} is not a valid secondary ability')

    def __init__(self, skill_costs: dict, skill_per_level: dict, **kwargs):
        self.check_ability([q for q in skill_costs])
        self.check_ability([q for q in skill_per_level])
        self.skill_costs = skill_costs
        self.skill_per_level = skill_per_level
        super().__init__(**kwargs)

class Skill(Ability):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[InnateBonus] = self.parse_innate

    def parse_innate(self, boost):
        return floor(boost['boost'].value/boost['cost'])*self.__stat_dict.get(self.STAT).modifier

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

    def base_value(self):
        append = 0
        if self.boosts.__len__() == 0:
            append = -30
        return append + super().base_value()

class Acrobatics(Skill):
    STAT = 'DEX'
    PHYSICAL = True

"""        'Acrobatics',
        'Athleticism',
        'Persuasion',
        'Style',
        'Empathy',
        'Notice',
        'Magic Appraisal',
        'Medicine',
        'Occult',
        'Composure',
        'Withstand Pain',
        'Poisons',
        'Sleight of Hand',
        'Stealth',
        'Alchemy',
        'Animism',
        'Forging',
        'Runes'"""

# class bonuses should not be calculated towards skill limit.

class Secondary(Module):
    DEFAULT_COST = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.innate_tracker = InnateBonusTracker(InnateBonus, limit_f=self.config.get_level)
        self.bonus_tracker = BonusTracker(Bonus, limit_f=lambda: self.config.get_level()*5)
        self.skills = {}
        for k in Skill.impl_list():
            self.skills[k] = Skill.impl_list()[k](presence_f=self.config.get_presence,
                                                  stat_dict=self.config.character.general.stats,
                                                  value_cap_f=lambda: 40+self.config.get_dp()*5+
                                                                      (40 if self.__class__.__name__ in
                                                                             self.config.skill_per_level
                                                                       else 0))
            self.bonus_tracker.add_local_limit(k, limit_f=self.config.get_level)