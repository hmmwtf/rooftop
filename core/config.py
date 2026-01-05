from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except ImportError:
    st = None

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("OKSSANGIMONG_ENV", "dev")
    data_dir: Path = Path(os.getenv("OKSSANGIMONG_DATA_DIR", "./data")).resolve()

    # Secrets: st.secrets -> os.getenv
    def _get_secret(self, key: str, default: str | None = None) -> str | None:
        # 1. try st.secrets (if available & nested key exists)
        if st is not None:
            try:
                # Assuming secrets might be flat or grouped. 
                # Checking top-level simple keys first.
                if key in st.secrets:
                    return str(st.secrets[key])
            except Exception:
                pass
        # 2. fallback to env
        return os.getenv(key, default)

    @property
    def kakao_rest_api_key(self) -> str | None:
        return self._get_secret("KAKAO_REST_API_KEY")

    @property
    def vworld_api_key(self) -> str | None:
        return self._get_secret("VWORLD_API_KEY")

    @property
    def vworld_domain(self) -> str | None:
        return self._get_secret("VWORLD_DOMAIN")

    # 버전 관리(계수/수식/데이터)
    engine_version: str = "0.1.0"
    coefficient_set_version: str = "v1"

settings = Settings()
