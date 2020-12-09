from combat import Combat, CombatConfig
from magic import Magic, MagicConfig
from psychic import Psychic, PsychicConfig
from secondary import Secondary, SecondaryConfig
from util.exceptions import NotFound, NotEnoughData
from common.resources import DevelopmentPoint, DevelopmentPointTracker
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


class AcrobaticWarrior(Character):
    repname = 'Acrobatic Warrior'
    general_config = (10, 10)
    combat_config = (2, 2, 2, 20, True, False, True, 25)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.33)
    psychic_dp_limit = 0.5
    secondary_config = ({'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {'Acrobatics': 10, 'Style': 10, 'Sleight of Hand': 10}, 75)
    buyable_config = (0, 0, 0, 0)

class Assassin(Character):
    general_config = (20, 10, 5)
    combat_config = (2, 2, 2, 25, True, False, False, 20)
    combat_dp_limit = 0.5
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.33)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Empathy': 1, 'Notice': 1, 'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3, 'Withstand Pain': 3, 'Stealth': 1}, {'Notice': 10, 'Composure': 10, 'Poisons': 10, 'Stealth': 10, 'Dominion Detection': 5}, 100)
    buyable_config = (0, 0, 0, 0)

class DarkPaladin(Character):
    repname = 'Dark Paladin'
    general_config = (5, 15)
    combat_config = (2, 2, 2, 20, True, False, False, 20)
    combat_dp_limit = 0.6
    magic_config = (2, 60, 3, 10, 3, 1, 3, 3, 20, 0, 10, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.33)
    psychic_dp_limit = 0.5
    secondary_config = ({'Persuasion': 1, 'Style': 1}, {'Athleticism': 5, 'Persuasion': 10, 'Style': 10, 'Composure': 10, 'Withstand Pain': 10}, 100)
    buyable_config = (0, 0, 0, 0)

class Freelancer(Character):
    general_config = (5, 5)
    combat_config = (2, 2, 2, 20, False, False, False, 20)
    combat_dp_limit = 0.6
    magic_config = (2, 60, 2, 10, 2, 2, 2, 2, 10, 0, 0, 0, 0)
    magic_dp_limit = 0.6
    psychic_config = (20, 2, 5, 0.50)
    psychic_dp_limit = 0.6
    secondary_config = ({}, {}, 125)
    buyable_config = (0, 0, 0, 0)

class Illusionist(Character):
    general_config = (5, 5)
    combat_config = (3, 3, 2, 25, False, False, False, 20)
    combat_dp_limit = 0.5
    magic_config = (1, 60, 2, 15, 3, 3, 3, 3, 75, 0, 0, 0, 0)
    magic_dp_limit = 0.6
    psychic_config = (20, 3, 5, 0.33)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Persuasion': 1, 'Composure': 3, 'Withstand Pain': 3}, {'Persuasion': 5, 'Magic Appraisal': 5, 'Sleight of Hand': 10, 'Stealth': 10}, 75)
    buyable_config = (0, 0, 0, 0)

class IllusionistSocial(Character):
    repname = 'Illusionist Social'
    general_config = (5, 5)
    combat_config = (3, 3, 2, 25, False, False, False, 20)
    combat_dp_limit = 0.5
    magic_config = (1, 60, 2, 15, 3, 3, 3, 3, 75, 0, 0, 0, 0)
    magic_dp_limit = 0.6
    psychic_config = (20, 3, 5, 0.33)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Magic Appraisal': 1, 'Composure': 3, 'Withstand Pain': 3}, {'Persuasion': 5, 'Empathy': 5, 'Magic Appraisal': 10, 'Occult': 10}, 75)
    buyable_config = (0, 0, 0, 0)

class Mentalist(Character):
    general_config = (5, 5)
    combat_config = (3, 3, 3, 30, False, False, False, 10)
    combat_dp_limit = 0.5
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (10, 2, 10, 1.00)
    psychic_dp_limit = 0.6
    secondary_config = ({'Athleticism': 3, 'Composure': 3, 'Withstand Pain': 3}, {}, 75)
    buyable_config = (0, 0, 0, 0)

class Paladin(Character):
    general_config = (5, 15)
    combat_config = (2, 2, 2, 20, False, True, False, 20)
    combat_dp_limit = 0.6
    magic_config = (2, 60, 3, 10, 3, 3, 3, 1, 20, 0, 0, 0, 10)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Persuasion': 1, 'Style': 1, 'Withstand Pain': 1, 'Poisons': 3, 'Sleight of Hand': 3, 'Stealth': 3}, {'Athleticism': 10, 'Style': 5, 'Empathy': 10, 'Composure': 10, 'Withstand Pain': 10}, 100)
    buyable_config = (0, 0, 0, 0)

class Ranger(Character):
    general_config = (5, 10)
    combat_config = (2, 2, 2, 25, True, False, False, 20)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Empathy': 1, 'Notice': 1, 'Magic Appraisal': 3, 'Occult': 3, 'Composure': 3, 'Withstand Pain': 3}, {'Notice': 10, 'Medicine': 10, 'Dominion Detection': 10}, 100)
    buyable_config = (0, 0, 0, 0)

