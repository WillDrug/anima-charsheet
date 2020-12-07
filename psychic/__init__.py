from util.config import ModuleConfig, Module

class PsychicConfig(ModuleConfig):
    def __init__(self, pp_cost, pproj_cost, **kwargs):
        pass


class Psychic(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)