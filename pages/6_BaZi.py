"""
===============================================================================
6_BaZi.py - Ming QiMenDunJia BaZi Pro Analysis Page
===============================================================================
Version: 10.6 (Joey Yap Aligned)
Updated: 2026-01-03

FIXES APPLIED:
✅ Month Pillar - Solar term calculation (CRITICAL)
✅ Day Pillar - Correct reference date algorithm
✅ Luck Pillar - Joey Yap method (days/3)
✅ DM Strength - Weighted algorithm with categories
✅ Hidden Stems - Correct order per branch
✅ Clash/Combine - Detection implemented

VALIDATED AGAINST JOEY YAP:
Test: June 27, 1978, 8 PM
- Year:  戊午 Wu Wu (Horse) ✅
- Month: 戊午 Wu Wu (Horse) ✅
- Day:   庚申 Geng Shen (Monkey) ✅
- Hour:  丙戌 Bing Xu (Dog) ✅
===============================================================================
"""

import streamlit as st
from datetime import date, datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONSTANTS
# =============================================================================

HEAVENLY_STEMS = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
HEAVENLY_STEMS_CN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
EARTHLY_BRANCHES = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
EARTHLY_BRANCHES_CN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
BRANCH_ANIMALS = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 
                  'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
MONTH_BRANCHES = ['Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 
                  'Shen', 'You', 'Xu', 'Hai', 'Zi', 'Chou']

STEM_ELEMENTS = {
    'Jia': 'Wood', 'Yi': 'Wood', 'Bing': 'Fire', 'Ding': 'Fire',
    'Wu': 'Earth', 'Ji': 'Earth', 'Geng': 'Metal', 'Xin': 'Metal',
    'Ren': 'Water', 'Gui': 'Water'
}

STEM_POLARITY = {
    'Jia': 'Yang', 'Yi': 'Yin', 'Bing': 'Yang', 'Ding': 'Yin',
    'Wu': 'Yang', 'Ji': 'Yin', 'Geng': 'Yang', 'Xin': 'Yin',
    'Ren': 'Yang', 'Gui': 'Yin'
}

BRANCH_ELEMENTS = {
    'Zi': 'Water', 'Chou': 'Earth', 'Yin': 'Wood', 'Mao': 'Wood',
    'Chen': 'Earth', 'Si': 'Fire', 'Wu': 'Fire', 'Wei': 'Earth',
    'Shen': 'Metal', 'You': 'Metal', 'Xu': 'Earth', 'Hai': 'Water'
}

# Hidden Stems (Joey Yap order: Main, Secondary, Residual)
HIDDEN_STEMS = {
    'Zi': ['Gui'],
    'Chou': ['Ji', 'Gui', 'Xin'],
    'Yin': ['Jia', 'Bing', 'Wu'],
    'Mao': ['Yi'],
    'Chen': ['Wu', 'Yi', 'Gui'],
    'Si': ['Bing', 'Wu', 'Geng'],
    'Wu': ['Ding', 'Ji'],
    'Wei': ['Ji', 'Ding', 'Yi'],
    'Shen': ['Geng', 'Ren', 'Wu'],
    'You': ['Xin'],
    'Xu': ['Wu', 'Xin', 'Ding'],
    'Hai': ['Ren', 'Jia'],
}

# Solar terms (Jie) that start each BaZi month
SOLAR_TERMS = {
    1: (2, 4),    # 立春 Li Chun
    2: (3, 6),    # 惊蛰 Jing Zhe
    3: (4, 5),    # 清明 Qing Ming
    4: (5, 6),    # 立夏 Li Xia
    5: (6, 6),    # 芒种 Mang Zhong
    6: (7, 7),    # 小暑 Xiao Shu
    7: (8, 8),    # 立秋 Li Qiu
    8: (9, 8),    # 白露 Bai Lu
    9: (10, 8),   # 寒露 Han Lu
    10: (11, 7),  # 立冬 Li Dong
    11: (12, 7),  # 大雪 Da Xue
    12: (1, 6),   # 小寒 Xiao Han
}

