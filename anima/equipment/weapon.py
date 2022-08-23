from anima.util.mixins import Referencable, Searchable
from math import floor
from anima.util.damage import DamageType, DamageFormula
from anima.actor.attributes import SizeType
from anima.util.exceptions import NotAllowed

class Weapon(Referencable, Searchable):
    SPEED = 0
    BASE_DAMAGE = 0
    PRIMARY_TYPES = []
    SECONDARY_TYPES = []
    AP = 0
    STAT = 'str'
    BREAKAGE = 0
    FORTITUDE = 0
    REACH = 0
    ALLOWED_ABILITY = ['light', 'heavy', 'ranged']

    ACTION_AREA = None

    PRECISION = False
    STR_REQ = 0

    TWO_HANDS_ALLOWED = False
    SHIELDED = False

    BASE_CRITICAL = 0

    def __init__(self, source, quality=0):
        self.source = source
        self.active = False
        self.quality = quality
        self.formulas = self.generate_formulas(self.PRIMARY_TYPES)
        # HOW THIS WORKS
        # If a maneuver uses secondary damage, it will re-generate formulas, plugging in SECONDARY Types before selection
        # If a maneuver substitues damage type but not value, it will take formula and switch the type after selection
        # MA would just add their own damage formulas
        # Auto-select will work either on max value or on first encountered (or both).

    # weapon specific
    def generate_formulas(self, damage_types: DamageType):
        formulas = [DamageFormula(q, self.get_base_damage, self.get_bonus_damage) for q in damage_types]
        if self.TWO_HANDS_ALLOWED:
            # same formula, extra bonus (2xSTR as default)
            formulas += [DamageFormula(q, self.get_base_damage, self.get_bonus_damage_2h, hands=2) for q
                         in damage_types]
        return formulas

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_bonus_damage(self):  # util function to generate formulas
        if self.STAT is None:
            return 0
        return self.source.access(f'stats.{self.STAT}').value

    def get_bonus_damage_2h(self):  # this is here to avoid a lambda in a default constructor
        if self.STAT is None:
            return 0
        return self.source.access(f'stats.{self.STAT}').value*2

    def get_base_damage(self): # util function to generate formulas
        return self.BASE_DAMAGE+self.quality*2

    def get_AP(self):
        return min(0, floor(2 * (self.source.access('stats.str').value / 3))) + self.quality

    def get_speed(self):
        return self.SPEED+self.quality

    def get_area(self):
        return self.ACTION_AREA

    def get_fortitude(self):
        return self.FORTITUDE+self.quality*2

    def get_breakage(self):
        return self.BREAKAGE+self.quality

    def get_shielded(self):
        return self.SHIELDED

    def get_base_critical(self):
        return self.BASE_CRITICAL

    # PROXY AREA (actual total values before augmentation based on character abilities
    def get_attack(self, atk_type: str = None):
        if atk_type is None:
            return self.source.attack.max_of(self.ALLOWED_ABILITY)
        if atk_type not in self.ALLOWED_ABILITY:
            raise NotAllowed(f'{atk_type} is not allowed with weapon {self}')
        return self.source.attack.__getattribute__(atk_type).value

    def get_defense(self, def_type: str = None):
        if def_type is None:
            return max(self.source.defense.block.value+self.quality, self.source.defense.dodge.value)
        if def_type == 'block':
            return self.source.defense.block.value+self.quality
        else:
            return self.source.defense.dodge.value

    def get_initiative(self):
        return self.get_speed()+self.source.initiative.value

    def __str__(self):
        return f'<Weapon({self.iam}+{self.quality})>'

class Ammunition:
    BASE_DAMAGE = 0

    def __init__(self, quality):
        self.quality = quality

    def get_base_damage(self):
        return self.BASE_DAMAGE + self.quality

class RangedWeapon(Weapon):
    def __init__(self, source, quality=0, ammo=None):
        super().__init__(source, quality=quality)
        if ammo is None:
            ammo = Ammunition(source)
        self.ammo = ammo

    def get_base_damage(self):
        return self.ammo.get_base_damage()

    def set_ammo(self, ammo: Ammunition):
        self.ammo = ammo

class Unarmed(Weapon):
    SPEED = 0
    BASE_DAMAGE = None
    PRIMARY_TYPES = [DamageType.impact]
    ALLOWED_ABILITY = ['light', 'heavy']

    def get_speed(self):
        base_speed = {
            SizeType.miniscule: 8,
            SizeType.small: 6,
            SizeType.medium: 4,
            SizeType.big: 2,
            SizeType.enormous: 0,
            SizeType.giant: -2,
            SizeType.colossal: -4
        }
        return base_speed[self.source.size.get_size_type()]

    def get_base_damage(self):
        base_damage = {
            SizeType.miniscule: 1,
            SizeType.small: 2,
            SizeType.medium: 2,
            SizeType.big: 4,
            SizeType.enormous: 6,
            SizeType.giant: 8,
            SizeType.colossal: 10
        }
        return base_damage[self.source.size.get_size_type()]

    def get_area(self):
        areas = {
            SizeType.enormous: 5,
            SizeType.giant: 15,
            SizeType.colossal: 60
        }
        if self.source.size.get_size_type() not in areas:
            return None
        else:
            return areas[self.source.size.get_size_type()]


class NaturalWeapon(Unarmed):
    SPEED = 0
    BASE_DAMAGE = None

    def get_base_damage(self):
        base_damage = {
            SizeType.miniscule: 4,
            SizeType.small: 6,
            SizeType.medium: 8,
            SizeType.big: 10,
            SizeType.enormous: 20,
            SizeType.giant: 24,
            SizeType.colossal: 28
        }
        return base_damage[self.source.size.get_size_type()]


class Broadsword(Weapon):
    SPEED = -1
    BASE_DAMAGE = 11
    AP = 0  # AP by default is based on STR
    STAT = 'dex'
    BREAKAGE = -5
    FORTITUDE = 8
    REACH = 1
    ALLOWED_ABILITY = ['light']
    PRIMARY_TYPES = [DamageType.cut]
    SECONDARY_TYPES = []