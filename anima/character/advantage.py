from anima.util.powers import Benefit


class Advantage(Benefit):
    pass

class JackOfAllTrades(Advantage):
    def initialize(self, *args, **kwargs):
        s = self.source.skills
        f = lambda: 4
        for skill in s.foreach():
            skill.get_penalty = f
            for spec in skill.foreach():
                spec.get_penalty = f

