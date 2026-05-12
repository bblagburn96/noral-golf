import streamlit as st

st.set_page_config(page_title="NorAL Golf | Official Site", page_icon="⛳", layout="wide")

# High-Class UI Styling
st.markdown("""
    <style>
    .main { background-color: #0b090a; }
    .hero {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1535131749006-b7f58c99034b?q=80&w=2070');
        background-size: cover;
        padding: 100px 20px;
        text-align: center;
        color: #d8f3dc;
        border-radius: 20px;
        border: 1px solid #1b4332;
    }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero"><h1>NORAL GOLF</h1><h3>The Standard for North Alabama Competitive Play</h3></div>', unsafe_allow_html=True)

st.divider()

# Core Content
col1, col2 = st.columns(2)
with col1:
    st.header("The Mission")
    st.write("Organizing premier amateur golf tournaments across the Tennessee Valley with a focus on integrity and high-level competition.")
with col2:
    st.header("Upcoming Showcase")
    st.success("📅 **July 25, 2026** | 2-Man Scramble | Guntersville State Park")

