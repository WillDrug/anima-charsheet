

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