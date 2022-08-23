"""

CharacterController

Character

Profile

Weapon

Attack == liaison between Profile and Controller

StatContest


Maneuvers
    area attack and split attack generates several Attack instances based on the maneuver
        -> CharacterController aguments ATTACK instance gotten from Profile
    secondary weapon applies penalty
        -> CharacterController aguments ATTACK instance gotten from Profile
    secondary damage switches Damage[] to SECONDARY
        !
    disarm -> remove weapon ref from controller (!!) as an attack result parsing
        !

Attack:
    Weapon
        Ability (function to get called via a base ATTACk type, if allowed. can be augmented)
        Damage (list of class instances) - (type, base(func), bonus(func), real(func, default base+bonus))
    Maneuvers
        Append to result based on self function


Martial Arts:
    Full bonus: Modify WEAPON
    PerRound choice: Choice class within Character
        -> parsed and used by Character Controller.
        -> on init, on attack, on defense
    Augment Maneuver (half penalty for X for instance):
        -> Within Container
How to add Choices and Augments to CONTAINER?

MA, benefit, character.controller.add?
MA, benefit, ControllerAugments -> apply when generating?

Benefit class __call__() -> dispatch Choice, Activatable and Augment.

"""