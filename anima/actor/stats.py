from anima.util.parameters import AttributeContainer, CoreValueAttribute


class Stats(AttributeContainer):
    STARTING_VALUE = 0

    def common_initialize(self, *args, **kwargs):
        value = kwargs.pop(self.iam, 0)
        self._core_value = value if value else self.STARTING_VALUE
        self._value_f = lambda iself: iself.core_value


class STR(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class DEX(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class AGI(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class CON(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class INT(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class POW(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class WIL(CoreValueAttribute, Stats):
    STARTING_VALUE = 0


class PER(CoreValueAttribute, Stats):
    STARTING_VALUE = 0
