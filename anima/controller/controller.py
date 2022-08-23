from anima.actor.creature import Creature
from anima.character.character import Character
from typing import Union, Iterable
from anima.util.tracker import Tracker
from anima.controller.frozen import FrozenWeapon, Attack, Defense
from anima.util.damage import Location
from anima.util.exceptions import Choice
from anima.controller.augments import Augment
from itertools import chain
from random import randint

def uses_dice_roll(dice_type: str):  # expected xdy
    def wrap_dice_roll(method):
        num, heads = dice_type.split('d')
        num = int(num)
        heads = int(heads)

        def with_roll(*args, roll=None, **kwargs):
            if roll is None:
                sum = 0
                for d in range(num):
                    sum += randint(1, heads)
            return method(*args, roll=sum, **kwargs)

        return with_roll

    return wrap_dice_roll

def uses_augments(method):
    def inner(self, *args, augments: Iterable = (), **kwargs):
        for augment in self.augments:
            if augment.lifespan == method.__name__:
                if isinstance(augments, tuple):  # only fire a set creation if there's a hit on the augs
                    augments = []
                augments.append(augment)
        for augment in self.augments:
            if augment in augments:
                if augment.ticks is not None:
                    augment.ticks -= 1
        self.augments = [q for q in self.augments if q.ticks is None or q.ticks > 0]
        return method(self, *args, augments=augments, **kwargs)
    return inner

class CharacterController:
    """ This class will track a creature or a character, tracking their abilities, maneuvers (and augments to them)
    as well as health, zeon, ki, etc."""
    def __init__(self, character: Union[Creature, Character], **kwargs):
        self.character = character
        self.augments = list(chain(*[benefit() for benefit in self.character.benefits]))
        # todo: enhance this to full
        self.lifepoints = Tracker(self.character.lifepoints.value, self.character.regeneration.get_regen,
                                  min_f=lambda: -self.character.stats.con.value*5, name='Life Points')
        self.tick()

    @uses_augments
    def add_status(self, augments: Iterable = ()):
        pass

    @uses_augments
    def use_maneuver(self, augments: Iterable = ()):
        pass

    @uses_augments
    def tick(self, augments: Iterable = ()):
        pass

    @uses_augments
    @uses_dice_roll('1d20')
    def attack(self, weapon: str = 'unarmed', location: Location = None, ability=None, formula=None,
               present_choice=False, augments: Iterable = ()):
        if not isinstance(location, Location) and location is not None:
            location = Location.get_by_name(location)
        weapon = self.character.combatprofile.get_weapon(weapon)
        if (formula is None or location is None or ability is None) and present_choice:
            raise Choice('Pick choices or resolve to first', {
                'ability': ability if ability is not None else weapon.ALLOWED_ABILITY,
                'formula': formula if formula is not None else weapon.formulas,
                'location': location if location is not None else Location.all()
            })
        frozen = FrozenWeapon(weapon, ability=ability, formula=formula)
        return Attack(frozen, location=location)

    @uses_augments
    @uses_dice_roll('1d20')
    def defense(self, weapon: str = 'unarmed', ability=None, present_choice=False, roll=None, augments: Iterable = ()):
        if ability is None and present_choice:
            raise Choice('Pick choices or resolve to first', {
                'ability': ability if ability is not None else [q.iam for q in cc.character.defense.attr_list()]
            })
        weapon = self.character.combatprofile.get_weapon(weapon)
        frozen = FrozenWeapon(weapon, def_ability=ability)
        defense = Defense(frozen, roll=roll)
        for aug in augments:
            aug(defense)
        return defense



if __name__ == '__main__':
    c = Character('test', 'acrobaticwarrior', '', starting_dp=20, con=1, presence=2, str=1, dex=4, attack=5,
                  acrobatics=1, withstandpain=10)
    from anima.character.advantage import JackOfAllTrades
    c.add_benefit(JackOfAllTrades)
    cc = CharacterController(c)
    from anima.equipment.weapon import Broadsword
    cc.character.combatprofile.add_weapon(Broadsword(cc.character))
    defense = cc.defense()
    print(defense)