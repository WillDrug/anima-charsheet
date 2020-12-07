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
char.general.invest_into_stats({'STR': 11, 'CON': 11, 'DEX': 11, 'AGI': 11})
char.combat.boost(char.combat.attack, 180)
char.combat.boost(char.combat.dominion, 100)
char.combat.boost(char.combat.maximum_martial_knowledge, 10)
print(char.combat.maximum_martial_knowledge.value)