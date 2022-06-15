# Anima calculator and runner
The main idea is to allow an easy and fast creation of a character sheet
based on Anima Beyond Fantasy rework of mine.
This repo should contain
* Character sheet calculator: Extendable, reworkable.
* Character instance worker, allowing statuses and data
* Quick combat calculator
* Saving states
* Potentially a web interface

# Status
* Made a base structure (Creature -> Monster\Character -> Controller -> Checker)
* Coded in stats and resistances

# To-Do
1) Character generation
2) Character saving-loading
3) Character tracking
4) Character instance saving-loading
5) Combat calculator
6) Stage setter, allowing all-to-all tracking

# Nomenclature
* Entity: Base attribute of an object, referencable
* Attribute: Base score of an entity
* Ability: Rollable and raisable score
* Power: Usable thing
* Actor: Living entity
* Object: Non-living entity