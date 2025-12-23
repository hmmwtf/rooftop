import streamlit as st

from components.common.footer import render_footer
from components.common.header import render_header
from core.services.analyze_service import AnalyzeService
from core.state import get_state, set_state
from ui.area_confirm_ui import render_area_confirm_ui

st.set_page_config(page_title="면적확인 | 옥상이몽", page_icon="📐", layout="wide")

render_header("simulate")

state = get_state()
loc = state.get("location")
if not loc:
    st.warning("먼저 '주소입력' 페이지에서 주소를 입력하세요.")
    st.stop()

svc = AnalyzeService()
estimate = svc.estimate_rooftop_area(loc)

suggested_area = estimate.roof_area_m2_suggested

floor_area = estimate.floor_area_m2
availability_ratio = estimate.availability_ratio

confirmed_area = state.get("roof_area_m2_confirmed")
default_area = confirmed_area if confirmed_area is not None else 0.0

address_title = loc.get("input_address") or "선택한 주소"
address_caption = loc.get("normalized_address") or address_title


ui_state = render_area_confirm_ui(
    address_title=address_title,
    address_caption=address_caption,
    floor_area=floor_area,
    suggested_area=suggested_area,
    availability_ratio=availability_ratio,
    default_area=default_area,
)

if ui_state["apply_clicked"]:
    try:
        parsed_area = float(ui_state["roof_area_value"].replace(",", "")) if ui_state["roof_area_value"] else 0.0
    except ValueError:
        parsed_area = -1
        
    if parsed_area <= 0:
        st.error("유효한 면적 값을 입력해주세요.")
    else:
        svc.confirm_area(parsed_area)
        set_state("roof_area_m2_confirmed", parsed_area)
        st.success("면적 값을 적용했습니다.")
        
        
if ui_state["prev_clicked"]:
    st.switch_page("pages/1_📍_주소입력.py")

if ui_state["next_clicked"]:
    if not get_state().get("roof_area_m2_confirmed") and suggested_area:
         st.info("추천 면적을 적용하려면 '값 적용'을 눌러주세요.")
    if not get_state().get("roof_area_m2_confirmed"):
        st.error("다음 단계로 이동하려면 면적을 입력해주세요.")
    else:
        st.switch_page("pages/3_🌿_녹화계획.py")


render_footer()