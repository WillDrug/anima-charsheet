from anima.util.parameters import Attribute
from anima.util.tracker import TimeType, Time

class Regeneration(Attribute):
    regen_lookup = {
        -4: 0,
        -3: 0,
        -2: 1,
        -1: 1,
        0: 1,
        1: 1,
        2: 1,
        3: 2,
        4: 2,
        5: 3,
        6: 4,
        7: 5,
        8: 6,
        9: 7,
        10: 8,
        11: 9,
        12: 10,
        13: 11,
        14: 12,
        15: 12
    }

    regen = {
        0: {True: (2, Time(TimeType.day, 1)), False: (1, Time(TimeType.day, 1))},
        1: {True: (4, Time(TimeType.day, 1)), False: (2, Time(TimeType.day, 1))},
        2: {True: (6, Time(TimeType.day, 1)), False: (3, Time(TimeType.day, 1))},
        3: {True: (8, Time(TimeType.day, 1)), False: (4, Time(TimeType.day, 1))},
        4: {True: (10, Time(TimeType.day, 1)), False: (5, Time(TimeType.day, 1))},
        5: {True: (15, Time(TimeType.day, 1)), False: (6, Time(TimeType.day, 1))},
        6: {True: (20, Time(TimeType.day, 1)), False: (20, Time(TimeType.day, 1))},
        7: {True: (50, Time(TimeType.day, 1)), False: (40, Time(TimeType.day, 1))},
        8: {True: (100, Time(TimeType.day, 1)), False: (100, Time(TimeType.day, 1))},
        9: {True: (1, Time(TimeType.minute, 5)), False: (1, Time(TimeType.minute, 5))},
        10: {True: (2, Time(TimeType.minute, 5)), False: (2, Time(TimeType.minute, 5))},
        11: {True: (5, Time(TimeType.minute, 5)), False: (5, Time(TimeType.minute, 5))},
        12: {True: (10, Time(TimeType.minute, 5)), False: (10, Time(TimeType.minute, 5))},
        13: {True: (1, Time(TimeType.round, 5)), False: (1, Time(TimeType.round, 5))},
        14: {True: (1, Time(TimeType.round, 1)), False: (1, Time(TimeType.round, 1))},
        15: {True: (2, Time(TimeType.round, 1)), False: (2, Time(TimeType.round, 1))},
        16: {True: (5, Time(TimeType.round, 1)), False: (5, Time(TimeType.round, 1))},
        17: {True: (10, Time(TimeType.round, 1)), False: (10, Time(TimeType.round, 1))},
        18: {True: (20, Time(TimeType.round, 1)), False: (20, Time(TimeType.round, 1))},
        19: {True: (50, Time(TimeType.round, 1)), False: (50, Time(TimeType.round, 1))}
    }
    def _value_f(self):
        stat = self.source.access('stats.con').value
        if stat > 15:
            stat = 15
        if stat < -4:
            stat = -4
        return self.regen_lookup[stat]

    def get_regen(self, resting):
        return self.regen[self.value][resting]
