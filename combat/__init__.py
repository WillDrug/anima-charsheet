from util.config import ModuleConfig, Module
from util.parameters import MultipartAttributeMixin, ChoiceAttributeMixin, Ability
from util.parameters import Attribute
from util.exceptions import OverLimit, Panik
from math import floor
from common.resources import DevelopmentPoint

class CombatConfig(ModuleConfig):
    def __init__(self, attack_cost, defense_cost, domine_cost, domine_accumulation_cost, attack_bool, block_bool, dodge_bool, mk_per_level, **kwargs):
        self.attack_cost = attack_cost
        self.defense_cost = defense_cost
        self.domine_cost = domine_cost
        self.domine_accumulation_cost = domine_accumulation_cost
        self.attack_bool = attack_bool
        self.block_bool = block_bool
        self.dodge_bool = dodge_bool
        self.mk_per_level = mk_per_level
        super(CombatConfig, self).__init__(**kwargs)


class CombatAbility(Ability, MultipartAttributeMixin):
    INSTANCE_LIST = {}
    DEFAULT_SUM_BASE_RESOURCE_CAP = 50
    BASE_RESOURCE = DevelopmentPoint
    DEFAULT_BASE_RESOURCE_COST = 2
    IMBALANCE_LIMIT = 50

    @property
    def full_cost(self):  # fixme this is utterly stupid, may be this is too much.
        attack = 0
        defense = 0
        for q in self.INSTANCE_LIST[self.container]:
            # q is instance of attack or defense
            sm = sum([z['boost'].value for z in q.boosts if isinstance(z['boost'], self.BASE_RESOURCE)])
            if isinstance(q, Attack):
                attack += sm
            elif isinstance(q, Defense):
                defense += sm
            else:
                raise Panik('Attack ability imbalance calculation hinges on having just two subclasses :(')
        return attack, defense

    def check_sum_cost(self, update_value):
        # check sum cost AND imbalance
        attack, defense = self.full_cost
        if self.get_sum_base_resource_cap() is not None:
            if isinstance(self, Attack):
                if (attack/self.get_base_resource_cost() + update_value/self.get_base_resource_cost()) - defense/self.get_base_resource_cost() > self.IMBALANCE_LIMIT:
                    raise OverLimit(f'Combat imbalance check failed')
            else:
                if (defense/self.get_base_resource_cost() + update_value/self.get_base_resource_cost()) - attack/self.get_base_resource_cost() > self.IMBALANCE_LIMIT:
                    raise OverLimit(f'Combat imbalance check failed')
            if attack+defense > self.get_sum_base_resource_cap():
                raise OverLimit(f'Combat Abilities are capped at {self.get_sum_base_resource_cap()}')

    def check_cost(self, update_value):
        for q in self.INSTANCE_LIST[self.container]:
            if isinstance(q, self.__class__):
                continue
            if q.cost == 0:  # no imbalance limit 20% check
                if self.cost + update_value/self.get_base_resource_cost() > self.get_base_resource_cap():
                    raise OverLimit(f'Single combat attribute development is capped at {self.get_base_resource_cap()}')
            else:
                self.check_sum_cost(update_value)


class Attack(CombatAbility, ChoiceAttributeMixin):
    # fixme: find a better way to cancel Multipart Mixin for further subclasses
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

class Light(Attack):
    STAT = 'DEX'

class Heavy(Attack):
    STAT = 'STR'

class Ranged(Attack):
    STAT = 'PER'

class Defense(CombatAbility, ChoiceAttributeMixin):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

class Block(Defense):
    STAT = 'DEX'

class Dodge(Defense):
    STAT = 'AGI'

class Dominion(Attribute):
    BASE_RESOURCE = DevelopmentPoint
    DEFAULT_BASE_RESOURCE_COST = 2

class DominionAccumulation(Attribute):
    BASE_RESOURCE = DevelopmentPoint
    DEFAULT_BASE_RESOURCE_COST = 20

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

class STR(DominionAccumulation):  # todo same class names are an anti-pattern but THIS IS SO USEFUL :(
    pass
class DEX(DominionAccumulation):
    pass
class AGI(DominionAccumulation):
    pass
class CON(DominionAccumulation):
    pass
class POW(DominionAccumulation):
    pass
class WIL(DominionAccumulation):
    pass

class MaximumMartialKnowledge(Attribute):  # martial arts give MK, oh fuck me
    BASE_RESOURCE = DevelopmentPoint
    DEFAULT_BASE_RESOURCE_COST = 5

    def domine_detection_bonus(self):
        def bonus_append(ca):
            return self.value/2
        return self.__class__, bonus_append


class Combat(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack = CombatAbility('Attack', self, presence_f=self.config.get_presence,
                                    stat_dict=self.config.character.general.stats,
                                    base_lim_f=lambda: floor(self.config.get_dp()*0.2),
                                    sum_resource_cap_f=lambda: floor(self.config.get_dp()*0.5),
                                    base_res_cost=self.config.attack_cost)
        self.attack.add_bonus(self, lambda x: floor(2.5*(self.config.attack_bool+1)*self.config.get_level()))
        self.defense = CombatAbility('Defense', self, presence_f=self.config.get_presence,
                                     stat_dict=self.config.character.general.stats,
                                     base_lim_f=lambda: floor(self.config.get_dp()*0.2),
                                     sum_resource_cap_f=lambda: floor(self.config.get_dp()*0.5),
                                     base_res_cost=self.config.defense_cost)
        self.defense.block.add_local_bonus(self, lambda x: floor(
            2.5 * (self.config.block_bool + 1) * self.config.get_level()),
                                           limited=True)
        self.defense.dodge.add_local_bonus(self, lambda x: floor(
            2.5 * (self.config.dodge_bool + 1) * self.config.get_level()),
                                           limited=True)
        self.dominion = Dominion(base_res_cost=self.config.domine_cost)
        self.dominion.add_bonus(self, lambda x: floor(self.config.get_presence()/5))
        for stat in DominionAccumulation.impl_list():  # fixme: move into parameters?
            self.dominion.add_bonus(*self.config.character.general.stats.get(stat).domine_bonus())
        self.accumulations = {k: DominionAccumulation.impl_list()[k]() for k in DominionAccumulation.impl_list()}
        for k in self.accumulations:
            self.accumulations[k].add_bonus(*self.config.character.general.stats.get(k).domine_accum_bonus())
        self.maximum_martial_knowledge = MaximumMartialKnowledge(base_lim_f=lambda: floor(self.config.get_dp()/10))
        self.maximum_martial_knowledge.add_bonus(self, lambda x: self.config.get_level()*self.config.mk_per_level)
        self.combat_profiles = {}

    # todo add buy bonuses\penalties for profiles
    def get_profile(self, pclass):
        if pclass in self.combat_profiles:
            return self.combat_profiles[pclass]
        else:
            return pclass(self.config.character.general.stats)

    def set_profile(self, pclass, pinstance):
        self.combat_profiles[pclass] = pinstance