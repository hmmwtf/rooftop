import streamlit as st
from core.state import clear_state

def render_header(active: str = "home"):
    cols = st.columns([1, 1, 1, 4])
    with cols[0]:
        st.markdown("### 🌿 옥상이몽")
    with cols[1]:
        st.page_link("app.py", label="홈", icon="🏠")
    with cols[2]:
        st.page_link("pages/1_📍_주소입력.py", label="시뮬레이션", icon="🧪")
    with cols[3]:
        st.write("")

    with st.sidebar:
        st.markdown("## Navigation")
        st.page_link("pages/1_📍_주소입력.py", label="1) 주소입력", icon="📍")
        st.page_link("pages/2_📐_면적확인.py", label="2) 면적확인", icon="📐")
        st.page_link("pages/3_🌿_녹화계획.py", label="3) 녹화계획", icon="🌿")
        st.page_link("pages/4_📊_결과확인.py", label="4) 결과확인", icon="📊")
        st.page_link("pages/5_📄_리포트.py", label="5) 리포트", icon="📄")
        st.divider()
        if st.button("세션 초기화"):
            clear_state()
            st.success("초기화 완료. 페이지를 다시 선택하세요.")
