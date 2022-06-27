from anima.util.parameters import AttributeContainer, CoreValueAttribute
from anima.util.exceptions import ClassMistmatch
class Skills(AttributeContainer):
    def common_initialize(self, *args, **kwargs):
        def val(iself):
            # go over container to character
            if iself.is_specialization:
                source = iself.source.source.source
            else:
                source = iself.source.source
            # fixme: this expects a mixin! specialization_bonus should be clear from the Skills container somehow.
            return iself.core_value + source.access(f'stats.{iself.STAT}.value') + iself.specialization_bonus + \
                   iself.get_penalty()
        if self.iam in kwargs:
            self._core_value = kwargs.pop(self.iam)
        else:
            self._core_value = self.STARTING_VALUE if self.STARTING_VALUE else 0
        self._value_f = val

class Skill:
    @property
    def trained(self):
        return self._core_value > 0

    def __init__(self, *args, **kwargs):
        self.specializations = {}
        self._penalty = -4
        for cls in self.__class__.__subclasses__():
            setattr(self, cls.iam, cls(self, *args, **kwargs))
            delattr(getattr(self, cls.iam), 'specializations')
            self.specializations[getattr(self, cls.iam)] = False
        super().__init__(*args, **kwargs)

    @property
    def is_specialization(self):
        return not hasattr(self, 'specializations')

    def get_penalty(self):
        return self._penalty if not self.trained else 0

    @property
    def specialization_bonus(self):
        val = 0
        adjust = 0
        if self.is_specialization:
            specs = self.source.specializations
            # check if self is specialized
            if specs[self]:
                val = 8
                adjust = 1
        else:
            specs = self.specializations
        return val-4*(sum(specs.values())-adjust)

    def set_specialization(self, spec, val):
        if not isinstance(spec, str):
            spec = spec.iam
        if not spec in self.specializations:
            raise ClassMistmatch(f'{spec} is not a specialization of {self}')
        self.specializations[spec] = val

    # fixme: this is dirty as your fuckng mom
    def foreach(self):
        for cls in self.__class__.__subclasses__():
            yield getattr(self, cls.iam)


class Acrobatics(Skill, CoreValueAttribute, Skills):
    STAT = 'agi'


class Tricks(Acrobatics):
    STAT = 'dex'

class Maneuvering(Acrobatics):
    STAT = 'agi'

class WithstandPain(Skill, CoreValueAttribute, Skills):
    STAT = 'con'