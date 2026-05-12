import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="NorAL Golf | Official Hub", page_icon="⛳", layout="wide")

# 2. Auto-Refresh (Updates every 60 seconds for live scoring feel)
st_autorefresh(interval=60 * 1000, key="leaderboard_refresh")

# 3. SME-Grade Custom Styling (Dark Mode & Gold Accents)
st.markdown("""
    <style>
    .main { background-color: #0b090a; }
    [data-testid="stMetricValue"] { font-size: 32px; color: #d4af37 !important; }
    [data-testid="stMetricLabel"] { font-size: 18px; color: #d8f3dc !important; }
    .hero {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1535131749006-b7f58c99034b?q=80&w=2070');
        background-size: cover;
        padding: 60px 20px;
        text-align: center;
        color: #d8f3dc;
        border-radius: 15px;
        border: 2px solid #1b4332;
        margin-bottom: 25px;
    }
    .section-header {
        color: #d4af37;
        font-family: 'serif';
        font-size: 28px;
        font-weight: bold;
        border-bottom: 1px solid #1b4332;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Hero Branding
st.markdown('<div class="hero"><h1>NORAL GOLF</h1><p>The Standard for North Alabama Competitive Play</p></div>', unsafe_allow_html=True)

# 5. Live Data Engine
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Pull data with 0 cache for instant updates
    df = conn.read(worksheet="Players", ttl=0)
    df = df.dropna(subset=['Name', 'Index']).sort_values("Index")

    # --- TOP 3 PODIUM SECTION ---
    st.markdown('<p class="section-header">🏆 Current Leaders</p>', unsafe_allow_html=True)
    top_3 = df.head(3)
    p_col1, p_col2, p_col3 = st.columns(3)
    
    podium_cols = [p_col1, p_col2, p_col3]
    for i, (index, row) in enumerate(top_3.iterrows()):
        with podium_cols[i]:
            st.metric(label=f"Rank #{i+1}", value=row['Name'], delta=f"Index: {row['Index']}", delta_color="off")

    st.write("") # Spacer

    # --- FULL FIELD SECTION ---
    st.markdown('<p class="section-header">📊 Full Field Standings</p>', unsafe_allow_html=True)
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Name": st.column_config.TextColumn("Competitor"),
            "Index": st.column_config.NumberColumn("Handicap Index", format="%.1f"),
            "Status": st.column_config.SelectboxColumn("Status", options=["Active", "Guest"])
        }
    )

except Exception as e:
    st.error("Waiting for tournament data connection...")
    st.info("Ensure your Google Sheet has 'Name' and 'Index' columns.")

st.divider()

# 6. Tournament Dashboard
st.markdown('<p class="section-header">📅 Upcoming Major</p>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**Event:** NorAL 2-Man Scramble")
    st.write("**Course:** Guntersville State Park")
with c2:
    st.write("**Date:** July 25, 2026")
    st.write("**Field:** Unified Pool")
with c3:
    st.button("View Registration Info", use_container_width=True)
