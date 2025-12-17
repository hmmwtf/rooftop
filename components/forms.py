import streamlit as st

def address_input_form() -> str | None:
    with st.form("address_form"):
        address = st.text_input("주소 입력", placeholder="예) 서울특별시 중구 세종대로 110")
        submitted = st.form_submit_button("주소 조회", type="primary")
    if submitted:
        return address.strip()
    return None