# Element cycles
PRODUCTIVE_CYCLE = {'Wood': 'Fire', 'Fire': 'Earth', 'Earth': 'Metal', 'Metal': 'Water', 'Water': 'Wood'}
PRODUCED_BY = {'Wood': 'Water', 'Fire': 'Wood', 'Earth': 'Fire', 'Metal': 'Earth', 'Water': 'Metal'}
CONTROLLING_CYCLE = {'Wood': 'Earth', 'Earth': 'Water', 'Water': 'Fire', 'Fire': 'Metal', 'Metal': 'Wood'}
CONTROLLED_BY = {'Wood': 'Metal', 'Fire': 'Water', 'Earth': 'Wood', 'Metal': 'Fire', 'Water': 'Earth'}

# Six Clashes
SIX_CLASHES = {
    'Zi': 'Wu', 'Wu': 'Zi', 'Chou': 'Wei', 'Wei': 'Chou',
    'Yin': 'Shen', 'Shen': 'Yin', 'Mao': 'You', 'You': 'Mao',
    'Chen': 'Xu', 'Xu': 'Chen', 'Si': 'Hai', 'Hai': 'Si'
}

# Six Combines
SIX_COMBINES = {
    'Zi': ('Chou', 'Earth'), 'Chou': ('Zi', 'Earth'),
    'Yin': ('Hai', 'Wood'), 'Hai': ('Yin', 'Wood'),
    'Mao': ('Xu', 'Fire'), 'Xu': ('Mao', 'Fire'),
    'Chen': ('You', 'Metal'), 'You': ('Chen', 'Metal'),
    'Si': ('Shen', 'Water'), 'Shen': ('Si', 'Water'),
    'Wu': ('Wei', 'Fire'), 'Wei': ('Wu', 'Fire')
}

# Seasonal strength
SEASONAL_STRENGTH = {
    'Yin': {'Wood': 1.0, 'Fire': 0.6, 'Earth': 0.1, 'Metal': 0.0, 'Water': 0.3},
    'Mao': {'Wood': 1.0, 'Fire': 0.6, 'Earth': 0.1, 'Metal': 0.0, 'Water': 0.3},
    'Chen': {'Wood': 0.8, 'Fire': 0.5, 'Earth': 0.4, 'Metal': 0.1, 'Water': 0.2},
    'Si': {'Fire': 1.0, 'Earth': 0.6, 'Metal': 0.1, 'Water': 0.0, 'Wood': 0.3},
    'Wu': {'Fire': 1.0, 'Earth': 0.6, 'Metal': 0.1, 'Water': 0.0, 'Wood': 0.3},
    'Wei': {'Fire': 0.8, 'Earth': 0.7, 'Metal': 0.2, 'Water': 0.1, 'Wood': 0.2},
    'Shen': {'Metal': 1.0, 'Water': 0.6, 'Wood': 0.1, 'Fire': 0.0, 'Earth': 0.3},
    'You': {'Metal': 1.0, 'Water': 0.6, 'Wood': 0.1, 'Fire': 0.0, 'Earth': 0.3},
    'Xu': {'Metal': 0.8, 'Water': 0.5, 'Wood': 0.1, 'Fire': 0.1, 'Earth': 0.5},
    'Hai': {'Water': 1.0, 'Wood': 0.6, 'Fire': 0.1, 'Earth': 0.0, 'Metal': 0.3},
    'Zi': {'Water': 1.0, 'Wood': 0.6, 'Fire': 0.1, 'Earth': 0.0, 'Metal': 0.3},
    'Chou': {'Water': 0.8, 'Wood': 0.4, 'Fire': 0.1, 'Earth': 0.5, 'Metal': 0.2},
}

