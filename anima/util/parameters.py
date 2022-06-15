from anima.util.mixins import Referencable, Searchable
from types import MethodType


class Attribute(Referencable):
    _value_f = lambda: 0

    def __init__(self, source, *args, **kwargs):
        self.source = source
        self.initialize(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        pass

    @property
    def value(self):
        return self._value_f()

    def __str__(self):
        return f"<{self.source}: {self.iam} ({self.value})>"


class CoreValueAttribute(Attribute):
    STARTING_VALUE = None

    def initialize(self, value, **kwargs):
        self._value = value if value is not None else self.STARTING_VALUE
        self._value_f = lambda: self._value


class AttributeContainer(Referencable, Searchable):
    @classmethod
    def attr_list(cls):
        return cls.__subclasses__()

    def __init__(self, source, **kwargs):
        self.source = source
        for cls in self.attr_list():
            cls.initialize = MethodType(self.common_initialize.__func__, cls)
            self.__setattr__(cls.iam, cls(self, kwargs.pop(cls.iam, None)))

    def common_initialize(self, *args, **kwargs):
        pass

    def __str__(self):
        return f"{self.source}: {self.iam} (container)"
