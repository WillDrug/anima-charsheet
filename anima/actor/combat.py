from anima.util.damage import Location, DamageType
from anima.util.exceptions import ClassMistmatch
from anima.util.mixins import Referencable, Searchable
from anima.util.bonuses import Bonus, Bonusable
from random import randint

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

    def defense_roll(self, defense_number, defense_type=None, roll=None):
        """
        This is implemented to be overridden by a cap function for PC
        :param defense_number: affects penalty
        :param defense_type: affects value
        :param roll: dice roll
        :return: int
        """
        if defense_number in self.penalties:
            penalty = self.penalties[defense_number]
        else:
            penalty = self.penalties[5]  # todo: pretty up if affected by advantages or styles much

        if roll is None:
            roll = randint(1, 20)

        if defense_type is not None:
            ability = self.source.access(f'defense.{defense_type}')
        else:
            ability = self.source.access('defense').max_of()

        return roll + ability + penalty

    def defense(self, defense_number: int, damage_type: DamageType, defense_type=None, roll: int = None,
                location: Location = Location.body):
        defense = self.defense_roll(defense_number, defense_type=defense_type, roll=roll)
        protection = self.protection.get_protection(location, damage_type)  # armour is always over cap
        
        final_ability = defense + protection

        # todo: implement extra functions for AoE and it's penalties, sizes, etc.

        return final_ability



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