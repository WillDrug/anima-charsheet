class AttributeMissingError(Exception):
    def __init__(self, source, attr, message=''):
        self.message = message
        self.source = source
        self.attr = attr
        super(AttributeMissingError, self).__init__(self.message)

    def __str__(self):
        return f'<{self.__class__.__name__}: entity {self.source} does not have an attribute {self.attr} ({self.message})>'


class PrerequisiteMissingError(Exception):
    def __init__(self, source, attr, message=''):
        self.message = message
        self.source = source
        self.attr = attr
        super(PrerequisiteMissingError, self).__init__(self.message)

    def __str__(self):
        return f'<{self.__class__.__name__}: entity {self.source} does not satisfy {self.attr} prerequisite ({self.message})>'


class ClassMistmatch(Exception):
    pass


class ValueOverLimit(Exception):
    pass


class NotAllowed(Exception):
    pass


class Choice(Exception):
    def __init__(self, message, kwargs: dict):
        super().__init__(message)
        self.kwargs = kwargs
        self.val = None

    def pick(self, k, val):
        if k not in self.kwargs:
            raise NotAllowed(f'{k} is not an applicable choice for. Allowed are {self.kwargs.keys()}')
        if val not in self.kwargs[k]:
            raise NotAllowed(f'{val} is not applicable for {k} choice. Allowed is: {self.kwargs[k]}')
        self.kwargs[k] = val

    def get_pickable(self):
        for k in self.kwargs:
            if isinstance(self.kwargs[k], list):
                yield k, self.kwargs[k]

    def resolve(self):
        for k in self.kwargs:
            if isinstance(self.kwargs[k], list):
                self.kwargs[k] = self.kwargs[k][0]
        return self.kwargs

    def __call__(self):
        return self.kwarg, self.val

    def __str__(self):
        return super().__str__()+f'(allowed {self.allowed})'