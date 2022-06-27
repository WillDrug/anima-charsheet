class Bonus:
    def __init__(self, code: str, value: int, value_f = None):
        self.code = code
        self._value = value
        if value_f is not None:
            self.value = value_f

    def value(self) -> int:
        return self._value

    def __radd__(self, other):
        if isinstance(other, Bonus):
            return self.value() + other.value()
        else:
            return self.value() + other

    def __eq__(self, other):
        if isinstance(other, Bonus):
            return self.code == other.code
        else:
            return self.code == other

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<Bonus ({self.code}: {self.value()})>'


class Bonusable:
    def __init__(self, *args, **kwargs):
        self.bonuses = set()

    def add_bonus(self, bonus: Bonus):
        if bonus in self.bonuses:
            self.bonuses.remove(bonus)  # this preserves the hash of a bonus object but allows to overwrite the value
        self.bonuses.add(bonus)

    def rem_bonus(self, bonus):
        self.bonuses.remove(bonus)
