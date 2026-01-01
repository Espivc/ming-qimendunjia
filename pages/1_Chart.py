# Ming QiMenDunJia v10.1 - QMDJ Chart Display
# pages/1_Chart.py
"""
QMDJ CHART - Fixed HTML display issues
"""

import streamlit as st
from datetime import datetime, date, timedelta
import pytz

import sys
sys.path.insert(0, '..')

try:
    from core.qmdj_engine import (
        generate_qmdj_chart, calculate_qmdj_pillars,
        PALACE_INFO, NINE_STARS, EIGHT_DOORS, EIGHT_DEITIES,
        calculate_death_emptiness, calculate_horse_star, calculate_nobleman,
        SGT
    )
    from core.formations import detect_formations, get_formation_score
    IMPORTS_OK = True
except ImportError as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)

st.set_page_config(page_title="QMDJ Chart | Ming Qimen", page_icon="🎯", layout="wide")

# =============================================================================
# STYLES
# =============================================================================

st.markdown("""
<style>
    .stApp { background-color: #0a1628; }
    
    .palace-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 12px;
        min-height: 100px;
        text-align: center;
    }
    .palace-selected {
        border: 2px solid #FFD700 !important;
        background: linear-gradient(135deg, #2d3748 0%, #1a2744 100%);
    }
    .palace-empty {
        border: 1px dashed #f56565 !important;
        opacity: 0.7;
    }
    .palace-horse {
        box-shadow: 0 0 10px #48bb78;
    }
    .palace-noble {
        box-shadow: 0 0 10px #ecc94b;
    }
    
    .indicator-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7em;
        margin: 2px;
    }
    .badge-horse { background: #276749; color: #48bb78; }
    .badge-noble { background: #744210; color: #ecc94b; }
    .badge-empty { background: #742a2a; color: #fc8181; }
    .badge-lead { background: #2c5282; color: #63b3ed; }
    
    .component-box {
        background: #1a2744;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #4a5568;
    }
    .component-star { border-left-color: #f6e05e; }
    .component-door { border-left-color: #48bb78; }
    .component-deity { border-left-color: #9f7aea; }
    
    .strength-timely { background: #276749; color: #48bb78; }
    .strength-prosperous { background: #2c5282; color: #63b3ed; }
    .strength-resting { background: #744210; color: #ecc94b; }
    .strength-confined { background: #742a2a; color: #fc8181; }
    .strength-dead { background: #1a202c; color: #a0aec0; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CONSTANTS
# =============================================================================

ELEMENT_COLORS = {
    "Wood": "#48bb78", "Fire": "#f56565", "Earth": "#ecc94b",
    "Metal": "#a0aec0", "Water": "#4299e1"
}

STAR_DATA = {
    "Canopy": {"cn": "天蓬", "elem": "Water", "nature": "Inauspicious"},
    "Grass": {"cn": "天芮", "elem": "Earth", "nature": "Inauspicious"},
    "Impulse": {"cn": "天冲", "elem": "Wood", "nature": "Auspicious"},
    "Assistant": {"cn": "天辅", "elem": "Wood", "nature": "Auspicious"},
    "Connect": {"cn": "天禽", "elem": "Earth", "nature": "Neutral"},
    "Heart": {"cn": "天心", "elem": "Metal", "nature": "Auspicious"},
    "Pillar": {"cn": "天柱", "elem": "Metal", "nature": "Inauspicious"},
    "Ren": {"cn": "天任", "elem": "Earth", "nature": "Auspicious"},
    "Hero": {"cn": "天英", "elem": "Fire", "nature": "Neutral"}
}

DOOR_DATA = {
    "Open": {"cn": "开门", "elem": "Metal", "nature": "Auspicious"},
    "Rest": {"cn": "休门", "elem": "Water", "nature": "Auspicious"},
    "Life": {"cn": "生门", "elem": "Earth", "nature": "Auspicious"},
    "Harm": {"cn": "伤门", "elem": "Wood", "nature": "Inauspicious"},
    "Delusion": {"cn": "杜门", "elem": "Wood", "nature": "Neutral"},
    "Scenery": {"cn": "景门", "elem": "Fire", "nature": "Neutral"},
    "Death": {"cn": "死门", "elem": "Earth", "nature": "Inauspicious"},
    "Fear": {"cn": "惊门", "elem": "Metal", "nature": "Inauspicious"}
}

DEITY_DATA = {
    "Chief": {"cn": "值符", "nature": "Auspicious"},
    "Serpent": {"cn": "腾蛇", "nature": "Inauspicious"},
    "Moon": {"cn": "太阴", "nature": "Auspicious"},
    "Six Harmony": {"cn": "六合", "nature": "Auspicious"},
    "Hook": {"cn": "勾陈", "nature": "Neutral"},
    "Tiger": {"cn": "白虎", "nature": "Inauspicious"},
    "Emptiness": {"cn": "玄武", "nature": "Inauspicious"},
    "Nine Earth": {"cn": "九地", "nature": "Auspicious"},
    "Nine Heaven": {"cn": "九天", "nature": "Auspicious"}
}

PALACE_NAMES = {
    1: ("Kan 坎", "N", "Water"),
    2: ("Kun 坤", "SW", "Earth"),
    3: ("Zhen 震", "E", "Wood"),
    4: ("Xun 巽", "SE", "Wood"),
    5: ("Center 中", "C", "Earth"),
    6: ("Qian 乾", "NW", "Metal"),
    7: ("Dui 兑", "W", "Metal"),
    8: ("Gen 艮", "NE", "Earth"),
    9: ("Li 离", "S", "Fire")
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_strength_class(strength: str) -> str:
    """Get CSS class for strength badge"""
    mapping = {
        "Timely": "strength-timely",
        "Prosperous": "strength-prosperous",
        "Resting": "strength-resting",
        "Confined": "strength-confined",
        "Dead": "strength-dead"
    }
    return mapping.get(strength, "strength-resting")

def calculate_component_strength(component_element: str, palace_element: str) -> str:
    """Calculate strength based on element relationship"""
    if component_element == palace_element:
        return "Timely"
    
    produces = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
    produced_by = {"Fire": "Wood", "Earth": "Fire", "Metal": "Earth", "Water": "Metal", "Wood": "Water"}
    controls = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}
    controlled_by = {"Earth": "Wood", "Water": "Earth", "Fire": "Water", "Metal": "Fire", "Wood": "Metal"}
    
    if produces.get(palace_element) == component_element:
        return "Prosperous"
    elif produced_by.get(component_element) == palace_element:
        return "Resting"
    elif controls.get(palace_element) == component_element:
        return "Confined"
    elif controlled_by.get(component_element) == palace_element:
        return "Dead"
    return "Resting"

# =============================================================================
# DISPLAY FUNCTIONS - FIXED HTML
# =============================================================================

def display_palace_card(palace_num: int, palace_data: dict, selected: bool = False, 
                        is_empty: bool = False, has_horse: bool = False, has_noble: bool = False):
    """Display a palace card with proper HTML escaping"""
    
    name, direction, element = PALACE_NAMES.get(palace_num, ("?", "?", "?"))
    
    star = palace_data.get("star", "?")
    door = palace_data.get("door", "?")
    deity = palace_data.get("deity", "?")
    
    # Build CSS classes
    classes = ["palace-card"]
    if selected:
        classes.append("palace-selected")
    if is_empty:
        classes.append("palace-empty")
    if has_horse:
        classes.append("palace-horse")
    if has_noble:
        classes.append("palace-noble")
    
    css_class = " ".join(classes)
    
    # Build indicators HTML - FIXED: properly escape and build
    indicators = []
    if has_horse:
        indicators.append('<span class="indicator-badge badge-horse">🐴 HORSE</span>')
    if has_noble:
        indicators.append('<span class="indicator-badge badge-noble">👑 NOBLEMAN</span>')
    if is_empty:
        indicators.append('<span class="indicator-badge badge-empty">⭕ EMPTY</span>')
    
    indicators_html = " ".join(indicators)
    
    # Get element color
    elem_color = ELEMENT_COLORS.get(element, "#fff")
    
    # Build the complete HTML - FIXED: no orphan tags
    html = f'''<div class="{css_class}">
        <div style="margin-bottom: 5px;">{indicators_html}</div>
        <div style="color: #4299e1; font-size: 0.85em;">🔮 PALACE {palace_num}: {name} ({direction})</div>
        <div style="color: {elem_color}; font-size: 0.75em; margin-top: 3px;">{element}</div>
        <div style="margin-top: 8px; font-size: 0.85em;">
            <span style="color: #f6e05e;">★ {star}</span>
        </div>
        <div style="font-size: 0.85em;">
            <span style="color: #48bb78;">🚪 {door}</span>
        </div>
        <div style="font-size: 0.85em;">
            <span style="color: #9f7aea;">👑 {deity}</span>
        </div>
    </div>'''
    
    st.markdown(html, unsafe_allow_html=True)


def display_component_details(comp_type: str, name: str, palace_element: str):
    """Display component details with strength calculation"""
    
    if comp_type == "star":
        data = STAR_DATA.get(name, {})
        icon = "⭐"
        label = "STAR 星"
        color = "#f6e05e"
    elif comp_type == "door":
        data = DOOR_DATA.get(name, {})
        icon = "🚪"
        label = "DOOR 门"
        color = "#48bb78"
    else:
        data = DEITY_DATA.get(name, {})
        icon = "👑"
        label = "DEITY 神"
        color = "#9f7aea"
    
    cn = data.get("cn", "")
    elem = data.get("elem", "")
    nature = data.get("nature", "Neutral")
    
    # Calculate strength
    if elem:
        strength = calculate_component_strength(elem, palace_element)
        strength_class = get_strength_class(strength)
    else:
        strength = ""
        strength_class = ""
    
    # Nature badge
    if nature == "Auspicious":
        nature_badge = '<span style="background: #276749; color: #48bb78; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">Auspicious</span>'
    elif nature == "Inauspicious":
        nature_badge = '<span style="background: #742a2a; color: #fc8181; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">Inauspicious</span>'
    else:
        nature_badge = '<span style="background: #4a5568; color: #a0aec0; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">Neutral</span>'
    
    # Strength badge
    if strength:
        strength_badge = f'<span class="indicator-badge {strength_class}">{strength}</span>'
    else:
        strength_badge = ""
    
    st.markdown(f"""
    <div class="component-box component-{comp_type}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: {color}; font-weight: bold;">{icon} {label}</span>
            {strength_badge}
        </div>
        <div style="font-size: 1.2em; margin: 8px 0;">
            <strong>{name}</strong> <span style="color: #718096;">{cn}</span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            {f'<span style="background: {ELEMENT_COLORS.get(elem, "#718096")}; color: #000; padding: 2px 8px; border-radius: 5px; font-size: 0.8em;">{elem}</span>' if elem else ''}
            {nature_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN
# =============================================================================

def main():
    st.title("🎯 QMDJ Chart")
    st.caption("Qi Men Dun Jia Hour Chart Analysis")
    
    if not IMPORTS_OK:
        st.error(f"Import error: {IMPORT_ERROR}")
        st.info("Using demo mode with sample data")
    
    # Sidebar - Time Selection
    with st.sidebar:
        st.header("⏰ Chart Time")
        
        tz = pytz.timezone('Asia/Singapore')
        now = datetime.now(tz)
        
        use_now = st.checkbox("Use current time", value=True)
        
        if use_now:
            chart_date = now.date()
            chart_hour = now.hour
            chart_minute = now.minute
            st.info(f"📍 {now.strftime('%Y-%m-%d %H:%M')} SGT")
        else:
            chart_date = st.date_input("Date", value=now.date())
            col1, col2 = st.columns(2)
            with col1:
                chart_hour = st.selectbox("Hour", range(24), index=now.hour, format_func=lambda x: f"{x:02d}")
            with col2:
                chart_minute = st.selectbox("Min", range(60), index=0, format_func=lambda x: f"{x:02d}")
        
        st.divider()
        
        # BaZi Profile
        profile = st.session_state.get("user_profile", None)
        if profile:
            st.success(f"🎴 {profile.get('day_master', '?')} {profile.get('day_master_cn', '')} DM")
            st.caption(f"Useful: {', '.join(profile.get('useful_gods', []))}")
        else:
            st.warning("Set BaZi profile for personalized analysis")
        
        st.divider()
        generate_btn = st.button("🔮 Generate Chart", type="primary", use_container_width=True)
    
    # Generate chart
    if generate_btn or st.session_state.get("current_chart"):
        if generate_btn:
            tz = pytz.timezone('Asia/Singapore')
            chart_dt = tz.localize(datetime.combine(chart_date, datetime.min.time().replace(hour=chart_hour, minute=chart_minute)))
            
            if IMPORTS_OK:
                try:
                    chart = generate_qmdj_chart(chart_dt)
                    st.session_state.current_chart = chart
                    st.session_state.chart_time = chart_dt
                except Exception as e:
                    st.error(f"Chart generation error: {e}")
                    # Use demo data
                    chart = generate_demo_chart()
                    st.session_state.current_chart = chart
            else:
                chart = generate_demo_chart()
                st.session_state.current_chart = chart
        else:
            chart = st.session_state.current_chart
            chart_dt = st.session_state.get("chart_time", datetime.now())
        
        # Get indicators
        palaces = chart.get("palaces", {})
        indicators = chart.get("indicators", {})
        empty_palaces = indicators.get("death_emptiness", {}).get("affected_palaces", [])
        horse_palace = indicators.get("horse_star", {}).get("palace", 0)
        noble_palaces = indicators.get("nobleman", {}).get("palaces", [])
        
        # Chart info header
        st.markdown(f"""
        ### 📅 {chart_dt.strftime('%Y-%m-%d')} at {chart_dt.strftime('%H:%M')}
        **Structure:** {chart.get('structure', 'Yang Dun')} | **Ju:** {chart.get('ju_number', '?')}
        """)
        
        st.divider()
        
        # 9 Palace Grid
        st.subheader("🏯 Nine Palaces")
        
        # Palace selection
        selected_palace = st.session_state.get("selected_palace", 5)
        
        grid = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        
        for row in grid:
            cols = st.columns(3)
            for i, p_num in enumerate(row):
                with cols[i]:
                    p_data = palaces.get(str(p_num), {})
                    is_selected = p_num == selected_palace
                    is_empty = p_num in empty_palaces
                    has_horse = p_num == horse_palace
                    has_noble = p_num in noble_palaces
                    
                    # Make clickable
                    if st.button(f"P{p_num}", key=f"palace_{p_num}", use_container_width=True):
                        st.session_state.selected_palace = p_num
                        selected_palace = p_num
                    
                    display_palace_card(p_num, p_data, is_selected, is_empty, has_horse, has_noble)
        
        st.divider()
        
        # Selected Palace Details
        st.subheader(f"🔍 Palace {selected_palace} Details")
        
        p_data = palaces.get(str(selected_palace), {})
        p_name, p_dir, p_elem = PALACE_NAMES.get(selected_palace, ("?", "?", "?"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Components 组件")
            display_component_details("star", p_data.get("star", "Unknown"), p_elem)
            display_component_details("door", p_data.get("door", "Unknown"), p_elem)
            display_component_details("deity", p_data.get("deity", "Unknown"), p_elem)
        
        with col2:
            st.markdown("### Analysis 分析")
            
            # Palace element
            elem_color = ELEMENT_COLORS.get(p_elem, "#fff")
            st.markdown(f"""
            <div style="background: #1a2744; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                <span style="color: {elem_color};">Palace Element: {p_elem}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Indicators
            is_empty = selected_palace in empty_palaces
            has_horse = selected_palace == horse_palace
            has_noble = selected_palace in noble_palaces
            
            if has_noble:
                st.success("👑 **Nobleman (贵人):** Helpful people will appear. Good for seeking assistance.")
            if has_horse:
                st.info("🐴 **Horse Star (驿马):** Movement, travel, quick action favored.")
            if is_empty:
                st.warning("⭕ **Death & Emptiness (空亡):** Energy is weak. Delay if possible.")
            
            # BaZi alignment
            profile = st.session_state.get("user_profile", None)
            if profile:
                st.markdown("### BaZi Alignment 八字配合")
                useful = profile.get("useful_gods", [])
                st.markdown(f"""
                <div style="background: #1a2744; padding: 10px; border-radius: 8px;">
                    <span style="color: #4299e1;">Palace element: {p_elem} | Your useful: {', '.join(useful)}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if p_elem in useful:
                    st.success(f"✅ Palace {p_elem} aligns with your useful element!")
        
        # Formations
        st.divider()
        st.subheader("📜 Formations")
        
        if IMPORTS_OK:
            try:
                formations = detect_formations(p_data)
                if formations:
                    for f in formations:
                        emoji = "✨" if f.category.value == "Auspicious" else "⚠️" if f.category.value == "Inauspicious" else "📜"
                        st.markdown(f"• {emoji} **{f.name_en}** ({f.category.value}) - {f.meaning[:100]}...")
                else:
                    st.info("No special formations detected in this palace")
            except:
                st.info("Formation detection unavailable")
        else:
            st.info("Formation detection requires full installation")
    
    else:
        st.info("👈 Click **Generate Chart** to create a QMDJ chart")


def generate_demo_chart():
    """Generate demo chart data when engine unavailable"""
    return {
        "structure": "Yang Dun",
        "ju_number": 3,
        "palaces": {
            "1": {"star": "Assistant", "door": "Open", "deity": "Chief"},
            "2": {"star": "Connect", "door": "Fear", "deity": "Serpent"},
            "3": {"star": "Heart", "door": "Life", "deity": "Moon"},
            "4": {"star": "Pillar", "door": "Rest", "deity": "Six Harmony"},
            "5": {"star": "Ren", "door": "Death", "deity": "Hook"},
            "6": {"star": "Hero", "door": "Harm", "deity": "Tiger"},
            "7": {"star": "Canopy", "door": "Delusion", "deity": "Emptiness"},
            "8": {"star": "Grass", "door": "Scenery", "deity": "Nine Earth"},
            "9": {"star": "Impulse", "door": "Open", "deity": "Nine Heaven"}
        },
        "indicators": {
            "death_emptiness": {"affected_palaces": [3, 8]},
            "horse_star": {"palace": 6},
            "nobleman": {"palaces": [2, 8]}
        }
    }


if __name__ == "__main__":
    main()
