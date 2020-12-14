from combat import Light
from .damage import *
from math import floor

class Item:
    QUALITY = 0

    def __init__(self, quality=0):
        self.QUALITY = quality

class Weapon(Item):
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

    def __init__(self, stat_dict: dict, **kwargs):
        self.stat_dict = stat_dict
        super().__init__(**kwargs)

    @property
    def damage_bonus(self):
        return self.SDAMAGE  # might be self.stat_dict.get('STR').modifier

    @property
    def armour_penetration(self):
        return self.PENETRATION+floor(self.QUALITY/5)  # might be formula around self.stat_dict

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

# todo: special mixins

class Armour(Item):
    CUT = 0
    IMPACT = 0
    THRUST = 0
    BALLISTIC = 0
    FIRE = 0
    ELECTRICITY = 0
    COLD = 0
    ENERGY = 0

    def get_at(self, damage: Damage):
        return getattr(self, damage.__class__.__name__.upper())+floor(self.QUALITY/5)
