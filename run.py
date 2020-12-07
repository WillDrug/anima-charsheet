from general import Stat
from character import Character
from util.parameters import Attribute
from combat import Attack, Dominion
from inspect import getmro
from util.exceptions import OverLimit
from util.resources import Resource, ResourceTracker
from common.resources import DevelopmentPoint

tr = ResourceTracker(DevelopmentPoint)

char = Character('Warrior', dp=900)
char.general.invest_into_stats({'STR': 11, 'CON': 11, 'DEX': 11, 'POW': 11})
char.magic.boost(char.magic.magic_accumulation, 2)
print(char.magic.magic_accumulation.value)

