# Ming QiMenDunJia v10.0 - Professional BaZi Analysis
# pages/4_BaZi.py
"""
PROFESSIONAL BAZI ANALYSIS (八字命盤)

Complete Four Pillars analysis with:
- Four Pillars + Hidden Stems
- 10-Year Luck Pillars
- DM Strength Analysis
- 10 Gods Distribution
- Symbolic Stars
- PDF Export
"""

import streamlit as st
from datetime import datetime, date
import pytz
import json
import io

# Import BaZi calculator
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


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="BaZi Analysis | Ming Qimen",
    page_icon="🎴",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0a1628; }
    
    .pillar-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        min-height: 200px;
    }
    .pillar-header {
        color: #718096;
        font-size: 0.85em;
        margin-bottom: 8px;
    }
    .pillar-stem {
        font-size: 2.5em;
        font-weight: bold;
        margin: 5px 0;
    }
    .pillar-branch {
        font-size: 2em;
        margin: 5px 0;
    }
    .pillar-animal {
        color: #a0aec0;
        font-size: 0.9em;
    }
    .hidden-stems {
        color: #718096;
        font-size: 0.8em;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px dashed #2d3748;
    }
    .ten-god-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75em;
        margin: 2px;
    }
    
    .strength-bar-container {
        background: #1a2744;
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        margin: 10px 0;
    }
    .strength-bar {
        height: 100%;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .luck-pillar {
        background: #1a2744;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        border: 1px solid #2d3748;
        min-width: 80px;
    }
    .luck-pillar-current {
        border: 2px solid #FFD700 !important;
        background: linear-gradient(135deg, #2d3748 0%, #1a2744 100%);
    }
    
    .dm-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 2px solid #4299e1;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .star-item {
        background: #1a2744;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        display: flex;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# ELEMENT COLORS
# =============================================================================

ELEMENT_COLORS = {
    "Wood": "#48bb78",
    "Fire": "#f56565",
    "Earth": "#ecc94b",
    "Metal": "#a0aec0",
    "Water": "#4299e1"
}

TEN_GOD_COLORS = {
    "F": "#4299e1", "RW": "#9f7aea",
    "IR": "#ecc94b", "DR": "#f6ad55",
    "EG": "#48bb78", "HO": "#38b2ac",
    "IW": "#ed64a6", "DW": "#fc8181",
    "7K": "#f56565", "DO": "#ed8936"
}


# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_pillar(pillar, title: str, day_master: str = None):
    """Display a single pillar with all details"""
    elem_color = ELEMENT_COLORS.get(pillar.stem_element, "#fff")
    branch_color = ELEMENT_COLORS.get(pillar.branch_element, "#fff")
    
    # Get 10 God for stem if day master provided
    ten_god_html = ""
    if day_master and pillar.stem != day_master:
        god_code, god_name, god_cn = get_ten_god(day_master, pillar.stem)
        god_color = TEN_GOD_COLORS.get(god_code, "#718096")
        ten_god_html = f'<span class="ten-god-badge" style="background: {god_color};">{god_code}</span>'
    
    # Hidden stems with 10 gods
    hidden_html = ""
    if pillar.hidden_stems and day_master:
        hs_parts = []
        for hs in pillar.hidden_stems:
            hs_cn = HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(hs)]
            if hs != day_master:
                code, _, _ = get_ten_god(day_master, hs)
                hs_parts.append(f"{hs_cn} <span style='color: {TEN_GOD_COLORS.get(code, '#718096')};'>{code}</span>")
            else:
                hs_parts.append(f"{hs_cn}")
        hidden_html = " ".join(hs_parts)
    
    st.markdown(f"""
    <div class="pillar-card">
        <div class="pillar-header">{title}</div>
        <div class="pillar-stem" style="color: {elem_color};">
            {pillar.stem_cn} {ten_god_html}
        </div>
        <div style="color: {elem_color}; font-size: 0.8em;">{pillar.stem} {pillar.stem_element}</div>
        <div class="pillar-branch" style="color: {branch_color};">
            {pillar.branch_cn}
        </div>
        <div class="pillar-animal">{pillar.animal} {pillar.animal_cn}</div>
        <div style="color: {branch_color}; font-size: 0.75em;">{pillar.branch_element}</div>
        <div class="hidden-stems">藏干: {hidden_html}</div>
    </div>
    """, unsafe_allow_html=True)


def display_strength_bar(strength_pct: float, category: str):
    """Display DM strength bar"""
    if strength_pct >= 60:
        color = "#48bb78"  # Green for strong
    elif strength_pct <= 40:
        color = "#f56565"  # Red for weak
    else:
        color = "#ecc94b"  # Yellow for balanced
    
    opposing_pct = 100 - strength_pct
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <span style="color: #48bb78;">Supporting: {strength_pct}%</span>
        <span style="color: #f56565;">Opposing: {opposing_pct}%</span>
    </div>
    <div class="strength-bar-container">
        <div class="strength-bar" style="width: {strength_pct}%; background: linear-gradient(90deg, #48bb78, {color});">
            {category}
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_luck_pillars(luck_pillars, day_master: str):
    """Display 10-year luck pillars"""
    cols = st.columns(min(len(luck_pillars), 10))
    
    for i, lp in enumerate(luck_pillars[:10]):
        with cols[i]:
            current_class = "luck-pillar-current" if lp.is_current else ""
            god_code, _, _ = get_ten_god(day_master, lp.stem)
            god_color = TEN_GOD_COLORS.get(god_code, "#718096")
            
            st.markdown(f"""
            <div class="luck-pillar {current_class}">
                <div style="color: #718096; font-size: 0.7em;">{lp.age_start}-{lp.age_end}</div>
                <div style="color: #FFD700; font-size: 1.5em;">{lp.stem_cn}</div>
                <div style="font-size: 1.3em;">{lp.branch_cn}</div>
                <div style="color: #718096; font-size: 0.7em;">{lp.animal}</div>
                <div style="color: {god_color}; font-size: 0.75em;">{god_code}</div>
            </div>
            """, unsafe_allow_html=True)


def display_ten_gods_chart(distribution: dict):
    """Display 10 Gods distribution as bars"""
    # Sort by percentage
    sorted_gods = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
    
    for god_code, pct in sorted_gods:
        if pct > 0:
            profile_name, _ = TEN_PROFILES.get(god_code, ("Unknown", ""))
            color = TEN_GOD_COLORS.get(god_code, "#718096")
            
            st.markdown(f"""
            <div style="margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="color: {color};">{god_code} {profile_name}</span>
                    <span style="color: #a0aec0;">{pct}%</span>
                </div>
                <div style="background: #1a2744; border-radius: 5px; height: 12px;">
                    <div style="background: {color}; width: {pct}%; height: 100%; border-radius: 5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def generate_pdf_content(chart: BaZiChart) -> str:
    """Generate HTML content for PDF export"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; background: #fff; color: #333; }}
            h1 {{ color: #1a365d; border-bottom: 2px solid #4299e1; padding-bottom: 10px; }}
            h2 {{ color: #2c5282; margin-top: 30px; }}
            .pillars {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .pillar {{ text-align: center; padding: 15px; border: 2px solid #e2e8f0; border-radius: 10px; min-width: 120px; }}
            .pillar-title {{ color: #718096; font-size: 12px; }}
            .stem {{ font-size: 36px; font-weight: bold; }}
            .branch {{ font-size: 28px; }}
            .animal {{ color: #718096; font-size: 14px; }}
            .hidden {{ color: #a0aec0; font-size: 12px; margin-top: 10px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
            .info-box {{ background: #f7fafc; padding: 15px; border-radius: 8px; }}
            .strength-bar {{ background: #e2e8f0; height: 25px; border-radius: 5px; margin: 10px 0; }}
            .strength-fill {{ background: linear-gradient(90deg, #48bb78, #38a169); height: 100%; border-radius: 5px; }}
            .luck-pillars {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }}
            .lp {{ text-align: center; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px; min-width: 70px; }}
            .lp-current {{ border: 2px solid #ecc94b; background: #fffbeb; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th, td {{ border: 1px solid #e2e8f0; padding: 10px; text-align: left; }}
            th {{ background: #f7fafc; }}
            .footer {{ margin-top: 40px; text-align: center; color: #a0aec0; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>🎴 BaZi Analysis Report</h1>
        <p><strong>Birth Date:</strong> {chart.birth_date.strftime('%B %d, %Y')} at {chart.birth_hour:02d}:{chart.birth_minute:02d}</p>
        <p><strong>Gender:</strong> {"Male" if chart.gender == "M" else "Female"}</p>
        
        <h2>Four Pillars (四柱)</h2>
        <div class="pillars">
            <div class="pillar">
                <div class="pillar-title">Hour 時</div>
                <div class="stem">{chart.hour_pillar.stem_cn}</div>
                <div class="branch">{chart.hour_pillar.branch_cn}</div>
                <div class="animal">{chart.hour_pillar.animal}</div>
                <div class="hidden">藏: {' '.join([HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(hs)] for hs in chart.hour_pillar.hidden_stems])}</div>
            </div>
            <div class="pillar" style="border-color: #4299e1; border-width: 3px;">
                <div class="pillar-title">Day 日 (Day Master)</div>
                <div class="stem" style="color: #2c5282;">{chart.day_pillar.stem_cn}</div>
                <div class="branch">{chart.day_pillar.branch_cn}</div>
                <div class="animal">{chart.day_pillar.animal}</div>
                <div class="hidden">藏: {' '.join([HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(hs)] for hs in chart.day_pillar.hidden_stems])}</div>
            </div>
            <div class="pillar">
                <div class="pillar-title">Month 月</div>
                <div class="stem">{chart.month_pillar.stem_cn}</div>
                <div class="branch">{chart.month_pillar.branch_cn}</div>
                <div class="animal">{chart.month_pillar.animal}</div>
                <div class="hidden">藏: {' '.join([HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(hs)] for hs in chart.month_pillar.hidden_stems])}</div>
            </div>
            <div class="pillar">
                <div class="pillar-title">Year 年</div>
                <div class="stem">{chart.year_pillar.stem_cn}</div>
                <div class="branch">{chart.year_pillar.branch_cn}</div>
                <div class="animal">{chart.year_pillar.animal}</div>
                <div class="hidden">藏: {' '.join([HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(hs)] for hs in chart.year_pillar.hidden_stems])}</div>
            </div>
        </div>
        
        <h2>Day Master Analysis</h2>
        <div class="info-grid">
            <div class="info-box">
                <p><strong>Day Master:</strong> {chart.day_master} {chart.day_pillar.stem_cn} ({chart.day_master_element} {chart.day_master_polarity})</p>
                <p><strong>Strength:</strong> {chart.strength_category} ({chart.dm_strength}%)</p>
                <div class="strength-bar">
                    <div class="strength-fill" style="width: {chart.dm_strength}%;"></div>
                </div>
            </div>
            <div class="info-box">
                <p><strong>Useful Gods:</strong> {', '.join(chart.useful_gods)}</p>
                <p><strong>Unfavorable:</strong> {', '.join(chart.unfavorable_elements)}</p>
                <p><strong>Main Profile:</strong> {chart.main_profile}</p>
            </div>
        </div>
        
        <h2>10-Year Luck Pillars (大運)</h2>
        <div class="luck-pillars">
    """
    
    for lp in chart.luck_pillars[:8]:
        current_class = "lp-current" if lp.is_current else ""
        html += f"""
            <div class="lp {current_class}">
                <div style="font-size: 10px; color: #718096;">{lp.age_start}-{lp.age_end}</div>
                <div style="font-size: 24px;">{lp.stem_cn}</div>
                <div style="font-size: 20px;">{lp.branch_cn}</div>
                <div style="font-size: 11px; color: #718096;">{lp.animal}</div>
            </div>
        """
    
    html += """
        </div>
        
        <h2>Symbolic Stars (神煞)</h2>
        <table>
            <tr><th>Star</th><th>Branch</th></tr>
    """
    
    for star_name, star_value in chart.symbolic_stars.items():
        html += f"<tr><td>{star_name}</td><td>{star_value}</td></tr>"
    
    html += f"""
        </table>
        
        <h2>10 Gods Distribution</h2>
        <table>
            <tr><th>10 God</th><th>Percentage</th></tr>
    """
    
    sorted_gods = sorted(chart.ten_gods_distribution.items(), key=lambda x: x[1], reverse=True)
    for god_code, pct in sorted_gods:
        if pct > 0:
            profile_name, _ = TEN_PROFILES.get(god_code, ("Unknown", ""))
            html += f"<tr><td>{god_code} - {profile_name}</td><td>{pct}%</td></tr>"
    
    html += f"""
        </table>
        
        <div class="footer">
            <p>Generated by Ming QiMenDunJia v10.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p>www.mingqimen.com | "Helping people first"</p>
        </div>
    </body>
    </html>
    """
    
    return html


# =============================================================================
# MAIN PAGE
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
        
        # Check for saved data from session state
        saved_birth = st.session_state.get("bazi_birth_info", {})
        
        birth_date = st.date_input(
            "Birth Date",
            value=saved_birth.get("date", date(1990, 1, 1)),
            min_value=date(1920, 1, 1),
            max_value=date.today()
        )
        
        unknown_time = st.checkbox("Unknown birth time", value=False)
        
        if unknown_time:
            st.info("Using 12:00 noon")
            birth_hour = 12
            birth_minute = 0
        else:
            col1, col2 = st.columns(2)
            with col1:
                birth_hour = st.selectbox(
                    "Hour", 
                    options=list(range(0, 24)), 
                    index=saved_birth.get("hour", 12),
                    format_func=lambda x: f"{x:02d}"
                )
            with col2:
                birth_minute = st.selectbox(
                    "Minute", 
                    options=list(range(0, 60)),
                    index=saved_birth.get("minute", 0),
                    format_func=lambda x: f"{x:02d}"
                )
        
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        gender_code = "M" if gender == "Male" else "F"
        
        st.divider()
        
        calculate_btn = st.button("🔮 Calculate BaZi", type="primary", use_container_width=True)
    
    # Main content
    if calculate_btn or st.session_state.get("bazi_chart"):
        if calculate_btn:
            # Calculate chart
            chart = calculate_bazi_chart(
                birth_date=birth_date,
                birth_hour=birth_hour,
                birth_minute=birth_minute,
                gender=gender_code
            )
            
            # Save to session state for Destiny page
            st.session_state.bazi_chart = chart
            st.session_state.bazi_birth_info = {
                "date": birth_date,
                "hour": birth_hour,
                "minute": birth_minute,
                "gender": gender_code
            }
            
            # Also save user profile for other pages
            st.session_state.user_profile = {
                "day_master": chart.day_master,
                "day_master_cn": chart.day_pillar.stem_cn,
                "element": chart.day_master_element,
                "polarity": chart.day_master_polarity,
                "strength": chart.strength_category,
                "strength_pct": chart.dm_strength,
                "useful_gods": chart.useful_gods,
                "unfavorable": chart.unfavorable_elements,
                "profile": chart.main_profile,
                "birth_date": birth_date.isoformat(),
                "birth_hour": birth_hour,
                "birth_minute": birth_minute
            }
        else:
            chart = st.session_state.bazi_chart
        
        # Display header
        st.markdown(f"""
        <div class="dm-card">
            <div style="color: #718096;">DAY MASTER 日主</div>
            <div style="font-size: 3em; color: {ELEMENT_COLORS[chart.day_master_element]};">
                {chart.day_pillar.stem_cn} {chart.day_master}
            </div>
            <div style="color: #a0aec0;">
                {chart.day_master_polarity} {chart.day_master_element} • {chart.main_profile}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Four Pillars
        st.subheader("📊 Four Pillars (四柱)")
        
        cols = st.columns(4)
        pillars = [
            (chart.hour_pillar, "Hour 時"),
            (chart.day_pillar, "Day 日 ★"),
            (chart.month_pillar, "Month 月"),
            (chart.year_pillar, "Year 年")
        ]
        
        for i, (pillar, title) in enumerate(pillars):
            with cols[i]:
                display_pillar(pillar, title, chart.day_master)
        
        st.divider()
        
        # Day Master Strength
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💪 Day Master Strength")
            display_strength_bar(chart.dm_strength, chart.strength_category)
            
            st.markdown(f"""
            **Useful Gods (用神):** {', '.join(chart.useful_gods)}  
            **Unfavorable (忌神):** {', '.join(chart.unfavorable_elements)}
            """)
        
        with col2:
            st.subheader("📈 10 Gods Distribution")
            display_ten_gods_chart(chart.ten_gods_distribution)
        
        st.divider()
        
        # Luck Pillars
        st.subheader("🎯 10-Year Luck Pillars (大運)")
        display_luck_pillars(chart.luck_pillars, chart.day_master)
        
        st.divider()
        
        # Symbolic Stars
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⭐ Symbolic Stars (神煞)")
            for star_name, star_value in chart.symbolic_stars.items():
                branch_cn = ""
                if star_value in EARTHLY_BRANCHES_CN:
                    branch_cn = EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES_CN.index(star_value)] if star_value in EARTHLY_BRANCHES_CN else ""
                
                st.markdown(f"""
                <div class="star-item">
                    <span>{star_name}</span>
                    <span style="color: #FFD700;">{star_value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("🏛️ Special Palaces")
            
            life_stem, life_branch = chart.life_palace
            life_stem_cn = HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(life_stem)]
            life_branch_cn = EARTHLY_BRANCHES_CN[["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"].index(life_branch)]
            
            con_stem, con_branch = chart.conception_palace
            con_stem_cn = HEAVENLY_STEMS_CN[["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"].index(con_stem)]
            con_branch_cn = EARTHLY_BRANCHES_CN[["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"].index(con_branch)]
            
            st.markdown(f"""
            <div class="star-item">
                <span>Life Palace (命宮)</span>
                <span style="color: #FFD700;">{life_stem_cn}{life_branch_cn}</span>
            </div>
            <div class="star-item">
                <span>Conception Palace (胎元)</span>
                <span style="color: #FFD700;">{con_stem_cn}{con_branch_cn}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Export Options
        st.subheader("📤 Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # PDF Export (HTML download)
            pdf_html = generate_pdf_content(chart)
            st.download_button(
                "📄 Download Report (HTML)",
                pdf_html,
                file_name=f"bazi_report_{birth_date.strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
            st.caption("Open in browser → Print → Save as PDF")
        
        with col2:
            # JSON Export
            json_data = json.dumps(chart_to_dict(chart), indent=2, default=str)
            st.download_button(
                "📊 Download Data (JSON)",
                json_data,
                file_name=f"bazi_data_{birth_date.strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # AI Analysis prompt
            if st.button("🤖 Get AI Analysis", use_container_width=True):
                st.session_state.show_bazi_prompt = True
        
        if st.session_state.get("show_bazi_prompt"):
            prompt = f"""Analyze this BaZi (Four Pillars) chart:

**Birth:** {birth_date.strftime('%B %d, %Y')} at {birth_hour:02d}:{birth_minute:02d}
**Gender:** {gender}

**Four Pillars:**
- Year: {chart.year_pillar.stem_cn} {chart.year_pillar.branch_cn} ({chart.year_pillar.animal})
- Month: {chart.month_pillar.stem_cn} {chart.month_pillar.branch_cn} ({chart.month_pillar.animal})
- Day: {chart.day_pillar.stem_cn} {chart.day_pillar.branch_cn} ({chart.day_pillar.animal}) ← Day Master
- Hour: {chart.hour_pillar.stem_cn} {chart.hour_pillar.branch_cn} ({chart.hour_pillar.animal})

**Day Master:** {chart.day_master} {chart.day_pillar.stem_cn} ({chart.day_master_polarity} {chart.day_master_element})
**Strength:** {chart.strength_category} ({chart.dm_strength}%)
**Useful Gods:** {', '.join(chart.useful_gods)}
**Main Profile:** {chart.main_profile}

**10 Gods Distribution:** {chart.ten_gods_distribution}

**Current Luck Pillar:** {next((lp for lp in chart.luck_pillars if lp.is_current), None)}

Please provide:
1. Day Master personality analysis
2. Chart structure interpretation  
3. Useful God strategy
4. Current luck period analysis
5. Career and wealth potential
6. Relationship insights
7. Key advice for life optimization"""
            
            st.code(prompt, language="markdown")
            st.info("Copy and paste to Claude for detailed analysis")
    
    else:
        st.info("👈 Enter birth information and click **Calculate BaZi**")
        
        st.markdown("""
        ### What You'll Get
        
        **Four Pillars Analysis:**
        - Year, Month, Day, Hour pillars
        - Hidden Stems in each branch
        - 10 Gods for each component
        
        **Day Master Analysis:**
        - Strength percentage (Strong/Weak/Balanced)
        - Useful Gods recommendations
        - 10 Profiles identification
        
        **Luck Pillars:**
        - 10-Year periods
        - Current period highlight
        - Life phase guidance
        
        **Symbolic Stars:**
        - Noble People, Peach Blossom
        - Sky Horse, Intelligence
        - Life Palace, Conception Palace
        
        **Export Options:**
        - PDF Report for printing
        - JSON for data analysis
        - AI prompt for deep interpretation
        """)


# Add earthly branches list for PDF function
EARTHLY_BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]

if __name__ == "__main__":
    main()
