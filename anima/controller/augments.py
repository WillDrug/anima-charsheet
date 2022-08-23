from anima.util.mixins import Referencable

class Augment(Referencable):
    """
    Usage: 1) Status, 2) Maneuver, 3) Augment of 1 and 2 due to Benefit.
    """
    lifespan = 'tick'  # name of the function on which augment is added or removed.
    ticks = 1  # amount of attacks, rounds or anything the augment persists. None is infinite
    # permanent augments of augments will have '__init__' as lifespan or None.
    target = None

    # def __init__(self, source):
    #     self.source = source

    def __call__(self, target):
        if not isinstance(target, self.target):
            return
        self.apply(target)

    def apply(self, target):
        pass