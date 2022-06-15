from anima.actor.attributes import Gnosis, Presence, Resistances
from anima.actor.stats import Stats, DEX
from anima.util.mixins import Searchable

class Creature(Searchable):
    def __init__(self, name, description='', **kwargs):
        self.name = name
        self.description = description

        self.gnosis = Gnosis(self, kwargs.pop(Gnosis.iam, None))
        self.presence = Presence(self, kwargs.pop(Presence.iam, None))
        self.stats = Stats(self, **kwargs)
        self.resistances = Resistances(self, **kwargs)

    def __str__(self):
        return f"<{self.__class__.__name__} ({self.name})>"


if __name__ == '__main__':
    c = Creature('my creature', presence=2, con=1)
    print(c.resistances.physres)
    print(c.resistances.critres)