from combat import Combat, CombatConfig
from magic import Magic, MagicConfig
from psychic import Psychic, PsychicConfig
from secondary import Secondary, SecondaryConfig
from util.exceptions import NotFound, NotEnoughData
from common.resources import DevelopmentPoint, DevelopmentPointTracker
from general import General, GeneralConfig

class Character:
    SURPRISE = True
    SURPRISE_DIFF = 150

    def is_surprised(self, dice_diff, gm_declared=False):
        if gm_declared:
            return self.SURPRISE
        if dice_diff >= self.SURPRISE_DIFF:
            return True
        else:
            return False

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
        return {subcl.__name__ if not hasattr(subcl, 'repname') else subcl.repname: subcl for subcl in cls.__subclasses__()}

    general_config = (1, 1)
    combat_config = (1, 1, 1, 1, False, False, False, 10)
    combat_dp_limit = 0.6
    magic_config = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    magic_dp_limit = 0.6
    psychic_config = (1, 1, 1, 1)
    psychic_dp_limit = 0.6
    secondary_config = ({}, {}, 75)

    buyable_config = (0, 0, 0, 0, 0)
    style_module_discount = 0
    minor_ars_magnus_discount = 0
    ars_magnus_discount = 0
    impossible_weapon_discount = 0
    martial_arts_discount = 0

    def get_dp(self):
        return self.dp

    def get_gnosis(self):
        return self.gnosis

    # todo: add value getting here keeping INHUMAN limit and stuff
    def __init__(self, classname, gnosis=10, dp=0):
        self.gnosis = gnosis
        self.dp = dp
        self.dp_tracker = DevelopmentPointTracker(DevelopmentPoint, limit_f=self.get_dp)
        self.general = General(GeneralConfig(*self.general_config, dp_tracker=self.dp_tracker, character=self))

        self.combat = Combat(CombatConfig(*self.combat_config, dp_limit=self.combat_dp_limit,
                                          dp_tracker=self.dp_tracker, character=self))
        self.magic = Magic(MagicConfig(*self.magic_config, dp_limit=self.magic_dp_limit,
                                       dp_tracker=self.dp_tracker, character=self))
        self.psychic = Psychic(PsychicConfig(*self.psychic_config, dp_limit=self.psychic_dp_limit,
                                             dp_tracker=self.dp_tracker, character=self))
        self.secondary = Secondary(SecondaryConfig(*self.secondary_config, dp_tracker=self.dp_tracker, character=self))

        # core ended, starting ext
        self.notes = set()
        self.activatables = set()
        self.reference = set()


    base_limit = 280

    def get_limit(self):
        return self.base_limit