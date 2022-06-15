from anima.util.exceptions import AttributeMissingError

class Referencable:
    I_NAME = None

    @classmethod
    @property
    def iam(cls):
        return cls.I_NAME if cls.I_NAME else cls.__name__.lower()

class Searchable:
    def access(self, attr):
        if not isinstance(attr, str):
            attr = attr.iam
        try:
            return self.__getattribute__(attr)
        except AttributeError:
            raise AttributeMissingError(self, attr)
