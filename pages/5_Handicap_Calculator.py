import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Handicap Engine | NorAL", page_icon="🧮", layout="wide")

st.markdown('<h1 style="color: #d4af37;">🧮 Course Handicap Generator</h1>', unsafe_allow_html=True)
st.write("Convert your NorAL Index into a Course Handicap for today's round.")
st.divider()

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. Fetch Data
    player_df = conn.read(worksheet="Players", ttl=0).dropna(subset=['Name', 'Index'])
    
    # 2. Hardcoded Course Data (Or pull from a 'Courses' tab if you prefer)
    # I've added Guntersville and Point Mallard as defaults
    courses = {
        "Guntersville State Park": {"Rating": 72.1, "Slope": 132, "Par": 72},
        "Point Mallard": {"Rating": 70.8, "Slope": 128, "Par": 72},
        "Custom Course": {"Rating": 72.0, "Slope": 113, "Par": 72}
    }

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Step 1: Select Player")
        player_name = st.selectbox("Select Competitor", player_df['Name'].tolist())
        user_index = player_df.loc[player_df['Name'] == player_name, 'Index'].values[0]
        st.info(f"Verified NorAL Index: **{user_index}**")

    with col2:
        st.subheader("Step 2: Select Course")
        course_name = st.selectbox("Select Tournament Venue", list(courses.keys()))
        
        if course_name == "Custom Course":
            rating = st.number_input("Course Rating", value=72.0, step=0.1)
            slope = st.number_input("Slope Rating", value=113, step=1)
            par = st.number_input("Course Par", value=72, step=1)
        else:
            rating = courses[course_name]["Rating"]
            slope = courses[course_name]["Slope"]
            par = courses[course_name]["Par"]
            st.write(f"**Rating:** {rating} | **Slope:** {slope} | **Par:** {par}")

    st.divider()

    # 3. THE CALCULATION (USGA Formula)
    # Course Handicap = (Index * (Slope/113)) + (Rating - Par)
    course_hcp = (user_index * (slope / 113)) + (rating - par)
    rounded_hcp = round(course_hcp)

    # 4. EXTREMELY IMPRESSIVE VISUAL DISPLAY
    st.markdown(f"""
        <div style="background-color: #1b4332; padding: 40px; border-radius: 15px; text-align: center; border: 2px solid #d4af37;">
            <h2 style="color: #d8f3dc; margin-bottom: 0;">OFFICIAL COURSE HANDICAP</h2>
            <h1 style="color: #d4af37; font-size: 80px; margin-top: 10px;">{rounded_hcp}</h1>
            <p style="color: #d8f3dc; font-style: italic;">Target Score for {player_name}: {par + rounded_hcp}</p>
        </div>
    """, unsafe_allow_html=True)

    st.caption("Calculated using the World Handicap System (WHS) standard formula.")

except Exception as e:
    st.error("Please ensure your 'Players' sheet is populated to use the generator.")
