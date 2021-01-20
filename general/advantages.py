from util.buyable import Buyable
from common.resources import CreationPoint

class Advantage(Buyable):
    def set_usage(self, res):
        res.set_usage(f'Buying {self.__class__}', stat=False)

"""
regen = Regeneration(CreationPoint.__name__= CreationPoint(1-3))
"""
class Regeneration(Advantage):
    COST = {
        CreationPoint: 1
    }
    REFERENCE = 'adv_regen'
    PREREQUISITE = []
    NOTE = None

    def regen_bonus(self):
        def bonus_append(regen):
            return self.invest[CreationPoint].value*2

        return self.__class__, bonus_append

    def add_bonuses(self):
        self.character.general.regen.add_bonus(*self.regen_bonus())

    def rem_bonuses(self):
        self.character.general.regen.rem_bonus(self.__class__)


class IncompleteGift(Advantage):
    COST = {
        CreationPoint: 1
    }
    REFERENCE = 'adv_lim_gift'
    PREREQUISITE = []
    NOTE = 'Able to accumulate and control Zeon but not so much cast'
    # fixme: this should work with casting limited to a power roll

    def add_bonuses(self):
        self.character.magic.magic_accumulation.ACTIVATED = True
        self.character.magic.magic_projection.ACTIVATED = True


    def rem_bonuses(self):
        self.character.magic.magic_accumulation.ACTIVATED = False
        self.character.magic.magic_projection.ACTIVATED = False

class Gift(Advantage):
    # fixme: doesn't do anything yet. should remove casting restrictions
    COST = {
        CreationPoint: 1
    }
    REFERENCE = 'adv_gift'
    PREREQUISITE = ['adv_lim_gift']
    NOTE = 'Ability to perform Magic'

class Ambidextrous(Advantage):
    COST = {
        CreationPoint: 1
    }
    REFERECE = 'adv_ambidextrous'
    NOTE = 'Skilled with using both hands'

    def add_bonuses(self):
        self.character.combat.offhand_penalty.add_bonus(self.__class__, lambda x: -30)

    def rem_bonuses(self):
        self.character.combat.offhand_penalty.rem_bonus(self.__class__)



class PsychicDiscipline(Advantage):
    COST = {
        CreationPoint: 1
    }

class Telepathy(PsychicDiscipline):
    REFERENCE = 'adv_psy_telepathy'

class AnyPsychicDiscipline(Advantage):
    COST = {
        CreationPoint: 2
    }
    REFERENCE = 'adv_psy_all'

    def __init__(self):
        self.cps = {}

    def add_bonuses(self):
        for sub in PsychicDiscipline.__subclasses__():
            cp = CreationPoint(lock_advantage=True)
            adv = sub(self.character, **{CreationPoint.__name__: cp})
            self.cps[cp] = adv

    def rem_bonuses(self):
        for k in self.cps:
            self.cps[k].deactivate()
            k.free()
            del self.cps[k]