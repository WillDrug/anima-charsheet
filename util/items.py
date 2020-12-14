from combat import Light
from .damage import *
from math import floor

class Item:
    QUALITY = 0

    def __init__(self, quality=0):
        self.QUALITY = quality

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
