

class AttributeMissingError(Exception):
    def __init__(self, source, attr, message=''):
        self.message = message
        self.source = source
        self.attr = attr
        super(AttributeMissingError, self).__init__(self.message)

    def __str__(self):
        return f'<AttributeMissingError: entity {self.source} does not have an attribute {self.attr} ({self.message})>'