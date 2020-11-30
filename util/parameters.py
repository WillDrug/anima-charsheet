from weakref import WeakSet
from .exceptions import NotEnoughData, NotFound, OverLimit, FollowTheRules
from .resources import Resource
from math import floor
import traceback

class ModuleConfig:
    def __init__(self):
        self.__dpf = None

    def set_dpf(self, f):  # todo: move up interface class
        self.__dpf = f

    def get_dp(self) -> int:
        if self.__dpf is None:
            raise NotEnoughData(f'{self.__name__} does not have a function to get DP from')
        return self.__dpf()



class Attribute:
    STARTING_VALUE = 0
    COST_LIMIT = -1

    def __init__(self):
        self.previous_value = self.STARTING_VALUE
        self.base_value = self.STARTING_VALUE  # base value is 5, which will immediately detract from given points to spend
        self.boosts = []
        self.bonuses = {}

    @property
    def cost(self):
        return self.base_value

    def bonus(self):
        def bonus_append(calling_attribute):
            # todo: check if this works well
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0  # todo logging with warning
            return self.value
        return self.__name__, bonus_append

    def rem_bonus(self, n):
        del self.bonuses[n]

    def add_bonus(self, n, f):
        self.bonuses[n] = f

    @property
    def value(self):
        return self.base_value+floor(sum([q.value for q in self.boosts]))+floor(sum([self.bonuses[q](self) for q in self.bonuses]))

    @property
    def modifier(self):
        return 0

    def boost(self, res: Resource):
        res.set_usage(f'Plus {res.value} to {self.__name__}')
        self.boosts.append(res)

    def rollback_base_value(self):
        self.base_value = self.previous_value
        self.previous_value = self.STARTING_VALUE

    def change_base_value(self, value):
        if value < 0:
            raise OverLimit(f'Don\'t go making negatives unless overridden, lol')
        self.previous_value = self.base_value
        self.base_value = value
        if not self.check_limit():
            self.rollback_base_value()
            raise OverLimit(f'{self.__class__} cost can\'t be over {self.COST_LIMIT}')

    def check_limit(self):
        if self.COST_LIMIT == -1:
            return True
        else:
            return self.cost <= self.COST_LIMIT


class MultipartAttribute(Attribute):
    INSTANCE_LIST = {}
    SUM_COST_LIMIT = -1

    @classmethod
    def __new__(cls, caller, attr_name, container, *args, **kwargs):
        """ Forces creation of an implementation on each Interface call
        """
        return_class = cls.impl_list().get(attr_name, None)
        if return_class is None:
            raise NotFound(
                "Character class not found"
            )
        ret = object.__new__(return_class)
        if container not in cls.INSTANCE_LIST:
            cls.INSTANCE_LIST[container] = WeakSet()
        cls.INSTANCE_LIST[container].add(ret)
        return ret

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

    @classmethod
    def cls_full_cost(cls, container):
        return sum([inst.cost for inst in cls.INSTANCE_LIST.get(container, [])])

    def full_cost(self, container):
        return sum([inst.cost for inst in self.INSTANCE_LIST.get(container, [])])

    def __init__(self, attr_name, container):
        super().__init__()

    def check_global_limit(self):
        if self.SUM_COST_LIMIT > -1:
            return self.full_cost() <= self.SUM_COST_LIMIT
        else:
            return True

    def change_base_value(self, value):
        self.previous_value = self.base_value
        self.base_value = value

        if not self.check_limit(value):
            self.rollback_base_value()
            raise OverLimit(f'{self.__class__} cost can\'t be over {self.COST_LIMIT}}')
        if not self.check_global_limit():
            self.rollback_base_value()
            raise OverLimit(f'{super().__class__} total cost can\'t be over {self.SUM_COST_LIMIT}')
