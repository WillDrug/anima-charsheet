from anima.util.powers import Benefit
from anima.util.exceptions import ValueOverLimit
from math import floor


class Advantage(Benefit):
    COST = 1
    ALLOWED_QUANTITY = 0

    def __init__(self, *args, times_taken = 1, **kwargs):
        self.times_taken = times_taken
        super().__init__(*args, **kwargs)

    def increase(self):
        if self.times_taken + 1 > self.ALLOWED_QUANTITY:
            raise ValueOverLimit(f'{self.iam} cannot be taken more than {self.ALLOWED_QUANTITY} times')
        self.times_taken += 1

class JackOfAllTrades(Advantage):
    COST = 4
    def initialize(self, *args, **kwargs):
        s = self.source.skills
        f = lambda: 4
        for skill in s.foreach():
            skill.get_penalty = f
            for spec in skill.foreach():
                spec.get_penalty = f

class Artifact(Advantage):
    DESCRIPTION = 'Character is entitled to {} artifacts of a power level {}'
    COST = 1

    def description(self):
        return self.DESCRIPTION.format(1+floor(self.times_taken/6), floor(self.times_taken/2))

