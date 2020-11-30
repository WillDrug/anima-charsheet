from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 10})
print(char.general.maximum_life_points.value)