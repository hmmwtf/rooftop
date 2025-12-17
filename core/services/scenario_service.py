from __future__ import annotations

from core.constants import (
    DEFAULT_BASELINE_SURFACE_TEMP_C,
    DEFAULT_GREENING_COEFFS,
    DEFAULT_PINE_FACTOR_KG_PER_YEAR,
)
from core.models import ScenarioInput, SimulationResult
from core.config import settings
from core.exceptions import InvalidScenarioError

class ScenarioService:
    def compute(
        self,
        roof_area_m2: float,
        scenario: ScenarioInput,
        baseline_surface_temp_c: float = DEFAULT_BASELINE_SURFACE_TEMP_C,
    ) -> SimulationResult:
        if roof_area_m2 <= 0:
            raise InvalidScenarioError("roof_area_m2 must be > 0")
        if scenario.coverage_ratio < 0 or scenario.coverage_ratio > 1:
            raise InvalidScenarioError("coverage_ratio must be in [0,1]")

        coeff = DEFAULT_GREENING_COEFFS.get(scenario.greening_type)
        if coeff is None:
            raise InvalidScenarioError(f"Unknown greening_type: {scenario.greening_type}")

        green_area = roof_area_m2 * scenario.coverage_ratio
        co2 = green_area * coeff.co2_kg_m2_y
        temp_reduction = coeff.temp_reduction_c_at_100 * scenario.coverage_ratio
        after_temp = baseline_surface_temp_c - temp_reduction
        tree_count = int(round(co2 / DEFAULT_PINE_FACTOR_KG_PER_YEAR)) if DEFAULT_PINE_FACTOR_KG_PER_YEAR > 0 else 0

        return SimulationResult(
            roof_area_m2=roof_area_m2,
            greening_type=scenario.greening_type,
            coverage_ratio=scenario.coverage_ratio,
            green_area_m2=green_area,
            co2_absorption_kg_per_year=co2,
            temp_reduction_c=temp_reduction,
            baseline_surface_temp_c=baseline_surface_temp_c,
            after_surface_temp_c=after_temp,
            tree_equivalent_count=tree_count,
            engine_version=settings.engine_version,
            coefficient_set_version=settings.coefficient_set_version,
            meta={
                "coeff": {
                    "co2_kg_m2_y": coeff.co2_kg_m2_y,
                    "temp_reduction_c_at_100": coeff.temp_reduction_c_at_100,
                }
            },
        )
