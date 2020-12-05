from math import floor
from util.exceptions import NotEnoughData

class ModuleConfig:

    def __init__(self, character=None, **kwargs):
        self.character = character

    def set_character(self, character):
        self.character = character

    def get_level(self):
        return floor(self.get_dp()/100)

    def get_presence(self):
        return self.get_level()*5

    def get_dp(self) -> int:
        if self.character is None:
            raise NotEnoughData(f'{self.__class__} is not connected to a character')
        return self.character.get_dp()

    def get_gnosis(self):
        if self.character is None:
            raise NotEnoughData(f'{self.__class__} is not connected to a character')
        return self.character.get_gnosis()
