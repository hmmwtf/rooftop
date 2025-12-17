"""Domain constants.

NOTE:
- 지금은 임의값/placeholder여도 OK.
- 중요한 건 '버전'과 '출처'를 구조적으로 담을 수 있게 해두는 것.
"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class GreeningCoeff:
    type_code: str
    # 예: kg CO2 / m2 / year
    co2_kg_m2_y: float
    # 예: C reduction at 100% coverage
    temp_reduction_c_at_100: float

DEFAULT_BASELINE_SURFACE_TEMP_C = 60.0

# MVP 기본 계수 세트 (임시)
DEFAULT_GREENING_COEFFS: dict[str, GreeningCoeff] = {
    "grass": GreeningCoeff("grass", co2_kg_m2_y=0.5, temp_reduction_c_at_100=2.5),
    "sedum": GreeningCoeff("sedum", co2_kg_m2_y=1.0, temp_reduction_c_at_100=4.7),
    "shrub": GreeningCoeff("shrub", co2_kg_m2_y=3.0, temp_reduction_c_at_100=3.8),
    "tree": GreeningCoeff("tree", co2_kg_m2_y=4.0, temp_reduction_c_at_100=5.5)
}

# 소나무 환산 (임시): kg CO2 / year / tree
DEFAULT_PINE_FACTOR_KG_PER_YEAR = 9.13
