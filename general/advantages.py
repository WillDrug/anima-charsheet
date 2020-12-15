from util.buyable import Buyable
from common.resources import CreationPoint

"""
regen = Regeneration(CreationPoint.__name__= CreationPoint(1-3))
"""
class Regeneration(Buyable):
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
        self.character.general.regen.add_bonus()