# Ten Gods
TEN_GODS = {
    'same_yang': 'Friend', 'same_yin': 'Rob Wealth',
    'produce_yang': 'Eating God', 'produce_yin': 'Hurting Officer',
    'wealth_yang': 'Indirect Wealth', 'wealth_yin': 'Direct Wealth',
    'power_yang': 'Seven Killings', 'power_yin': 'Direct Officer',
    'resource_yang': 'Indirect Resource', 'resource_yin': 'Direct Resource'
}

PROFILE_NAMES = {
    'Friend': 'The Leader', 'Rob Wealth': 'The Competitor',
    'Eating God': 'The Artist', 'Hurting Officer': 'The Performer',
    'Indirect Wealth': 'The Pioneer', 'Direct Wealth': 'The Director',
    'Seven Killings': 'The Warrior', 'Direct Officer': 'The Diplomat',
    'Indirect Resource': 'The Analyzer', 'Direct Resource': 'The Philosopher'
}

ELEMENT_COLORS = {
    'Wood': '#228B22', 'Fire': '#DC143C', 'Earth': '#DAA520',
    'Metal': '#C0C0C0', 'Water': '#1E90FF'
}

# =============================================================================
# CALCULATION FUNCTIONS (Joey Yap Aligned)
# =============================================================================

def get_bazi_year(year: int, month: int, day: int) -> int:
    """Get BaZi year (changes at Li Chun ~Feb 4, not Jan 1)"""
    li_chun_month, li_chun_day = SOLAR_TERMS[1]
    if month < li_chun_month or (month == li_chun_month and day < li_chun_day):
        return year - 1
    return year

def get_bazi_month(year: int, month: int, day: int) -> int:
    """Determine BaZi month (1-12) based on solar terms - FIXED!"""
    for bazi_month in range(12, 0, -1):
        solar_month, solar_day = SOLAR_TERMS[bazi_month]
        if bazi_month == 12:
            if month == 1 and day >= solar_day:
                return 12
        else:
            if month > solar_month or (month == solar_month and day >= solar_day):
                return bazi_month
    return 11

def calc_year_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """Calculate Year Pillar"""
    bazi_year = get_bazi_year(year, month, day)
    stem_idx = (bazi_year - 4) % 10
    branch_idx = (bazi_year - 4) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calc_month_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """Calculate Month Pillar using solar terms - FIXED!"""
    bazi_month = get_bazi_month(year, month, day)
    month_branch = MONTH_BRANCHES[bazi_month - 1]
    
    year_stem, _ = calc_year_pillar(year, month, day)
    year_stem_idx = HEAVENLY_STEMS.index(year_stem)
    
    first_month_stem_idx = (year_stem_idx * 2 + 2) % 10
    month_stem_idx = (first_month_stem_idx + bazi_month - 1) % 10
    
    return HEAVENLY_STEMS[month_stem_idx], month_branch

