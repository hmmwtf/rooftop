import streamlit as st
import pandas as pd

def point_map(lat: float, lon: float):
    df = pd.DataFrame([{"lat": lat, "lon": lon}])
    st.map(df)
