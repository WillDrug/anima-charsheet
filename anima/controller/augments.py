from anima.util.mixins import Referencable
from anima.util.exceptions import PrerequisiteMissingError
class Augment(Referencable):
    """
    Usage: 1) Status, 2) Maneuver, 3) Augment of 1 and 2 due to Benefit.
    """
    lifespan = 'tick'  # name of the function on which augment is added or removed.
    ticks = 1  # amount of attacks, rounds or anything the augment persists. None is infinite
    # permanent augments of augments will have '__init__' as lifespan or None.
    target = None

    def __init__(self, source):
        self.source = source

    def __call__(self, target):
        if isinstance(self.target, str):
            test = target.__class__.__name__ == self.target
        else:
            test = isinstance(target, self.target)
        if not test:
            return
        return self.apply(target)

    def apply(self, target):
        pass


class Maneuver(Augment):
    def __init__(self, source):
        super().__init__(source)
        self.test_prerequisites()

    def test_prerequisites(self):
        raise PrerequisiteMissingError('General maneuver class is not usable.')


class Status(Augment):
    pass


class PermanentAugment(Augment):
    ticks = None  # forever alive
