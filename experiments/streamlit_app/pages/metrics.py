import streamlit as st
import pandas as pd

st.title("📊 TrojanChat Performance")

data = pd.DataFrame({
    "latency_ms": [380, 410, 395, 402],
    "tokens_used": [110, 128, 121, 130]
})

st.line_chart(data)