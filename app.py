"""
Ming QiMenDunJia 明奇门遁甲 - Main Application v6.0
Complete Edition with all QMDJ indicators
"""

import streamlit as st
from datetime import datetime, timezone, timedelta
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Ming QiMenDunJia 明奇门",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
    :root {
        --bg-primary: #0a0a12;
        --bg-secondary: #12121e;
        --bg-card: #1a1a2e;
        --gold-primary: #FFD700;
        --gold-secondary: #FFA500;
        --text-primary: #E8E8E8;
        --text-secondary: #888888;
        --accent-purple: #9B59B6;
        --success: #2ecc71;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0d0d1a 100%) !important;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 1rem;
        border-bottom: 2px solid var(--gold-primary);
        margin-bottom: 1rem;
    }
    
    .sidebar-logo h1 {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 1.6rem;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .sidebar-logo .chinese {
        font-size: 1.1rem;
        color: var(--gold-secondary);
        letter-spacing: 4px;
    }
    
    .sidebar-logo .version {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 0.3rem;
    }
    
    .nav-section {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 0.85rem;
        letter-spacing: 2px;
        padding: 0.75rem 1rem 0.5rem;
        margin-top: 0.5rem;
        border-top: 1px solid #333;
    }
    
    /* Main content */
    .main-header {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 2.5rem;
        text-align: center;
        letter-spacing: 3px;
    }
    
    .main-subtitle {
        font-family: 'Cormorant Garamond', serif;
        color: var(--text-secondary);
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    .energy-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0d0d1a 100%);
        border: 2px solid var(--gold-primary);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0 2rem 0;
    }
    
    .energy-time {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 3rem;
        font-weight: 700;
    }
    
    .energy-date {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    
    .dash-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .dash-card:hover {
        border-color: var(--gold-primary);
        transform: translateY(-3px);
    }
    
    .dash-card .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
    .dash-card .title {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 1rem;
        letter-spacing: 1px;
    }
    .dash-card .desc {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-purple), #8E44AD);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0.2rem;
    }
    
    .element-badge {
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.1rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1>MING QMDJ</h1>
        <div class="chinese">明 奇 门 遁 甲</div>
        <div class="version">v6.0 Complete Edition</div>
    </div>
    """, unsafe_allow_html=True)
    
    # GENERAL Section
    st.markdown('<div class="nav-section">GENERAL</div>', unsafe_allow_html=True)
    
    if st.button("📊 Chart Generator", key="nav_chart", use_container_width=True):
        st.switch_page("pages/1_Chart.py")
    
    if st.button("📤 Export Center", key="nav_export", use_container_width=True):
        st.switch_page("pages/2_Export.py")
    
    if st.button("📜 History", key="nav_history", use_container_width=True):
        st.switch_page("pages/3_History.py")
    
    # PERSONAL Section
    st.markdown('<div class="nav-section">PERSONAL</div>', unsafe_allow_html=True)
    
    if st.button("🎂 BaZi Calculator", key="nav_bazi", use_container_width=True):
        st.switch_page("pages/6_BaZi.py")
    
    if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")
    
    if st.button("❓ Help & Guide", key="nav_help", use_container_width=True):
        st.switch_page("pages/5_Help.py")
    
    # Profile Section
    st.markdown('<div class="nav-section">YOUR PROFILE</div>', unsafe_allow_html=True)
    
    if st.session_state.get("user_profile"):
        profile = st.session_state.user_profile
        st.markdown(f"**{profile.get('day_master', 'Unknown')}**")
        st.markdown(f"{profile.get('polarity', '')} {profile.get('element', '')} • {profile.get('strength', '')}")
        
        useful = profile.get('useful_gods', [])
        if useful:
            badges = " ".join([f'<span class="element-badge {g.lower()}">{g}</span>' for g in useful])
            st.markdown(f"Useful: {badges}", unsafe_allow_html=True)
        
        structures = []
        if profile.get('wealth_vault'):
            structures.append("💰 Vault")
        if profile.get('nobleman'):
            structures.append("👑 Noble")
        if structures:
            st.caption(" • ".join(structures))
    else:
        st.info("No profile set")
        if st.button("🔮 Set Up Profile", type="primary", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")

# ============================================================
# MAIN CONTENT
# ============================================================

st.markdown('<h1 class="main-header">MING QIMENDUNJIA</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">明奇门遁甲分析系统 • Qi Men Dun Jia Analysis System • v6.0 Complete Edition</p>', unsafe_allow_html=True)

# v6.0 Feature badges
st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <span class="feature-badge">✅ QMDJ Pillars</span>
    <span class="feature-badge">✅ Death & Emptiness</span>
    <span class="feature-badge">✅ Lead Indicators</span>
    <span class="feature-badge">✅ Horse Star</span>
    <span class="feature-badge">✅ Nobleman</span>
    <span class="feature-badge">✅ Ju Number</span>
</div>
""", unsafe_allow_html=True)