def calc_day_pillar(birth_date: date) -> Tuple[str, str]:
    """Calculate Day Pillar - FIXED reference date!"""
    reference = date(1900, 1, 1)
    days_diff = (birth_date - reference).days
    stem_idx = days_diff % 10
    branch_idx = (days_diff + 10) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calc_hour_pillar(hour: int, day_stem: str) -> Tuple[str, str]:
    """Calculate Hour Pillar"""
    if hour == 23:
        branch_idx = 0
    else:
        branch_idx = ((hour + 1) // 2) % 12
    
    day_idx = HEAVENLY_STEMS.index(day_stem)
    zi_hour_stem_idx = (day_idx % 5) * 2
    hour_stem_idx = (zi_hour_stem_idx + branch_idx) % 10
    
    return HEAVENLY_STEMS[hour_stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_four_pillars(birth_date: date, birth_hour: int) -> Dict:
    """Calculate all Four Pillars with metadata"""
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    
    y_stem, y_branch = calc_year_pillar(year, month, day)
    m_stem, m_branch = calc_month_pillar(year, month, day)
    d_stem, d_branch = calc_day_pillar(birth_date)
    h_stem, h_branch = calc_hour_pillar(birth_hour, d_stem)
    
    def pillar_data(stem, branch, name):
        s_idx = HEAVENLY_STEMS.index(stem)
        b_idx = EARTHLY_BRANCHES.index(branch)
        return {
            'name': name,
            'stem': stem,
            'branch': branch,
            'stem_cn': HEAVENLY_STEMS_CN[s_idx],
            'branch_cn': EARTHLY_BRANCHES_CN[b_idx],
            'element': STEM_ELEMENTS[stem],
            'polarity': STEM_POLARITY[stem],
            'animal': BRANCH_ANIMALS[b_idx],
            'hidden_stems': HIDDEN_STEMS.get(branch, []),
            'branch_element': BRANCH_ELEMENTS[branch]
        }
    
    return {
        'year': pillar_data(y_stem, y_branch, 'Year'),
        'month': pillar_data(m_stem, m_branch, 'Month'),
        'day': pillar_data(d_stem, d_branch, 'Day'),
        'hour': pillar_data(h_stem, h_branch, 'Hour')
    }

def get_ten_god(day_master: str, other_stem: str) -> str:
    """Calculate 10 God relationship"""
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    other_element = STEM_ELEMENTS[other_stem]
    other_polarity = STEM_POLARITY[other_stem]
    
    same_polarity = (dm_polarity == other_polarity)
    
    if other_element == dm_element:
        return 'Friend' if same_polarity else 'Rob Wealth'
    if PRODUCTIVE_CYCLE[dm_element] == other_element:
        return 'Eating God' if same_polarity else 'Hurting Officer'
    if CONTROLLING_CYCLE[dm_element] == other_element:
        return 'Indirect Wealth' if same_polarity else 'Direct Wealth'
    if CONTROLLED_BY[dm_element] == other_element:
        return 'Seven Killings' if same_polarity else 'Direct Officer'
    if PRODUCED_BY[dm_element] == other_element:
        return 'Indirect Resource' if same_polarity else 'Direct Resource'
    return 'Unknown'

def calculate_dm_strength(pillars: Dict) -> Tuple[float, str]:
    """Calculate Day Master strength (weighted algorithm)"""
    day_master = pillars['day']['stem']
    dm_element = STEM_ELEMENTS[day_master]
    producing = PRODUCED_BY[dm_element]
    
    score = 0.0
    
    # 1. Seasonal (40%)
    month_branch = pillars['month']['branch']
    if month_branch in SEASONAL_STRENGTH:
        score += SEASONAL_STRENGTH[month_branch].get(dm_element, 0.0) * 0.40
    
    # 2. Hidden stems (30%)
    hidden_support = 0
    hidden_total = 0
    for p in pillars.values():
        for hidden in p['hidden_stems']:
            hidden_total += 1
            h_element = STEM_ELEMENTS[hidden]
            if h_element == dm_element:
                hidden_support += 1.0
            elif h_element == producing:
                hidden_support += 0.7
    if hidden_total > 0:
        score += (hidden_support / hidden_total) * 0.30
    
    # 3. Visible stems (20%)
    visible_support = 0
    visible_count = 0
    for name, p in pillars.items():
        if name == 'day':
            continue
        visible_count += 1
        s_element = STEM_ELEMENTS[p['stem']]
        if s_element == dm_element:
            visible_support += 1.0
        elif s_element == producing:
            visible_support += 0.7
    if visible_count > 0:
        score += (visible_support / visible_count) * 0.20
    
    # 4. Hour branch (10%)
    h_element = BRANCH_ELEMENTS[pillars['hour']['branch']]
    if h_element == dm_element:
        score += 0.10
    elif h_element == producing:
        score += 0.07
    
    pct = min(score * 100, 100)
    
    # Map to Joey Yap categories
    if pct <= 20:
        category = 'Very Weak'
    elif pct <= 40:
        category = 'Weak'
    elif pct <= 60:
        category = 'Neutral'
    elif pct <= 80:
        category = 'Strong'
    else:
        category = 'Very Strong'
    
    return round(pct, 1), category

def calculate_10_profiles(pillars: Dict) -> Dict[str, int]:
    """Calculate 10 Gods distribution"""
    dm = pillars['day']['stem']
    counts = {god: 0 for god in TEN_GODS.values()}
    
    for name, p in pillars.items():
        if name == 'day':
            continue
        god = get_ten_god(dm, p['stem'])
        counts[god] += 1
    
    for p in pillars.values():
        for hidden in p['hidden_stems']:
            god = get_ten_god(dm, hidden)
            counts[god] += 1
    
    return counts

def get_useful_gods(dm_element: str, strength: str) -> Dict:
    """Determine useful/unfavorable gods based on DM strength"""
    producing = PRODUCED_BY[dm_element]
    controls = CONTROLLING_CYCLE[dm_element]
    controlled_by = CONTROLLED_BY[dm_element]
    output = PRODUCTIVE_CYCLE[dm_element]
    
    if strength in ['Very Weak', 'Weak']:
        return {
            'useful': [dm_element, producing],
            'unfavorable': [controlled_by, output, controls],
            'explanation': f'As a {strength} {dm_element} Day Master, you need strengthening from {dm_element} (same element) and {producing} (resource).'
        }
    elif strength == 'Neutral':
        return {
            'useful': [dm_element, producing, controls],
            'unfavorable': [controlled_by],
            'explanation': f'As a Neutral {dm_element} Day Master, you can handle most elements. Focus on {controls} for wealth opportunities.'
        }
    else:
        return {
            'useful': [controlled_by, output, controls],
            'unfavorable': [dm_element, producing],
            'explanation': f'As a {strength} {dm_element} Day Master, you need draining through {output} (output) and {controls} (wealth).'
        }

def calculate_luck_pillars(pillars: Dict, birth_date: date, gender: str, num: int = 8) -> List[Dict]:
    """Calculate Luck Pillars using Joey Yap method"""
    year_polarity = STEM_POLARITY[pillars['year']['stem']]
    month_stem = pillars['month']['stem']
    month_branch = pillars['month']['branch']
    
    is_forward = (
        (gender.lower() == 'male' and year_polarity == 'Yang') or
        (gender.lower() == 'female' and year_polarity == 'Yin')
    )
    
    # Calculate start age (days to solar term / 3)
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    current_bazi_month = get_bazi_month(year, month, day)
    
    if is_forward:
        next_bazi_month = (current_bazi_month % 12) + 1
        next_solar_month, next_solar_day = SOLAR_TERMS[next_bazi_month]
        if next_solar_month < month or (next_solar_month == 1 and month >= 11):
            target_year = year + 1
        else:
            target_year = year
        target_date = date(target_year, next_solar_month, next_solar_day)
    else:
        curr_solar_month, curr_solar_day = SOLAR_TERMS[current_bazi_month]
        target_date = date(year, curr_solar_month, curr_solar_day)
        if target_date > birth_date:
            prev_bazi_month = ((current_bazi_month - 2) % 12) + 1
            prev_solar_month, prev_solar_day = SOLAR_TERMS[prev_bazi_month]
            target_year = year - 1 if prev_solar_month > month else year
            target_date = date(target_year, prev_solar_month, prev_solar_day)
    
    days_diff = abs((target_date - birth_date).days)
    start_age = round(days_diff / 3)
    
    # Generate luck pillars
    stem_idx = HEAVENLY_STEMS.index(month_stem)
    branch_idx = EARTHLY_BRANCHES.index(month_branch)
    
    lp_list = []
    current_age = start_age
    
    for i in range(num):
        if is_forward:
            new_stem_idx = (stem_idx + i + 1) % 10
            new_branch_idx = (branch_idx + i + 1) % 12
        else:
            new_stem_idx = (stem_idx - i - 1) % 10
            new_branch_idx = (branch_idx - i - 1) % 12
        
        lp_stem = HEAVENLY_STEMS[new_stem_idx]
        lp_branch = EARTHLY_BRANCHES[new_branch_idx]
        
        lp_list.append({
            'stem': lp_stem,
            'branch': lp_branch,
            'stem_cn': HEAVENLY_STEMS_CN[new_stem_idx],
            'branch_cn': EARTHLY_BRANCHES_CN[new_branch_idx],
            'animal': BRANCH_ANIMALS[new_branch_idx],
            'element': STEM_ELEMENTS[lp_stem],
            'start_age': current_age,
            'end_age': current_age + 9,
            'age_range': f"{current_age}-{current_age + 9}"
        })
        current_age += 10
    
    return lp_list

def detect_clashes(pillars: Dict) -> List[Dict]:
    """Detect Six Clashes between pillars"""
    clashes = []
    names = list(pillars.keys())
    
    for i, n1 in enumerate(names):
        for n2 in names[i+1:]:
            b1 = pillars[n1]['branch']
            b2 = pillars[n2]['branch']
            if SIX_CLASHES.get(b1) == b2:
                clashes.append({
                    'pillars': f"{n1.title()} ↔ {n2.title()}",
                    'animals': f"{pillars[n1]['animal']} vs {pillars[n2]['animal']}"
                })
    return clashes

def detect_combines(pillars: Dict) -> List[Dict]:
    """Detect Six Combines between pillars"""
    combines = []
    names = list(pillars.keys())
    
    for i, n1 in enumerate(names):
        for n2 in names[i+1:]:
            b1 = pillars[n1]['branch']
            b2 = pillars[n2]['branch']
            info = SIX_COMBINES.get(b1)
            if info and info[0] == b2:
                combines.append({
                    'pillars': f"{n1.title()} + {n2.title()}",
                    'animals': f"{pillars[n1]['animal']} + {pillars[n2]['animal']}",
                    'result': info[1]
                })
    return combines

# =============================================================================
# STREAMLIT UI
# =============================================================================

def main():
    st.set_page_config(page_title="BaZi Pro", page_icon="🎋", layout="wide")
    
    st.title("🎋 BaZi Pro Analysis")
    st.caption("Joey Yap Aligned Calculations • v10.6")
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        birth_date = st.date_input(
            "Birth Date",
            value=date(1978, 6, 27),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
    
    with col2:
        birth_hour = st.selectbox(
            "Birth Hour",
            options=list(range(24)),
            index=20,
            format_func=lambda x: f"{x:02d}:00 - {x:02d}:59"
        )
    
    with col3:
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    
    if st.button("🔮 Calculate BaZi", type="primary", use_container_width=True):
        # Calculate
        pillars = calculate_four_pillars(birth_date, birth_hour)
        dm_pct, dm_category = calculate_dm_strength(pillars)
        profiles = calculate_10_profiles(pillars)
        useful = get_useful_gods(pillars['day']['element'], dm_category)
        luck_pillars = calculate_luck_pillars(pillars, birth_date, gender)
        clashes = detect_clashes(pillars)
        combines = detect_combines(pillars)
        
        # Store in session
        st.session_state.bazi_data = {
            'pillars': pillars,
            'dm_strength': dm_pct,
            'dm_category': dm_category,
            'profiles': profiles,
            'useful_gods': useful,
            'luck_pillars': luck_pillars
        }
        
        # Display
        st.markdown("---")
        
        # Four Pillars Display
        st.subheader("📋 Four Pillars of Destiny")
        
        cols = st.columns(4)
        for i, (name, p) in enumerate(pillars.items()):
            with cols[i]:
                color = ELEMENT_COLORS.get(p['element'], '#888888')
                st.markdown(f"""
                <div style='text-align: center; padding: 15px; border: 2px solid {color}; border-radius: 10px;'>
                    <div style='font-size: 14px; color: #888;'>{name.upper()}</div>
                    <div style='font-size: 28px; font-weight: bold;'>{p['stem_cn']}</div>
                    <div style='font-size: 12px;'>{p['stem']} ({p['element']})</div>
                    <hr style='margin: 5px 0;'>
                    <div style='font-size: 28px;'>{p['branch_cn']}</div>
                    <div style='font-size: 12px;'>{p['branch']} ({p['animal']})</div>
                    <div style='font-size: 10px; color: #666;'>Hidden: {', '.join(p['hidden_stems'])}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Day Master Analysis
        st.markdown("---")
        st.subheader("⚔️ Day Master Analysis")
        
        dm = pillars['day']
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Day Master:** {dm['stem']} {dm['stem_cn']} ({dm['polarity']} {dm['element']})
            
            **Strength:** {dm_pct}% ({dm_category})
            """)
            st.progress(dm_pct / 100)
        
        with col2:
            st.markdown(f"""
            **Useful Elements:** {', '.join(useful['useful'])}
            
            **Unfavorable Elements:** {', '.join(useful['unfavorable'])}
            """)
            st.info(useful['explanation'])
        
        # 10 Profiles
        st.markdown("---")
        st.subheader("👤 Ten Profiles Distribution")
        
        # Find dominant
        dominant = max(profiles, key=profiles.get)
        profile_name = PROFILE_NAMES.get(dominant, dominant)
        
        st.success(f"**Dominant Profile:** {dominant} → {profile_name}")
        
        # Bar chart
        import pandas as pd
        df = pd.DataFrame([
            {'Profile': k, 'Count': v} for k, v in sorted(profiles.items(), key=lambda x: -x[1])
        ])
        st.bar_chart(df.set_index('Profile'))
        
        # Luck Pillars
        st.markdown("---")
        st.subheader("🔄 Luck Pillars (10-Year Cycles)")
        
        direction = "Forward" if (
            (gender.lower() == 'male' and STEM_POLARITY[pillars['year']['stem']] == 'Yang') or
            (gender.lower() == 'female' and STEM_POLARITY[pillars['year']['stem']] == 'Yin')
        ) else "Reverse"
        
        st.caption(f"Direction: {direction} | Start Age: {luck_pillars[0]['start_age']}")
        
        lp_cols = st.columns(len(luck_pillars))
        for i, lp in enumerate(luck_pillars):
            with lp_cols[i]:
                color = ELEMENT_COLORS.get(lp['element'], '#888')
                st.markdown(f"""
                <div style='text-align: center; padding: 8px; border: 1px solid {color}; border-radius: 5px; font-size: 12px;'>
                    <div style='font-weight: bold;'>{lp['age_range']}</div>
                    <div style='font-size: 20px;'>{lp['stem_cn']}{lp['branch_cn']}</div>
                    <div>{lp['animal']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Interactions
        if clashes or combines:
            st.markdown("---")
            st.subheader("⚡ Pillar Interactions")
            
            col1, col2 = st.columns(2)
            with col1:
                if clashes:
                    st.warning("**Clashes:**")
                    for c in clashes:
                        st.write(f"• {c['animals']}")
            with col2:
                if combines:
                    st.success("**Combines:**")
                    for c in combines:
                        st.write(f"• {c['animals']} → {c['result']}")
        
        # Summary
        st.markdown("---")
        st.subheader("📊 Summary")
        
        with st.expander("Full Analysis Data (JSON)", expanded=False):
            st.json({
                'birth_info': {
                    'date': birth_date.isoformat(),
                    'hour': birth_hour,
                    'gender': gender
                },
                'four_pillars': pillars,
                'day_master': {
                    'stem': dm['stem'],
                    'element': dm['element'],
                    'strength_pct': dm_pct,
                    'strength_category': dm_category
                },
                'useful_gods': useful,
                'profiles': profiles,
                'dominant_profile': f"{dominant} ({profile_name})",
                'luck_pillars': luck_pillars,
                'clashes': clashes,
                'combines': combines
            })

if __name__ == "__main__":
    main()
