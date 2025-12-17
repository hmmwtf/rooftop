from __future__ import annotations

from core.models import RooftopAreaEstimate
from core.data_access.repositories import get_roof_area_from_candidate

class RooftopService:
    def estimate_area(self, candidates) -> RooftopAreaEstimate:
        """Estimate rooftop area from candidates or fallback to None."""
        suggested = None
        confidence = "low"
        note = "면적 데이터가 없으면 사용자가 직접 입력하도록 유도합니다."

        for c in candidates or []:
            v = get_roof_area_from_candidate(c)
            if v and v > 0:
                suggested = float(v)
                confidence = "medium"
                note = "데이터 테이블의 roof_area_m2 값을 기반으로 추정했습니다. 정확도를 위해 확인이 필요합니다."
                break

        return RooftopAreaEstimate(
            roof_area_m2_suggested=suggested,
            confidence=confidence,
            note=note,
            candidates=candidates or [],
        )
