from util.exceptions import NotFound

class SecondaryConfig:
    def __init__(self, skills: dict):
        for k in skills:
            if k not in Skill.impl_list():
                raise NotFound(f'{k} is not a valid seconary ability')
        self.skills = skills

class Skill:
    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

class Acrobatics(Skill):
    pass

"""        'Acrobatics',
        'Athleticism',
        'Persuasion',
        'Style',
        'Empathy',
        'Notice',
        'Magic Appraisal',
        'Medicine',
        'Occult',
        'Composure',
        'Withstand Pain',
        'Poisons',
        'Sleight of Hand',
        'Stealth',
        'Alchemy',
        'Animism',
        'Forging',
        'Runes'"""

# class bonuses should not be calculated towards skill limit.

class Secondary:
    DEFAULT_COST = 2