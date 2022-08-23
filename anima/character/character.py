
from anima.actor.creature import Creature
"""
    1) Add modules: General (advantages), Physical (Style, Ki), Magical (Magic, Summoning), 
    Psionic (Powers, shit), Secondary (Skills, Background)
    
    2) Proxy each type into activatable or benefit via a function
    
    3) Setup base-classes for advantages, raise NotImplemented for non-implemented
    
    4) Setup weapon profiles
    
    5) Start setting up style modules, martial arts, etc.
"""
from anima.character.skills import Skills
from math import floor
from anima.character.character_class import CharacterClass
from anima.character.attributes import DP, MK, Zeon, PsychicPoints, PsychicPotential
from anima.equipment.weapon import Unarmed


class Character(Creature):
    def __init__(self, name, character_class, race, starting_dp, description='', *args, **kwargs):
        super().__init__(name, description=description, *args, **kwargs)
        self.combatprofile.add_weapon(Unarmed(self))
        self.dp = DP(self, dp=starting_dp)
        self.mk = MK(self)
        # regenerate presence
        self.presence._value_f = lambda: floor(self.dp.value/20)
        # create skills
        self.skills = Skills(self, **kwargs)

        # magic specifics
        self.zeon = Zeon(self, **kwargs)

        # psychic specifics
        self.psychicpoints = PsychicPoints(self, **kwargs)
        self.psychicpotential = PsychicPotential(self, **kwargs)

        if isinstance(character_class, str):
            character_class = CharacterClass.get_class(character_class)
        self.character_class = character_class(self)



if __name__ == '__main__':
    from anima.util.bonuses import Bonus
    c = Character('test', 'acrobaticwarrior', '', starting_dp=20, con=1, presence=2, str=1, dex=4, attack=5, acrobatics=1, withstandpain=10)
    print(c.combatprofile.weapons)