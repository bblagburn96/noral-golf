import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("👥 The NorAL Roster")

conn = st.connection("gsheets", type=GSheetsConnection)
try:
    df = conn.read(worksheet="Players")
    for _, row in df.iterrows():
        st.subheader(f"🏅 {row['Name']}")
        st.caption(f"Current Index: {row['Index']}")
        st.divider()
except:
    st.info("The Roster is currently being updated for the 2026 season.")