class Shadow(Character):
    general_config = (10, 5)
    combat_config = (2, 2, 2, 20, True, False, True, 25)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {'Notice': 10, 'Stealth': 10, 'Dominion Concealment': 5}, 75)
    buyable_config = (0, 0, 0, 0)

class Summoner(Character):
    general_config = (5, 5)
    combat_config = (3, 3, 3, 30, False, False, False, 10)
    combat_dp_limit = 0.5
    magic_config = (1, 60, 3, 5, 1, 1, 1, 1, 50, 10, 10, 10, 10)
    magic_dp_limit = 0.6
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Occult': 1, 'Composure': 3, 'Withstand Pain': 3}, {'Magic Appraisal': 5, 'Occult': 10}, 75)
    buyable_config = (0, 0, 0, 0)

class Tao(Character):
    general_config = (5, 10)
    combat_config = (2, 2, 2, 15, False, False, False, 30)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {'Style': 5}, 75)
    buyable_config = (0, 0, 0, 0)

class Technician(Character):
    general_config = (5, 5)
    combat_config = (2, 2, 1, 10, True, False, False, 50)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {}, 75)
    buyable_config = (0, 0, 0, 0)

class Thief(Character):
    general_config = (10, 5)
    combat_config = (2, 2, 2, 25, False, False, True, 20)
    combat_dp_limit = 0.5
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Acrobatics': 1, 'Athleticism': 3, 'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3, 'Poisons': 1, 'Sleight of Hand': 1, 'Stealth': 1}, {'Notice': 5, 'Sleight of Hand': 10, 'Stealth': 5, 'Dominion Concealment': 10}, 100)
    buyable_config = (0, 0, 0, 0)

class Warmage(Character):
    general_config = (5, 10)
    combat_config = (2, 2, 2, 25, True, True, True, 20)
    combat_dp_limit = 0.5
    magic_config = (1, 50, 2, 10, 2, 2, 2, 2, 20, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({}, {'Magic Appraisal': 5}, 75)
    buyable_config = (0, 0, 0, 0)

class Warrior(Character):
    general_config = (5, 15)
    combat_config = (2, 2, 2, 20, True, True, False, 30)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {'Athleticism': 5}, 75)
    buyable_config = (0, 0, 0.5, 0)

class WarriorMentalist(Character):
    repname = 'Warrior Mentalist'
    general_config = (5, 10)
    combat_config = (2, 2, 2, 25, True, True, True, 20)
    combat_dp_limit = 0.5
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (15, 2, 10, 1.00)
    psychic_dp_limit = 0.6
    secondary_config = ({'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3}, {}, 75)
    buyable_config = (0, 0, 0, 0)

class WarriorSummoner(Character):
    repname = 'Warrior Summoner'
    general_config = (5, 10)
    combat_config = (2, 2, 2, 20, True, True, True, 20)
    combat_dp_limit = 0.5
    magic_config = (1, 60, 3, 5, 1, 1, 1, 1, 20, 5, 5, 5, 5)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Poisons': 3}, {'Occult': 5}, 75)
    buyable_config = (0, 0, 0, 0)

class Weaponsmaster(Character):
    general_config = (5, 20)
    combat_config = (2, 2, 3, 30, True, True, False, 15)
    combat_dp_limit = 0.6
    magic_config = (3, 70, 3, 5, 3, 3, 3, 3, 0, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 1, 'Magic Appraisal': 3, 'Medicine': 3, 'Occult': 3, 'Composure': 1, 'Withstand Pain': 1}, {'Athleticism': 10}, 75)
    buyable_config = (0.5, 0.5, 0, 0.5)

class Wizard(Character):
    general_config = (5, 5)
    combat_config = (3, 3, 3, 30, False, False, False, 10)
    combat_dp_limit = 0.5
    magic_config = (1, 50, 2, 20, 2, 2, 2, 2, 100, 0, 0, 0, 0)
    magic_dp_limit = 0.6
    psychic_config = (20, 3, 5, 0.50)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Magic Appraisal': 1, 'Composure': 3, 'Withstand Pain': 3}, {'Magic Appraisal': 10, 'Occult': 5}, 75)
    buyable_config = (0, 0, 0, 0)

class WizardMentalist(Character):
    repname = 'Wizard Mentalist'
    general_config = (5, 5)
    combat_config = (3, 3, 3, 30, False, False, False, 10)
    combat_dp_limit = 0.5
    magic_config = (1, 50, 2, 15, 2, 2, 2, 2, 100, 0, 0, 0, 0)
    magic_dp_limit = 0.5
    psychic_config = (10, 2, 10, 1.00)
    psychic_dp_limit = 0.5
    secondary_config = ({'Athleticism': 3, 'Magic Appraisal': 1, 'Composure': 3, 'Withstand Pain': 3}, {'Magic Appraisal': 10, 'Occult': 5}, 75)
    buyable_config = (0, 0, 0, 0)