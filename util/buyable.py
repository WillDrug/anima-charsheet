from util.resources import Resource
from util.exceptions import NotEnoughData, PrerequisiteError, NotEnough
from util.activatable import Activatable


class Note:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class Buyable:
    REFERENCE = 'GENERIC'
    NOTE = None
    COST = {
        Resource: 10
    }

    PREREQUISITE = []

    def __init__(self, character, **kwargs):
        self.character = character
        self.invest = {}
        for k in self.COST:
            res = kwargs.get(k.__name__)
            if res is None:
                raise NotEnoughData(f'There needs to be {self.COST[k]} {k} to buy {self.__class__}')
            if res.value < self.COST[k]:
                raise NotEnough(f'{self.__class__} takes at least {self.COST[k]} of {k}.')
            self.invest[k] = res
        for pre in self.PREREQUISITE:
            if pre not in self.character.reference:
                raise PrerequisiteError(f'{self.__class__} requires {pre} referencing buyable first')
        self.activate()

    def set_usage(self, res):
        res.set_usage(f'Buying {self.__class__}')

    def deactivate(self):
        self.rem_bonuses()
        self.rem_notes()
        self.rem_activatables()
        self.rem_reference()
        for k in self.invest:
            self.invest[k].free()

    def rem_bonuses(self):
        pass

    def rem_notes(self):
        try:
            self.character.notes.remove(self.NOTE)
        except KeyError:
            pass

    def rem_activatables(self):
        pass

    def rem_reference(self):
        self.character.reference.remove(self.REFERENCE)

    def activate(self):
        self.add_bonuses()
        self.add_notes()
        self.add_activatables()
        self.add_reference()

    def add_bonuses(self):
        pass

    def add_notes(self):
        self.character.notes.add(self.NOTE)

    def add_activatables(self):
        pass
        # self.activatable = Activatable(character=self.character)
        # self.character.activatables.add(self.activatable)

    def add_reference(self):
        self.character.reference.add(self.REFERENCE)
