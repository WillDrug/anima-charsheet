from util.parameters import ModuleConfig

class MagicConfig(ModuleConfig):
    def __init__(self, zeon_cost, ma_multiple_cost, mp_cost, summon_cost, control_cost, bind_cost, banish_cost, **kwargs):

        super().__init__(**kwargs)

class Magic:
    def __init__(self, config: MagicConfig):
        pass