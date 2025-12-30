"""
Ming Qimen 明奇门 - BaZi Calculator v6.0
Calculate Four Pillars of Destiny
"""

import streamlit as st
from datetime import datetime, date, timezone, timedelta

st.set_page_config(page_title="BaZi | Ming Qimen", page_icon="🎂", layout="wide")

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
    
    .pillar-box {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
        border: 2px solid #333;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        min-height: 180px;
    }
    
    .pillar-label {
        font-family: 'Cinzel', serif;
        color: #888;
        font-size: 0.8rem;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .pillar-stem {
        font-family: 'Noto Sans SC', sans-serif;
        color: #FFD700;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    .pillar-branch {
        font-family: 'Noto Sans SC', sans-serif;
        color: #87CEEB;
        font-size: 2.5rem;
        font-weight: 500;
        line-height: 1.2;
    }
    
    .pillar-pinyin {
        color: #888;
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
    
    .dm-card {
        background: linear-gradient(135deg, #2d1f3d 0%, #1a1a2e 100%);
        border: 2px solid #9B59B6;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .dm-title {
        font-family: 'Cinzel', serif;
        color: #9B59B6;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .dm-character {
        font-family: 'Noto Sans SC', sans-serif;
        color: #FFD700;
        font-size: 4rem;
        font-weight: 700;
    }
    
    .dm-name {
        font-family: 'Cinzel', serif;
        color: #E8E8E8;
        font-size: 1.5rem;
        margin-top: 0.5rem;
    }
    
    .analysis-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .analysis-title {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .element-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
    
    .strength-meter {
        background: #333;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .strength-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# BAZI CALCULATION FUNCTIONS
# ============================================================

HEAVENLY_STEMS = [
    ("Jia", "甲", "Wood", "Yang"),
    ("Yi", "乙", "Wood", "Yin"),
    ("Bing", "丙", "Fire", "Yang"),
    ("Ding", "丁", "Fire", "Yin"),
    ("Wu", "戊", "Earth", "Yang"),
    ("Ji", "己", "Earth", "Yin"),
    ("Geng", "庚", "Metal", "Yang"),
    ("Xin", "辛", "Metal", "Yin"),
    ("Ren", "壬", "Water", "Yang"),
    ("Gui", "癸", "Water", "Yin"),
]

EARTHLY_BRANCHES = [
    ("Zi", "子", "Water", "Rat"),
    ("Chou", "丑", "Earth", "Ox"),
    ("Yin", "寅", "Wood", "Tiger"),
    ("Mao", "卯", "Wood", "Rabbit"),
    ("Chen", "辰", "Earth", "Dragon"),
    ("Si", "巳", "Fire", "Snake"),
    ("Wu", "午", "Fire", "Horse"),
    ("Wei", "未", "Earth", "Goat"),
    ("Shen", "申", "Metal", "Monkey"),
    ("You", "酉", "Metal", "Rooster"),
    ("Xu", "戌", "Earth", "Dog"),
    ("Hai", "亥", "Water", "Pig"),
]

def calculate_year_pillar(year):
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_month_pillar(year, month, day):
    # Simplified - use month directly (adjust for solar terms in production)
    solar_month = month
    if day < 5:
        solar_month = month - 1 if month > 1 else 12
    
    branch_idx = (solar_month + 1) % 12
    year_stem_idx = (year - 4) % 10
    stem_idx = ((year_stem_idx % 5) * 2 + solar_month) % 10
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_day_pillar(year, month, day):
    from datetime import date as dt_date
    ref_date = dt_date(1900, 1, 1)
    target_date = dt_date(year, month, day)
    days_diff = (target_date - ref_date).days
    
    stem_idx = (days_diff + 0) % 10
    branch_idx = (days_diff + 4) % 12
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_hour_pillar(day_stem_idx, hour):
    # Chinese hour (2-hour blocks)
    hour_branch_idx = ((hour + 1) // 2) % 12
    hour_stem_idx = ((day_stem_idx % 5) * 2 + hour_branch_idx) % 10
    
    return HEAVENLY_STEMS[hour_stem_idx], EARTHLY_BRANCHES[hour_branch_idx]

def calculate_dm_strength(pillars):
    """Calculate Day Master strength (simplified)"""
    day_stem = pillars["Day"]["stem"]
    dm_element = day_stem[2]
    
    # Count supporting elements
    support_count = 0
    drain_count = 0
    
    # Production cycle
    production = {
        "Wood": "Water", "Fire": "Wood", "Earth": "Fire",
        "Metal": "Earth", "Water": "Metal"
    }
    
    # Control cycle
    control = {
        "Wood": "Metal", "Fire": "Water", "Earth": "Wood",
        "Metal": "Fire", "Water": "Earth"
    }
    
    for pillar_name, pillar in pillars.items():
        stem_element = pillar["stem"][2]
        branch_element = pillar["branch"][2]
        
        for element in [stem_element, branch_element]:
            if element == dm_element or element == production[dm_element]:
                support_count += 1
            elif element == control[dm_element]:
                drain_count += 1
    
    # Calculate strength score (1-10)
    score = 5 + support_count - drain_count
    score = max(1, min(10, score))
    
    if score <= 3:
        strength = "Weak"
    elif score <= 5:
        strength = "Balanced"
    else:
        strength = "Strong"
    
    return strength, score

def calculate_useful_gods(dm_element, strength):
    """Determine Useful Gods based on Day Master element and strength"""
    
    production = {
        "Wood": "Water", "Fire": "Wood", "Earth": "Fire",
        "Metal": "Earth", "Water": "Metal"
    }
    
    produced = {
        "Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
        "Metal": "Water", "Water": "Wood"
    }
    
    control = {
        "Wood": "Metal", "Fire": "Water", "Earth": "Wood",
        "Metal": "Fire", "Water": "Earth"
    }
    
    controlled = {
        "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
        "Metal": "Wood", "Water": "Fire"
    }
    
    if strength in ["Weak", "Very Weak"]:
        # Weak DM needs support
        useful = [production[dm_element], dm_element]  # Producer + same element
        unfavorable = [control[dm_element]]  # Controller is bad
    else:
        # Strong DM needs draining
        useful = [produced[dm_element], controlled[dm_element]]  # Output + wealth
        unfavorable = [production[dm_element], dm_element]  # Producer + same element
    
    return useful, unfavorable

def get_ten_god_profile(dm_element, dm_polarity, dominant_element):
    """Determine Ten God profile"""
    
    profiles = {
        ("Wood", "Yang", "Metal"): ("Warrior", "7 Killings"),
        ("Wood", "Yin", "Metal"): ("Leader", "Direct Officer"),
        ("Wood", "Yang", "Earth"): ("Pioneer", "Indirect Wealth"),
        ("Wood", "Yin", "Earth"): ("Director", "Direct Wealth"),
        ("Metal", "Yang", "Fire"): ("Warrior", "7 Killings"),
        ("Metal", "Yin", "Fire"): ("Leader", "Direct Officer"),
        ("Metal", "Yang", "Wood"): ("Pioneer", "Indirect Wealth"),
        ("Metal", "Yin", "Wood"): ("Director", "Direct Wealth"),
        # Add more combinations...
    }
    
    key = (dm_element, dm_polarity, dominant_element)
    return profiles.get(key, ("Pioneer", "Indirect Wealth"))

# ============================================================
# PAGE CONTENT
# ============================================================

st.markdown('<h1 class="page-header">🎂 BAZI CALCULATOR</h1>', unsafe_allow_html=True)
st.markdown("*Calculate your Four Pillars of Destiny 四柱八字*")

st.divider()

# Input section
st.subheader("📅 Enter Birth Information")

col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input(
        "Birth Date 出生日期",
        value=date(1978, 6, 27),  # Ben's birth date as default
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

with col2:
    unknown_time = st.checkbox("I don't know my birth time")
    
    if not unknown_time:
        time_col1, time_col2 = st.columns(2)
        with time_col1:
            birth_hour = st.selectbox(
                "Hour 时",
                options=list(range(0, 24)),
                index=12,
                format_func=lambda x: f"{x:02d}:00"
            )
        with time_col2:
            birth_minute = st.selectbox(
                "Minute 分",
                options=[0, 15, 30, 45],
                index=0
            )
    else:
        birth_hour = 12
        birth_minute = 0
        st.info("Without birth time, Hour Pillar will be estimated. For accurate results, try to find your birth time.")

# Calculate button
if st.button("🔮 CALCULATE MY BAZI", type="primary", use_container_width=True):
    with st.spinner("Calculating Four Pillars..."):
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        # Calculate pillars
        year_stem, year_branch = calculate_year_pillar(year)
        month_stem, month_branch = calculate_month_pillar(year, month, day)
        day_stem, day_branch = calculate_day_pillar(year, month, day)
        hour_stem, hour_branch = calculate_hour_pillar(
            HEAVENLY_STEMS.index(day_stem), birth_hour
        )
        
        pillars = {
            "Year": {"stem": year_stem, "branch": year_branch},
            "Month": {"stem": month_stem, "branch": month_branch},
            "Day": {"stem": day_stem, "branch": day_branch},
            "Hour": {"stem": hour_stem, "branch": hour_branch}
        }
        
        # Calculate strength
        strength, strength_score = calculate_dm_strength(pillars)
        
        # Calculate useful gods
        useful_gods, unfavorable = calculate_useful_gods(day_stem[2], strength)
        
        # Get profile
        profile_name, dominant_god = get_ten_god_profile(
            day_stem[2], day_stem[3], useful_gods[0] if useful_gods else "Earth"
        )
        
        # Check for special structures (simplified)
        wealth_vault = day_branch[0] in ["Chou", "Chen", "Wei", "Xu"]  # Earth branches
        
        # Store in session state
        st.session_state.calculated_bazi = {
            "pillars": pillars,
            "day_master": f"{day_stem[0]} {day_stem[1]}",
            "element": day_stem[2],
            "polarity": day_stem[3],
            "strength": strength,
            "strength_score": strength_score,
            "useful_gods": useful_gods,
            "unfavorable": unfavorable,
            "profile": f"{profile_name} ({dominant_god})",
            "wealth_vault": wealth_vault,
            "nobleman": False,
            "birth_date": str(birth_date),
            "birth_time": f"{birth_hour:02d}:{birth_minute:02d}",
            "unknown_time": unknown_time
        }
        
        st.success("✅ BaZi calculated!")
        st.rerun()

# Display results
if st.session_state.get("calculated_bazi"):
    bazi = st.session_state.calculated_bazi
    pillars = bazi["pillars"]
    
    st.divider()
    st.subheader("📜 Your Four Pillars 四柱")
    
    # Pillar display
    pillar_cols = st.columns(4)
    pillar_order = ["Hour", "Day", "Month", "Year"]
    pillar_chinese = ["时柱", "日柱", "月柱", "年柱"]
    
    for i, (name, chinese) in enumerate(zip(pillar_order, pillar_chinese)):
        with pillar_cols[i]:
            p = pillars[name]
            stem = p["stem"]
            branch = p["branch"]
            
            # Highlight Day Pillar
            border_color = "#9B59B6" if name == "Day" else "#333"
            
            st.markdown(f"""
            <div class="pillar-box" style="border-color: {border_color};">
                <div class="pillar-label">{name.upper()} • {chinese}</div>
                <div class="pillar-stem">{stem[1]}</div>
                <div class="pillar-branch">{branch[1]}</div>
                <div class="pillar-pinyin">{stem[0]} {stem[2]}<br>{branch[0]} {branch[2]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Day Master card
    st.markdown(f"""
    <div class="dm-card">
        <div class="dm-title">DAY MASTER 日主</div>
        <div class="dm-character">{pillars['Day']['stem'][1]}</div>
        <div class="dm-name">{bazi['day_master']} • {bazi['polarity']} {bazi['element']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analysis cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Strength
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title">💪 Day Master Strength</div>
            <div style="font-size: 1.5rem; color: #FFD700;">{bazi['strength']}</div>
            <div class="strength-meter">
                <div class="strength-fill" style="width: {bazi['strength_score'] * 10}%; background: linear-gradient(90deg, #e74c3c, #f39c12, #2ecc71);"></div>
            </div>
            <div style="color: #888;">{bazi['strength_score']}/10</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Profile
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title">🎭 Ten God Profile</div>
            <div style="font-size: 1.2rem; color: #FFD700;">{bazi['profile']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Useful Gods
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-title">💎 Useful Gods 用神</div>', unsafe_allow_html=True)
        for god in bazi['useful_gods']:
            element_class = god.lower()
            st.markdown(f'<span class="element-badge {element_class}">{god}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Unfavorable
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-title">⚠️ Unfavorable 忌神</div>', unsafe_allow_html=True)
        for element in bazi['unfavorable']:
            element_class = element.lower()
            st.markdown(f'<span class="element-badge {element_class}">{element}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Special structures
    if bazi['wealth_vault'] or bazi['nobleman']:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-title">✨ Special Structures</div>', unsafe_allow_html=True)
        if bazi['wealth_vault']:
            st.markdown("💰 **Wealth Vault** - Potential for accumulating wealth")
        if bazi['nobleman']:
            st.markdown("👑 **Nobleman Present** - Helpful people in your life")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save button
    st.divider()
    
    if st.button("💾 SAVE TO PROFILE", type="primary", use_container_width=True):
        st.session_state.user_profile = {
            "day_master": bazi['day_master'],
            "element": bazi['element'],
            "polarity": bazi['polarity'],
            "strength": bazi['strength'],
            "strength_score": bazi['strength_score'],
            "useful_gods": bazi['useful_gods'],
            "unfavorable": bazi['unfavorable'],
            "profile": bazi['profile'],
            "wealth_vault": bazi['wealth_vault'],
            "nobleman": bazi['nobleman'],
            "birth_date": bazi['birth_date'],
            "birth_time": bazi['birth_time'],
            "unknown_time": bazi['unknown_time'],
            "manual_entry": False
        }
        st.success("✅ Profile saved! You can now see personalized QMDJ analysis.")
        st.balloons()

# Sidebar
with st.sidebar:
    st.markdown("### 🎂 BaZi Calculator")
    
    if st.session_state.get("user_profile"):
        st.success("✅ Profile Saved")
        profile = st.session_state.user_profile
        st.markdown(f"**{profile.get('day_master', 'Unknown')}**")
        st.markdown(f"{profile.get('polarity', '')} {profile.get('element', '')}")
    elif st.session_state.get("calculated_bazi"):
        st.warning("⚠️ Not saved yet")
    else:
        st.info("Enter birth info above")
    
    st.markdown("---")
    st.markdown("### 📖 Quick Links")
    
    if st.button("📊 Chart Generator", use_container_width=True):
        st.switch_page("pages/1_Chart.py")
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/4_Settings.py")

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | BaZi Calculator v6.0")
