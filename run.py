from general import Stat
from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 10, 'DEX': 8, 'AGI': 8})


print(char.general.resistance.surprise.value)
print(char.general.resistance.physical.value)
char.general.resistance.surprise.add_bonus('test', lambda x: 5)
print(char.general.resistance.surprise.value)
print(char.general.resistance.physical.value)
