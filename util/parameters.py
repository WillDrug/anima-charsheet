from weakref import WeakSet
from .exceptions import NotEnoughData, NotFound, OverLimit, FollowTheRules
from .resources import Resource
from math import floor
import traceback

class Base:
    def __init__(self, *args, **kwargs):
        pass


class Attribute(Base):
    # Any attribute in the game has
    # Value limit affected resource injection
    # For the main resource, there is a value cap
    # For the non-main resources there is no cap by default
    # Value Limit affected boosts
    # Function boosting as usual
    # Non-limit affected reousrce injections and boosts
    # Free-form injection should be possible.
    # -> limit affect becomes a by default True kwarg.
    # -> value limit is injected on value calculation
    # -> value limit is always got via a function (for DP dependent)
    # -> main resource is preset in class overrides or initiative
    # -> main resource cost cap is injected on boost function
    # -> main resource cost cap if always gotten via a function
    # -> everything else is free-form.
    DEFAULT_VALUE_CAP = None
    DEFAULT_BASE_RESOURCE_CAP = None
    BASE_RESOURCE = Resource

    def get_value_cap(self):  # overridable to be a function
        # THIS IS NOT A PROPERTY TO BE OVERRIDEN ESAILY
        return self.DEFAULT_VALUE_CAP

    def get_base_resource_cap(self):  # overridable to be a function
        return self.DEFAULT_BASE_RESOURCE_CAP  # this expects to have a base resource

    def get_base_resource_cost(self):
        return self.DEFAULT_BASE_RESOURCE_COST

    BASE_VALUE = 0  # not necessary, but a useful variable for like "base 20 initiative"
    DEFAULT_BASE_RESOURCE_COST = None

    def base_value(self):
        return self.BASE_VALUE

    def __init__(self, *args, base: Resource=None, base_res_cost=None,
                 base_lim_f=None, value_cap_f=None, **kwargs):
        self.boosts = []
        self.bonuses = {}
        if base is not None:
            self.BASE_RESOURCE = base
        if base_lim_f is not None:
            self.get_base_resource_cap = base_lim_f
        if value_cap_f is not None:
            self.get_value_cap = value_cap_f
        if base_res_cost is not None:
            self.DEFAULT_BASE_RESOURCE_COST = base_res_cost
        super().__init__(*args, **kwargs)

    def set_base_value_function(self, f):
        self.base_value = f

    @property
    def cost(self):
        """
        By default the cost property uses base_resource to calculate the actual cost. For the resource cost *IS* value
        It's the value prop of the Attribute which applies the cost for buying.
        :return: Attribut
        """
        return sum([q['boost'].value for q in self.boosts if isinstance(q['boost'], self.BASE_RESOURCE)])

    def bonus(self):
        """
        Append a function to value calculation of another attribute
        :return: Returns a function to use based on this attribute parm.
        """

        def bonus_append(calling_attribute):
            # todo: check if this works well
            if traceback.format_stack().__len__() > set(traceback.format_stack()).__len__():
                return 0  # todo logging with warning
            return self.value

        return self.__class__, bonus_append

    def rem_bonus(self, n):
        """
        Remove
        :param n: Name of bonus origin
        :return:
        """
        del self.bonuses[n]

    def add_bonus(self, n, f, limited=True):
        """
        Adds personal bonus
        :param n: Name of caller to delete later
        :param f: Function of bonus
        :return:
        """
        self.bonuses[n] = {'f': f, 'limited': limited}

    @property
    def value(self):
        limited = self.base_value() + sum([floor(q['boost'].value / q['cost']) for q in self.boosts if q['limited']]) + \
                  sum([self.bonuses[q]['f'](self) for q in self.bonuses if self.bonuses[q]['limited']])
        if self.get_value_cap() is not None:
            limited = min(limited, self.get_value_cap())
        return limited + \
               sum([floor(q['boost'].value / q['cost']) for q in self.boosts if not q['limited']]) + \
               sum([self.bonuses[q]['f'](self) for q in self.bonuses if not self.bonuses[q]['limited']])

    @property
    def modifier(self):  # free use, not affected much
        return 0

    def check_cost(self, update_value):
        cap = self.get_base_resource_cap()
        if cap is not None:
            if self.cost + update_value > cap:
                raise OverLimit(f'{self.__class__} cost can\'t go over {cap}.')


        super().check_sum_cost(update_value) # fixme doesn't work sometimes, might be best to declare in Base

    def boost(self, res: Resource, cost=None,
              limited=True):  # limited is VALUE LIMIT. COST limit always applies for base_resource
        if isinstance(res, self.BASE_RESOURCE):
            self.check_cost(res.value)
            if cost is None:
                cost = self.get_base_resource_cost()  # fixme
        if cost is None:
            cost = 1
        res.set_usage(f'Plus {res.value} to {self.__class__}')
        self.boosts.append({'boost': res, 'limited': limited, 'cost': cost})


class MultipartAttributeMixin(Base):
    INSTANCE_LIST = {}
    DEFAULT_SUM_BASE_RESOURCE_CAP = None

    @classmethod
    def __new__(cls, caller, attr_name, container, *args, **kwargs):
        """ Forces creation of an implementation on each Interface call
        """
        return_class = cls.impl_list().get(attr_name, None)
        if return_class is None:
            raise NotFound(
                f"{cls} class {attr_name} not found"
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

    @property
    def full_cost(self):
        return sum([inst.cost for inst in self.INSTANCE_LIST.get(self.container, [])])

    def get_sum_base_resource_cap(self):
        return self.DEFAULT_SUM_BASE_RESOURCE_CAP

    def __init__(self, attr_name, container, sum_resource_cap_f=None, *args, **kwargs):  # repeated to correctly pass attributes on
        if sum_resource_cap_f is not None:
            self.get_sum_base_resource_cap = sum_resource_cap_f
        self.container = container
        super().__init__(*([attr_name, container] + list(args)), **kwargs)

    def check_sum_cost(self, update_value):
        if self.get_sum_base_resource_cap() is not None:
            if self.full_cost + update_value > self.get_sum_base_resource_cap():
                raise OverLimit(f'Costs for {super()} cannot go over {self.get_sum_base_resource_cap()}')


class ChoiceAttributeMixin(Base):
    IGNORE = []

    def __init__(self, *args, **kwargs):
        for cls in self.impl_list():
            setattr(self, cls.lower(), self.impl_list().get(cls)(*args, **kwargs))
            for k in getattr(self, cls.lower()).__dict__:
                if k not in self.IGNORE:
                    setattr(getattr(self, cls.lower()), k, getattr(self, k))

    @classmethod
    def impl_list(cls) -> dict:
        return {subcl.__name__: subcl for subcl in cls.__subclasses__()}

    def add_local_bonus(self, n, f, limited=True):
        self.bonuses[n] = {'f': lambda x: 0 if not isinstance(x, self.__class__) else f(x), 'limited': limited}
