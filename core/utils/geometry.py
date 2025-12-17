from __future__ import annotations

import math
from typing import Iterable, Tuple

# NOTE:
# - 공간데이터(폴리곤)가 들어오면 shapely/pyproj로 확장하세요.
# - MVP 1차는 단순 계산/placeholder로도 충분.

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def polygon_area_m2(coords_lonlat: Iterable[Tuple[float, float]]) -> float:
    """Very rough planar area placeholder.

    coords_lonlat: [(lon, lat), ...] closed or open polygon.
    WARNING: Not accurate for real geographic coordinates.
    Replace with shapely + projected CRS in production.
    """
    pts = list(coords_lonlat)
    if len(pts) < 3:
        return 0.0
    # naive shoelace on degrees (placeholder)
    area = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0
