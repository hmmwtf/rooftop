from __future__ import annotations

import requests
from core.models import LocationResult

class KakaoGeocodingProvider:
    """Kakao local API: address search.

    Docs: https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord
    """

    BASE_URL = "https://dapi.kakao.com/v2/local/search/address.json"

    def __init__(self, api_key: str, timeout_s: float = 5.0):
        self.api_key = api_key
        self.timeout_s = timeout_s

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None

        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        resp = requests.get(self.BASE_URL, headers=headers, params={"query": address}, timeout=self.timeout_s)
        resp.raise_for_status()
        data = resp.json()
        docs = data.get("documents") or []
        if not docs:
            return None

        d0 = docs[0]
        # x: lon, y: lat
        lon = float(d0.get("x"))
        lat = float(d0.get("y"))
        normalized = d0.get("address_name") or address

        return LocationResult(
            input_address=address,
            normalized_address=normalized,
            point={"lat": lat, "lon": lon},
            provider="kakao",
            extra={"raw": d0},
        )
