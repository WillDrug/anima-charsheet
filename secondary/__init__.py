from util.exceptions import NotFound, NotAvailable
from util.config import ModuleConfig, Module
from util.parameters import MultipartAttributeMixin
from util.abilities import Ability
from .resources import InnateBonusTracker, InnateBonus, Bonus, BonusTracker, TertiaryPoint, ResourceTracker
from math import floor

class SecondaryConfig(ModuleConfig):
    def check_ability(self, skilllist):
        for skill in skilllist:
            if skill not in Skill.impl_list():
                raise NotFound(f'{skill} is not a valid secondary ability')

    def __init__(self, skill_costs: dict, skill_per_level: dict, tertiary_pts, **kwargs):
        self.check_ability([q for q in skill_costs])
        self.check_ability([q for q in skill_per_level])
        self.skill_costs = skill_costs
        self.skill_per_level = skill_per_level
        self.tertiary_pts = tertiary_pts
        super().__init__(**kwargs)

class Skill(Ability):
    DEFAULT_BASE_RESOURCE_COST = 2
    MENTAL = None

    @classmethod
    def get_name(cls):
        return cls.__name__ if not hasattr(cls, 'repname') else cls.repname

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[InnateBonus] = self.parse_innate

    def parse_innate(self, boost):
        return floor(boost['boost'].value/boost['cost'])*self._stat_dict.get(self.STAT).modifier

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.get_name(): subcl for subcl in cls.__subclasses__()}

    def base_value(self):
        append = 0
        if self.boosts.__len__() == 0:
            append = -30
        return append + super().base_value()



class Acrobatics(Skill):
    STAT = 'AGI'
    MENTAL = False

class Athleticism(Skill):
    STAT = 'STR'
    MENTAL = False

class Persuasion(Skill):
    STAT = 'INT'
    MENTAL = True

class Style(Skill):
    STAT = 'POW'
    MENTAL = True

class Empathy(Skill):
    STAT = 'PER'
    MENTAL = True

class Notice(Skill):
    STAT = 'PER'
    MENTAL = True

class MagicAppraisal(Skill):
    repname = 'Magic Appraisal'
    STAT = 'POW'
    MENTAL = True

class Medicine(Skill):
    STAT = 'INT'
    MENTAL = True  # fixme is this physical?

class Occult(Skill):
    STAT = 'INT'
    MENTAL = True

class Composure(Skill):
    STAT = 'WIL'
    MENTAL = False

class WithstandPain(Skill):
    repname = 'Withstand Pain'
    STAT = 'CON'
    MENTAL = False

    def health_bonus(self):
        def bonus_append(mlp):
            return floor(sum([self.parse_boost({'boost': q['boost'], 'cost': 1}) for q in self.boosts])/4)
        return self.__class__.__name__, bonus_append

class Poisons(Skill):
    STAT = 'INT'
    MENTAL = True # fixme physical?

class SleightOfHand(Skill):
    repname = 'Sleight of Hand'
    STAT = 'DEX'
    MENTAL = False

class Stealth(Skill):
    STAT = 'AGI'
    MENTAL = False

class Alchemy(Skill):
    STAT = 'INT'
    MENTAL = True

class Animism(Skill):
    STAT = 'POW'
    MENTAL = True

class Forging(Skill):
    STAT = 'DEX'
    MENTAL = False

class Runes(Skill):
    STAT = 'DEX'
    MENTAL = False


class DominionDetection(Skill):
    repname = 'Dominion Detection'
    STAT = 'POW'
    DEFAULT_BASE_RESOURCE_CAP = 0
    ACTIVATED = False

    def base_value(self):
        if not self.ACTIVATED:
            raise NotAvailable(f'This character cannot detect Ki')
        return super(Skill, self).base_value()

class DominionConcealment(Skill):
    repname = 'Dominion Concealment'
    STAT = 'POW'
    DEFAULT_BASE_RESOURCE_CAP = 0
    ACTIVATED = False

    def base_value(self):
        if not self.ACTIVATED:
            raise NotAvailable(f'This character cannot conceal Ki')
        return super().super().base_value()

class Secondary(Module):
    def get_value_cap(self, skillname):
        def value_cap_calc():
            return 40+floor(self.config.get_dp()/5)+(0 if skillname not in self.config.skill_per_level else 40)
        return value_cap_calc

    def __init__(self, *args, **kwargs):
        # fixme cheeky hack?
        super().__init__(*args, **kwargs)
        self.innate_tracker = InnateBonusTracker(InnateBonus, limit_f=self.config.get_level)
        self.bonus_tracker = BonusTracker(Bonus, limit_f=lambda: self.config.get_level()*25)
        self.tertiary_tracker = ResourceTracker(TertiaryPoint, limit_f=lambda: (self.config.get_dp()/20)*(self.config.tertiary_pts/5))  # fixme just divide original values.
        self.skills = {}
        for k in Skill.impl_list():
            self.skills[k] = Skill.impl_list()[k](presence_f=self.config.get_presence,
                                                  stat_dict=self.config.character.general.stats,
                                                  base_res_cost=self.config.skill_costs.get(k),
                                                  value_cap_f=self.get_value_cap(k))

            if k in self.config.skill_per_level:
                self.skills[k].add_bonus(self, lambda x: self.config.get_level()*self.config.skill_per_level[x.__class__.get_name()])
            self.bonus_tracker.add_local_limit(k, limit_f=self.config.get_level)
        self.config.character.general.maximum_life_points.add_bonus(*self.get_skill('Withstand Pain').health_bonus())

    def add_skill(self, skill: str, stat: str, mental: bool):
        attr = Skill(presence_f=self.config.get_presence,
                     stat_dict=self.config.character.general.stats)
        attr.STAT = stat
        attr.DEFAULT_BASE_RESOURCE_COST = 1
        attr.BASE_RESOURCE = TertiaryPoint
        attr.MENTAL = mental
        self.skills[skill] = attr

    def get_skill(self, skill):
        attr = self.skills.get(skill)
        if attr is None:
            raise NotFound(f'{skill} is not a Secondary or Tertiary skill, matey')
        return attr

    def boost_tertiary(self, attr, value):
        tp = self.tertiary_tracker.emit_resource(value)
        return attr.boost(tp)

    def boost_skill(self, skill, value):
        attr = self.get_skill(skill)
        if attr.__class__.get_name() in Skill.impl_list():
            return self.boost(self.get_skill(skill), value)
        else:
            return self.boost_tertiary(attr, value)

    def boost_with_innate(self, skill, value=1):
        attr = self.get_skill(skill)
        innate = self.innate_tracker.emit_resource(value)
        return attr.boost(innate, mental=attr.MENTAL, cost=1)

    def boost_with_bonus(self, skill, value=5):
        attr = self.get_skill(skill)
        boost = self.bonus_tracker.emit_resource(value, attr)
        attr.boost(boost, cost=1)