from general import Stat
from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 11, 'DEX': 11, 'AGI': 11, 'PER': 11, 'INT': 11, 'POW': 11, 'WIL': 11})
print(char.general.stats.get('DEX').full_cost)