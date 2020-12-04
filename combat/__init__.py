from util.config import ModuleConfig
from util.parameters import Attribute, MultipartAttributeMixin
from util.exceptions import OverLimit

class CombatConfig(ModuleConfig):
    def __init__(self, attack_cost, defense_cost, domine_cost, domine_accumulation_cost, attack_bool, block_bool, dodge_bool, **kwargs):
        self.attack_cost = attack_cost
        self.defense_cost = defense_cost
        self.domine_cost = domine_cost
        self.domine_accumulation_cost = domine_accumulation_cost
        self.attack_bool = attack_bool
        self.block_bool = block_bool
        self.dodge_bool = dodge_bool
        super(CombatConfig, self).__init__(**kwargs)

class Combat:
    def __init__(self, config: CombatConfig):
        self.config = config
        # (2.5 if self.config.attack_bool else 5)*self.config.get_level()