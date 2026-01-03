"""
===============================================================================
6_BaZi.py - Ming QiMenDunJia BaZi Pro Analysis Page
===============================================================================
Version: 10.7 (Joey Yap Aligned)
Updated: 2026-01-03

This page imports calculations from core/bazi_calculator.py
===============================================================================
"""

import streamlit as st
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path for imports
ROOT_DIR = Path(__file__).parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import from core module
try:
    from core.bazi_calculator import (
        calculate_four_pillars,
        calculate_dm_strength,
        calculate_ten_profiles,
        calculate_luck_pillars,
        calculate_profile_percentages_joey_yap,
        calculate_symbolic_stars,
        calculate_life_stages_for_chart,
        determine_useful_gods,
        detect_clashes,
        detect_combines,
        detect_three_harmony,
        get_dominant_profile,
        get_dominant_profile_joey_yap,
        get_luck_direction,
        pillars_to_dict,
        analyze_bazi,
        ELEMENT_COLORS,
        PROFILE_NAMES,
        TEN_GODS_CN,
        STEM_POLARITY,
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="BaZi Pro | Ming QiMenDunJia",
    page_icon="🎋",
    layout="wide"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    .pillar-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin: 5px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .pillar-stem {
        font-size: 32px;
        font-weight: bold;
        margin: 5px 0;
    }
    .pillar-branch {
        font-size: 28px;
        margin: 5px 0;
    }
    .pillar-label {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
    }
    .pillar-info {
        font-size: 11px;
        color: #666;
    }
    .luck-pillar {
        text-align: center;
        padding: 8px;
        border-radius: 5px;
        font-size: 12px;
        background: #1a1a2e;
    }
    .section-header {
        border-bottom: 2px solid #DAA520;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    st.title("🎋 BaZi Pro Analysis")
    st.caption("Four Pillars of Destiny • v10.7")
    
    # Check import
    if not IMPORT_SUCCESS:
        st.error(f"Failed to import core module: {IMPORT_ERROR}")
        st.info("Make sure `core/bazi_calculator.py` exists in your project root.")
        st.stop()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📅 Birth Information")
        
        birth_date = st.date_input(
            "Birth Date",
            value=date(1978, 6, 27),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            help="Select your date of birth"
        )
        
        birth_hour = st.selectbox(
            "Birth Hour",
            options=list(range(24)),
            index=20,
            format_func=lambda x: f"{x:02d}:00 - {x:02d}:59",
            help="Select the hour of birth"
        )
        
        gender = st.radio(
            "Gender",
            options=["Male", "Female"],
            horizontal=True,
            help="Gender affects Luck Pillar direction"
        )
        
        st.markdown("---")
        
        calculate_btn = st.button(
            "🔮 Calculate BaZi",
            type="primary",
            use_container_width=True
        )
    
    # Main content
    if calculate_btn or 'bazi_result' in st.session_state:
        if calculate_btn:
            # Run analysis
            result = analyze_bazi(birth_date, birth_hour, gender.lower())
            st.session_state.bazi_result = result
            st.session_state.bazi_birth_info = {
                'date': birth_date,
                'hour': birth_hour,
                'gender': gender
            }
        
        result = st.session_state.bazi_result
        
        # =====================================================================
        # FOUR PILLARS DISPLAY
        # =====================================================================
        
        st.markdown('<h3 class="section-header">📋 Four Pillars of Destiny</h3>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        pillar_order = ['hour', 'day', 'month', 'year']  # Right to left traditionally
        
        for i, name in enumerate(pillar_order):
            p = result['four_pillars'][name]
            color = ELEMENT_COLORS.get(p['element'], '#888888')
            
            with cols[i]:
                st.markdown(f"""
                <div class="pillar-card" style="border: 2px solid {color};">
                    <div class="pillar-label">{name.upper()}</div>
                    <div class="pillar-stem" style="color: {color};">{p['stem_cn']}</div>
                    <div class="pillar-info">{p['stem']} ({p['element']})</div>
                    <hr style="border-color: {color}; margin: 8px 0;">
                    <div class="pillar-branch">{p['branch_cn']}</div>
                    <div class="pillar-info">{p['branch']} ({p['animal']})</div>
                    <div class="pillar-info" style="margin-top: 5px;">
                        藏干: {', '.join(p['hidden_stems'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # =====================================================================
        # DAY MASTER ANALYSIS
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">⚔️ Day Master Analysis</h3>', unsafe_allow_html=True)
        
        dm = result['day_master']
        dm_color = ELEMENT_COLORS.get(dm['element'], '#888')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Day Master:** <span style="color: {dm_color}; font-size: 24px; font-weight: bold;">
            {dm['stem']} {dm['stem_cn']}</span> ({dm['polarity']} {dm['element']})
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Strength:** {dm['strength_pct']}% ({dm['strength_category']})")
            
            # Strength bar with color
            if dm['strength_pct'] <= 40:
                bar_color = '#DC143C'  # Red for weak
            elif dm['strength_pct'] <= 60:
                bar_color = '#DAA520'  # Gold for neutral
            else:
                bar_color = '#228B22'  # Green for strong
            
            st.markdown(f"""
            <div style="background: #333; border-radius: 5px; height: 20px; width: 100%;">
                <div style="background: {bar_color}; width: {dm['strength_pct']}%; height: 100%; border-radius: 5px;"></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            ug = result['useful_gods']
            
            useful_colors = [ELEMENT_COLORS.get(e, '#888') for e in ug['useful']]
            unfav_colors = [ELEMENT_COLORS.get(e, '#888') for e in ug['unfavorable']]
            
            useful_html = ' '.join([f'<span style="color: {c}; font-weight: bold;">{e}</span>' 
                                   for e, c in zip(ug['useful'], useful_colors)])
            unfav_html = ' '.join([f'<span style="color: {c}; font-weight: bold;">{e}</span>' 
                                  for e, c in zip(ug['unfavorable'], unfav_colors)])
            
            st.markdown(f"**Useful Elements:** {useful_html}", unsafe_allow_html=True)
            st.markdown(f"**Unfavorable:** {unfav_html}", unsafe_allow_html=True)
            
            st.info(ug['explanation'])
        
        # =====================================================================
        # TEN PROFILES
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">👤 Ten Profiles Distribution</h3>', unsafe_allow_html=True)
        
        profiles = result['profiles']
        dominant = profiles['dominant']
        profile_name = profiles['profile_name']
        
        st.success(f"**Main Profile:** {dominant} ({TEN_GODS_CN.get(dominant, '')}) → **{profile_name}**")
        
        # Sort profiles by percentage (Joey Yap method)
        sorted_profiles = sorted(profiles['percentages'].items(), key=lambda x: -x[1])
        
        # Create bar chart data
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Visual bars
            for god, pct in sorted_profiles:
                if pct > 0:
                    cn_name = TEN_GODS_CN.get(god, '')
                    count = profiles['counts'].get(god, 0)
                    st.markdown(f"""
                    <div style="margin: 5px 0;">
                        <div style="display: flex; align-items: center;">
                            <span style="width: 180px; font-size: 12px;">{god} {cn_name}</span>
                            <div style="flex: 1; background: #333; border-radius: 3px; height: 20px; margin: 0 10px;">
                                <div style="background: #DAA520; width: {pct}%; height: 100%; border-radius: 3px;"></div>
                            </div>
                            <span style="width: 50px; text-align: right;">{pct:.0f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Profile Meanings:**")
            st.markdown(f"""
            - 👔 **{profile_name}**
            - Based on {dominant}
            - {TEN_GODS_CN.get(dominant, '')}
            """)
        
        # =====================================================================
        # SYMBOLIC STARS (NEW!)
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">⭐ Symbolic Stars 神煞</h3>', unsafe_allow_html=True)
        
        stars = result.get('symbolic_stars', {})
        celestial = result.get('celestial_animal', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Identity 身份**")
            st.markdown(f"- 生肖 Celestial Animal: **{celestial.get('animal', 'N/A')}** ({celestial.get('branch', '')})")
            if stars.get('noble_people'):
                np = stars['noble_people']
                st.markdown(f"- 贵人 Noble People: **{', '.join(np['animals'])}**")
            if stars.get('life_palace'):
                lp = stars['life_palace']
                st.markdown(f"- 命宫 Life Palace: **{lp.get('full', '')}** ({lp.get('animal', '')})")
        
        with col2:
            st.markdown("**Talents 才能**")
            if stars.get('intelligence'):
                intel = stars['intelligence']
                st.markdown(f"- 文昌 Intelligence: **{intel['animal']}** ({intel['branch']})")
            if stars.get('peach_blossom'):
                pb = stars['peach_blossom']
                st.markdown(f"- 桃花 Peach Blossom: **{pb['animal']}** ({pb['branch']})")
            if stars.get('conception_palace'):
                cp = stars['conception_palace']
                st.markdown(f"- 胎元 Conception: **{cp.get('full', '')}** ({cp.get('animal', '')})")
        
        with col3:
            st.markdown("**Movement 动态**")
            if stars.get('sky_horse'):
                sh = stars['sky_horse']
                st.markdown(f"- 驿马 Sky Horse: **{sh['animal']}** ({sh['branch']})")
            if stars.get('solitary'):
                sol = stars['solitary']
                st.markdown(f"- 孤辰 Solitary: **{sol['animal']}** ({sol['branch']})")
        
        # =====================================================================
        # LUCK PILLARS
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">🔄 Luck Pillars (10-Year Cycles)</h3>', unsafe_allow_html=True)
        
        lp_data = result['luck_pillars']
        
        st.caption(f"**Direction:** {lp_data['direction']} | **Start Age:** {lp_data['start_age']}")
        
        # Display luck pillars
        lp_cols = st.columns(len(lp_data['pillars']))
        
        for i, lp in enumerate(lp_data['pillars']):
            color = ELEMENT_COLORS.get(lp['element'], '#888')
            
            with lp_cols[i]:
                st.markdown(f"""
                <div class="luck-pillar" style="border: 1px solid {color};">
                    <div style="font-weight: bold; color: {color};">{lp['age_range']}</div>
                    <div style="font-size: 18px; margin: 5px 0;">{lp['chinese']}</div>
                    <div style="font-size: 10px;">{lp['animal']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # =====================================================================
        # INTERACTIONS (Clashes & Combines)
        # =====================================================================
        
        interactions = result['interactions']
        
        if interactions['clashes'] or interactions['combines'] or interactions['three_harmony']:
            st.markdown("---")
            st.markdown('<h3 class="section-header">⚡ Pillar Interactions</h3>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🔥 Clashes (冲)**")
                if interactions['clashes']:
                    for c in interactions['clashes']:
                        st.warning(f"↔ {c['animals']}")
                else:
                    st.caption("No clashes detected")
            
            with col2:
                st.markdown("**💫 Combines (合)**")
                if interactions['combines']:
                    for c in interactions['combines']:
                        st.success(f"→ {c['description']}")
                else:
                    st.caption("No combines detected")
            
            with col3:
                st.markdown("**🔺 Three Harmony (三合)**")
                if interactions['three_harmony']:
                    for h in interactions['three_harmony']:
                        status = "Complete ✓" if h['complete'] else "Partial"
                        st.info(f"{h['element']} ({status})")
                else:
                    st.caption("No harmony detected")
        
        # =====================================================================
        # EXPORT DATA
        # =====================================================================
        
        st.markdown("---")
        
        with st.expander("📊 Full Analysis Data (JSON)", expanded=False):
            st.json(result)
        
        # Store in session state for other pages
        st.session_state.bazi_data = result
    
    else:
        # Welcome message
        st.info("👈 Enter your birth information in the sidebar and click **Calculate BaZi** to begin.")
        
        with st.expander("ℹ️ About BaZi Analysis"):
            st.markdown("""
            **BaZi (八字)** or Four Pillars of Destiny is an ancient Chinese system that uses 
            your birth date and time to create a unique chart revealing your:
            
            - **Day Master** - Your core element and personality
            - **Strength** - Whether you're weak, neutral, or strong
            - **Useful Gods** - Elements that support you
            - **Ten Profiles** - Your dominant characteristics
            - **Luck Pillars** - 10-year periods of influence
            
            The calculations follow classical methodology with proper solar term boundaries
            for accurate results.
            """)


if __name__ == "__main__":
    main()
