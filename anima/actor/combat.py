from anima.util.damage import Location, DamageType
from anima.util.exceptions import ClassMistmatch
from anima.util.mixins import Referencable, Searchable
from anima.util.bonuses import Bonus, Bonusable


class ProtectionBonus(Bonus):
    def __init__(self, code, value, locations=Location.armour_locations(), damage_types=DamageType.all()):
        self.locations = locations
        self.damage_types = damage_types
        super().__init__(code, value)

class Protection(Bonusable, Referencable):
    def __init__(self):
        super().__init__()

    def get_protection(self, location, damage_type):
        return sum([q for q in self.bonuses if location in q.locations and damage_type in q.damage_types])

    def add_bonus(self, bonus: ProtectionBonus):
        if not isinstance(bonus, ProtectionBonus):
            raise ClassMistmatch(f'Protection cannot accept regular Bonus')
        super().add_bonus(bonus)


class CombatProfile(Referencable, Searchable):
    penalties = {
        1: 0,
        2: -6,
        3: -10,
        4: -14,
        5: -18
    }
    def __init__(self, source):
        self.source = source
        self.protection = Protection()
        self.weapons = set()

    def add_weapon(self, weapon: "Weapon"):
        if weapon in self.weapons:
            self.weapons.remove(weapon)
        self.weapons.add(weapon)

    def rem_weapon(self, weapon):
        self.weapons.remove(weapon)

    def get_weapon(self, weapon: str):
        return next((q for q in self.weapons if q == weapon))

    def attack(self, weapon, attack_types=(), damage_types=(), maneuvers=(), effects=()):
        pass


if __name__ == '__main__':
    p = Protection()
    arm = ProtectionBonus('gm', 4)
    arm2 = ProtectionBonus('gm2', 2, [Location.body, Location.arm], [DamageType.energy, DamageType.ballistic])
    p.add_bonus(arm)
    p.add_bonus(arm2)
    print(p.get_protection(Location.body, DamageType.energy))
    print(p.get_protection(Location.leg, DamageType.energy))
    print(p.get_protection(Location.body, DamageType.thrust))
    p.rem_bonus('gm')
    print(p.get_protection(Location.body, DamageType.thrust))