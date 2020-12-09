from general import Stat
from character import Character
from util.parameters import Attribute
from combat import Attack, Dominion
from inspect import getmro
from util.exceptions import OverLimit
from util.resources import Resource, ResourceTracker
from common.resources import DevelopmentPoint

char = Character('Wizard', dp=800)
char.general.invest_into_stats(dict(STR=5, DEX=5, AGI=8, CON=8, INT=11, POW=11, WIL=6, PER=11))
char.general.boost_stat_with_cp('POW', 2)
char.general.boost_stat_with_cp('INT', 2)
char.magic.boost(char.magic.magic_accumulation, 150)
char.magic.boost(char.magic.magic_projection, 230)
char.magic.boost(char.magic.maximum_zeon, 75)
char.magic.boost(char.magic.zeon_regeneration, 25)


