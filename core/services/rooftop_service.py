from __future__ import annotations

from core.models import RooftopAreaEstimate
from core.data_access.repositories import get_roof_area_from_candidate
from core.config import settings
from core.utils.geometry import polygon_area_m2
from api.vworld_wfs import get_building_polygon
from core.utils.availability import compute_availability_ratio

class RooftopService:
    def estimate_area(self, candidates, lat: float | None = None, lon: float | None = None) -> RooftopAreaEstimate:
        """Estimate rooftop area from candidates or fallback to None."""
        suggested = None
        floor_area_m2 = None
        confidence = "low"
        note = "면적 데이터가 없으면 사용자가 직접 입력하도록 유도합니다."

        for c in candidates or []:
            v = get_roof_area_from_candidate(c)
            if v and v > 0:
                suggested = float(v)
                floor_area_m2 = None
                confidence = "medium"
                note = "데이터 테이블의 roof_area_m2 값을 기반으로 추정했습니다. 정확도를 위해 확인이 필요합니다."
                break
            
            
        polygon = None
        if lat is not None and lon is not None and settings.vworld_api_key:
            try:
                polygon = get_building_polygon((lat, lon), api_key=settings.vworld_api_key)
            except Exception:
                polygon = None
            if polygon:
                area = polygon_area_m2(polygon)
                if area > 0:
                    floor_area_m2 = float(area)
                    if suggested is None:
                        suggested = float(area)
                        confidence = "low"
                        note = "VWorld 건물 폴리곤(WFS)으로 면적을 추정했습니다. 참고용으로 확인이 필요합니다."

        return RooftopAreaEstimate(
            roof_area_m2_suggested=suggested,
            floor_area_m2=floor_area_m2,
            availability_ratio=compute_availability_ratio(suggested, floor_area_m2),
            confidence=confidence,
            note=note,
            candidates=candidates or [],
        )