# Current Energy Card
SGT = timezone(timedelta(hours=8))
now = datetime.now(SGT)
st.markdown(f"""
<div class="energy-card">
    <div style="color: #888; font-size: 0.8rem; letter-spacing: 2px;">CURRENT COSMIC ENERGY</div>
    <div class="energy-time">{now.strftime("%H:%M")}</div>
    <div class="energy-date">{now.strftime("%A, %B %d, %Y")}</div>
</div>
""", unsafe_allow_html=True)

# Quick Action Cards
st.subheader("Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">📊</div>
        <div class="title">GENERATE CHART</div>
        <div class="desc">Full QMDJ with all indicators</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_chart", use_container_width=True):
        st.switch_page("pages/1_Chart.py")

with col2:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">🎂</div>
        <div class="title">BAZI CALCULATOR</div>
        <div class="desc">Your Four Pillars of Destiny</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_bazi", use_container_width=True):
        st.switch_page("pages/6_BaZi.py")

with col3:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">📤</div>
        <div class="title">EXPORT DATA</div>
        <div class="desc">Universal Schema v2.0 JSON</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_export", use_container_width=True):
        st.switch_page("pages/2_Export.py")

st.markdown("")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">📜</div>
        <div class="title">HISTORY</div>
        <div class="desc">Past readings & outcomes</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_history", use_container_width=True):
        st.switch_page("pages/3_History.py")

with col5:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">⚙️</div>
        <div class="title">SETTINGS</div>
        <div class="desc">Configure preferences</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")

with col6:
    st.markdown("""
    <div class="dash-card">
        <div class="icon">❓</div>
        <div class="title">HELP</div>
        <div class="desc">Learn QMDJ & BaZi</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open →", key="action_help", use_container_width=True):
        st.switch_page("pages/5_Help.py")

# v6.0 Features Info
st.markdown("---")
with st.expander("🆕 What's New in v6.0"):
    st.markdown("""
    ### v6.0 Complete Edition Features
    
    **Core QMDJ Indicators (Phase A):**
    - ✅ **QMDJ Four Pillars** - Chart time pillars (different from your BaZi!)
    - ✅ **Death & Emptiness (空亡)** - Know which palaces are weakened
    - ✅ **Lead Stem Palace (值符宫)** - The command palace
    - ✅ **Lead Star & Lead Door (直符/直使)** - Hour commanders
    - ✅ **Horse Star (驿马)** - Travel & fast results indicator
    - ✅ **Nobleman Star (贵人)** - Helpful people indicator
    - ✅ **Ju Number (局数)** - Structure number display
    
    **Coming in v6.0 Full Release:**
    - 📅 Strategic Execution Mode - Find golden moments
    - ⭐ QMDJ Destiny Analysis - Your birth as QMDJ chart
    - 📚 50+ Formation Database
    """)

# Footer
st.markdown("---")
st.caption("🌟 Ming QiMenDunJia 明奇门 | Developer Engine v6.0 | Universal Schema v2.0")
