from __future__ import annotations


def compute_availability_ratio(roof_area_m2: float | None, floor_area_m2: float | None) -> float | None:
    if roof_area_m2 is None or floor_area_m2 is None:
        return None
    if roof_area_m2 <= 0 or floor_area_m2 <= 0:
        return None
    return (roof_area_m2 / floor_area_m2) * 100