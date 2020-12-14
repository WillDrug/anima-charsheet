from util.items import Weapon
from combat import Light, Heavy
from math import floor

class Unarmed(Weapon):
    ATTACK_OPTIONS = [Light]
    INITIATIVE = 20
    BASE_DAMAGE = 10
    SDAMAGE = 0


class Longsword(Weapon):
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
