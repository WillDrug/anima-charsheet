from .character import Character
from util.items import Item

class Controller:
    def __init__(self, character: Character):
        self.character = character
        self.equipment = set()

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
