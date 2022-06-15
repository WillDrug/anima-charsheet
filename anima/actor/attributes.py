from anima.util.parameters import CoreValueAttribute, AttributeContainer, Attribute

class Gnosis(CoreValueAttribute):
    pass

class Presence(CoreValueAttribute):
    pass

class Resistances(AttributeContainer):
    STAT = ''
    MULTIPLIER = 2

    def common_initialize(self, *args, **kwargs):
        self._value_f = lambda iself: iself.source.access('source').access('presence').value * iself.MULTIPLIER + \
                                      iself.source.access('source').access('stats').access(iself.STAT).value

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
