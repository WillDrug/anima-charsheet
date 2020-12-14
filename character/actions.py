from util.tracked import Tracked

class ActiveAction(Tracked):
    pass

class PhysicalAction(ActiveAction):
    pass

class MentalAction(ActiveAction):
    pass

class CombatAction(PhysicalAction):
    split = 0
    executed = 0

class MagicAction(MentalAction):
    pass

class PsyAction(MentalAction):
    pass