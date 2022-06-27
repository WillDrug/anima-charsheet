from anima.util.parameters import CoreValueAttribute, Attribute


class DP(CoreValueAttribute):
    pass


class MK(Attribute):
    pass


class Zeon(CoreValueAttribute):
    def stat_bonus(self):
        return 14 + 3 * self.source.stats.pow.value

    def _value_f(self):
        return self.core_value + self.stat_bonus() + self.source.presence.value

class PsychicPoints(CoreValueAttribute):
    def _value_f(self):
        return self.source.stats.int.value + self.source.presence.value

class PsychicPotential(Attribute):
    def _value_f(self):
        return 2+2*self.source.stats.int.value