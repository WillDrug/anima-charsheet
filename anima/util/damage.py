"""
In this file, a base reference for damage type and location should be managed.
"""
from random import randint
from typing import Callable
from enum import Enum, auto
from anima.util.mixins import Referencable

class Location(Enum):
    """
    This is used for armour values, for targeted strikes and to get a random bodypart for a crit
    """
    body = auto()
    stomach = auto()
    heart = auto()
    groin = auto()
    arm = auto()
    shoulder = auto()
    elbow = auto()
    hand = auto()
    leg = auto()
    knee = auto()
    calf = auto()
    foot = auto()
    head = auto()
    neck = auto()
    eye = auto()

    @classmethod
    def get_random(cls, number=None):
        if number is None:
            number = randint(1, 100)
        results = {
            range(1, 12): cls.body,
            range(12, 17): cls.stomach,
            range(17, 23): cls.heart,
            range(23, 29): cls.groin,
            range(29, 42): cls.arm,
            range(42, 48): cls.shoulder,
            range(48, 54): cls.elbow,
            range(54, 60): cls.hand,
            range(60, 73): cls.leg,
            range(73, 79): cls.knee,
            range(79, 85): cls.calf,
            range(85, 91): cls.foot,
            range(91, 95): cls.head,
            range(95, 98): cls.neck,
            range(98, 101): cls.eye
        }
        for k in results:
            if number in k:
                return results[k]
        else:
            raise ValueError(f'{number} is not a proper result of a d100')

    @classmethod
    def armour_locations(cls):
        return [Location.body, Location.arm, Location.leg, Location.head]

    @staticmethod
    def all():
        return [q._name_ for q in Location]

    @classmethod
    def get_by_name(cls, name):
        return next((q for q in cls if q._name_ == name), None)


class DamageType(Enum):
    cut = auto()
    thrust = auto()
    impact = auto()
    ballistic = auto()
    heat = auto()
    electricity = auto()
    cold = auto()
    energy = auto()

    @staticmethod
    def all():
        return [q for q in DamageType]

    def __repr__(self):
        return f"<DamageType({self._name_})>"

    def __str__(self):
        return self.__repr__()

class Damage:
    def __init__(self, dtype: DamageType, damage: int, location: Location = None):
        self.dtype = dtype
        self.damage = damage
        self.location = location

    def __repr__(self):
        return f'<Damage({self.damage} of {self.dtype} at {self.location})>'


class DamageFormula(Referencable):
    def __init__(self, dtype: DamageType, base: Callable, bonus: Callable, hands=1, iam=None):
        self.__base = base
        self.__bonus = bonus
        self.__type = dtype
        self.hands = hands
        self.iam = iam if iam is not None else dtype._name_+str(self.get_damage())

    def get_base(self):
        return self.__base()

    def get_bonus(self):
        return self.__bonus()

    def get_damage(self):
        return self.get_base()+self.get_bonus()

    def get_type(self):
        return self.__type

    def __call__(self, location=None):
        return Damage(self.__type, self.get_damage(), location=location)

    def __repr__(self):  # why am I making a generalization to support multi-handed characters? the fuck?
        return f'<DamageFormula[{self.iam}]({self.get_base()}+{self.get_bonus()} of ' \
               f'{self.get_type()} {"("+self.hands+"h)" if self.hands>1 else ""})>'

if __name__ == '__main__':
    print(DamageType.all())
    print(isinstance(DamageType.cut, DamageType))
