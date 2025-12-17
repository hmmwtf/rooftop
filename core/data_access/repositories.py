from __future__ import annotations

import pandas as pd

from core.data_access.loaders import load_buildings_table
from core.models import BuildingCandidate
from core.utils.geometry import haversine_m

def find_nearby_buildings(lat: float, lon: float, radius_m: float = 150.0, limit: int = 5) -> list[BuildingCandidate]:
    df: pd.DataFrame = load_buildings_table()
    if df.empty:
        return []

    # 매우 단순한 거리 계산 (MVP)
    candidates = []
    for _, row in df.iterrows():
        try:
            d = haversine_m(lat, lon, float(row["lat"]), float(row["lon"]))
        except Exception:
            continue
        if d <= radius_m:
            candidates.append((d, row))

    candidates.sort(key=lambda x: x[0])
    out: list[BuildingCandidate] = []
    for d, row in candidates[:limit]:
        out.append(
            BuildingCandidate(
                building_id=str(row.get("building_id")),
                name=row.get("name"),
                address=row.get("address"),
                distance_m=float(d),
                extra={"roof_area_m2": row.get("roof_area_m2")},
            )
        )
    return out

def get_roof_area_from_candidate(candidate: BuildingCandidate) -> float | None:
    v = candidate.extra.get("roof_area_m2") if candidate.extra else None
    try:
        return float(v) if v is not None and v != "" else None
    except Exception:
        return None
