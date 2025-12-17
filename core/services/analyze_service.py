from __future__ import annotations

import streamlit as st

from core.models import LocationResult, RooftopAreaEstimate, ScenarioInput, SimulationResult
from core.services.geocoding_service import GeocodingService
from core.services.building_service import BuildingService
from core.services.rooftop_service import RooftopService
from core.services.scenario_service import ScenarioService
from core.services.report_service import ReportService
from core.state import ensure_session


class AnalyzeService:
    """UI(페이지)에서 호출하는 유스케이스 진입점.

    멀티페이지 Streamlit에서는 세션 상태를 통해 입력/중간결과를 이어갑니다.
    추후 FastAPI로 분리할 때는 session_state 대신 DB를 붙이면 됩니다.
    """

    def __init__(self):
        ensure_session()
        self.geocoding = GeocodingService()
        self.buildings = BuildingService()
        self.rooftop = RooftopService()
        self.scenario = ScenarioService()
        self.report = ReportService()

    def set_address(self, address: str) -> LocationResult:
        loc = self.geocoding.geocode(address)
        st.session_state["location"] = loc.model_dump()
        return loc

    def estimate_rooftop_area(self, loc_dict: dict) -> RooftopAreaEstimate:
        lat = float(loc_dict["point"]["lat"])
        lon = float(loc_dict["point"]["lon"])
        candidates = self.buildings.find_candidates(lat, lon)
        est = self.rooftop.estimate_area(candidates)
        return est

    def confirm_area(self, roof_area_m2: float) -> None:
        st.session_state["roof_area_m2_confirmed"] = float(roof_area_m2)

    def set_scenario(self, scenario: ScenarioInput) -> None:
        st.session_state["scenario"] = scenario.model_dump()

    def compute(self) -> SimulationResult:
        roof_area = float(st.session_state["roof_area_m2_confirmed"] or 0.0)
        scenario_dict = st.session_state.get("scenario") or {}
        scenario = ScenarioInput(**scenario_dict)
        result = self.scenario.compute(roof_area_m2=roof_area, scenario=scenario)
        st.session_state["result"] = result.model_dump()
        return result

    def export_pdf(self) -> tuple[bytes, str]:
        result_dict = st.session_state.get("result") or {}
        result = SimulationResult(**result_dict)
        return self.report.build_pdf(result)

    def export_excel(self) -> tuple[bytes, str]:
        result_dict = st.session_state.get("result") or {}
        result = SimulationResult(**result_dict)
        return self.report.build_excel(result)
