from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 10, 'DEX': 8, 'AGI': 8})
char.general.boost_stat_with_cp('STR', 2)
char.general.boost_stat_with_cp('DEX', 2)
print(char.general.surprise_res.value)