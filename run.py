from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 10, 'DEX': 8, 'AGI': 8})
char.general.boost_stat_with_cp('STR', 3)
print(char.general.maximum_life_points.value)