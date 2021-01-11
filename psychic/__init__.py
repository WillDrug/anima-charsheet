from util.config import ModuleConfig, Module
from util.parameters import Attribute, Ability
from util.exceptions import MergedResource
from common.resources import DevelopmentPoint
from .resources import PsychicPoint, PsychicPointTracker
from math import floor

class PsychicConfig(ModuleConfig):
    def __init__(self, pp_cost, pproj_cost, potential_per_level, pp_per_level, **kwargs):
        self.pp_cost = pp_cost
        self.pproj_cost = pproj_cost
        self.potential_per_level = potential_per_level
        self.pp_per_level = pp_per_level
        super().__init__(**kwargs)

class Potential(Attribute):
    BASE_RESOURCE = PsychicPoint
    DEFAULT_BASE_RESOURCE_COST = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_f[PsychicPoint] = self.calc_pp_bonus

    def calc_pp_bonus(self, boost):
        if boost['boost'].value >= 55:
            return 100
        elif boost['boost'].value >= 45:
            return 90
        elif boost['boost'].value >= 36:
            return 80
        elif boost['boost'].value >= 28:
            return 70
        elif boost['boost'].value >= 21:
            return 60
        elif boost['boost'].value >= 15:
            return 50
        elif boost['boost'].value >= 10:
            return 40
        elif boost['boost'].value >= 6:
            return 30
        elif boost['boost'].value >= 3:
            return 20
        elif boost['boost'].value >= 1:
            return 10
        else:
            return 0

    def boost(self, res, cost=None,
              limited=True, **kwargs):
        if not isinstance(res, PsychicPoint):
            return super().boost(res, cost=cost, limited=limited, **kwargs)
        else:
            for q in self.boosts:
                if isinstance(q, PsychicPoint):
                    q.set_value(q.value+res.value)
                    raise MergedResource(f'Merged PP used')
            else:
                return super().boost(res, cost=cost, limited=limited, **kwargs)

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
        self.psychic_points_tracker = PsychicPointTracker(PsychicPoint, limit_f=lambda: self.maximum_psychic_points.value)

    def get_power(self, power):
        pass

    def increase_potential(self, value):
        pp = self.psychic_points_tracker.emit_resource(value)
        try:
            self.potential.boost(pp)
        except MergedResource:
            pp.free()
