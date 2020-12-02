from character import Character
char = Character('Warrior', dp=900)
char.general.set_stats({'STR': 11, 'CON': 10, 'DEX': 8, 'AGI': 8})
print(char.general.resistances['Surprise'].value)
char.dp = 1000
print(char.general.resistances['Surprise'].value)