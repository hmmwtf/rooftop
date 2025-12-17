from __future__ import annotations

from core.models import BuildingCandidate
from core.data_access.repositories import find_nearby_buildings
from core.exceptions import BuildingNotFoundError

class BuildingService:
    def find_candidates(self, lat: float, lon: float) -> list[BuildingCandidate]:
        return find_nearby_buildings(lat, lon, radius_m=200.0, limit=5)

    def choose_best(self, candidates: list[BuildingCandidate]) -> BuildingCandidate:
        if not candidates:
            raise BuildingNotFoundError("근처 건물 후보를 찾지 못했습니다.")
        # MVP: 가장 가까운 후보
        return candidates[0]
