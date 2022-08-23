
from anima.equipment.weapon import Weapon
from anima.util.damage import Damage, DamageFormula, Location

class FrozenFormula:
    def __init__(self, formula: DamageFormula):
        self._base = formula.get_base()
        self._bonus = formula.get_bonus()
        self._type = formula.get_type()
        self.limit = None

    def get_base(self):
        return self._base

    def get_bonus(self):
        return self._bonus

    def get_damage(self):
        return self.get_base()+self.get_bonus()

    def get_type(self):
        return self._type

    def __call__(self, location=None):
        dmg = self.get_damage()
        if self.limit is not None:
            dmg = max(self.limit, dmg)
        return Damage(self._type, dmg, location=location)

    def __repr__(self):
        return f'<FrozenFormula({self.get_base()}+{self.get_bonus()} of {self.get_type()})>'

class FrozenWeapon:
    def __init__(self, weapon: Weapon, ability: str = None, def_ability: str = None, formula: str = None):
        # todo: find a way to automatically collect all necessary methods =_=
        # SPEED, BASE_DAMAGE, PRIMARY_TYPES, SECONDARY_TYPES, AP, STAT, BREAKAGE, FORTITUDE, REACH, ALLOWED_ABILITY,
        # ACTION_AREA, PRECISION, STR_REQ, TWO_HANDS_ALLOWED, SHIELDED, get_bonus_damage, get_base_damage, get_damage,
        # get_AP, get_speed, get_area, get_fortitude, get_breakage, get_shielded, get_attack, get_defense, get_block,
        # get_dodge, get_initiative
        self._weapon = weapon
        proxied = ['get_bonus_damage', 'get_base_damage', 'get_AP', 'get_speed', 'get_area',
                   'get_fortitude', 'get_breakage', 'get_shielded', 'get_initiative']
        for func in proxied:  # static-up the values to modify to hell.
            val = getattr(self._weapon, func)()
            setattr(self, func, lambda: val)

        self.atk_type = ability
        if ability is None:
            self.atk = 0
            for q in self._weapon.ALLOWED_ABILITY:
                tmp = self._weapon.get_attack(q)
                if tmp > self.atk:
                    self.atk_type = q
        self.atk = self._weapon.get_attack(self.atk_type)

        self.def_type = def_ability
        if def_ability is None:
            self.defense = 0
            for q in self._weapon.source.defense.attr_list():
                if self._weapon.get_defense(q.iam) > self.defense:
                    self.def_type = q.iam
        self.defense = self._weapon.get_defense(self.def_type)

        if formula is None:
            q = 0
            for test in self._weapon.formulas:
                if test().damage > q:
                    formula = test
        else:
            formula = next((q for q in self._weapon.formulas if q == formula))
        self.damage_formula = FrozenFormula(formula)

    def generate_formulas(self, damage_types):
        return self._weapon.generate_formulas(damage_types)

    def get_attack(self):
        return self.atk

    def get_defense(self):
        return self.defense

    def get_damage(self, limit=None, location=None):
        ret = self.damage_formula(location=location)
        ret.limit = limit
        return ret

    def __str__(self):
        return f'<FrozenWeapon(attack {self.get_attack()} ({self.atk_type}), ' \
               f'damage {self.get_damage()}, defense {self.get_defense()}({self.def_type}))>'


class Attack:
    # this class represents the final output that a controller can do, consisting of everything an attack can have
    # in values. damage type, damage, final ability, maneuver, effects it produces, etc.
    def __init__(self, weapon: FrozenWeapon, location: Location = None, roll=0, limit=None):
        self.weapon = weapon
        self.location = location
        self.limit = limit
        self.roll = roll
        # weapon provides:
        # final augmented base damage
        # final augmented bonus damage
        # final augmented attack value

    def get_attack(self):  # calculated and done attack value
        return self.weapon.get_attack() if self.limit is None else max(self.weapon.get_attack(), self.limit)

    def get_damage(self):
        return self.weapon.damage_formula(location=self.location)

    def __str__(self):
        return f'<Attack(Weapon: {self.weapon._weapon}, Attack: ' \
               f'{self.get_attack() (self.weapon.get_attack()+self.roll)}, Damage {self.get_damage()})>'

class Defense:
    def __init__(self, weapon: FrozenWeapon, roll=0, limit=None):
        self.weapon = weapon
        self.limit = limit
        self.roll = roll

    def get_defense(self):
        return self.weapon.get_defense()+self.roll if self.limit is None else max(self.weapon.get_defense()+self.roll,
                                                                                  self.limit)

    def __str__(self):
        return f'<Defense(Weapon: {self.weapon._weapon}, Defense: ' \
               f'{self.get_defense()} ({self.weapon.get_defense()} ({self.weapon.def_type}) + {self.roll})>'

