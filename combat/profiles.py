from math import floor

from . import Light, Heavy, Ranged

class CombatProfile:
    INITIATIVE = 0
    ATTACK_OPTIONS = [Light]
    BASE_DAMAGE = 10

    SDAMAGE = 0
    PENETRATION = 0
    CRITICAL = 0
    BREAKAGE = 0
    FORTITUDE = 0
    REACH = 0
    SIZE = 1

    PENALTY = 60

    def __init__(self, stat_dict: dict):
        self.stat_dict = stat_dict

    @property
    def damage_bonus(self):
        return self.SDAMAGE  # might be self.stat_dict.get('STR').modifier

    @property
    def armour_penetration(self):
        return self.PENETRATION  # might be formula around self.stat_dict

    @property
    def critical(self):
        return self.CRITICAL

    @property
    def breakage(self):
        return self.BREAKAGE

    @property
    def fortitude(self):
        return self.FORTITUDE

    @property
    def reach(self):
        return self.REACH

    @property
    def multiple_attack_penalty(self):
        return 10+self.SIZE*10

class Unarmed(CombatProfile):
    ATTACK_OPTIONS = [Light]
    INITIATIVE = 20
    BASE_DAMAGE = 10
    SDAMAGE = 0
    BREAKAGE = -2
    FORTITUDE = 10
    REACH = 1
    SIZE = 1  # fixme: not stated

    @property
    def armour_penetration(self):
        return 0 if self.stat_dict.get('STR').value <= 3 else floor((self.stat_dict.get('STR').value-5)/3)

class Longsword(CombatProfile):
    ATTACK_OPTIONS = [Light, Heavy]
    INITIATIVE = 0
    BASE_DAMAGE = 50
    BREAKAGE = 3
    FORTITUDE = 13
    REACH = 2
    SIZE = 2

    @property
    def damage_bonus(self):
        return self.stat_dict.get('STR').modifier

    @property
    def armour_penetration(self):
        return 0 if self.stat_dict.get('STR').value <= 3 else floor((self.stat_dict.get('STR').value-5)/3)
