import streamlit as st

from components.header import render_header
from core.state import ensure_session

def main():
    st.set_page_config(page_title="Okssangimong App", layout="wide")
    st.title("옥상이몽 (Okssangimong) - 屋上異夢")
    st.write("Roof Analysis & Effect Simulation")

if __name__ == "__main__":
    main()
    

st.set_page_config(
    page_title="옥상이몽 MVP",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

ensure_session()
render_header(active="home")

st.title("옥상이몽 MVP")
st.caption("주소 → 면적확인 → 녹화계획 → 결과 → 리포트 (Streamlit 멀티페이지)")

st.markdown(
    """
    ### 사용 방법
    왼쪽 사이드바에서 페이지를 순서대로 진행하세요.

    - 📍 주소입력
    - 📐 면적확인
    - 🌿 녹화계획
    - 📊 결과확인
    - 📄 리포트
    """
)

st.info(
    "이 스캐폴드는 코어 개발을 바로 시작할 수 있도록 '도메인 로직(core/)' 중심으로 뼈대를 잡아둔 상태입니다."
)
