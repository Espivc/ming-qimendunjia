# Ming QiMenDunJia v10.0 - Professional BaZi Analysis
# pages/6_BaZi.py
"""
PROFESSIONAL BAZI ANALYSIS with Joey Yap style 10 Profiles display
"""

import streamlit as st
from datetime import datetime, date
import pytz
import json
import math

import sys
sys.path.insert(0, '..')

try:
    from core.bazi_calculator import (
        calculate_bazi_chart, chart_to_dict, BaZiChart,
        STEM_ELEMENTS, HEAVENLY_STEMS_CN, EARTHLY_BRANCHES_CN,
        TEN_PROFILES, get_ten_god
    )
    BAZI_IMPORTS_OK = True
except ImportError as e:
    BAZI_IMPORTS_OK = False
    import_error = str(e)

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
    
    .dm-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 2px solid #4299e1;
        border-radius: 12px;
        padding: 20px;
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
    .profile-fill {
        height: 100%;
        border-radius: 5px;
        display: flex;
        align-items: center;
        padding-left: 10px;
        color: white;
        font-weight: bold;
        font-size: 0.85em;
    }
    .profile-pct {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: white;
        font-weight: bold;
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
    
    .structure-label {
        font-size: 0.75em;
        color: #a0aec0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CONSTANTS
# =============================================================================

ELEMENT_COLORS = {
    "Wood": "#48bb78", "Fire": "#f56565", "Earth": "#ecc94b",
    "Metal": "#a0aec0", "Water": "#4299e1"
}

# 10 Profile colors (matching Joey Yap style)
PROFILE_COLORS = {
    "DO": "#c53030",  # Direct Officer - Dark Red
    "IR": "#d69e2e",  # Indirect Resource - Gold
    "7K": "#9b2c2c",  # Seven Killings - Deep Red
    "DR": "#dd6b20",  # Direct Resource - Orange
    "F": "#3182ce",   # Friend - Blue
    "EG": "#38a169",  # Eating God - Green
    "RW": "#805ad5",  # Rob Wealth - Purple
    "DW": "#d53f8c",  # Direct Wealth - Pink
    "IW": "#e53e3e",  # Indirect Wealth - Red
    "HO": "#319795",  # Hurting Officer - Teal
}

PROFILE_NAMES = {
    "DO": "The Diplomat (Direct Officer)",
    "IR": "The Philosopher (Indirect Resource)",
    "7K": "The Warrior (Seven Killings)",
    "DR": "The Analyzer (Direct Resource)",
    "F": "The Friend (Friend)",
    "EG": "The Artist (Eating God)",
    "RW": "The Leader (Rob Wealth)",
    "DW": "The Director (Direct Wealth)",
    "IW": "The Pioneer (Indirect Wealth)",
    "HO": "The Performer (Hurting Officer)",
}

PROFILE_CN = {
    "DO": "正官格", "IR": "偏印格", "7K": "七殺格", "DR": "正印格", "F": "比肩格",
    "EG": "食神格", "RW": "劫財格", "DW": "正財格", "IW": "偏財格", "HO": "傷官格"
}

# 5 Structures mapping
STRUCTURE_MAPPING = {
    "Wealth": ["DW", "IW"],      # Wood - Manager
    "Influence": ["DO", "7K"],   # Fire - Supporters
    "Resources": ["DR", "IR"],   # Earth - Thinkers
    "Companion": ["F", "RW"],    # Metal - Connectors
    "Output": ["EG", "HO"],      # Water - Creators
}

STRUCTURE_COLORS = {
    "Wealth": "#48bb78",      # Green (Wood)
    "Influence": "#f56565",   # Red (Fire)
    "Resources": "#ecc94b",   # Yellow (Earth)
    "Companion": "#a0aec0",   # Gray (Metal)
    "Output": "#4299e1",      # Blue (Water)
}

# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_pillar(pillar, title: str, is_dm: bool = False, day_master: str = None):
    """Display pillar card"""
    elem_color = ELEMENT_COLORS.get(pillar.stem_element, "#fff")
    
    ten_god = ""
    if day_master and pillar.stem != day_master:
        code, _, _ = get_ten_god(day_master, pillar.stem)
        ten_god = f" ({code})"
    
    hidden = " ".join([HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(h)] for h in pillar.hidden_stems])
    
    cls = "pillar-dm" if is_dm else ""
    
    st.markdown(f"""
    <div class="pillar-card {cls}">
        <div style="color: #718096; font-size: 0.8em;">{title}</div>
        <div style="font-size: 2.5em; color: {elem_color}; font-weight: bold;">{pillar.stem_cn}</div>
        <div style="color: {elem_color}; font-size: 0.8em;">{pillar.stem} {pillar.stem_element}{ten_god}</div>
        <div style="font-size: 2em; margin: 5px 0;">{pillar.branch_cn}</div>
        <div style="color: #718096; font-size: 0.85em;">{pillar.animal} {pillar.animal_cn}</div>
        <div style="color: #4a5568; font-size: 0.75em; margin-top: 8px; border-top: 1px dashed #2d3748; padding-top: 8px;">
            藏干: {hidden}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_10_profiles(distribution: dict):
    """Display 10 Profiles with beautiful bar chart like Joey Yap"""
    st.markdown("### 10 PROFILES STRENGTH CHART 十神格")
    
    # Sort by percentage descending
    sorted_profiles = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
    
    for code, pct in sorted_profiles:
        color = PROFILE_COLORS.get(code, "#718096")
        name = PROFILE_NAMES.get(code, code)
        cn = PROFILE_CN.get(code, "")
        
        # Calculate width (minimum 5% for visibility)
        width = max(pct, 5) if pct > 0 else 0
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 6px 0;">
            <div style="width: 30px; color: #718096; font-size: 0.85em;">{code}</div>
            <div style="flex: 1; margin: 0 10px;">
                <div class="profile-bar">
                    <div class="profile-fill" style="width: {width}%; background: {color};">
                        {name}
                    </div>
                    <span class="profile-pct">{pct:.0f}%</span>
                </div>
            </div>
            <div style="width: 60px; color: #718096; font-size: 0.75em; text-align: right;">{cn}</div>
        </div>
        """, unsafe_allow_html=True)


def display_5_structures_radar(distribution: dict):
    """Display 5 Structures as a visual representation"""
    st.markdown("### 5 STRUCTURES 五型格")
    
    # Calculate structure percentages
    structures = {}
    for struct_name, gods in STRUCTURE_MAPPING.items():
        total = sum(distribution.get(g, 0) for g in gods)
        structures[struct_name] = total
    
    # Normalize to max 100
    max_val = max(structures.values()) if structures.values() else 1
    
    # Create visual bars for each structure
    struct_order = ["Wealth", "Influence", "Resources", "Companion", "Output"]
    struct_cn = {"Wealth": "管理型 Wealth", "Influence": "忠誠型 Influence", "Resources": "智慧型 Resources", 
                 "Companion": "交際型 Companion", "Output": "創作型 Output"}
    struct_elem = {"Wealth": "木 WOOD", "Influence": "火 FIRE", "Resources": "土 EARTH", 
                   "Companion": "金 METAL", "Output": "水 WATER"}
    
    cols = st.columns(5)
    for i, struct in enumerate(struct_order):
        with cols[i]:
            pct = structures.get(struct, 0)
            color = STRUCTURE_COLORS.get(struct, "#718096")
            height = int(pct * 1.5) + 20  # Scale for visual
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: {color}; font-weight: bold; font-size: 0.9em;">{struct_elem[struct]}</div>
                <div style="background: #1a2744; border-radius: 5px; height: 100px; position: relative; margin: 10px auto; width: 60px;">
                    <div style="position: absolute; bottom: 0; width: 100%; height: {min(height, 100)}px; background: {color}; border-radius: 5px;"></div>
                </div>
                <div style="color: #a0aec0; font-size: 0.75em;">{struct_cn[struct]}</div>
                <div style="color: {color}; font-weight: bold;">{pct:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Show main structure
    main_struct = max(structures.items(), key=lambda x: x[1])[0]
    st.markdown(f"**Main Structure:** {struct_cn[main_struct]}")


def display_luck_pillars(luck_pillars, day_master: str):
    """Display luck pillars"""
    cols = st.columns(min(len(luck_pillars), 10))
    
    for i, lp in enumerate(luck_pillars[:10]):
        with cols[i]:
            cls = "luck-current" if lp.is_current else ""
            code, _, _ = get_ten_god(day_master, lp.stem)
            color = PROFILE_COLORS.get(code, "#718096")
            
            st.markdown(f"""
            <div class="luck-pillar {cls}">
                <div style="font-size: 0.7em; color: #718096;">{lp.age_start}-{lp.age_end}</div>
                <div style="font-size: 1.5em; color: {color};">{lp.stem_cn}</div>
                <div style="font-size: 1.2em;">{lp.branch_cn}</div>
                <div style="font-size: 0.7em; color: #718096;">{lp.animal}</div>
                <div style="font-size: 0.7em; color: {color};">{code}</div>
            </div>
            """, unsafe_allow_html=True)


def generate_pdf_html(chart: BaZiChart) -> str:
    """Generate HTML for PDF export"""
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
body {{ font-family: Arial; padding: 20px; }}
h1 {{ color: #1a365d; border-bottom: 2px solid #4299e1; }}
h2 {{ color: #2c5282; margin-top: 25px; }}
.pillars {{ display: flex; gap: 20px; margin: 20px 0; }}
.pillar {{ text-align: center; padding: 15px; border: 2px solid #e2e8f0; border-radius: 10px; min-width: 100px; }}
.pillar-dm {{ border-color: #4299e1; }}
.stem {{ font-size: 32px; font-weight: bold; }}
.branch {{ font-size: 26px; }}
.lp-row {{ display: flex; gap: 10px; flex-wrap: wrap; }}
.lp {{ text-align: center; padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; min-width: 60px; }}
.lp-current {{ border: 2px solid #ecc94b; background: #fffbeb; }}
table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
th, td {{ border: 1px solid #e2e8f0; padding: 8px; text-align: left; }}
th {{ background: #f7fafc; }}
.bar {{ background: #e2e8f0; height: 20px; border-radius: 3px; margin: 3px 0; }}
.bar-fill {{ height: 100%; border-radius: 3px; }}
</style></head><body>
<h1>🎴 BaZi Analysis Report</h1>
<p><b>Birth:</b> {chart.birth_date.strftime('%B %d, %Y')} at {chart.birth_hour:02d}:{chart.birth_minute:02d}</p>
<p><b>Day Master:</b> {chart.day_master} {chart.day_pillar.stem_cn} ({chart.day_master_polarity} {chart.day_master_element})</p>
<p><b>Strength:</b> {chart.strength_category} ({chart.dm_strength}%)</p>

<h2>Four Pillars 四柱</h2>
<div class="pillars">
<div class="pillar"><div style="color:#718096;font-size:12px;">Hour 時</div><div class="stem">{chart.hour_pillar.stem_cn}</div><div class="branch">{chart.hour_pillar.branch_cn}</div><div style="color:#718096;">{chart.hour_pillar.animal}</div></div>
<div class="pillar pillar-dm"><div style="color:#718096;font-size:12px;">Day 日 ★</div><div class="stem" style="color:#2c5282;">{chart.day_pillar.stem_cn}</div><div class="branch">{chart.day_pillar.branch_cn}</div><div style="color:#718096;">{chart.day_pillar.animal}</div></div>
<div class="pillar"><div style="color:#718096;font-size:12px;">Month 月</div><div class="stem">{chart.month_pillar.stem_cn}</div><div class="branch">{chart.month_pillar.branch_cn}</div><div style="color:#718096;">{chart.month_pillar.animal}</div></div>
<div class="pillar"><div style="color:#718096;font-size:12px;">Year 年</div><div class="stem">{chart.year_pillar.stem_cn}</div><div class="branch">{chart.year_pillar.branch_cn}</div><div style="color:#718096;">{chart.year_pillar.animal}</div></div>
</div>

<h2>Analysis</h2>
<table>
<tr><th>Aspect</th><th>Value</th></tr>
<tr><td>Day Master</td><td>{chart.day_master} {chart.day_pillar.stem_cn} ({chart.day_master_element})</td></tr>
<tr><td>Strength</td><td>{chart.strength_category} ({chart.dm_strength}%)</td></tr>
<tr><td>Useful Gods</td><td>{', '.join(chart.useful_gods)}</td></tr>
<tr><td>Unfavorable</td><td>{', '.join(chart.unfavorable_elements)}</td></tr>
<tr><td>Main Profile</td><td>{chart.main_profile}</td></tr>
</table>

<h2>10-Year Luck Pillars 大運</h2>
<div class="lp-row">"""
    
    for lp in chart.luck_pillars[:8]:
        cls = "lp-current" if lp.is_current else ""
        html += f'<div class="lp {cls}"><div style="font-size:10px;color:#718096;">{lp.age_start}-{lp.age_end}</div><div style="font-size:20px;">{lp.stem_cn}</div><div style="font-size:16px;">{lp.branch_cn}</div></div>'
    
    html += f"""</div>

<h2>10 Profiles Distribution</h2>
<table><tr><th>Profile</th><th>Percentage</th></tr>"""
    
    for code, pct in sorted(chart.ten_gods_distribution.items(), key=lambda x: x[1], reverse=True):
        if pct > 0:
            html += f"<tr><td>{code} - {PROFILE_NAMES.get(code, '')}</td><td>{pct:.1f}%</td></tr>"
    
    html += f"""</table>
<div style="margin-top:40px;text-align:center;color:#a0aec0;font-size:12px;">
Generated by Ming QiMenDunJia v10.0 | {datetime.now().strftime('%Y-%m-%d')}
</div></body></html>"""
    
    return html


# =============================================================================
# MAIN
# =============================================================================

def main():
    st.title("🎴 BaZi Analysis")
    st.caption("Four Pillars of Destiny • Professional Analysis")
    
    if not BAZI_IMPORTS_OK:
        st.error(f"BaZi module not loaded: {import_error}")
        return
    
    # Sidebar
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
                birth_minute = st.selectbox("Minute", range(60), index=saved.get("minute", 8), format_func=lambda x: f"{x:02d}")
        
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        gender_code = "M" if gender == "Male" else "F"
        
        st.divider()
        calc_btn = st.button("🔮 Calculate BaZi", type="primary", use_container_width=True)
    
    # Main
    if calc_btn or st.session_state.get("bazi_chart"):
        if calc_btn:
            chart = calculate_bazi_chart(birth_date, birth_hour, birth_minute, gender_code)
            st.session_state.bazi_chart = chart
            st.session_state.bazi_birth_info = {"date": birth_date, "hour": birth_hour, "minute": birth_minute, "gender": gender_code}
            st.session_state.user_profile = {
                "day_master": chart.day_master, "day_master_cn": chart.day_pillar.stem_cn,
                "element": chart.day_master_element, "polarity": chart.day_master_polarity,
                "strength": chart.strength_category, "strength_pct": chart.dm_strength,
                "useful_gods": chart.useful_gods, "unfavorable": chart.unfavorable_elements,
                "profile": chart.main_profile, "birth_date": birth_date.isoformat(),
                "birth_hour": birth_hour, "birth_minute": birth_minute
            }
        else:
            chart = st.session_state.bazi_chart
        
        # Day Master Card
        elem_color = ELEMENT_COLORS[chart.day_master_element]
        st.markdown(f"""
        <div class="dm-card">
            <div style="color: #718096;">DAY MASTER 日主</div>
            <div style="font-size: 3em; color: {elem_color}; font-weight: bold;">{chart.day_pillar.stem_cn} {chart.day_master}</div>
            <div style="color: #a0aec0;">{chart.day_master_polarity} {chart.day_master_element} • {chart.main_profile}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Four Pillars
        st.subheader("📊 Four Pillars 四柱")
        cols = st.columns(4)
        pillars = [(chart.hour_pillar, "Hour 時", False), (chart.day_pillar, "Day 日 ★", True),
                   (chart.month_pillar, "Month 月", False), (chart.year_pillar, "Year 年", False)]
        for i, (p, t, dm) in enumerate(pillars):
            with cols[i]:
                display_pillar(p, t, dm, chart.day_master)
        
        st.divider()
        
        # Strength + Useful Gods
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💪 Day Master Strength")
            pct = chart.dm_strength
            opp = 100 - pct
            color = "#48bb78" if pct >= 60 else "#f56565" if pct <= 40 else "#ecc94b"
            
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
            st.markdown(f"**Unfavorable 忌神:** {', '.join(chart.unfavorable_elements)}")
        
        with col2:
            display_5_structures_radar(chart.ten_gods_distribution)
        
        st.divider()
        
        # 10 Profiles
        display_10_profiles(chart.ten_gods_distribution)
        
        st.divider()
        
        # Luck Pillars
        st.subheader("🎯 10-Year Luck Pillars 大運")
        display_luck_pillars(chart.luck_pillars, chart.day_master)
        
        st.divider()
        
        # Symbolic Stars
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("⭐ Symbolic Stars 神煞")
            for star, val in chart.symbolic_stars.items():
                st.markdown(f"**{star}:** {val}")
        
        with col2:
            st.subheader("🏛️ Special Palaces")
            lp_s, lp_b = chart.life_palace
            cp_s, cp_b = chart.conception_palace
            lp_cn = HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(lp_s)]
            lp_bcn = EARTHLY_BRANCHES_CN[["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"].index(lp_b)]
            cp_cn = HEAVENLY_STEMS_CN[["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"].index(cp_s)]
            cp_bcn = EARTHLY_BRANCHES_CN[["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"].index(cp_b)]
            st.markdown(f"**Life Palace 命宮:** {lp_cn}{lp_bcn}")
            st.markdown(f"**Conception Palace 胎元:** {cp_cn}{cp_bcn}")
        
        st.divider()
        
        # Export
        st.subheader("📤 Export")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pdf_html = generate_pdf_html(chart)
            st.download_button("📄 Download Report (HTML)", pdf_html, f"bazi_{birth_date}.html", "text/html", use_container_width=True)
            st.caption("Open → Print → Save as PDF")
        
        with col2:
            json_data = json.dumps(chart_to_dict(chart), indent=2, default=str)
            st.download_button("📊 Download Data (JSON)", json_data, f"bazi_{birth_date}.json", "application/json", use_container_width=True)
        
        with col3:
            if st.button("🤖 Get AI Analysis", use_container_width=True):
                st.session_state.show_bazi_prompt = True
        
        if st.session_state.get("show_bazi_prompt"):
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

**10 Gods:** {chart.ten_gods_distribution}
**Current Luck:** Age {chart.luck_pillars[4].age_start}-{chart.luck_pillars[4].age_end if len(chart.luck_pillars) > 4 else '?'}

Please provide:
1. Day Master personality
2. Chart structure interpretation
3. Useful God strategy
4. Current luck period analysis
5. Career & wealth potential
6. Relationship insights
7. Key life advice"""
            
            st.code(prompt, language="markdown")
            st.info("Copy and paste to Claude")
    
    else:
        st.info("👈 Enter birth info and click **Calculate BaZi**")

if __name__ == "__main__":
    main()
