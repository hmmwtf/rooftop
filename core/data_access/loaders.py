from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import pandas as pd

from core.config import settings

@lru_cache(maxsize=8)
def load_buildings_table() -> pd.DataFrame:
    """Load processed building table.

    Expected columns (example):
    - building_id, name, address, lat, lon, roof_area_m2 (optional)
    """
    path = Path(settings.data_dir) / "processed" / "buildings.parquet"
    if not path.exists():
        # MVP: empty table if not provided
        return pd.DataFrame(columns=["building_id", "name", "address", "lat", "lon", "roof_area_m2"])
    return pd.read_parquet(path)

@lru_cache(maxsize=8)
def load_lookup_table(name: str) -> pd.DataFrame:
    path = Path(settings.data_dir) / "lookup" / f"{name}.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
