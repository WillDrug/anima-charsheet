from util.exceptions import NotFound
from util.config import ModuleConfig, Module
from util.parameters import MultipartAttributeMixin
from util.abilities import Ability

class SecondaryConfig(ModuleConfig):
    def __init__(self, skills: dict, **kwargs):
        for k in skills:
            if k not in Skill.impl_list():
                raise NotFound(f'{k} is not a valid seconary ability')
        self.skills = skills
        super().__init__(**kwargs)

class Skill(Ability, MultipartAttributeMixin):
    pass

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

class Secondary(Module):
    DEFAULT_COST = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add class bonuses with limited=false