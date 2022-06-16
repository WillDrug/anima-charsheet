from anima.util.exceptions import AttributeMissingError
from anima.util.bonuses import Bonus
from weakref import proxy

class Referencable:
    I_NAME = None

    @classmethod
    @property
    def iam(cls) -> str:
        return cls.I_NAME if cls.I_NAME else cls.__name__.lower()

    def __eq__(self, other):
        if isinstance(other, Referencable):
            other = other.iam
        return self.iam == other

    def __hash__(self):
        return hash(self.iam)

class Searchable:
    def access(self, attr):
        if not isinstance(attr, str):
            attr = attr.iam
        attrs = attr.split('.')
        ref = self
        try:
            for attr in attrs:
                ref = ref.__getattribute__(attr)
            return ref
        except AttributeError:
            raise AttributeMissingError(self, attr)

    def has(self, path):
        elems = path.split('.')
        ref = self
        try:
            for elem in elems:
                ref = ref.access(elem)
        except AttributeMissingError as e:
            return False
        else:
            return True


class DispatchesBonuses:
    def __init__(self):
        self.bonuses = dict()

    def dispatch_bonus(self, to, value, code=None):
        if code is None and not hasattr(self, 'iam'):
            code = self.__class__.__name__.lower()
        elif code is None:
            code = self.iam

        b = Bonus(code, value)
        self.bonuses[to] = b  # if there was previous bonus, it will be deleted on the next step anyway
        to.add_bonus(b)

    def __del__(self):
        for target in self.bonuses:
            target.rem_bonus(self.bonuses[target])
