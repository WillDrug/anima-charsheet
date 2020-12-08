from .parameters import Attribute
from .exceptions import NotEnoughData

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


class BaseResourceFree(Attribute):
    @property
    def value(self):  # change to yeet DP, they are used in STAT bonus.
        limited = self.base_value() + sum([floor(q['boost'].value / q['cost']) for q in self.boosts if q['limited']
                                           and not isinstance(q['boost'], self.BASE_RESOURCE)]) + \
                  sum([self.bonuses[q]['f'](self) for q in self.bonuses if self.bonuses[q]['limited']])
        if self.get_value_cap() is not None:
            limited = min(limited, self.get_value_cap())
        return limited + \
               sum([floor(q['boost'].value / q['cost']) for q in self.boosts if not q['limited']
                    and not isinstance(q['boost'], self.BASE_RESOURCE)]) + \
               sum([self.bonuses[q]['f'](self) for q in self.bonuses if not self.bonuses[q]['limited']])