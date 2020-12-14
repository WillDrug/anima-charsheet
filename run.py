from general import Stat
from character import Character
from util.parameters import Attribute
from combat import Attack, Dominion
from inspect import getmro
from util.exceptions import OverLimit
from util.resources import Resource, ResourceTracker
from common.resources import DevelopmentPoint
from character.controller import Controller
from combat.profiles import Unarmed

char = Character('Wizard', dp=800)
char.general.invest_into_stats(dict(STR=5, DEX=5, AGI=8, CON=8, INT=11, POW=11, WIL=6, PER=11))
char.general.boost_stat_with_cp('POW', 2)
char.general.boost_stat_with_cp('INT', 2)
char.magic.boost(char.magic.magic_accumulation, 150)
char.magic.boost(char.magic.magic_projection, 230)
char.magic.boost(char.magic.maximum_zeon, 75)
char.magic.boost(char.magic.zeon_regeneration, 25)

char.secondary.boost_skill('Acrobatics', 5)
char.secondary.boost_skill('Persuasion', 50)
char.secondary.boost_skill('Style', 50)
char.secondary.boost_skill('Empathy', 50)
char.secondary.boost_skill('Notice', 50)
char.secondary.boost_skill('Magic Appraisal', 60)
char.secondary.boost_skill('Medicine', 20)
char.secondary.boost_skill('Occult', 20)
char.secondary.boost_skill('Composure', 5)
char.secondary.boost_skill('Stealth', 10)
char.secondary.boost_with_innate('Style', 1)
char.secondary.boost_with_innate('Occult', 2)
char.secondary.boost_with_innate('Withstand Pain', 4)
char.secondary.boost_with_innate('Alchemy', 1)
char.secondary.boost_with_bonus('Athleticism', 5)
char.secondary.boost_with_bonus('Persuasion', 25)
char.secondary.boost_with_bonus('Style', 25)
char.secondary.boost_with_bonus('Empathy', 10)
char.secondary.boost_with_bonus('Notice', 35)
char.secondary.boost_with_bonus('Magic Appraisal', 15)
char.secondary.boost_with_bonus('Medicine', 15)
char.secondary.boost_with_bonus('Occult', 5)
char.secondary.boost_with_bonus('Withstand Pain', 25)
char.secondary.boost_with_bonus('Alchemy', 40)

controller = Controller(char)
print(controller.attack_action(Unarmed))
controller.tick()