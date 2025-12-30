"""
Ming Qimen 明奇门 - Settings v6.0
Configure preferences and manage BaZi profile
"""

import streamlit as st

st.set_page_config(page_title="Settings | Ming Qimen", page_icon="⚙️", layout="wide")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    .page-header {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 2rem;
        letter-spacing: 2px;
    }
    
    .settings-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .settings-title {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
    }
    
    .profile-card {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%);
        border: 2px solid #2ecc71;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .profile-title {
        font-family: 'Cinzel', serif;
        color: #2ecc71;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .dm-display {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 2rem;
        color: #FFD700;
        text-align: center;
        margin: 1rem 0;
    }
    
    .element-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-header">⚙️ SETTINGS</h1>', unsafe_allow_html=True)
st.markdown("*Configure preferences and manage your profile*")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["👤 BaZi Profile", "✏️ Manual Entry", "🎨 Preferences"])

# TAB 1: BaZi Profile
with tab1:
    st.subheader("Your BaZi Profile")
    
    profile = st.session_state.get("user_profile", {})
    
    if profile:
        # Display current profile
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-title">✅ Profile Active</div>
            <div class="dm-display">
                {profile.get('day_master', 'Unknown')}
            </div>
            <div style="text-align: center; margin-bottom: 1rem;">
                <span style="color: #888;">
                    {profile.get('polarity', '')} {profile.get('element', '')} • 
                    {profile.get('strength', '')} ({profile.get('strength_score', 5)}/10)
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Useful Gods 用神:**")
            useful = profile.get('useful_gods', [])
            for god in useful:
                element_class = god.lower()
                st.markdown(f'<span class="element-badge {element_class}">{god}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Unfavorable 忌神:**")
            unfavorable = profile.get('unfavorable', [])
            for element in unfavorable:
                element_class = element.lower()
                st.markdown(f'<span class="element-badge {element_class}">{element}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("**Special Structures:**")
        structures = []
        if profile.get('wealth_vault'):
            structures.append("💰 Wealth Vault")
        if profile.get('nobleman'):
            structures.append("👑 Nobleman Present")
        
        if structures:
            st.markdown(" • ".join(structures))
        else:
            st.markdown("*None identified*")
        
        st.markdown("**Profile Type:**")
        st.markdown(f"*{profile.get('profile', 'Unknown')}*")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Recalculate BaZi", use_container_width=True):
                st.switch_page("pages/6_BaZi.py")
        
        with col2:
            if st.button("🗑️ Clear Profile", use_container_width=True):
                if st.checkbox("Confirm clear profile"):
                    st.session_state.user_profile = None
                    st.success("Profile cleared!")
                    st.rerun()
    
    else:
        st.info("No BaZi profile set. Calculate your BaZi or enter manually.")
        
        if st.button("🎂 Calculate My BaZi", type="primary", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")

# TAB 2: Manual Entry
with tab2:
    st.subheader("Manual BaZi Entry")
    st.markdown("*For users who already know their BaZi profile*")
    
    with st.form("manual_bazi"):
        col1, col2 = st.columns(2)
        
        with col1:
            day_master = st.selectbox(
                "Day Master 日主",
                ["Jia 甲", "Yi 乙", "Bing 丙", "Ding 丁", "Wu 戊", 
                 "Ji 己", "Geng 庚", "Xin 辛", "Ren 壬", "Gui 癸"]
            )
            
            strength = st.select_slider(
                "Day Master Strength",
                options=["Very Weak", "Weak", "Balanced", "Strong", "Very Strong"],
                value="Balanced"
            )
            
            strength_score = st.slider("Strength Score (1-10)", 1, 10, 5)
        
        with col2:
            useful_gods = st.multiselect(
                "Useful Gods 用神",
                ["Wood", "Fire", "Earth", "Metal", "Water"],
                max_selections=2
            )
            
            unfavorable = st.multiselect(
                "Unfavorable Elements 忌神",
                ["Wood", "Fire", "Earth", "Metal", "Water"],
                max_selections=2
            )
        
        st.markdown("**Special Structures:**")
        col3, col4 = st.columns(2)
        with col3:
            wealth_vault = st.checkbox("💰 Wealth Vault Present")
        with col4:
            nobleman = st.checkbox("👑 Nobleman Present")
        
        profile_type = st.selectbox(
            "Ten God Profile",
            ["Pioneer (Indirect Wealth)", "Philosopher (Eating God)", 
             "Director (Direct Wealth)", "Warrior (7 Killings)",
             "Leader (Direct Officer)", "Diplomat (Direct Resource)",
             "Artist (Hurting Officer)", "Scholar (Indirect Resource)",
             "Friend (Rob Wealth)", "Advisor (Friend)"]
        )
        
        submitted = st.form_submit_button("💾 Save Manual Profile", use_container_width=True)
        
        if submitted:
            # Parse day master
            dm_parts = day_master.split()
            dm_name = dm_parts[0]
            dm_chinese = dm_parts[1] if len(dm_parts) > 1 else ""
            
            # Determine element and polarity
            stem_elements = {
                "Jia": ("Wood", "Yang"), "Yi": ("Wood", "Yin"),
                "Bing": ("Fire", "Yang"), "Ding": ("Fire", "Yin"),
                "Wu": ("Earth", "Yang"), "Ji": ("Earth", "Yin"),
                "Geng": ("Metal", "Yang"), "Xin": ("Metal", "Yin"),
                "Ren": ("Water", "Yang"), "Gui": ("Water", "Yin")
            }
            
            element, polarity = stem_elements.get(dm_name, ("Unknown", "Unknown"))
            
            st.session_state.user_profile = {
                "day_master": day_master,
                "element": element,
                "polarity": polarity,
                "strength": strength,
                "strength_score": strength_score,
                "useful_gods": useful_gods,
                "unfavorable": unfavorable,
                "wealth_vault": wealth_vault,
                "nobleman": nobleman,
                "profile": profile_type,
                "manual_entry": True
            }
            
            st.success("✅ Manual profile saved!")
            st.rerun()

# TAB 3: Preferences
with tab3:
    st.subheader("Display Preferences")
    
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">🌐 Language</div>', unsafe_allow_html=True)
    
    language = st.radio(
        "Display Language",
        ["English + Chinese", "English Only", "Chinese Only"],
        index=0,
        horizontal=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">📊 Chart Display</div>', unsafe_allow_html=True)
    
    show_chinese = st.checkbox("Show Chinese characters", value=True)
    show_pinyin = st.checkbox("Show Pinyin", value=True)
    show_elements = st.checkbox("Show element colors", value=True)
    beginner_mode = st.checkbox("Beginner-friendly descriptions", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">📤 Export Format</div>', unsafe_allow_html=True)
    
    export_format = st.selectbox(
        "Default Export Format",
        ["Universal Schema v3.0 (JSON)", "CSV", "Markdown"]
    )
    
    include_bazi = st.checkbox("Include BaZi data in exports", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("💾 Save Preferences", type="primary", use_container_width=True):
        st.session_state.preferences = {
            "language": language,
            "show_chinese": show_chinese,
            "show_pinyin": show_pinyin,
            "show_elements": show_elements,
            "beginner_mode": beginner_mode,
            "export_format": export_format,
            "include_bazi": include_bazi
        }
        st.success("✅ Preferences saved!")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    if st.session_state.get("user_profile"):
        st.success("✅ Profile Active")
        profile = st.session_state.user_profile
        st.markdown(f"**{profile.get('day_master', 'Unknown')}**")
    else:
        st.warning("No profile set")
    
    st.markdown("---")
    st.markdown("### 📖 Quick Links")
    
    if st.button("📊 Chart Generator", use_container_width=True):
        st.switch_page("pages/1_Chart.py")
    
    if st.button("🎂 BaZi Calculator", use_container_width=True):
        st.switch_page("pages/6_BaZi.py")

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Settings v6.0")
