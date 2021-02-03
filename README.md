# Automatic Charsheet
This is supposed to be a backend for an automatic anima tool.
Creates a character sheet by homebrew rules.

# TODO
* Make controller actions return and accept *Action classes
  * Like `defend(atk: AttackAction) -> DefendAction`
  * Create unconnected combat controller `combat(atk: AttackAction, def: DefendAction) -> Damage`
  * Create `damage(dmg: Damage)` doing damage to character
* Make no controller action automatic (to be: frontend job)
* Martial Arts
* Weapon Profiles
* Ars Magnus
* Advantages
* 

# Done
* Buyables
* Combat Base
* General Base
* Mystic Base
* Psychic Base
* Secondary Base
* Tertiary