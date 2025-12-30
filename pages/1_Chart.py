"""
Ming Qimen 明奇门 - Chart Generator v6.0
Features:
- QMDJ Pillars (chart time, NOT BaZi)
- All indicators: Death & Emptiness, Lead Palace, Horse Star, Nobleman
- Ju Number and Structure display
- Rich palace details with indicator badges
"""

import streamlit as st
from datetime import datetime, date, timedelta, timezone
import sys
import os

# Add core module to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.qmdj_engine import (
    generate_qmdj_chart,
    PALACE_INFO,
    LUOSHU_GRID,
    NINE_STARS,
    EIGHT_DOORS,
    EIGHT_DEITIES,
    SGT
)

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(page_title="Chart | Ming Qimen", page_icon="📊", layout="wide")

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    :root {
        --bg-primary: #0a0a12;
        --bg-card: #1a1a2e;
        --bg-card-hover: #252542;
        --gold-primary: #FFD700;
        --gold-secondary: #FFA500;
        --gold-muted: #B8860B;
        --text-primary: #E8E8E8;
        --text-secondary: #888888;
        --accent-purple: #9B59B6;
        --success: #2ecc71;
        --warning: #f39c12;
        --danger: #e74c3c;
        --info: #3498db;
    }
    
    .page-header {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 2rem;
        letter-spacing: 2px;
    }
    
    .page-subtitle {
        font-family: 'Cormorant Garamond', serif;
        color: var(--text-secondary);
        font-style: italic;
    }
    
    /* Structure Banner */
    .structure-banner {
        background: linear-gradient(135deg, #2d1f3d 0%, #1a1a2e 100%);
        border: 2px solid var(--accent-purple);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .structure-title {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 1.3rem;
        letter-spacing: 2px;
    }
    
    .structure-detail {
        font-family: 'Cormorant Garamond', serif;
        color: var(--text-secondary);
        font-size: 0.95rem;
    }
    
    /* QMDJ Pillars Banner */
    .qmdj-pillars-banner {
        background: linear-gradient(135deg, #1a2a3a 0%, #12121e 100%);
        border: 2px solid var(--info);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .qmdj-pillars-title {
        font-family: 'Cinzel', serif;
        color: var(--info);
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    
    .pillar-box {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
        border: 1px solid #444;
        border-radius: 8px;
        padding: 0.75rem 0.5rem;
        text-align: center;
        min-width: 80px;
    }
    
    .pillar-label {
        font-family: 'Cinzel', serif;
        color: var(--text-secondary);
        font-size: 0.7rem;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    
    .pillar-stem {
        font-family: 'Noto Sans SC', sans-serif;
        color: var(--gold-primary);
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .pillar-branch {
        font-family: 'Noto Sans SC', sans-serif;
        color: #87CEEB;
        font-size: 1.4rem;
        font-weight: 500;
    }
    
    /* Indicators Row */
    .indicators-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .indicator-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-family: 'Cormorant Garamond', serif;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .indicator-lead { background: linear-gradient(135deg, #9B59B6, #8E44AD); color: white; }
    .indicator-horse { background: linear-gradient(135deg, #3498DB, #2980B9); color: white; }
    .indicator-noble { background: linear-gradient(135deg, #F1C40F, #F39C12); color: black; }
    .indicator-empty { background: linear-gradient(135deg, #7F8C8D, #95A5A6); color: white; }
    
    /* Palace Grid */
    .palace-grid-container {
        background: linear-gradient(135deg, #12121e 0%, #0a0a12 100%);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .palace-cell {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #444;
        border-radius: 10px;
        padding: 0.75rem;
        text-align: center;
        min-height: 140px;
        transition: all 0.2s ease;
        position: relative;
    }
    
    .palace-cell:hover {
        border-color: var(--gold-primary);
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.15);
    }
    
    .palace-cell.selected {
        border: 2px solid var(--gold-primary);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.3);
    }
    
    .palace-cell.has-indicator {
        border-color: var(--accent-purple);
    }
    
    .palace-cell.is-empty {
        opacity: 0.7;
        border-style: dashed;
    }
    
    .palace-badges {
        position: absolute;
        top: 5px;
        right: 5px;
        display: flex;
        gap: 2px;
    }
    
    .palace-badge {
        font-size: 0.7rem;
        padding: 2px 4px;
        border-radius: 4px;
    }
    
    .palace-number {
        font-family: 'Cinzel', serif;
        color: var(--text-secondary);
        font-size: 0.65rem;
        position: absolute;
        top: 5px;
        left: 8px;
    }
    
    .palace-name {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .palace-direction {
        color: var(--text-secondary);
        font-size: 0.7rem;
    }
    
    .palace-components {
        margin-top: 0.5rem;
        font-size: 0.75rem;
        line-height: 1.4;
    }
    
    .palace-star { color: #F1C40F; }
    .palace-door { color: #3498DB; }
    .palace-deity { color: #9B59B6; }
    
    /* Detail Panel */
    .detail-panel {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 2px solid var(--gold-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .detail-title {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .component-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .component-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .component-name {
        font-family: 'Cinzel', serif;
        color: var(--gold-primary);
        font-size: 1rem;
    }
    
    .component-chinese {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .strength-badge {
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
    }
    
    .strength-timely { background: #27ae60; color: white; }
    .strength-prosperous { background: #2ecc71; color: white; }
    .strength-resting { background: #f39c12; color: black; }
    .strength-confined { background: #e67e22; color: white; }
    .strength-dead { background: #c0392b; color: white; }
    
    /* Element colors */
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
    
    /* BaZi Profile Card (sidebar style) */
    .bazi-profile-card {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%);
        border: 1px solid var(--success);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .bazi-profile-title {
        font-family: 'Cinzel', serif;
        color: var(--success);
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_element_class(element: str) -> str:
    return element.lower() if element else "earth"

def get_strength_class(strength: str) -> str:
    return f"strength-{strength.lower()}" if strength else "strength-resting"

def extract_chinese(text: str) -> str:
    """Extract Chinese character from 'Pinyin 中文' format"""
    if " " in text:
        return text.split()[-1]
    return text

# ============================================================
# PAGE CONTENT
# ============================================================

st.markdown('<h1 class="page-header">📊 CHART GENERATOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Qi Men Dun Jia Analysis with Full Indicators • 奇门遁甲全指标分析</p>', unsafe_allow_html=True)

st.divider()

# ============================================================
# CHART GENERATION CONTROLS
# ============================================================

st.subheader("⚡ Generate Reading")

ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([2, 1, 1, 1])

with ctrl_col1:
    chart_date = st.date_input(
        "Date 日期",
        value=date.today(),
        help="Select date for the reading"
    )

with ctrl_col2:
    chart_hour = st.selectbox(
        "Hour 时",
        options=list(range(0, 24)),
        index=datetime.now().hour,
        format_func=lambda x: f"{x:02d}:00"
    )

with ctrl_col3:
    chart_minute = st.selectbox(
        "Minute 分",
        options=[0, 15, 30, 45],
        index=0
    )

with ctrl_col4:
    chart_type = st.selectbox(
        "Type 类型",
        options=["Hour 时盘", "Day 日盘"],
        help="Hour chart or Day chart"
    )

# Generate button
if st.button("🔮 GENERATE CHART 生成盘", type="primary", use_container_width=True):
    with st.spinner("Calculating Qi Men Dun Jia... 计算奇门遁甲中..."):
        # Create datetime
        chart_dt = datetime(
            chart_date.year, chart_date.month, chart_date.day,
            chart_hour, chart_minute,
            tzinfo=SGT
        )
        
        # Generate chart using v6.0 engine
        chart = generate_qmdj_chart(chart_dt)
        
        # Save to session state
        st.session_state.current_chart = chart
        st.session_state.selected_palace = None
        
        st.success("✅ Chart generated! 盘已生成!")
        st.rerun()

# ============================================================
# DISPLAY CHART
# ============================================================

if st.session_state.get("current_chart"):
    chart = st.session_state.current_chart
    
    # ========== STRUCTURE BANNER ==========
    structure = chart["structure"]
    st.markdown(f"""
    <div class="structure-banner">
        <div>
            <div class="structure-title">{structure['ju_display']}</div>
            <div class="structure-detail">
                {chart['metadata']['date_display']} {chart['metadata']['time_display']} • 
                Chinese Hour: {chart['metadata']['chinese_hour']['name']} ({chart['metadata']['chinese_hour']['range']})
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: var(--gold-primary); font-size: 0.9rem;">Lead Palace 值符宫</div>
            <div style="color: var(--text-primary); font-size: 1.1rem;">
                Palace {chart['lead_indicators']['lead_stem_palace']} • {chart['lead_indicators']['lead_stem_palace_name']} {chart['lead_indicators']['lead_stem_palace_chinese']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== QMDJ PILLARS (Chart Time) ==========
    st.markdown("""
    <div class="qmdj-pillars-banner">
        <div class="qmdj-pillars-title">QMDJ CHART PILLARS 奇门时盘四柱 (Chart Time, Not Your BaZi)</div>
    </div>
    """, unsafe_allow_html=True)
    
    pillars = chart["qmdj_pillars"]
    pillar_cols = st.columns(4)
    pillar_order = ["Hour", "Day", "Month", "Year"]
    pillar_chinese = ["时柱", "日柱", "月柱", "年柱"]
    
    for i, (name, chinese) in enumerate(zip(pillar_order, pillar_chinese)):
        with pillar_cols[i]:
            p = pillars[name]
            stem_char = extract_chinese(p['stem'])
            branch_char = extract_chinese(p['branch'])
            
            st.markdown(f"""
            <div class="pillar-box">
                <div class="pillar-label">{name.upper()} • {chinese}</div>
                <div class="pillar-stem">{stem_char}</div>
                <div class="pillar-branch">{branch_char}</div>
                <div style="font-size: 0.7rem; color: #888; margin-top: 0.3rem;">
                    {p['stem_element']} / {p['branch_element']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== SPECIAL INDICATORS ROW ==========
    st.markdown("")
    
    indicators_html = '<div class="indicators-row">'
    
    # Lead Palace
    lead = chart['lead_indicators']
    indicators_html += f'<span class="indicator-badge indicator-lead">⭐ Lead: P{lead["lead_stem_palace"]} {lead["lead_stem_palace_name"]}</span>'
    
    # Horse Star
    horse = chart['horse_star']
    if horse.get('horse_palace'):
        indicators_html += f'<span class="indicator-badge indicator-horse">🐴 Horse: P{horse["horse_palace"]} ({horse["horse_branch"]})</span>'
    
    # Nobleman
    noble = chart['nobleman']
    if noble.get('day_nobleman_palaces'):
        palaces_str = ", ".join([f"P{p}" for p in noble['day_nobleman_palaces']])
        indicators_html += f'<span class="indicator-badge indicator-noble">👑 Nobleman: {palaces_str}</span>'
    
    # Death & Emptiness
    de = chart['death_emptiness']
    if de.get('affected_palaces'):
        palaces_str = ", ".join([f"P{p}" for p in de['affected_palaces']])
        indicators_html += f'<span class="indicator-badge indicator-empty">💀 Empty: {palaces_str} ({", ".join(de["empty_branches"])})</span>'
    
    indicators_html += '</div>'
    st.markdown(indicators_html, unsafe_allow_html=True)
    
    # ========== 9-PALACE GRID ==========
    st.markdown('<div class="palace-grid-container">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Nine Palaces 九宫格")
    
    palaces = chart["palaces"]
    selected_palace = st.session_state.get("selected_palace")
    
    # Create 3x3 grid
    for row_idx, row in enumerate(LUOSHU_GRID):
        cols = st.columns(3)
        for col_idx, palace_num in enumerate(row):
            with cols[col_idx]:
                palace = palaces[palace_num]
                info = palace["palace_info"]
                star = palace["star"]
                door = palace["door"]
                deity = palace["deity"]
                indicators = palace["indicators"]
                
                # Build badge HTML
                badges = []
                if indicators["is_lead_palace"]:
                    badges.append("⭐")
                if indicators["has_horse_star"]:
                    badges.append("🐴")
                if indicators["has_nobleman"]:
                    badges.append("👑")
                if indicators["is_empty"]:
                    badges.append("💀")
                
                badges_html = "".join([f'<span class="palace-badge">{b}</span>' for b in badges])
                
                # Cell classes
                cell_classes = ["palace-cell"]
                if selected_palace == palace_num:
                    cell_classes.append("selected")
                if badges:
                    cell_classes.append("has-indicator")
                if indicators["is_empty"]:
                    cell_classes.append("is-empty")
                
                st.markdown(f"""
                <div class="{' '.join(cell_classes)}">
                    <div class="palace-number">P{palace_num}</div>
                    <div class="palace-badges">{badges_html}</div>
                    <div class="palace-name">{info['name']} {info['chinese']}</div>
                    <div class="palace-direction">{info['direction']} • {info['element']}</div>
                    <div class="palace-components">
                        <div class="palace-star">⭐ {star['name']} {star['chinese']}</div>
                        <div class="palace-door">🚪 {door['name']} {door['chinese']}</div>
                        <div class="palace-deity">👁️ {deity['name']} {deity['chinese']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Analyze P{palace_num}", key=f"btn_p{palace_num}", use_container_width=True):
                    st.session_state.selected_palace = palace_num
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== SELECTED PALACE DETAIL ==========
    if st.session_state.get("selected_palace"):
        palace_num = st.session_state.selected_palace
        palace = palaces[palace_num]
        info = palace["palace_info"]
        star = palace["star"]
        door = palace["door"]
        deity = palace["deity"]
        indicators = palace["indicators"]
        
        st.markdown(f"""
        <div class="detail-panel">
            <div class="detail-title">
                🔍 Palace {palace_num}: {info['name']} {info['chinese']} ({info['direction']})
                {' ⭐ LEAD PALACE' if indicators['is_lead_palace'] else ''}
                {' 🐴 HORSE STAR' if indicators['has_horse_star'] else ''}
                {' 👑 NOBLEMAN' if indicators['has_nobleman'] else ''}
                {' 💀 EMPTY' if indicators['is_empty'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Components 组件")
            
            # Star
            star_strength_class = get_strength_class(star.get('strength', 'Resting'))
            st.markdown(f"""
            <div class="component-card">
                <div class="component-header">
                    <span class="component-name">⭐ Star 星</span>
                    <span class="strength-badge {star_strength_class}">{star.get('strength', 'N/A')}</span>
                </div>
                <div><strong>{star['name']}</strong> <span class="component-chinese">{star['chinese']}</span></div>
                <div><span class="element-badge {get_element_class(star['element'])}">{star['element']}</span> • {star['nature']}</div>
                <div style="color: #888; font-size: 0.85rem; margin-top: 0.3rem;">{star.get('friendly_name', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Door
            door_strength_class = get_strength_class(door.get('strength', 'Resting'))
            st.markdown(f"""
            <div class="component-card">
                <div class="component-header">
                    <span class="component-name">🚪 Door 门</span>
                    <span class="strength-badge {door_strength_class}">{door.get('strength', 'N/A')}</span>
                </div>
                <div><strong>{door['name']}</strong> <span class="component-chinese">{door['chinese']}</span></div>
                <div><span class="element-badge {get_element_class(door['element'])}">{door['element']}</span> • {door['nature']}</div>
                <div style="color: #888; font-size: 0.85rem; margin-top: 0.3rem;">{door.get('friendly_name', '')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Deity
            st.markdown(f"""
            <div class="component-card">
                <div class="component-header">
                    <span class="component-name">👁️ Deity 神</span>
                </div>
                <div><strong>{deity['name']}</strong> <span class="component-chinese">{deity['chinese']}</span></div>
                <div>{deity['nature']} • {deity.get('function', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Analysis 分析")
            
            # Palace element
            st.info(f"**Palace Element:** {info['element']}")
            
            # Special indicators explanation
            if indicators['is_lead_palace']:
                st.success("⭐ **Lead Palace (值符宫):** This is the command palace of the chart. Actions here have authority and leadership energy.")
            
            if indicators['has_horse_star']:
                st.info("🐴 **Horse Star (驿马):** Indicates travel, mobility, and fast results. Good for movement and change.")
            
            if indicators['has_nobleman']:
                st.warning("👑 **Nobleman (贵人):** Helpful people will appear. Good for seeking assistance and making connections.")
            
            if indicators['is_empty']:
                st.error("💀 **Death & Emptiness (空亡):** Energy is diminished. Results may be reduced or delayed. Consider alternative timing.")
            
            # BaZi cross-reference
            if st.session_state.get("user_profile"):
                st.markdown("---")
                st.markdown("#### BaZi Alignment 八字配合")
                profile = st.session_state.user_profile
                useful = profile.get('useful_gods', [])
                
                if info['element'] in useful:
                    st.success(f"✅ Palace element ({info['element']}) matches your Useful God! Favorable for you.")
                elif info['element'] in profile.get('unfavorable', []):
                    st.error(f"⚠️ Palace element ({info['element']}) is unfavorable for you. Exercise caution.")
                else:
                    st.info(f"Palace element: {info['element']} | Your useful: {', '.join(useful)}")

else:
    # No chart yet
    st.info("👆 Select date and time above, then click **Generate Chart** to see the Qi Men Dun Jia analysis.")
    
    # Quick actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔮 Generate NOW Chart", use_container_width=True):
            chart = generate_qmdj_chart()
            st.session_state.current_chart = chart
            st.rerun()
    
    with col2:
        if st.button("🎂 Set Up BaZi Profile", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("### 📊 Chart Info")
    
    if st.session_state.get("current_chart"):
        chart = st.session_state.current_chart
        st.markdown(f"**Date:** {chart['metadata']['date_display']}")
        st.markdown(f"**Time:** {chart['metadata']['time_display']}")
        st.markdown(f"**Structure:** {chart['structure']['structure']}")
        st.markdown(f"**Ju:** {chart['structure']['ju_number']}")
        
        st.markdown("---")
        st.markdown("**Lead Indicators:**")
        st.markdown(f"⭐ Lead Palace: P{chart['lead_indicators']['lead_stem_palace']}")
        if chart['horse_star'].get('horse_palace'):
            st.markdown(f"🐴 Horse: P{chart['horse_star']['horse_palace']}")
        if chart['nobleman'].get('day_nobleman_palaces'):
            st.markdown(f"👑 Noble: P{', P'.join(map(str, chart['nobleman']['day_nobleman_palaces']))}")
        if chart['death_emptiness'].get('affected_palaces'):
            st.markdown(f"💀 Empty: P{', P'.join(map(str, chart['death_emptiness']['affected_palaces']))}")
    
    st.markdown("---")
    st.markdown("### 👤 Your Profile")
    
    if st.session_state.get("user_profile"):
        profile = st.session_state.user_profile
        st.markdown(f"**{profile.get('day_master', 'Unknown')}**")
        st.markdown(f"{profile.get('polarity', '')} {profile.get('element', '')} • {profile.get('strength', '')}")
        useful = profile.get('useful_gods', [])
        if useful:
            st.caption(f"Useful: {', '.join(useful)}")
    else:
        st.info("No profile set")
        if st.button("🔮 Set Up", key="sidebar_setup"):
            st.switch_page("pages/6_BaZi.py")

# Footer
st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Chart Generator v6.0 | All Indicators Enabled")
