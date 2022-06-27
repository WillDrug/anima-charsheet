from anima.util.parameters import Ability


class Attack(Ability):
    pass


class Light(Attack):
    STAT = 'dex'


class Heavy(Attack):
    STAT = 'str'


class Ranged(Attack):
    STAT = 'per'


class Defense(Ability):
    pass


class Block(Defense):
    STAT = 'dex'


class Dodge(Defense):
    STAT = 'agi'


class MagicProjection(Ability):
    pass


class OffensiveMagicProjection(MagicProjection):
    STAT = 'per'


class DefensiveMagicProjection(MagicProjection):
    STAT = 'per'


class PsychicProjection(Ability):
    pass


class OffensivePsychicProjection(Ability):
    STAT = 'per'


class DefensivePsychicProjection(Ability):
    STAT = 'per'


class Summon(Ability):
    STAT = 'pow'

class Bind(Ability):
    STAT = 'pow'

class Banish(Ability):
    STAT = 'pow'

class Control(Ability):
    STAT = 'wil'