from anima.util.parameters import CoreValueAttribute, AttributeContainer, Attribute
from math import floor
from enum import Enum, auto


class Gnosis(CoreValueAttribute):
    pass


class Presence(CoreValueAttribute):
    pass


class Resistances(AttributeContainer):
    STAT = ''
    MULTIPLIER = 2

    def common_initialize(self, *args, **kwargs):
        self._value_f = lambda iself: iself.source.access('source.presence').value * iself.MULTIPLIER + \
                                      iself.source.access('source.stats').access(iself.STAT).value


class PhysicalResistance(Attribute, Resistances):
    I_NAME = 'physres'
    STAT = 'con'


class MagicResistance(Attribute, Resistances):
    I_NAME = 'magres'
    STAT = 'pow'


class PsychicResistance(Attribute, Resistances):
    I_NAME = 'psires'
    STAT = 'wil'


class CriticalResistance(Attribute, Resistances):
    I_NAME = 'critres'
    STAT = 'con'
    MULTIPLIER = 1

class SizeType(Enum):
    miniscule = auto()
    small = auto()
    medium = auto()
    big = auto()
    enormous = auto()
    giant = auto()
    colossal = auto()

    @classmethod
    def get_size(cls, size):
        if size < -7:
            return cls.miniscule
        elif size < -2:
            return cls.small
        elif size < 12:
            return cls.medium
        elif size < 14:
            return cls.big
        elif size < 18:
            return cls.enormous
        elif size < 23:
            return cls.giant
        else:
            return cls.colossal

class Size(Attribute):
    def _value_f(self):
        # size is a basic attribute and cannot change for random bonuses to STR or CON.
        # therefore, if something would to increase STR or CON *and* size, it should add a specialty bonus here.
        return self.source.access('stats.str').clean_value + self.source.access('stats.con').clean_value

    def get_size_type(self):
        return SizeType.get_size(self.value)

    def base_initiative(self):
        if self.value < -7:
            return 8
        elif self.value < -2:
            return 6
        elif self.value < 12:
            return 4
        elif self.value < 14:
            return 2
        elif self.value < 18:
            return 0
        elif self.value < 23:
            return -2
        else:
            return -4

    def movement_bonus(self):
        if self.value < -7:
            return -4
        elif self.value < -2:
            return -2
        elif self.value > 15:
            return 1
        elif self.value > 19:
            return 2
        elif self.value > 24:
            return 3
        else:
            return 0


class Initiative(Attribute):
    def _value_f(self):
        return self.source.access('size').base_initiative() + \
               self.source.access('stats.dex').value + \
               self.source.access('stats.agi').value


class Movement(Attribute):
    def _value_f(self):
        return self.source.access('stats.ago').value+self.source.access('size').movement_bonus()

    def meters(self):
        speed = {
            -4: 0.25, -3: 1, -2: 2, -1: 3, 0: 4, 1: 5, 2: 6,
            3: 7, 4: 8, 5: 9, 6: 10, 7: 12, 8: 20, 9: 40, 10: 60,
            11: 120, 12: 250, 13: 1250, 14: 6250, 15: 9999999
        }
        if self.value not in speed:
            if self.value < 0:
                return 0
            else:
                return 9999999

        return speed[self.value]


class LifePoints(Attribute):
    """
    All "resource" attributes denote just the maximum amounts.
    """

    def _value_f(self):  # fixme see if this should be core_value
        return 14 + self.source.access('stats.con').value * 2 + \
               self.source.access('stats.str').value



class Fatigue(Attribute):
    def _value_f(self):
        return self.source.access('stats.con').value


class Willpower(Attribute):
    def _value_f(self):
        return self.source.access('stats.wil').value


# fixme: move to wherever character stuff is
class KiAccumulations(AttributeContainer):
    STAT = ''

    def common_initialize(self, *args, **kwargs):
        self._value_f = lambda iself: 1 + floor(self.source.access('stats').access(iself.STAT) / 5)


class StrAccum(Attribute, KiAccumulations):
    STAT = 'str'


class DexAccum(Attribute, KiAccumulations):
    STAT = 'dex'


class AgiAccum(Attribute, KiAccumulations):
    STAT = 'agi'


class ConAccum(Attribute, KiAccumulations):
    STAT = 'con'


class IntAccum(Attribute, KiAccumulations):
    STAT = 'int'


class PowAccum(Attribute, KiAccumulations):
    STAT = 'pow'


class WilAccum(Attribute, KiAccumulations):
    STAT = 'wil'


class PerAccum(Attribute, KiAccumulations):
    STAT = 'per'
