from math import floor

class ModuleConfig:

    def __init__(self, dpf=None, gf=None, dp_limit=None, level_f=None):
        self.__dpf = dpf
        self.__gf = gf
        self.dp_limit = dp_limit

    def get_level(self):
        return floor(self.get_dp()/100)

    def get_presence(self):
        return self.get_level()*5

    def set_dpf(self, f):  # todo: move up interface class
        self.__dpf = f

    def get_dp(self) -> int:
        if self.__dpf is None:
            raise NotEnoughData(f'{self.__class__} does not have a function to get DP from')
        return self.__dpf()

    def set_gnosis_f(self, f):
        self.__gf = f

    def get_gnosis(self):
        return self.__gf()
