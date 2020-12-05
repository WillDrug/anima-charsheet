from .exceptions import NotFound, OverLimit
from math import ceil

class Resource:
    def __init__(self, value=1):
        self.__usage = None
        self.__value = value

    def set_usage(self, usage):
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
