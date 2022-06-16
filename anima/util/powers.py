import re

from anima.util.mixins import Referencable, DispatchesBonuses
from anima.util.exceptions import PrerequisiteMissingError


class Effect:
    """
    Constitutes both effect and status
    """
    pass


class Activatable:
    """
    Anything which can be used by the character
    """
    pass


class Benefit(Referencable, DispatchesBonuses):
    """
    Advantage, GM grants, race plugins, etc.
    Has prerequisites, limitations, stuff.
    """

    REQUIRED_BENEFIT = ()
    REQUIRED_PARAM = ()

    def __init__(self, source, *args, **kwargs):
        """

        :param source: Should not point to the container (like ".benefits"), should always be source object
        :param args:
        :param kwargs:
        """
        super().__init__()
        self.source = source
        self.pattern = re.compile(r'((?:\w+\.)+)(\w+)\s{0,}([><!=]+)\s{0,}(\d+)')
        self.comparators = {
            '>': '__gt__',
            '<': '__lt__',
            '>=': '__ge__',
            '<=': '__le__',
            '=': '__eq__',
            '==': '__eq__',
            '!=': '__ne__'
        }
        self.initialize(*args, **kwargs)
        self.check_prerequisites()

    def check_prerequisites(self):
        for benefit in self.REQUIRED_BENEFIT:
            if not self.source.has(benefit):
                raise PrerequisiteMissingError(self.source, benefit, message='Required benefit is missing')
        for param in self.REQUIRED_PARAM:
            path, attr, comparator, value = self.pattern.match(param).groups()
            path = path[:-1]  # remove the dot
            value = int(value)  # value is int now
            ref = self.source.access(path)  # get the attribute
            test = ref.__getattribute__(attr)  # get the field
            if not test.__getattribute__(self.comparators[comparator])(value):  # compare
                raise PrerequisiteMissingError(self.source, path,
                                               message=f'{path} should be {comparator} {value}, actually {test}')

    def initialize(self, *args, **kwargs):
        """
        Function to override to make benefit do shit
        :param args:
        :param kwargs:
        :return:
        """
        pass

