from .parameters import Attribute
from .exceptions import NotEnoughData
from math import floor

class Ability(Attribute):
    STAT = None
    def __init__(self, *args, presence_f=None, stat_dict=None, **kwargs):
        kwargs['presence_f'] = presence_f
        kwargs['stat_dict'] = stat_dict  # this is done not to lose 'em
        if presence_f is None or stat_dict is None:
            raise NotEnoughData('Please pass presence function and stat dict.')
        self.__pres_f = presence_f
        self.__stat_dict = stat_dict
        super().__init__(*args, **kwargs)

    def base_value(self):
        return self.__pres_f() + self.__stat_dict.get(self.STAT).modifier


