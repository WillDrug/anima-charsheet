"""
In this file, a base reference for damage type and location should be managed.
"""
from random import randint
from enum import Enum, auto


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


if __name__ == '__main__':
    print(DamageType.all())
