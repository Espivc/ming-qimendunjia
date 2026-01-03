"""
===============================================================================
6_BaZi.py - Ming QiMenDunJia BaZi Pro Analysis Page
===============================================================================
Version: 10.8 (Life Star + Five Structures + Detailed Guidance)
Updated: 2026-01-03

Features:
- Four Pillars with Hidden Stems
- Day Master Strength Analysis
- Ten Profiles (Joey Yap method)
- Life Star / Gua Number (風水命卦)
- Eight Mansions Directions (八宅)
- Five Structures Radar (五型格)
- Symbolic Stars (神煞)
- Luck Pillars
- Detailed explanations and guidance
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
        calculate_gua_number,
        get_gua_info,
        calculate_eight_mansions,
        calculate_five_structures,
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
        GUA_INFO,
        DIRECTION_MEANINGS,
        FIVE_STRUCTURES_INFO,
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
    st.caption("Four Pillars of Destiny • v10.8")
    
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
        # LIFE STAR / GUA NUMBER (風水命卦)
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">🌟 Life Star 風水命卦</h3>', unsafe_allow_html=True)
        
        life_star = result.get('life_star', {})
        gua_info = life_star.get('gua_info', {})
        gua_number = life_star.get('gua_number', 0)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display Gua card
            gua_color = ELEMENT_COLORS.get(gua_info.get('element', 'Earth'), '#DAA520')
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 15px; 
                        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                        border: 3px solid {gua_color};">
                <div style="font-size: 48px;">{gua_info.get('trigram', '☰')}</div>
                <div style="font-size: 36px; color: {gua_color}; font-weight: bold;">
                    {gua_number}
                </div>
                <div style="font-size: 18px; color: {gua_color};">
                    {gua_info.get('color_cn', '')}
                </div>
                <div style="font-size: 14px; margin-top: 10px;">
                    {gua_info.get('name', '')} ({gua_info.get('chinese', '')})
                </div>
                <div style="font-size: 12px; color: #888;">
                    {gua_info.get('element', '')} • {gua_info.get('direction', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Your Life Star:** Gua {gua_number} - {gua_info.get('name', '')} ({gua_info.get('chinese', '')})")
            st.markdown(f"**Element:** {gua_info.get('element', '')} | **Direction:** {gua_info.get('direction', '')} | **Group:** {gua_info.get('group', '')} Group")
            
            st.info(f"💡 {gua_info.get('description', '')}")
            
            with st.expander("📖 What does my Life Star mean?"):
                st.markdown(f"""
                Your Life Star (Gua) number is **{gua_number}**, belonging to the **{gua_info.get('group', '')} Group**.
                
                **The {gua_info.get('name', '')} Trigram** represents:
                - **Element:** {gua_info.get('element', '')} - This influences your compatible directions and relationships
                - **Direction:** {gua_info.get('direction', '')} - Your "home" direction for stability
                - **Color:** {gua_info.get('color', '')} ({gua_info.get('color_cn', '')}) - Beneficial color for you
                
                **East vs West Group:**
                - **East Group** (1, 3, 4, 9): Best with East, Southeast, North, South directions
                - **West Group** (2, 6, 7, 8): Best with West, Northwest, Southwest, Northeast directions
                
                Your group determines which directions are most supportive for your main door, bedroom, and desk placement.
                """)
        
        # =====================================================================
        # EIGHT MANSIONS / DIRECTIONS (八宅)
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">🧭 Eight Mansions 八宅方位</h3>', unsafe_allow_html=True)
        
        eight_mansions = result.get('eight_mansions', {})
        favorable = eight_mansions.get('favorable', [])
        unfavorable = eight_mansions.get('unfavorable', [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Favorable Directions 吉方")
            for d in favorable:
                color = "#228B22" if d['rank'] == 1 else "#32CD32" if d['rank'] == 2 else "#90EE90"
                st.markdown(f"""
                <div style="padding: 12px; margin: 8px 0; border-radius: 8px; 
                            background: linear-gradient(90deg, {color}22, transparent);
                            border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; font-size: 16px;">{d['compass']}</span>
                        <span style="color: {color};">{d['name']} ({d['chinese']})</span>
                    </div>
                    <div style="font-size: 12px; color: #888; margin-top: 4px;">
                        {d['english']} • Rank #{d['rank']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ❌ Unfavorable Directions 凶方")
            for d in unfavorable:
                color = "#FF6B6B" if d['rank'] == 8 else "#FF8C8C" if d['rank'] == 7 else "#FFB3B3"
                st.markdown(f"""
                <div style="padding: 12px; margin: 8px 0; border-radius: 8px; 
                            background: linear-gradient(90deg, {color}22, transparent);
                            border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; font-size: 16px;">{d['compass']}</span>
                        <span style="color: {color};">{d['name']} ({d['chinese']})</span>
                    </div>
                    <div style="font-size: 12px; color: #888; margin-top: 4px;">
                        {d['english']} • Rank #{d['rank']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed direction guidance
        with st.expander("📖 Direction Meanings & Practical Application"):
            st.markdown("""
            ### Favorable Directions - How to Use Them
            
            | Direction | Best Use | What It Brings |
            |-----------|----------|----------------|
            | **Sheng Qi 生氣** | Main door, Office desk, Important meetings | Wealth, Success, Vitality |
            | **Tian Yi 天醫** | Bedroom (if sick), Kitchen, Dining | Health, Helpful people, Recovery |
            | **Yan Nian 延年** | Master bedroom, Living room | Romance, Relationships, Harmony |
            | **Fu Wei 伏位** | Meditation spot, Study | Stability, Peace, Self-development |
            
            ### Unfavorable Directions - What to Avoid
            
            | Direction | Avoid For | Potential Problems |
            |-----------|-----------|-------------------|
            | **Huo Hai 禍害** | Important work, Negotiations | Arguments, Setbacks |
            | **Wu Gui 五鬼** | Storing valuables, Fire placement | Theft, Backstabbing, Fire hazards |
            | **Liu Sha 六煞** | Bedroom, Romance | Scandals, Affairs, Legal issues |
            | **Jue Ming 絕命** | Everything important! | Serious misfortune, Health problems |
            
            ### Practical Tips
            1. **Main Door**: Should ideally face your Sheng Qi direction
            2. **Bed Position**: Head pointing towards Tian Yi (health) or Yan Nian (romance)
            3. **Desk Direction**: Face your Sheng Qi direction while working
            4. **Stove Position**: Fire should "burn" towards your Tian Yi
            """)
        
        # =====================================================================
        # FIVE STRUCTURES RADAR (五型格)
        # =====================================================================
        
        st.markdown("---")
        st.markdown('<h3 class="section-header">⭐ Five Structures 五型格</h3>', unsafe_allow_html=True)
        
        five_structures = result.get('five_structures', {})
        structures = five_structures.get('structures', {})
        dominant_structure = five_structures.get('dominant', '')
        dominant_info = five_structures.get('dominant_info', {})
        
        # Display dominant structure
        dominant_element = five_structures.get('dominant_element', 'Earth')
        dominant_color = ELEMENT_COLORS.get(dominant_element, '#DAA520')
        
        st.success(f"**Main Structure:** {dominant_structure} ({dominant_info.get('chinese', '')}) → **{dominant_info.get('english_name', '')}** ({dominant_info.get('structure_name', '')})")
        
        # Visual radar/bars
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Structure Distribution:**")
            
            # Create visual bars for each structure
            structure_order = ['Wealth', 'Influence', 'Resources', 'Companion', 'Output']
            for name in structure_order:
                data = structures.get(name, {})
                element = data.get('element', 'Earth')
                color = ELEMENT_COLORS.get(element, '#888')
                pct = data.get('percentage', 0)
                score = data.get('score', 0)
                chinese = data.get('chinese', '')
                english_name = data.get('info', {}).get('english_name', name)
                
                is_dominant = name == dominant_structure
                border = f"border: 2px solid {color};" if is_dominant else ""
                
                st.markdown(f"""
                <div style="padding: 8px; margin: 6px 0; border-radius: 8px; 
                            background: #1a1a2e; {border}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span style="font-weight: {'bold' if is_dominant else 'normal'};">
                            {element} {chinese} {name}
                        </span>
                        <span style="color: {color};">{english_name}</span>
                    </div>
                    <div style="background: #333; border-radius: 4px; height: 20px;">
                        <div style="background: linear-gradient(90deg, {color}, {color}88); 
                                    width: {pct}%; height: 100%; border-radius: 4px;
                                    display: flex; align-items: center; justify-content: flex-end; padding-right: 8px;">
                            <span style="font-size: 11px; color: white;">{pct:.0f}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Element Mapping:**")
            st.markdown("""
            | Element | Structure |
            |---------|-----------|
            | 木 Wood | 財 Wealth |
            | 火 Fire | 官 Influence |
            | 土 Earth | 印 Resources |
            | 金 Metal | 比 Companion |
            | 水 Water | 食 Output |
            """)
        
        # Detailed explanation of dominant structure
        with st.expander(f"📖 About Your Main Structure: {dominant_structure} ({dominant_info.get('english_name', '')})"):
            if dominant_info:
                st.markdown(f"### {dominant_info.get('english_name', '')} ({dominant_info.get('structure_name', '')})")
                st.markdown(f"**Element:** {dominant_info.get('element', '')} | **Chinese:** {dominant_info.get('chinese', '')}")
                
                st.info(dominant_info.get('description', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Strengths:**")
                    for s in dominant_info.get('strengths', []):
                        st.markdown(f"- {s}")
                
                with col2:
                    st.markdown("**⚠️ Challenges:**")
                    for c in dominant_info.get('challenges', []):
                        st.markdown(f"- {c}")
                
                st.markdown("**💼 Suitable Careers:**")
                careers = dominant_info.get('careers', [])
                st.markdown(", ".join(careers))
                
                st.markdown("**💡 Advice:**")
                st.success(dominant_info.get('advice', ''))
        
        # All structures explanation
        with st.expander("📖 Understanding All Five Structures"):
            st.markdown("""
            The Five Structures map your Ten Gods distribution to the Five Elements, revealing your core tendencies:
            
            | Structure | Element | Type | Characteristics |
            |-----------|---------|------|-----------------|
            | **Wealth 財** | Wood | Manager 管理型 | Business-minded, resource-focused, practical |
            | **Influence 官** | Fire | Supporters 忠誠型 | Leadership, authority, discipline |
            | **Resources 印** | Earth | Thinkers 智慧型 | Analytical, knowledge-seeking, wise |
            | **Companion 比** | Metal | Connectors 交際型 | Social, networking, team-oriented |
            | **Output 食** | Water | Creators 創作型 | Creative, expressive, innovative |
            
            **How to Read Your Chart:**
            - Your **highest structure** shows your natural inclination and strengths
            - A **balanced chart** (all around 50-70%) suggests versatility
            - Very **low structures** may indicate areas for personal development
            - Your Day Master element determines how these structures manifest
            """)
        
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
