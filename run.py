from general import Stat
from character import Character
from util.parameters import Attribute
from combat import Attack
from inspect import getmro
from util.exceptions import OverLimit
from util.resources import Resource, ResourceTracker
from common.resources import DevelopmentPoint
tr = ResourceTracker(DevelopmentPoint)

char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 11, 'DEX': 11, 'AGI': 11})
char.combat.boost(char.combat.attack, 180)
print(char.combat.attack.heavy.value)
print(char.combat.attack.light.value)
print(char.combat.attack.ranged.value)
