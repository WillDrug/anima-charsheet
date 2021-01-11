from util.buyable import Buyable
from .resources import PsychicPoint
from util.exceptions import RuleError

class Power(Buyable):
    def potential_bonus(self):
        return min((self.invest[PsychicPoint].value-1)*10, 50)

    def increase_potential(self, res: PsychicPoint):
        if PsychicPoint not in self.invest:
            raise RuleError(f'Somehow bought {self.__class__} with no PP')
        self.invest[PsychicPoint].set_value(self.invest[PsychicPoint].value+res.value)
        res.free()

class Telepathy(Buyable):
    REFERENCE = 'psy_t_telepathy'
    NOTE = 'Has access to Telepathy psychic discipline'
    COST = {
        PsychicPoint: 1
    }

class AreaScanning(Power):
    REFERENCE = 'psy_t_tel_area_scan'
    COST = {
        PsychicPoint: 1
    }
    PREREQUISITE = ['psy_t_telepathy']


    def add_activatables(self):
        pass  # should add the activated effect here. provides no bonus.
