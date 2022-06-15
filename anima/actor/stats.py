from anima.util.parameters import AttributeContainer, CoreValueAttribute


class Stats(AttributeContainer):
    def common_initialize(self, value, *args, **kwargs):
        self._value = value
        self._value_f = lambda self: self._value


class STR(CoreValueAttribute, Stats):
    pass


class DEX(CoreValueAttribute, Stats):
    pass


class AGI(CoreValueAttribute, Stats):
    pass


class CON(CoreValueAttribute, Stats):
    pass


class INT(CoreValueAttribute, Stats):
    pass


class POW(CoreValueAttribute, Stats):
    pass


class WIL(CoreValueAttribute, Stats):
    pass


class PER(CoreValueAttribute, Stats):
    pass
