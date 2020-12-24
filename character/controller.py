from .character import Character
from util.items import Item
from util.time import TimeUnit, TimeTracker
from combat.profiles import CombatProfile
from combat.options import CombatOption
from .actions import PhysicalAction, CombatAction, MagicAction, PsyAction
from combat import Light
from util.tracked import Tracker
from util.exceptions import NotCompatible, NotAllowed
from secondary import Skill

def roll_d100():
    return 0

class Controller:
    def __init__(self, character: Character):
        self.character = character
        self.equipment = set()
        self.time = TimeTracker()
        self.action_tracker = Tracker(
            lambda: self.character.general.stats.get('DEX').value + self.character.general.stats.get('AGI').value,
            self.character,
            emit_limit={
                CombatAction: lambda: 1,
                MagicAction: lambda: 1,
                PsyAction: lambda: 1
            })
        self.time.track(*self.action_tracker.get_tick())
        self.time.track(*self.action_tracker.get_tick_emit())
        self.time.track(self.reset_actions, TimeUnit.ROUND)
        self.reset_actions()

    # time
    def tick(self, value: int = 1, unit: TimeUnit = TimeUnit.ROUND):
        self.time.tick(value, unit)

    # stuffs accumulations

    # actions
    def reset_actions(self):
        if self.__combat_action is not None:
            self.__combat_action.use()
        self.__combat_action = None
        if self.__magic_action is not None:
            self.__magic_action.use()
        self.__magic_action = None
        if self.__psy_action is not None:
            self.__psy_action.use()
        self.__psy_action = None

    # todo ROLLZ
    def combat_action(self, split=0):
        self.reset_actions()
        self.__combat_action = self.action_tracker.emit(1, CombatAction)
        self.__combat_action.split = split
        self.__combat_action.executed = 0

    def attack_action(self, profile: type, attack_type: type = Light, special: CombatOption = None, roll=None):
        if roll is None:
            roll = roll_d100()
        if self.__combat_action is None:
            self.combat_action()
        profile = self.character.combat.get_profile(profile)
        penalty = profile.PENALTY
        if attack_type not in profile.ATTACK_OPTIONS:
            raise NotCompatible(f'{profile} does not allow for a {attack_type} attack')
        if self.__combat_action.split > 0:
            penalty += profile.multiple_attack_penalty * self.__combat_action.split
        if special is not None:
            penalty += special.PENALTY
        try:
            return min(getattr(self.character.combat.attack, attack_type.__name__.lower()).value - penalty + roll,
                       self.character.get_limit()), special
        finally:
            if self.__combat_action.executed >= self.__combat_action.split:
                self.__combat_action.use()
            else:
                self.__combat_action.executed += 1

    def start_magic_action(self):
        self.reset_actions()
        self.__magic_action = self.action_tracker.emit(1, MagicAction)

    def end_magic_action(self):
        self.__magic_action.use()  # fixme when should it be used?

    def cast_spell(self, roll=None):  # todo: takes spell to cast, checks zeon trackers and shit.
        if self.__magic_action is None:
            raise NotAllowed('You need to initiate MAGICS first')
        if roll is None:
            roll = roll_d100()
        return min(self.character.magic.magic_projection.value + roll, self.character.get_limit())

    def psionic_action(self):
        self.reset_actions()
        self.__psy_action = self.action_tracker.emit(1, PsyAction)

    def cast_psy(self, roll=None):  # todo: takes psy ability to cast, checks PP and shit, may punch your fatigue.
        pass

    def skill_action(self, skill: type, roll=None):  # todo skill conditioning
        self.reset_actions()
        if not issubclass(skill, Skill):
            raise NotCompatible(f'{skill} is not a skill')
        action = self.action_tracker.emit(1)
        try:
            return min(self.character.get_limit(),
                       self.character.secondary.get_skill(skill.get_name()).value)
        finally:
            action.use()

    def generic_action(self, activatable):  # todo: switches any generic activatable on-off
        pass      # todo: activatable should declare if it takes an ACTION to use and what resources it needs.

    def defend(self):
        pass  # fixme implement

    def move(self):
        pass  # fixme should this even be tracked

    # equipment

    def add_equipment(self, e: Item):
        self.equipment.add(e)

    def rem_equipment(self, e):
        self.equipment.remove(e)

    # Physical Action
    # Attack Action
    # Magic Action
    # Psy Action
    # Action tracker
    # time tracker
    # action limit restore
    # equipment
