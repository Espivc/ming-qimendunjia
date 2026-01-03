"""
===============================================================================
4_Settings.py - Ming QiMenDunJia Settings Page
===============================================================================
Version: 10.9
Updated: 2026-01-03

Features:
- BaZi Profile storage and retrieval
- Manual BaZi entry
- App preferences
===============================================================================
"""

import streamlit as st
from datetime import date, datetime
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Try to import BaZi calculator
try:
    from core.bazi_calculator import analyze_bazi, ELEMENT_COLORS
    IMPORT_SUCCESS = True
except ImportError:
    IMPORT_SUCCESS = False
    ELEMENT_COLORS = {
        'Wood': '#228B22', 'Fire': '#DC143C', 'Earth': '#DAA520',
        'Metal': '#C0C0C0', 'Water': '#1E90FF'
    }


def main():
    st.set_page_config(
        page_title="Settings | Ming Qimen",
        page_icon="⚙️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .profile-card {
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #DAA520;
        margin: 10px 0;
    }
    .section-header {
        color: #DAA520;
        border-bottom: 2px solid #DAA520;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# ⚙️ SETTINGS")
    st.caption("Configure preferences and manage your profile")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["👤 BaZi Profile", "✏️ Manual Entry", "🎨 Preferences"])
    
    # =========================================================================
    # TAB 1: BAZI PROFILE
    # =========================================================================
    with tab1:
        st.markdown("### Your BaZi Profile")
        
        # Check if profile exists in session state
        has_profile = 'user_profile' in st.session_state and st.session_state.user_profile is not None
        has_bazi = 'bazi_result' in st.session_state and st.session_state.bazi_result is not None
        
        if has_profile or has_bazi:
            # Get the profile data
            if has_bazi:
                result = st.session_state.bazi_result
                birth_info = st.session_state.get('bazi_birth_info', {})
            elif has_profile:
                result = st.session_state.user_profile
                birth_info = result.get('birth_info', {})
            
            # Display profile card
            dm = result.get('day_master', {})
            dm_color = ELEMENT_COLORS.get(dm.get('element', 'Earth'), '#DAA520')
            
            st.markdown(f"""
            <div class="profile-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: {dm_color};">
                            {dm.get('stem', '')} {dm.get('stem_cn', '')} Day Master
                        </h3>
                        <p style="margin: 5px 0; color: #888;">
                            {dm.get('polarity', '')} {dm.get('element', '')} | 
                            {dm.get('strength_pct', 0):.0f}% {dm.get('strength_category', '')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 12px; color: #888;">Birth Date</div>
                        <div style="font-size: 16px;">{birth_info.get('date', 'N/A')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show Four Pillars summary
            pillars = result.get('four_pillars', {})
            if pillars:
                cols = st.columns(4)
                for i, (name, pillar) in enumerate(pillars.items()):
                    with cols[i]:
                        color = ELEMENT_COLORS.get(pillar.get('element', 'Earth'), '#888')
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; border-radius: 8px;
                                    background: #1a1a2e; border: 1px solid {color};">
                            <div style="font-size: 11px; color: #888;">{name.upper()}</div>
                            <div style="font-size: 20px; color: {color};">{pillar.get('chinese', '')}</div>
                            <div style="font-size: 11px;">{pillar.get('animal', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Profile details
            with st.expander("📊 Profile Details", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Useful Elements:**")
                    useful = result.get('useful_gods', {}).get('useful', [])
                    st.success(", ".join(useful) if useful else "N/A")
                    
                    st.markdown("**Main Profile:**")
                    profile = result.get('profiles', {})
                    st.info(f"{profile.get('dominant', '')} → {profile.get('profile_name', '')}")
                
                with col2:
                    st.markdown("**Unfavorable Elements:**")
                    unfavorable = result.get('useful_gods', {}).get('unfavorable', [])
                    st.error(", ".join(unfavorable) if unfavorable else "N/A")
                    
                    st.markdown("**Life Star (Gua):**")
                    life_star = result.get('life_star', {})
                    gua_info = life_star.get('gua_info', {})
                    st.info(f"Gua {life_star.get('gua_number', '')} - {gua_info.get('name', '')}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Clear Profile", use_container_width=True):
                    if 'user_profile' in st.session_state:
                        del st.session_state.user_profile
                    if 'bazi_result' in st.session_state:
                        del st.session_state.bazi_result
                    if 'bazi_birth_info' in st.session_state:
                        del st.session_state.bazi_birth_info
                    st.success("Profile cleared!")
                    st.rerun()
            
            with col2:
                # Save as permanent profile
                if st.button("💾 Save as Default", use_container_width=True):
                    st.session_state.user_profile = result
                    st.session_state.user_profile['birth_info'] = birth_info
                    st.success("✅ Profile saved as default!")
            
            with col3:
                if st.button("📤 Export JSON", use_container_width=True):
                    json_str = json.dumps(result, indent=2, default=str)
                    st.download_button(
                        "⬇️ Download",
                        json_str,
                        "bazi_profile.json",
                        "application/json"
                    )
        
        else:
            st.warning("No BaZi profile set. Calculate your BaZi or enter manually.")
            
            # Quick calculate button
            if IMPORT_SUCCESS:
                st.markdown("---")
                st.markdown("### Quick Calculate")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    calc_date = st.date_input(
                        "Birth Date",
                        value=date(1978, 6, 27),
                        min_value=date(1900, 1, 1),
                        max_value=date.today()
                    )
                
                with col2:
                    calc_hour = st.selectbox(
                        "Birth Hour",
                        options=list(range(0, 24)),
                        index=20,
                        format_func=lambda x: f"{x:02d}:00 - {x:02d}:59"
                    )
                
                with col3:
                    calc_gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
                
                if st.button("🔮 Calculate My BaZi", type="primary", use_container_width=True):
                    with st.spinner("Calculating..."):
                        result = analyze_bazi(calc_date, calc_hour, calc_gender.lower())
                        st.session_state.bazi_result = result
                        st.session_state.bazi_birth_info = {
                            'date': calc_date.isoformat(),
                            'hour': calc_hour,
                            'gender': calc_gender
                        }
                        st.session_state.user_profile = result
                        st.session_state.user_profile['birth_info'] = st.session_state.bazi_birth_info
                        st.success("✅ BaZi calculated and saved!")
                        st.rerun()
            
            # Link to BaZi page
            st.markdown("---")
            st.info("👉 Or go to **BaZi** page for full analysis with detailed explanations.")
    
    # =========================================================================
    # TAB 2: MANUAL ENTRY
    # =========================================================================
    with tab2:
        st.markdown("### Manual BaZi Entry")
        st.caption("For advanced users who know their BaZi pillars")
        
        st.warning("⚠️ This is for users who already know their Four Pillars from another source.")
        
        # Manual entry form
        with st.form("manual_bazi"):
            st.markdown("**Four Pillars (天干地支)**")
            
            stems = ['Jia 甲', 'Yi 乙', 'Bing 丙', 'Ding 丁', 'Wu 戊', 
                    'Ji 己', 'Geng 庚', 'Xin 辛', 'Ren 壬', 'Gui 癸']
            branches = ['Zi 子 Rat', 'Chou 丑 Ox', 'Yin 寅 Tiger', 'Mao 卯 Rabbit',
                       'Chen 辰 Dragon', 'Si 巳 Snake', 'Wu 午 Horse', 'Wei 未 Goat',
                       'Shen 申 Monkey', 'You 酉 Rooster', 'Xu 戌 Dog', 'Hai 亥 Pig']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Year 年**")
                year_stem = st.selectbox("Stem", stems, key="y_stem")
                year_branch = st.selectbox("Branch", branches, key="y_branch")
            
            with col2:
                st.markdown("**Month 月**")
                month_stem = st.selectbox("Stem", stems, key="m_stem")
                month_branch = st.selectbox("Branch", branches, key="m_branch")
            
            with col3:
                st.markdown("**Day 日**")
                day_stem = st.selectbox("Stem", stems, key="d_stem", index=6)  # Default Geng
                day_branch = st.selectbox("Branch", branches, key="d_branch", index=8)  # Default Shen
            
            with col4:
                st.markdown("**Hour 时**")
                hour_stem = st.selectbox("Stem", stems, key="h_stem")
                hour_branch = st.selectbox("Branch", branches, key="h_branch")
            
            submitted = st.form_submit_button("Save Manual Entry", use_container_width=True)
            
            if submitted:
                st.info("Manual entry saved! Note: For full analysis, use the automatic calculator.")
    
    # =========================================================================
    # TAB 3: PREFERENCES
    # =========================================================================
    with tab3:
        st.markdown("### App Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Display Options**")
            
            show_chinese = st.checkbox("Show Chinese characters", value=True)
            show_pinyin = st.checkbox("Show Pinyin romanization", value=True)
            show_explanations = st.checkbox("Show detailed explanations", value=True)
        
        with col2:
            st.markdown("**Default Settings**")
            
            default_year = st.number_input("Default Analysis Year", 
                                          min_value=2020, max_value=2030, 
                                          value=2026)
            timezone = st.selectbox("Timezone", 
                                   ["UTC+8 (Singapore/HK/Beijing)", 
                                    "UTC+9 (Japan/Korea)",
                                    "UTC+7 (Thailand/Vietnam)"],
                                   index=0)
        
        if st.button("💾 Save Preferences", type="primary"):
            st.session_state.preferences = {
                'show_chinese': show_chinese,
                'show_pinyin': show_pinyin,
                'show_explanations': show_explanations,
                'default_year': default_year,
                'timezone': timezone
            }
            st.success("✅ Preferences saved!")
    
    # Footer
    st.markdown("---")
    st.caption("🌟 Ming Qimen 明奇门 | Settings v10.9")
    
    # Sidebar status
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        if has_profile or has_bazi:
            dm = result.get('day_master', {})
            st.success(f"Profile: {dm.get('stem', '')} {dm.get('element', '')}")
        else:
            st.warning("No profile set")
        
        st.markdown("---")
        st.markdown("### 📚 Quick Links")
        st.page_link("pages/6_BaZi.py", label="🎋 BaZi Calculator", icon="🔮")


if __name__ == "__main__":
    main()
