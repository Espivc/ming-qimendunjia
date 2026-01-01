# Ming QiMenDunJia v10.1 - Professional BaZi with Annual Overlay
# pages/6_BaZi.py
"""
PROFESSIONAL BAZI with:
- 10 Profiles (Joey Yap style)
- 5 Structures display
- 2025 Annual Pillar overlay
- Improved accuracy
"""

import streamlit as st
from datetime import datetime, date
import json

import sys
sys.path.insert(0, '..')

try:
    from core.bazi_calculator import (
        calculate_bazi_chart, chart_to_dict, BaZiChart,
        STEM_ELEMENTS, HEAVENLY_STEMS_CN, EARTHLY_BRANCHES_CN,
        TEN_PROFILES, get_ten_god, calculate_annual_pillar
    )
    BAZI_OK = True
except ImportError as e:
    BAZI_OK = False
    IMPORT_ERR = str(e)

st.set_page_config(page_title="BaZi Analysis | Ming Qimen", page_icon="🎴", layout="wide")

# =============================================================================
# STYLES
# =============================================================================

st.markdown("""
<style>
    .stApp { background-color: #0a1628; }
    .pillar-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .pillar-dm { border: 2px solid #4299e1 !important; }
    .pillar-annual { border: 2px solid #f6ad55 !important; background: linear-gradient(135deg, #2d3020 0%, #1a2744 100%); }
    .dm-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 2px solid #4299e1;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .annual-card {
        background: linear-gradient(135deg, #3d2e0a 0%, #1a2744 100%);
        border: 2px solid #f6ad55;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .profile-bar {
        background: #1a2744;
        border-radius: 5px;
        height: 28px;
        margin: 4px 0;
        position: relative;
        overflow: hidden;
    }
    .luck-pillar {
        background: #1a2744;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        border: 1px solid #2d3748;
        min-width: 70px;
    }
    .luck-current { border: 2px solid #FFD700 !important; background: #2d3748; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CONSTANTS
# =============================================================================

ELEMENT_COLORS = {
    "Wood": "#48bb78", "Fire": "#f56565", "Earth": "#ecc94b",
    "Metal": "#a0aec0", "Water": "#4299e1"
}

PROFILE_COLORS = {
    "DO": "#c53030", "IR": "#d69e2e", "7K": "#9b2c2c", "DR": "#dd6b20",
    "F": "#3182ce", "EG": "#38a169", "RW": "#805ad5", "DW": "#d53f8c",
    "IW": "#e53e3e", "HO": "#319795"
}

PROFILE_NAMES = {
    "DO": "The Diplomat 正官格", "IR": "The Philosopher 偏印格",
    "7K": "The Warrior 七殺格", "DR": "The Analyzer 正印格",
    "F": "The Friend 比肩格", "EG": "The Artist 食神格",
    "RW": "The Leader 劫財格", "DW": "The Director 正財格",
    "IW": "The Pioneer 偏財格", "HO": "The Performer 傷官格"
}

STRUCTURE_MAPPING = {
    "Wealth": ["DW", "IW"], "Influence": ["DO", "7K"],
    "Resources": ["DR", "IR"], "Companion": ["F", "RW"], "Output": ["EG", "HO"]
}

STRUCTURE_COLORS = {
    "Wealth": "#48bb78", "Influence": "#f56565", "Resources": "#ecc94b",
    "Companion": "#a0aec0", "Output": "#4299e1"
}

# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_pillar(pillar, title: str, is_dm: bool = False, is_annual: bool = False, day_master: str = None):
    """Display pillar card"""
    elem_color = ELEMENT_COLORS.get(pillar.stem_element, "#fff")
    
    ten_god = ""
    if day_master and pillar.stem != day_master:
        code, _, _ = get_ten_god(day_master, pillar.stem)
        ten_god = f"({code})"
        god_color = PROFILE_COLORS.get(code, "#718096")
    else:
        god_color = elem_color
    
    hidden = " ".join([HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(h)] for h in pillar.hidden_stems])
    
    cls = "pillar-dm" if is_dm else ("pillar-annual" if is_annual else "")
    border_color = "#f6ad55" if is_annual else ("#4299e1" if is_dm else "#2d3748")
    
    st.markdown(f"""
    <div class="pillar-card {cls}" style="border-color: {border_color};">
        <div style="color: #718096; font-size: 0.8em;">{title}</div>
        <div style="font-size: 2.5em; color: {elem_color}; font-weight: bold;">{pillar.stem_cn}</div>
        <div style="color: {god_color}; font-size: 0.8em;">{pillar.stem} {pillar.stem_element} {ten_god}</div>
        <div style="font-size: 2em; margin: 5px 0;">{pillar.branch_cn}</div>
        <div style="color: #718096; font-size: 0.85em;">{pillar.animal} {pillar.animal_cn}</div>
        <div style="color: #4a5568; font-size: 0.75em; margin-top: 8px; border-top: 1px dashed #2d3748; padding-top: 8px;">
            藏干: {hidden}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_10_profiles(distribution: dict):
    """Display 10 Profiles bar chart"""
    st.markdown("### 10 PROFILES STRENGTH 十神格")
    
    sorted_profiles = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
    
    for code, pct in sorted_profiles:
        if pct <= 0:
            continue
        color = PROFILE_COLORS.get(code, "#718096")
        name = PROFILE_NAMES.get(code, code)
        width = max(pct, 5)
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 5px 0;">
            <div style="width: 35px; color: #a0aec0; font-size: 0.85em; font-weight: bold;">{code}</div>
            <div style="flex: 1; margin: 0 10px;">
                <div class="profile-bar">
                    <div style="width: {width}%; height: 100%; background: {color}; border-radius: 5px; display: flex; align-items: center; padding-left: 10px; color: white; font-size: 0.8em;">
                        {name}
                    </div>
                </div>
            </div>
            <div style="width: 50px; color: {color}; font-weight: bold; text-align: right;">{pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)


def display_5_structures(distribution: dict):
    """Display 5 Structures visualization"""
    st.markdown("### 5 STRUCTURES 五型格")
    
    structures = {}
    for name, gods in STRUCTURE_MAPPING.items():
        structures[name] = sum(distribution.get(g, 0) for g in gods)
    
    struct_info = {
        "Wealth": ("木 WOOD", "管理型"), "Influence": ("火 FIRE", "忠誠型"),
        "Resources": ("土 EARTH", "智慧型"), "Companion": ("金 METAL", "交際型"),
        "Output": ("水 WATER", "創作型")
    }
    
    cols = st.columns(5)
    for i, name in enumerate(["Wealth", "Influence", "Resources", "Companion", "Output"]):
        with cols[i]:
            pct = structures.get(name, 0)
            color = STRUCTURE_COLORS.get(name, "#718096")
            elem, cn = struct_info[name]
            height = int(pct * 1.2) + 20
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: {color}; font-weight: bold; font-size: 0.85em;">{elem}</div>
                <div style="background: #1a2744; border-radius: 5px; height: 80px; position: relative; margin: 8px auto; width: 50px;">
                    <div style="position: absolute; bottom: 0; width: 100%; height: {min(height, 80)}px; background: {color}; border-radius: 5px;"></div>
                </div>
                <div style="color: #a0aec0; font-size: 0.7em;">{cn}</div>
                <div style="color: {color}; font-weight: bold;">{pct:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    main = max(structures.items(), key=lambda x: x[1])[0]
    st.caption(f"**Main Structure:** {struct_info[main][1]} {main}")


def display_luck_pillars(luck_pillars, day_master: str):
    """Display luck pillars in a row"""
    cols = st.columns(min(len(luck_pillars), 10))
    
    for i, lp in enumerate(luck_pillars[:10]):
        with cols[i]:
            cls = "luck-current" if lp.is_current else ""
            code, _, _ = get_ten_god(day_master, lp.stem)
            color = PROFILE_COLORS.get(code, "#718096")
            
            st.markdown(f"""
            <div class="luck-pillar {cls}">
                <div style="font-size: 0.65em; color: #718096;">{lp.age_start}-{lp.age_end}</div>
                <div style="font-size: 1.4em; color: {color};">{lp.stem_cn}</div>
                <div style="font-size: 1.1em;">{lp.branch_cn}</div>
                <div style="font-size: 0.65em; color: #718096;">{lp.animal}</div>
                <div style="font-size: 0.65em; color: {color};">{code}</div>
            </div>
            """, unsafe_allow_html=True)


def display_annual_analysis(chart: BaZiChart, annual_year: int):
    """Display annual pillar analysis"""
    if not chart.annual_pillar:
        return
    
    ap = chart.annual_pillar
    dm = chart.day_master
    
    # Get 10 God for annual stem
    code, name, cn = get_ten_god(dm, ap.stem)
    color = PROFILE_COLORS.get(code, "#718096")
    
    st.markdown(f"""
    <div class="annual-card">
        <div style="color: #f6ad55; font-size: 0.9em;">📅 {annual_year} ANNUAL PILLAR 流年</div>
        <div style="font-size: 2em; color: {ELEMENT_COLORS.get(ap.stem_element, '#fff')}; font-weight: bold; margin: 5px 0;">
            {ap.stem_cn} {ap.branch_cn}
        </div>
        <div style="color: #a0aec0;">
            {ap.stem} {ap.stem_element} • {ap.animal} {ap.animal_cn}
        </div>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #4a5568;">
            <span style="color: {color}; font-weight: bold;">10 God: {code} {name} {cn}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Annual influence interpretation
    st.markdown("#### 📊 Annual Influence")
    
    interpretations = {
        "F": "Year of **peers and competition**. Network actively, watch for rivalry.",
        "RW": "Year of **expenditure and socializing**. Control spending, build connections.",
        "IR": "Year of **learning and innovation**. Study, but watch for overthinking.",
        "DR": "Year of **support and guidance**. Seek mentors, academic pursuits favored.",
        "EG": "Year of **creativity and expression**. Create, but avoid overindulgence.",
        "HO": "Year of **performance and change**. Speak up, manage reputation.",
        "IW": "Year of **opportunity and action**. Take calculated risks for wealth.",
        "DW": "Year of **steady income**. Good for traditional business, marriage matters.",
        "7K": "Year of **pressure and transformation**. Face challenges, emerge stronger.",
        "DO": "Year of **recognition and authority**. Career advancement, follow rules."
    }
    
    st.info(interpretations.get(code, "Analyze based on your specific chart context."))
    
    # Element interaction with DM
    annual_elem = ap.stem_element
    dm_elem = chart.day_master_element
    
    if annual_elem in chart.useful_gods:
        st.success(f"✅ {annual_year}'s {annual_elem} element is your **Useful God** - favorable year!")
    elif annual_elem in chart.unfavorable_elements:
        st.warning(f"⚠️ {annual_year}'s {annual_elem} element is **Unfavorable** - exercise caution.")
    else:
        st.info(f"📌 {annual_year}'s {annual_elem} element is neutral for your chart.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    st.title("🎴 BaZi Analysis")
    st.caption("Four Pillars of Destiny • Professional Analysis with Annual Overlay")
    
    if not BAZI_OK:
        st.error(f"Module error: {IMPORT_ERR}")
        return
    
    current_year = date.today().year
    
    with st.sidebar:
        st.header("🎂 Birth Information")
        
        saved = st.session_state.get("bazi_birth_info", {})
        
        birth_date = st.date_input("Birth Date", value=saved.get("date", date(1978, 6, 27)))
        
        unknown = st.checkbox("Unknown birth time")
        if unknown:
            st.info("Using 12:00 noon")
            birth_hour, birth_minute = 12, 0
        else:
            col1, col2 = st.columns(2)
            with col1:
                birth_hour = st.selectbox("Hour", range(24), index=saved.get("hour", 20), format_func=lambda x: f"{x:02d}")
            with col2:
                birth_minute = st.selectbox("Min", range(60), index=saved.get("minute", 8), format_func=lambda x: f"{x:02d}")
        
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        gender_code = "M" if gender == "Male" else "F"
        
        st.divider()
        
        # Annual year selection
        st.subheader("📅 Annual Overlay")
        annual_year = st.selectbox("Year to analyze", 
                                   options=list(range(current_year - 5, current_year + 11)),
                                   index=5)  # Default to current year
        
        st.divider()
        calc_btn = st.button("🔮 Calculate BaZi", type="primary", use_container_width=True)
    
    # Main content
    if calc_btn or st.session_state.get("bazi_chart"):
        if calc_btn:
            chart = calculate_bazi_chart(
                birth_date, birth_hour, birth_minute, gender_code,
                current_year=annual_year, include_annual=True
            )
            st.session_state.bazi_chart = chart
            st.session_state.bazi_birth_info = {
                "date": birth_date, "hour": birth_hour, "minute": birth_minute
            }
            st.session_state.user_profile = {
                "day_master": chart.day_master,
                "day_master_cn": chart.day_pillar.stem_cn,
                "element": chart.day_master_element,
                "polarity": chart.day_master_polarity,
                "strength": chart.strength_category,
                "strength_pct": chart.dm_strength,
                "useful_gods": chart.useful_gods,
                "unfavorable": chart.unfavorable_elements,
                "profile": chart.main_profile
            }
        else:
            chart = st.session_state.bazi_chart
        
        # Day Master Header
        elem_color = ELEMENT_COLORS[chart.day_master_element]
        st.markdown(f"""
        <div class="dm-card">
            <div style="color: #718096;">DAY MASTER 日主</div>
            <div style="font-size: 2.5em; color: {elem_color}; font-weight: bold;">{chart.day_pillar.stem_cn} {chart.day_master}</div>
            <div style="color: #a0aec0;">{chart.day_master_polarity} {chart.day_master_element} • {chart.main_profile}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Four Pillars + Annual
        st.subheader("📊 Four Pillars + Annual Overlay 四柱 + 流年")
        
        cols = st.columns(5)
        pillars = [
            (chart.hour_pillar, "Hour 時", False, False),
            (chart.day_pillar, "Day 日 ★", True, False),
            (chart.month_pillar, "Month 月", False, False),
            (chart.year_pillar, "Year 年", False, False),
            (chart.annual_pillar, f"{annual_year} 流年", False, True) if chart.annual_pillar else (None, "", False, False)
        ]
        
        for i, (p, title, is_dm, is_annual) in enumerate(pillars):
            if p:
                with cols[i]:
                    display_pillar(p, title, is_dm, is_annual, chart.day_master)
        
        st.divider()
        
        # Strength & Useful Gods + Annual Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Day Master Strength")
            pct = chart.dm_strength
            opp = 100 - pct
            color = "#48bb78" if pct >= 55 else ("#f56565" if pct <= 45 else "#ecc94b")
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #48bb78;">Supporting: {pct:.0f}%</span>
                <span style="color: #f56565;">Opposing: {opp:.0f}%</span>
            </div>
            <div style="background: #1a2744; border-radius: 10px; height: 30px; overflow: hidden;">
                <div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #48bb78, {color}); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                    {chart.strength_category}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Useful Gods 用神:** {', '.join(chart.useful_gods)}")
            if chart.unfavorable_elements:
                st.markdown(f"**Unfavorable 忌神:** {', '.join(chart.unfavorable_elements)}")
            
            st.caption(f"Luck Pillar starts at age {chart.luck_pillar_start_age}")
        
        with col2:
            display_annual_analysis(chart, annual_year)
        
        st.divider()
        
        # 5 Structures + 10 Profiles
        col1, col2 = st.columns([1, 2])
        
        with col1:
            display_5_structures(chart.ten_gods_distribution)
        
        with col2:
            display_10_profiles(chart.ten_gods_distribution)
        
        st.divider()
        
        # Luck Pillars
        st.subheader("🎯 10-Year Luck Pillars 大運")
        display_luck_pillars(chart.luck_pillars, chart.day_master)
        
        st.divider()
        
        # Symbolic Stars + Palaces
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⭐ Symbolic Stars 神煞")
            for star, val in chart.symbolic_stars.items():
                st.markdown(f"**{star}:** {val}")
        
        with col2:
            st.subheader("🏛️ Special Palaces")
            if chart.life_palace:
                lp_cn = HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(chart.life_palace[0])]
                lp_bcn = EARTHLY_BRANCHES_CN[["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"].index(chart.life_palace[1])]
                st.markdown(f"**Life Palace 命宮:** {lp_cn}{lp_bcn}")
            if chart.conception_palace:
                cp_cn = HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(chart.conception_palace[0])]
                cp_bcn = EARTHLY_BRANCHES_CN[["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"].index(chart.conception_palace[1])]
                st.markdown(f"**Conception Palace 胎元:** {cp_cn}{cp_bcn}")
        
        st.divider()
        
        # Export
        st.subheader("📤 Export")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            json_data = json.dumps(chart_to_dict(chart), indent=2, default=str)
            st.download_button("📊 Download JSON", json_data, f"bazi_{birth_date}.json", "application/json", use_container_width=True)
        
        with col2:
            if st.button("🤖 AI Analysis Prompt", use_container_width=True):
                st.session_state.show_prompt = True
        
        with col3:
            st.button("📄 PDF Report", use_container_width=True, disabled=True)
            st.caption("Coming soon")
        
        if st.session_state.get("show_prompt"):
            prompt = f"""Analyze this BaZi chart:

**Birth:** {birth_date} at {birth_hour:02d}:{birth_minute:02d} ({gender})

**Four Pillars:**
- Year: {chart.year_pillar.stem_cn} {chart.year_pillar.branch_cn} ({chart.year_pillar.animal})
- Month: {chart.month_pillar.stem_cn} {chart.month_pillar.branch_cn} ({chart.month_pillar.animal})
- Day: {chart.day_pillar.stem_cn} {chart.day_pillar.branch_cn} ({chart.day_pillar.animal}) ← Day Master
- Hour: {chart.hour_pillar.stem_cn} {chart.hour_pillar.branch_cn} ({chart.hour_pillar.animal})

**Day Master:** {chart.day_master} {chart.day_pillar.stem_cn} ({chart.day_master_polarity} {chart.day_master_element})
**Strength:** {chart.strength_category} ({chart.dm_strength:.0f}%)
**Useful Gods:** {', '.join(chart.useful_gods)}
**Main Profile:** {chart.main_profile}

**{annual_year} Annual Pillar:** {chart.annual_pillar.stem_cn} {chart.annual_pillar.branch_cn} ({chart.annual_pillar.animal})

**10 Gods Distribution:** {chart.ten_gods_distribution}

Please provide:
1. Day Master personality analysis
2. Chart structure interpretation
3. Useful God strategy
4. {annual_year} annual forecast
5. Career & wealth potential
6. Relationship insights
7. Key life advice"""
            
            st.code(prompt, language="markdown")
            st.info("Copy and paste to Claude for detailed analysis")
    
    else:
        st.info("👈 Enter birth info and click **Calculate BaZi**")
        
        with st.expander("ℹ️ What's New in v10.1"):
            st.markdown("""
            **Improvements:**
            - ✅ Accurate solar term calculations for month pillar
            - ✅ Proper luck pillar start age calculation
            - ✅ **Annual Pillar Overlay** - see how any year affects your chart
            - ✅ Better DM strength calculation (seasonal weighting)
            - ✅ Fixed 10 Gods distribution accuracy
            
            **Annual Overlay Feature:**
            - Select any year (past or future) to see its influence
            - Shows the 10 God relationship with your Day Master
            - Provides interpretation of annual themes
            - Indicates whether the year element is favorable for you
            """)


if __name__ == "__main__":
    main()
