import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("👥 The NorAL Roster")
st.write("All active players competing in the unified pool.")
st.divider()

conn = st.connection("gsheets", type=GSheetsConnection)
try:
    df = conn.read(worksheet="Players", ttl=0)
    
    # Filter to ensure we only show valid rows
    valid_players = df.dropna(subset=['Name'])
    
    for _, row in valid_players.iterrows():
        st.subheader(f"🏅 {row['Name']}")
        st.caption(f"Current Index: {row['Index']} | Status: {row.get('Status', 'Active')}")
        st.divider()
except Exception:
    st.info("The Roster is currently being updated for the 2026 season.")
