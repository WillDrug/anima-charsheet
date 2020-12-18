from .tracked import Tracker
from .exceptions import NotCompatible

class Activatable:
    active = False

    def __init__(self, character=None, buyable=None):
        self.character = character
        self.buyable = buyable

    def use(self):
        pass

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def maintain(self):
        pass

# todo from common import tracker, USES = (Tracker type)
# todo ACTIONS = 0 to identify physical action taking place
# todo take character on init to affect
# todo may return thing which can be done
# todo distinct between ACTIVATE\DEACTIVATE and USE