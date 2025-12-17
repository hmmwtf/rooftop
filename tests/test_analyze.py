from core.services.scenario_service import ScenarioService
from core.models import ScenarioInput

def test_scenario_compute_runs():
    svc = ScenarioService()
    res = svc.compute(roof_area_m2=1000.0, scenario=ScenarioInput(greening_type="sedum", coverage_ratio=0.5))
    assert res.green_area_m2 == 500.0
    assert res.co2_absorption_kg_per_year > 0
