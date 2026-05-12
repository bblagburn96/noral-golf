import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Scoring Admin | NorAL", page_icon="✍️")

st.title("✍️ Tournament Scoring Admin")

# Simple Security Check
pin = st.sidebar.text_input("Enter Admin PIN", type="password")

if pin == "1924": # You can change this PIN
    st.success("Authorized: Scoring Mode Active")
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    with st.form("new_entry", clear_on_submit=True):
        st.subheader("Add New Competitor or Update Score")
        name = st.text_input("Player Name")
        index = st.number_input("Handicap Index", min_value=0.0, max_value=54.0, step=0.1)
        status = st.selectbox("Player Status", ["Active", "Guest"])
        
        submitted = st.form_submit_button("Push to Live Leaderboard")

    if submitted:
        if name:
            try:
                # 1. Fetch current data
                existing_df = conn.read(worksheet="Players", ttl=0)
                
                # 2. Add new row
                new_data = pd.DataFrame([{"Name": name, "Index": index, "Status": status}])
                updated_df = pd.concat([existing_df, new_data], ignore_index=True)
                
                # 3. Update Google Sheets
                conn.update(worksheet="Players", data=updated_df)
                st.balloons()
                st.success(f"Successfully added {name} to the NorAL field.")
            except Exception as e:
                st.error(f"Sync Error: {e}")
        else:
            st.error("Name field is required.")
else:
    st.warning("Please enter the Admin PIN in the sidebar to access scoring controls.")
