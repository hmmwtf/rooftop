"""Streamlit session state helpers.

UI가 바뀌어도 상태 키를 한 곳에서 관리하면 유지보수가 쉬워집니다.
"""

from __future__ import annotations
import streamlit as st

DEFAULTS = {
    "location": None,
    "roof_area_m2_confirmed": None,
    "scenario": None,
    "result": None,
}

def ensure_session() -> None:
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_state() -> dict:
    return {k: st.session_state.get(k) for k in DEFAULTS.keys()}

def set_state(key: str, value):
    st.session_state[key] = value

def clear_state():
    for k in DEFAULTS.keys():
        st.session_state[k] = DEFAULTS[k]
