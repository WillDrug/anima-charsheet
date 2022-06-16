from anima.util.mixins import Referencable, Searchable
from types import MethodType
from typing import Iterable
from anima.util.bonuses import Bonus


class Attribute(Referencable):
    _value_f = lambda: 0

    def __init__(self, source, *args, **kwargs):
        """
        :rtype: object
        """
        self.source = source
        self.bonuses = set()
        self.initialize(*args, **kwargs)

    def add_bonus(self, bonus: Bonus):
        if bonus in self.bonuses:
            self.bonuses.remove(bonus)  # this preserves the hash of a bonus object but allows to overwrite the value
        self.bonuses.add(bonus)

    def rem_bonus(self, bonus):
        self.bonuses.remove(bonus)

    def initialize(self, *args, **kwargs):
        pass

    @property
    def value(self):
        return self._value_f() + sum(self.bonuses)

    @property
    def clean_value(self):
        return self._value_f()

    def __str__(self):
        return f"<{self.source}: {self.iam} ({self.value})>"


class CoreValueAttribute(Attribute):
    STARTING_VALUE = None

    def initialize(self, value, **kwargs):
        self._core_value = value if value is not None else self.STARTING_VALUE
        self._value_f = lambda: self.core_value

    @property
    def core_value(self):
        return self._core_value

    def set_core_value(self, value):
        self._core_value = value


class AttributeContainer(Referencable, Searchable):
    @classmethod
    def attr_list(cls):
        return cls.__subclasses__()

    def __init__(self, source, **kwargs):
        self.source = source
        for cls in self.attr_list():
            cls.initialize = MethodType(self.common_initialize.__func__, cls)
            # noinspection PyTypeChecker
            self.__setattr__(cls.iam, cls(self, kwargs.pop(cls.iam, None)))

    def common_initialize(self, *args, **kwargs):
        """
        This method will be called by every child of the container class, unifying logic
        :param args: any, passed from class init as a base "initialize" function
        :param kwargs: same
        :return: None
        """
        pass

    def max_of(self, refs: Iterable):
        vals = [self.access(q).value for q in refs]
        return max(vals)

    def __str__(self):
        return f"{self.source}: {self.iam} (container)"


class Ability(CoreValueAttribute, AttributeContainer):
    def __init__(self, source, value, *args, **kwargs):
        super(Ability, self).__init__(source, value, *args, **kwargs)
        AttributeContainer.__init__(self, source, *args, **kwargs)

    @property
    def core_value(self):
        if isinstance(self.source, Ability):
            return self.source._core_value
        else:
            return self._core_value

    def set_core_value(self, value):
        if isinstance(self.source, Ability):
            self.source._core_value = value
        else:
            self._core_value = value

    STAT = ''

    def common_initialize(self, *args, **kwargs):
        def val(iself):
            return iself.core_value + iself.source.access('source').access('presence').value + \
                   iself.source.access('source').access('stats').access(iself.STAT).value

        self._value_f = val


if __name__ == '__main__':
    l = [Bonus('test', 5), Bonus('test2', 1), Bonus('test3', 10)]
    print('test' in l)
    print(sum(l))
    print(l[0].__hash__())
