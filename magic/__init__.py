from util.config import ModuleConfig, Module

class MagicConfig(ModuleConfig):
    def __init__(self, zeon_cost, ma_multiple_cost, mp_cost, summon_cost, control_cost, bind_cost, banish_cost, **kwargs):

        super().__init__(**kwargs)

class Magic(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)