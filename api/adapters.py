from __future__ import annotations

from typing import Protocol, Optional
from core.models import LocationResult

class GeocodingProvider(Protocol):
    def geocode(self, address: str) -> Optional[LocationResult]:
        ...
