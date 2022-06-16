from anima.actor.attributes import Gnosis, Presence, Resistances, Size, Initiative, Movement, LifePoints, Fatigue, \
    Willpower
from anima.actor.stats import Stats
from anima.util.mixins import Searchable, Referencable
from anima.actor.abilities import Attack, Defense, MagicProjection, PsychicProjection


class Creature(Searchable):
    # noinspection PyTypeChecker
    def __init__(self, name, description='', **kwargs):
        self.name = name
        self.description = description

        # Core block
        self.gnosis = Gnosis(self, kwargs.pop(Gnosis.iam, None))
        self.presence = Presence(self, kwargs.pop(Presence.iam, None))
        self.stats = Stats(self, **kwargs)
        self.resistances = Resistances(self, **kwargs)
        self.size = Size(self)
        self.initiative = Initiative(self)
        self.movement = Movement(self)
        self.lifepoints = LifePoints(self)
        self.fatigue = Fatigue(self)
        self.willpower = Willpower(self)

        # Ability block
        self.attack = Attack(self, kwargs.pop(Attack.iam, None))
        self.defense = Defense(self, kwargs.pop(Defense.iam, None))
        self.magicprojection = MagicProjection(self, kwargs.pop(MagicProjection.iam, None))
        self.psychicprojection = PsychicProjection(self, kwargs.pop(PsychicProjection.iam, None))

        # benefits and abilities
        self.benefits = set()
        self.activatable = set()

    def __str__(self):
        return f"<{self.__class__.__name__} ({self.name})>"

    def add_benefit(self, cls, *args, **kwargs):
        if cls.iam in self.benefits:
            self.benefits.remove(cls.iam)
        self.benefits.add(cls(self, *args, **kwargs))

    def rem_benefit(self, cls):
        if issubclass(cls, Referencable):
            cls = cls.iam
        self.benefits.remove(cls)

    def add_activatable(self, cls, *args, **kwargs):
        if cls.iam in self.activatable:
            self.activatable.remove(cls.iam)
        self.activatable.add(cls(self, *args, **kwargs))

    def rem_activatable(self, cls):
        self.activatable.remove(cls)


if __name__ == '__main__':
    c = Creature('my creature', presence=2, con=1, str=2, attack=10, defense=5, dex=2, wil=5)
    print(c.stats.wil)