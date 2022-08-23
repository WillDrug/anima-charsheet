from anima.actor.attributes import Gnosis, Presence, Resistances, Size, Initiative, Movement, LifePoints, Fatigue, \
    Willpower
from anima.actor.stats import Stats
from anima.util.mixins import Searchable, Referencable
from anima.actor.abilities import Attack, Defense, MagicProjection, PsychicProjection, Summon, Bind, Banish, Control
from anima.actor.combat import CombatProfile
from anima.actor.regenerations import Regeneration

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
        self.regeneration = Regeneration(self)
        self.fatigue = Fatigue(self)
        self.willpower = Willpower(self)

        # Ability block
        self.attack = Attack(self, **kwargs)
        self.defense = Defense(self, **kwargs)
        self.magicprojection = MagicProjection(self, **kwargs)
        self.summon = Summon(self, **kwargs)
        self.banish = Banish(self, **kwargs)
        self.bind = Bind(self, **kwargs)
        self.control = Control(self, **kwargs)
        self.psychicprojection = PsychicProjection(self, **kwargs)

        # profiles
        """
        In this section all possible attack and defense profiles are created. Controller is responsible for choosing 
        active ones and calculating initiative. For Character, Armour will extend DefenseProfile
        """
        self.combatprofile = CombatProfile(self)


        # benefits and powers
        self.benefits = set()


    def __str__(self):
        return f"<{self.__class__.__name__} ({self.name})>"

    def add_attr(self, container, cls, *args, **kwargs):
        if not hasattr(self, container):
            raise AttributeError(f'{self.iam} has no container {container}')
        if cls.iam in getattr(self, container):
            getattr(self, container).remove(cls.iam)
        getattr(self, container).add(cls(self, *args, **kwargs))

    def rem_attr(self, container, cls):
        if not hasattr(self, container):
            raise AttributeError(f'{self.iam} has no container {container}')
        if issubclass(cls, Referencable):
            cls = cls.iam
        getattr(self, container).remove(cls)

    def add_benefit(self, cls, *args, **kwargs):
        return self.add_attr('benefits', cls, *args, **kwargs)

    def rem_benefit(self, cls):
        return self.rem_attr('benefits', cls)




if __name__ == '__main__':
    c = Creature('my creature', presence=2, con=1, str=2, attack=10, defense=5, dex=2, wil=5)
    print(c.attack.value)
