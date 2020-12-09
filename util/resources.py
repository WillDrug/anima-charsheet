from .exceptions import NotFound, OverLimit, NotEnoughData
from math import ceil, floor

class Resource:
    def __init__(self, value=1):
        self.__usage = None
        self.__value = value

    def set_usage(self, usage, **kwargs):
        self.__usage = usage

    def set_value(self, value):
        self.__value = value

    @property
    def usage(self):
        return self.__usage

    @property
    def value(self):
        return self.__value


class ResourceTracker:
    def get_limit(self):
        return self.__limit()

    def __limit(self):
        raise NotImplementedError('This tracker does not support limit calculation')

    def __init__(self, resource: Resource, limit_f=None):
        self.resource_cls = resource
        self.track = []
        self.local_limits = {}
        if limit_f is not None:
            self.__limit = limit_f

    # todo: if there are more overrides, split into distinct functions
    def emit_resource(self, value=1, **kwargs):
        try:
            if self.get_total() + value > self.get_limit():
                raise OverLimit(f'{self.resource_cls} cannot be spent over {self.get_limit()}')
        except NotImplementedError:  # fixme: move to a base CheekyHack exception
            pass
        res = self.resource_cls(value=value)
        self.track.append(res)
        return res

    def free_resource(self, resource):
        try:
            del self.track[self.track.index(resource)]
        except ValueError:
            raise NotFound(f'Resource {resource} not in use')

    def _update_value(self, resource, value):  # dangerous function, make attributes use it
        # fixme: delete, just use resource's set_value from appropriate places
        try:
            idx = self.track.index(resource)
        except ValueError:
            raise NotFound(f'Resource {resource} is not tracked')
        self.track[idx].set_value(value)

    def get_total(self):
        return sum([q.value for q in self.track])


class IterativePointTracker(ResourceTracker):
    def get_total(self, only_one=False, only_two=False):
        if only_one == only_two:
            return super().get_total()
        if only_one:
            return sum([q.value for q in self.track if q.used_one == True])
        if only_two:
            return sum([q.value for q in self.track if q.used_two == True])

    def emit_resource(self, value=1, **kwargs):
        lock_one = False
        lock_two = False
        if self.get_limit() is not None:
            if self.get_total() + value > self.get_limit():
                raise OverLimit(f'There is no {self.resource_cls} left')
            if self.get_total(only_one=True) + value > ceil(self.get_limit() / 2):
                lock_one = True
            if self.get_total(only_two=True) + value > ceil(self.get_limit() / 2):
                lock_two = True
            if not lock_one and not lock_two:
                if self.get_total(only_one=True) + value > self.get_limit() / 2 and self.get_total(
                        only_two=True) + value > self.get_limit() / 2:
                    if self.track.__len__() > 0:
                        if self.track[-1].used_one:
                            lock_one = True
                        else:
                            lock_two = True
            if lock_two and lock_one:
                raise OverLimit(f'Too much {self.resource_cls} requested for single use')
            res = self.resource_cls(value=value, lock_one=lock_one, lock_two=lock_two)
            self.track.append(res)
            return res


class IterativePoint(Resource):
    def __init__(self, lock_one=False, lock_two=False, **kwargs):
        super().__init__(**kwargs)
        self.lock_one = lock_one
        self.lock_two = lock_two
        self.used_one = None
        self.used_two = None

    def set_usage(self, usage, one=False):
        if (one and self.lock_one) or (not one and self.lock_two):
            raise OverLimit(f'This {self.__class__} can\'t be used for this purpose.')
        self.used_one = one
        self.used_two = not one
        super().set_usage(usage)


class LocalLimitedPointTracker(ResourceTracker):
    def __init__(self, *args, **kwargs):
        self.local_limits = {}
        super().__init__(*args, **kwargs)

    def add_local_limit(self, k, limit_f=None, limit_pct=None):
        if limit_f is None and limit_pct is None:
            raise NotEnoughData('Provide either a lim function or lim percentage')
        if limit_pct is not None:
            limit_f = lambda: floor(self.get_limit()*limit_pct)
        self.local_limits[k] = limit_f

    def get_local_limit(self, module):
        if self.local_limits.get(module) is not None:
            return self.local_limits.get(module)()
        else:
            raise NotEnoughData('Local limit called with no local limit function set')  # fixme this should not be happening

    def get_local(self, usage):
        return sum([q.value for q in self.track if q.usage == usage])

    def emit_resource(self, value, module):
        if module in self.local_limits:
            if self.get_local(module)+value > self.get_local_limit(module):
                raise OverLimit(f'Local DP limit for {module} exceeded')
        return super().emit_resource(value)