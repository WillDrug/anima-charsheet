from math import floor
from util.exceptions import NotEnoughData, OverLimit

class ModuleConfig:

    def __init__(self, character=None, dp_tracker=None, dp_limit=None, **kwargs):
        self.dp_tracker = dp_tracker
        self.character = character
        self.dp_limit = dp_limit

    def set_character(self, character):
        self.character = character

    def get_level(self):
        return floor(self.get_dp()/100)

    def get_presence(self):
        return self.get_level()*5

    def get_dp(self) -> int:
        if self.character is None:
            raise NotEnoughData(f'{self.__class__} is not connected to a character')
        return self.character.get_dp()

    def get_gnosis(self):
        if self.character is None:
            raise NotEnoughData(f'{self.__class__} is not connected to a character')
        return self.character.get_gnosis()

class Module:
    def __init__(self, config: ModuleConfig):
        self.config = config
        if self.config.dp_tracker is not None and self.config.dp_limit is not None:
            self.config.dp_tracker.add_local_limit(self, limit_pct=self.config.dp_limit)

    def boost(self, attribute, value, cost=None, limited=True):
        dp = self.config.dp_tracker.emit_resource(value, self)  # here over limit might occur
        try:
            attribute.boost(dp, cost=cost, limited=limited)
        except OverLimit as e:
            self.config.dp_tracker.free_resource(dp)
            raise e