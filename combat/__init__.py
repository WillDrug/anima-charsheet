

class CombatConfig:
    def __init__(self, limit, attack_cost, defense_cost, domine_cost, domine_accumulation_cost):
        self.limit = limit
        self.attack_cost = attack_cost
        self.defense_cost = defense_cost
        self.domine_cost = domine_cost
        self.domine_accumulation_cost = domine_accumulation_cost


class Combat:
    def __init__(self, config: CombatConfig):
        pass