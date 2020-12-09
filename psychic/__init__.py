from util.config import ModuleConfig, Module
from util.parameters import Attribute
from util.abilities import Ability
from common.resources import DevelopmentPoint
from math import floor

class PsychicConfig(ModuleConfig):
    def __init__(self, pp_cost, pproj_cost, potential_per_level, pp_per_level, **kwargs):
        self.pp_cost = pp_cost
        self.pproj_cost = pproj_cost
        self.potential_per_level = potential_per_level
        self.pp_per_level = pp_per_level
        super().__init__(**kwargs)

class Potential(Attribute):
    pass

class PsychicProjection(Ability):
    STAT = 'PER'
    BASE_RESOURCE = DevelopmentPoint

class MaximumPsychicPoints(Attribute):
    BASE_RESOURCE = DevelopmentPoint

# todo PP Recovery somehow

class Psychic(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.potential = Potential()
        self.potential.add_bonus(self, lambda x: self.config.potential_per_level*self.config.get_level())
        self.potential.add_bonus(*self.config.character.general.stats.get('WIL').psy_potential_bonus())
        self.projection = PsychicProjection(presence_f=self.config.get_presence,
                                            stat_dict=self.config.character.general.stats,
                                            base_res_cost=self.config.pproj_cost)
        self.maximum_psychic_points = MaximumPsychicPoints(base_res_cost=self.config.pp_cost)
        self.maximum_psychic_points.add_bonus(self, lambda x: 1+floor(self.config.pp_per_level*self.config.get_level()))
        self.maximum_psychic_points.add_bonus(*self.config.character.general.stats.get('INT').pp_bonus())

