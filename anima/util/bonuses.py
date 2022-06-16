class Bonus:
    def __init__(self, code, value):
        self.code = code
        self.value = value

    def __radd__(self, other):
        if isinstance(other, Bonus):
            return self.value + other.value
        else:
            return self.value + other

    def __eq__(self, other):
        if isinstance(other, Bonus):
            return self.code == other.code
        else:
            return self.code == other

    def __hash__(self):
        return hash(self.code)