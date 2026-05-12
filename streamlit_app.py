import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration
st.set_page_config(page_title="NorAL Golf | Hub", page_icon="⛳", layout="wide")

# 2. Auto-Refresh (Updates the leaderboard every 60 seconds without a manual refresh)
st_autorefresh(interval=60 * 1000, key="leaderboard_refresh")

# 3. High-End Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0b090a; }
    .hero {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1535131749006-b7f58c99034b?q=80&w=2070');
        background-size: cover;
        padding: 80px 20px;
        text-align: center;
        color: #d8f3dc;
        border-radius: 20px;
        border: 1px solid #1b4332;
        margin-bottom: 30px;
    }
    .leaderboard-title {
        color: #d8f3dc;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Hero Section
st.markdown('<div class="hero"><h1>NORAL GOLF</h1><p>North Alabama\'s Premier Tournament Series</p></div>', unsafe_allow_html=True)

st.divider()

# 5. Live Leaderboard Section
st.markdown('<p class="leaderboard-title">🏆 Live Tracking Leaderboard</p>', unsafe_allow_html=True)

# Initialize Connection
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Read the 'Players' tab from your Google Sheet
    # ttl=0 ensures the app pulls fresh data every time it refreshes
    df = conn.read(worksheet="Players", ttl=0)
    
    # Filter out empty rows and sort by Index (lowest to highest)
    leaderboard_df = df.dropna(subset=['Name', 'Index']).sort_values("Index")
    
    # Display the Leaderboard in a professional table
    st.dataframe(
        leaderboard_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Name": "Player Name",
            "Index": st.column_config.NumberColumn("Current Index", format="%.1f"),
            "Status": "Member Status"
        }
    )
except Exception as e:
    st.info("Leaderboard is initializing... Please ensure your Google Sheet has headers: Name, Index, Status.")

st.divider()

# 6. Quick Navigation Info
col1, col2 = st.columns(2)
with col1:
    st.write("### Next Event")
    st.success("📅 **July 25, 2026** | Guntersville State Park")
with col2:
    st.write("### Join the Roster")
    st.write("Contact us to verify your handicap and join the 2026 season.")
