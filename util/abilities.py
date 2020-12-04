from .parameters import Attribute


class Ability(Attribute):
    STAT = None
    def __init__(self, *args, presence_f, stat_dict):
        self.__pres_f = presence_f
        self.__stat_dict = stat_dict

    def base_value(self):
        return self.__pres_f() + self.__stat_dict.get(self.STAT).value