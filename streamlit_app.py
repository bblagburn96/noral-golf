import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="NorAL Golf | Live", page_icon="⛳", layout="wide")

# 1. AUTO-REFRESH (Every 60 seconds)
st_autorefresh(interval=60 * 1000, key="leaderboard_refresh")

# 2. BRANDING CSS
st.markdown("""
    <style>
    .leaderboard-card {
        background-color: #1b4332;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }
    .live-indicator {
        color: #4ade80;
        font-weight: bold;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⛳ NorAL Golf Hub")

# 3. LIVE LEADERBOARD SECTION
st.markdown('### 🏆 Live Tracking Leaderboard <span class="live-indicator">● LIVE UPDATING</span>', unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Pulling data from your 'Rounds' or 'LiveScores' tab
    df = conn.read(worksheet="Players", ttl=0) # ttl=0 forces it to bypass cache
    
    # Sort by Score/Index
    leaderboard = df.sort_values("Index").head(5) 
    
    # Display the Top 5 in professional cards
    for i, row in leaderboard.iterrows():
        st.markdown(f"""
            <div class="leaderboard-card">
                <span>{row['Name']}</span>
                <span><b>{row['Index']}</b></span>
            </div>
        """, unsafe_allow_html=True)

except Exception:
    st.info("Leaderboard will populate once the first scores are logged.")

st.divider()

# 4. REST OF YOUR HOME PAGE
st.write("### Upcoming: July 25th Scramble")
st.write("Registration is currently open for the Guntersville event.")
