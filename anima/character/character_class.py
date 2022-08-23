from anima.util.bonuses import Bonus
from anima.util.mixins import DispatchesBonuses, Referencable
from math import floor
from anima.util.parameters import Attribute

#fixme fill in skill_bonuses

class SkillPoints(Attribute):
    def initialize(self, *args, **kwargs):
        def val():
            return self.source.source.presence.value * self.source.SP_BONUS

        self._value_f = val


class CharacterClass(DispatchesBonuses, Referencable):
    LP_BONUS = 0
    LPM = 1
    INITIATIVE = 0
    MK = 0
    # physical
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 2
    ATK_BONUS_MULTIPLE = 0
    BLK_BONUS_MULTIPLE = 0
    DDG_BONUS_MULTIPLE = 0
    WEAPON_NUM = 1

    # magical
    MAGIC_LIMIT = 0.5
    ZEON_COST = 2
    ZEON_ACCUM_COST = 2
    MAGIC_PROJECTION_COST = 2
    ML_COST = 2
    SUMMON_COST = 2
    CONTROL_COST = 2
    BIND_COST = 2
    BANISH_COST = 2
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BANISH_BONUS = 0
    BIND_BONUS = 0

    # psychic
    PSYCH_LIMIT = 0.5
    PP_COST = 2
    PSYCHIC_PROJECTION_COST = 2
    POTENTIAL_BONUS = 1
    PP_BONUS = 1

    # secondary
    SP_BONUS = 1
    SKILLS_HIGH = []
    SKILLS_LOW = []
    CLASS_SKILLS = []  # those get +8 to their limit. should be used by the Limiter
    BONUS_SKILLS = []

    def __init__(self, source: "Character", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = source
        self.apply_lifepoints()
        self.apply_initiative()
        self.apply_mk()
        self.apply_combat()
        self.apply_magic()
        self.apply_psychic()
        self.skillpoints = SkillPoints(self, **kwargs)
        self.apply_skills()

    def apply_lifepoints(self):
        def val():
            return self.source.presence.value * self.LP_BONUS + self.source.stats.con.value * \
                   floor(self.source.skills.withstandpain.core_value / self.LPM)
            # fixme: this should account for SP not value

        self.dispatch_bonus(self.source.lifepoints, 0, value_f=val)

    def apply_initiative(self):
        def val():
            return self.source.presence.value * self.INITIATIVE

        self.dispatch_bonus(self.source.initiative, 0, self.iam, value_f=val)

    def apply_mk(self):
        self.source.mk._value_f = lambda: self.source.presence.value * self.MK

    def attack_bonus(self):
        return floor(min(2, self.ATK_BONUS_MULTIPLE) * self.source.presence.value)

    def block_bonus(self):
        return floor(min(2, self.BLK_BONUS_MULTIPLE) * self.source.presence.value)

    def dodge_bonus(self):
        return floor(min(2, self.DDG_BONUS_MULTIPLE) * self.source.presence.value)

    def apply_combat(self):
        self.dispatch_bonus(self.source.attack, 0, value_f=lambda: min(10, self.attack_bonus()))
        self.dispatch_bonus(self.source.defense.block, 0, value_f=lambda: min(10, self.block_bonus()))
        self.dispatch_bonus(self.source.defense.dodge, 0, value_f=lambda: min(10, self.dodge_bonus()))

    def zeon_bonus(self):
        return self.ZEON_BONUS * self.source.presence.value

    def apply_magic(self):
        self.dispatch_bonus(self.source.summon, 0, value_f=lambda: self.source.presence.value * self.SUMMON_BONUS)
        self.dispatch_bonus(self.source.banish, 0, value_f=lambda: self.source.presence.value * self.BANISH_BONUS)
        self.dispatch_bonus(self.source.bind, 0, value_f=lambda: self.source.presence.value * self.BIND_BONUS)
        self.dispatch_bonus(self.source.control, 0, value_f=lambda: self.source.presence.value * self.CONTROL_BONUS)
        self.dispatch_bonus(self.source.zeon, 0, value_f=self.zeon_bonus)

    def apply_psychic(self):
        self.dispatch_bonus(self.source.psychicpoints, 0, value_f=1 + self.PP_BONUS * self.source.presence.value)
        self.dispatch_bonus(self.source.psychicpotential, 0, value_f=self.source.presence.value + self.POTENTIAL_BONUS)

    def apply_skills(self):
        for skill_name in self.BONUS_SKILLS:
            self.dispatch_bonus(self.source.access(f'skills.{skill_name}'), 0,
                                value_f=lambda: self.source.presence.value)

    @classmethod
    def impl_list(cls):
        return {q.iam: q for q in cls.__subclasses__()}

    @classmethod
    def get_class(cls, name):
        im = cls.impl_list()
        if name not in im:
            raise ModuleNotFoundError(f'{name} is not a valid character class')
        return im[name]


class AcrobaticWarrior(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 2
    MK = 5
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['acrobatics', 'style', 'sleightofhand', 'performance']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.33
    LPM = 4
    WEAPON_NUM = 3


class Assassin(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 2
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 20
    SKILLS_HIGH = ['athleticism', 'magicappraisal', 'medicine', 'occult', 'withstandpain']
    SKILLS_LOW = ['insight', 'notice', 'stealth', 'locksmithing']
    CLASS_SKILLS = ['insight', 'composure', 'poisons', 'stealth', 'locksmithing', 'disguise', 'deception']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.33
    LPM = 4
    WEAPON_NUM = 2


class DarkPaladin(CharacterClass):
    LP_BONUS = 3
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 20
    SKILLS_HIGH = ['']
    SKILLS_LOW = ['socialize', 'style']
    CLASS_SKILLS = ['socialize', 'style', 'composure', 'withstandpain', 'religion']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 2
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 3
    ML_COST = 10
    SUMMON_COST = 3
    CONTROL_COST = 1
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 4
    SUMMON_BONUS = 0
    CONTROL_BONUS = 2
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.33
    LPM = 3
    WEAPON_NUM = 2


class Freelancer(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 25
    SKILLS_HIGH = ['']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['acrobatics', 'animals', 'history', 'disguise', 'medicine', 'insight', 'forging', 'athleticism',
                    'locksmithing', 'nature', 'notice', 'composure', 'poisons', 'performance', 'sleightofhand',
                    'politics', 'ships', 'ride', 'survival', 'magic', 'stealth', 'religion', 'alchemy', 'withstandpain',
                    'socialize', 'animism', 'magicappraisal', 'style', 'magictech', 'occult']
    MAGIC_LIMIT = 0.6
    ZEON_COST = 2
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 2
    ML_COST = 10
    SUMMON_COST = 2
    CONTROL_COST = 2
    BIND_COST = 2
    BANISH_COST = 2
    ZEON_BONUS = 2
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.6
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 2
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Illusionist(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain', 'magictech']
    SKILLS_LOW = ['socialize']
    CLASS_SKILLS = ['sleightofhand', 'stealth', 'performance', 'socialize']
    MAGIC_LIMIT = 0.6
    ZEON_COST = 1
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 2
    ML_COST = 15
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 15
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.33
    LPM = 4
    WEAPON_NUM = 1


class IllusionistSocial(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain', 'magictech']
    SKILLS_LOW = ['magicappraisal']
    CLASS_SKILLS = ['magicappraisal', 'occult', 'performance']
    MAGIC_LIMIT = 0.6
    ZEON_COST = 1
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 2
    ML_COST = 15
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 15
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.33
    LPM = 4
    WEAPON_NUM = 1


class Mentalist(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 2
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 3
    KI_ACCUM_COST = 6
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.6
    PP_COST = 2
    PSYCHIC_PROJECTION_COST = 2
    POTENTIAL_BONUS = 2
    PP_BONUS = 1.00
    LPM = 4
    WEAPON_NUM = 1


class Paladin(CharacterClass):
    LP_BONUS = 3
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 20
    SKILLS_HIGH = ['poisons', 'sleightofhand', 'stealth', 'magictech']
    SKILLS_LOW = ['socialize', 'style', 'withstandpain']
    CLASS_SKILLS = ['athleticism', 'empathy', 'composure', 'withstandpain', 'socialize', 'religion', 'ride']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 2
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 3
    ML_COST = 10
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 1
    ZEON_BONUS = 4
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 2
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 3
    WEAPON_NUM = 2


class Ranger(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 20
    SKILLS_HIGH = ['magicappraisal', 'occult', 'composure', 'withstandpain', 'magictech']
    SKILLS_LOW = ['insight', 'notice', 'animals', 'survival']
    CLASS_SKILLS = ['insight', 'medicine', 'notice', 'survival', 'nature', 'animals']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Shadow(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 2
    MK = 5
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['insight', 'stealth', 'locksmithing', 'disguise', 'deception']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Summoner(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 2
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 3
    KI_ACCUM_COST = 6
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain']
    SKILLS_LOW = ['occult']
    CLASS_SKILLS = ['occult', 'religion']
    MAGIC_LIMIT = 0.6
    ZEON_COST = 1
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 1
    CONTROL_COST = 1
    BIND_COST = 1
    BANISH_COST = 1
    ZEON_BONUS = 10
    SUMMON_BONUS = 2
    CONTROL_BONUS = 2
    BIND_BONUS = 2
    BANISH_BONUS = 2
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 1


class Tao(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 1
    MK = 6
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 3
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['acrobatics', 'athleticism', 'stealth', 'performance']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Technician(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 10
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 1
    KI_ACCUM_COST = 2
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['style']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Thief(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 2
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 20
    SKILLS_HIGH = ['athleticism', 'magicappraisal', 'medicine', 'occult']
    SKILLS_LOW = ['acrobatics', 'poisons', 'sleightofhand', 'stealth', 'locksmithing']
    CLASS_SKILLS = ['acrobatics', 'sleightofhand', 'stealth', 'locksmithing', 'disguise', 'traplore']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Warmage(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 15
    SKILLS_HIGH = ['']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 1
    ZEON_ACCUM_COST = 10
    MAGIC_PROJECTION_COST = 2
    ML_COST = 10
    SUMMON_COST = 2
    CONTROL_COST = 2
    BIND_COST = 2
    BANISH_COST = 2
    ZEON_BONUS = 4
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Warrior(CharacterClass):
    LP_BONUS = 3
    INITIATIVE = 1
    MK = 6
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['athleticism', 'intimidation']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 3
    WEAPON_NUM = 3


class WarriorMentalist(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 5
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.6
    PP_COST = 3
    PSYCHIC_PROJECTION_COST = 2
    POTENTIAL_BONUS = 2
    PP_BONUS = 1.00
    LPM = 4
    WEAPON_NUM = 2


class WarriorSummoner(CharacterClass):
    LP_BONUS = 2
    INITIATIVE = 1
    MK = 4
    PHYS_LIMIT = 0.5
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 2
    KI_ACCUM_COST = 4
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 1
    SP_BONUS = 15
    SKILLS_HIGH = ['poisons', 'nature']
    SKILLS_LOW = ['']
    CLASS_SKILLS = ['religion']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 1
    ZEON_ACCUM_COST = 12
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 1
    CONTROL_COST = 1
    BIND_COST = 1
    BANISH_COST = 1
    ZEON_BONUS = 4
    SUMMON_BONUS = 1
    CONTROL_BONUS = 1
    BIND_BONUS = 1
    BANISH_BONUS = 1
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 2


class Weaponsmaster(CharacterClass):
    LP_BONUS = 4
    INITIATIVE = 1
    MK = 3
    PHYS_LIMIT = 0.6
    ATK_COST = 2
    DEF_COST = 2
    KI_COST = 3
    KI_ACCUM_COST = 6
    ATK_BONUS_MULTIPLE = 1
    BLK_BONUS_MULTIPLE = 1
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['magicappraisal', 'medicine', 'occult', 'magictech']
    SKILLS_LOW = ['athleticism', 'composure', 'withstandpain']
    CLASS_SKILLS = ['athleticism', 'composure', 'withstandpain', 'ride']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 3
    ZEON_ACCUM_COST = 14
    MAGIC_PROJECTION_COST = 3
    ML_COST = 5
    SUMMON_COST = 3
    CONTROL_COST = 3
    BIND_COST = 3
    BANISH_COST = 3
    ZEON_BONUS = 0
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 2
    WEAPON_NUM = 4


class Wizard(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 2
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 3
    KI_ACCUM_COST = 6
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain']
    SKILLS_LOW = ['magicappraisal']
    CLASS_SKILLS = ['magicappraisal', 'magictech']
    MAGIC_LIMIT = 0.6
    ZEON_COST = 1
    ZEON_ACCUM_COST = 10
    MAGIC_PROJECTION_COST = 2
    ML_COST = 20
    SUMMON_COST = 2
    CONTROL_COST = 2
    BIND_COST = 2
    BANISH_COST = 2
    ZEON_BONUS = 20
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 4
    PSYCHIC_PROJECTION_COST = 3
    POTENTIAL_BONUS = 1
    PP_BONUS = 0.50
    LPM = 4
    WEAPON_NUM = 1


class WizardMentalist(CharacterClass):
    LP_BONUS = 1
    INITIATIVE = 1
    MK = 2
    PHYS_LIMIT = 0.5
    ATK_COST = 3
    DEF_COST = 3
    KI_COST = 3
    KI_ACCUM_COST = 6
    ATK_BONUS_MULTIPLE = 0.5
    BLK_BONUS_MULTIPLE = 0.5
    DDG_BONUS_MULTIPLE = 0.5
    SP_BONUS = 15
    SKILLS_HIGH = ['athleticism', 'composure', 'withstandpain']
    SKILLS_LOW = ['magicappraisal']
    CLASS_SKILLS = ['magicappraisal']
    MAGIC_LIMIT = 0.5
    ZEON_COST = 1
    ZEON_ACCUM_COST = 10
    MAGIC_PROJECTION_COST = 2
    ML_COST = 15
    SUMMON_COST = 2
    CONTROL_COST = 2
    BIND_COST = 2
    BANISH_COST = 2
    ZEON_BONUS = 20
    SUMMON_BONUS = 0
    CONTROL_BONUS = 0
    BIND_BONUS = 0
    BANISH_BONUS = 0
    PSYCH_LIMIT = 0.5
    PP_COST = 2
    PSYCHIC_PROJECTION_COST = 2
    POTENTIAL_BONUS = 2
    PP_BONUS = 1.00
    LPM = 4
    WEAPON_NUM = 1
