import re

from anima.util.mixins import Referencable, DispatchesBonuses
from anima.util.exceptions import PrerequisiteMissingError
from typing import Union, List


class Benefit(DispatchesBonuses, Referencable):
    """
    Advantage, GM grants, race plugins, etc.
    Has prerequisites, limitations, stuff.
    """

    REQUIRED_BENEFIT = ()
    REQUIRED_PARAM = ()
    DESCRIPTION = None

    def __init__(self, source, *args, **kwargs):
        """

        :param source: Should not point to the container (like ".benefits"), should always be source object
        :param args:
        :param kwargs:
        """

        self.source = source  # source is duplicated as to check rpereqs
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
        self.check_prerequisites()
        super().__init__(source, *args, **kwargs)
        self.dispatched = []
        self.initialize()

    def description(self):
        return self.DESCRIPTION

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

    def initialize(self):
        """
        Function should be used to generate any Controller-specific bonuses a benefit gives
        :return: None
        """
        pass

    def __call__(self, *args, **kwargs) -> List["Augment"]:
        """
        :param args: unused
        :param kwargs: unused
        :return: Returns a list of Activatables, Choices and Augments for Controller to use.
        """
        return self.dispatched
