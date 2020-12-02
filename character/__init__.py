from combat import Combat, CombatConfig
from magic import Magic, MagicConfig
from psychic import Psychic, PsychicConfig
from secondary import Secondary, SecondaryConfig
from util.exceptions  import NotFound, NotEnoughData
from general import General, GeneralConfig

class Character:
    @classmethod
    def __new__(cls, *args, **kwargs):
        """ Forces creation of an implementation on each Interface call
        """
        if args.__len__() < 2:
            raise NotEnoughData('Please specify character class as first param')
        character_class = args[1]
        return_class = cls.impl_list().get(character_class, None)
        if return_class is None:
            raise NotFound(
                "Character class not found"
            )
        return object.__new__(return_class)

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

    # PER LEVEL  fixme: package those up
    MK = 1
    PSY_PTS = 1
    ML = 1
    PSY_POT = 1
    ZEON = 1
    SUMMON = 1
    CONTROL = 1
    BIND = 1
    BANISH = 1
    SECONDARY = {}  # fixme: class skill bonuses need to be tighter
    # / PER LEVEL
    general_config = GeneralConfig(1, 1, 1)  # fixme: I want to somehow pass functions to get levels and shit right from here
    combat_config = CombatConfig(1, 1, 1, 1, False, False, False, dp_limit=0.6)
    magic_config = MagicConfig(1, 1, 1, 1, 1, 1, 1, dp_limit=0.6)
    psychic_config = PsychicConfig(1, 1, dp_limit=0.6)
    secondary_config = SecondaryConfig({})
    TERTIARY = 1

    def get_dp(self):
        return self.dp

    def get_gnosis(self):
        return self.gnosis

    def __init__(self, classname, gnosis=10, dp=0):
        self.gnosis = gnosis
        self.dp = dp
        self.general_config.set_dpf(self.get_dp)
        self.general_config.set_gnosis_f(self.get_gnosis)
        self.general = General(self.general_config)
        self.combat_config.set_dpf(self.get_dp)
        self.general_config.set_gnosis_f(self.get_gnosis)
        self.combat = Combat(self.combat_config)


class Warrior(Character):
    pass