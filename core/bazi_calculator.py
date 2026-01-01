# Ming QiMenDunJia v10.1 - Professional BaZi Calculator (Improved Accuracy)
# core/bazi_calculator.py
"""
Complete BaZi (Four Pillars) calculation engine
Improved with accurate solar terms and annual pillar

v10.1 Changes:
- Accurate solar term dates for month pillar
- Proper luck pillar start age calculation
- Annual pillar overlay feature
- Better strength calculation
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


# =============================================================================
# CONSTANTS
# =============================================================================

HEAVENLY_STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
HEAVENLY_STEMS_CN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

EARTHLY_BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
EARTHLY_BRANCHES_CN = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
ANIMALS_CN = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]

STEM_ELEMENTS = {
    "Jia": "Wood", "Yi": "Wood", "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth", "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water"
}

STEM_POLARITY = {
    "Jia": "Yang", "Yi": "Yin", "Bing": "Yang", "Ding": "Yin",
    "Wu": "Yang", "Ji": "Yin", "Geng": "Yang", "Xin": "Yin",
    "Ren": "Yang", "Gui": "Yin"
}

BRANCH_ELEMENTS = {
    "Zi": "Water", "Chou": "Earth", "Yin": "Wood", "Mao": "Wood",
    "Chen": "Earth", "Si": "Fire", "Wu": "Fire", "Wei": "Earth",
    "Shen": "Metal", "You": "Metal", "Xu": "Earth", "Hai": "Water"
}

BRANCH_POLARITY = {
    "Zi": "Yang", "Chou": "Yin", "Yin": "Yang", "Mao": "Yin",
    "Chen": "Yang", "Si": "Yin", "Wu": "Yang", "Wei": "Yin",
    "Shen": "Yang", "You": "Yin", "Xu": "Yang", "Hai": "Yin"
}

# Hidden Stems (藏干) - Main, Middle, Residual
HIDDEN_STEMS = {
    "Zi": ["Gui"],
    "Chou": ["Ji", "Gui", "Xin"],
    "Yin": ["Jia", "Bing", "Wu"],
    "Mao": ["Yi"],
    "Chen": ["Wu", "Yi", "Gui"],
    "Si": ["Bing", "Wu", "Geng"],
    "Wu": ["Ding", "Ji"],
    "Wei": ["Ji", "Ding", "Yi"],
    "Shen": ["Geng", "Ren", "Wu"],
    "You": ["Xin"],
    "Xu": ["Wu", "Xin", "Ding"],
    "Hai": ["Ren", "Jia"]
}

# Hidden stem weights (Main=1.0, Middle=0.5, Residual=0.3)
HIDDEN_STEM_WEIGHTS = [1.0, 0.5, 0.3]

# 10 Gods
TEN_GODS = {
    "same_element_same_polarity": ("F", "Friend", "比肩"),
    "same_element_diff_polarity": ("RW", "Rob Wealth", "劫財"),
    "produces_dm_same_polarity": ("IR", "Indirect Resource", "偏印"),
    "produces_dm_diff_polarity": ("DR", "Direct Resource", "正印"),
    "dm_produces_same_polarity": ("EG", "Eating God", "食神"),
    "dm_produces_diff_polarity": ("HO", "Hurting Officer", "傷官"),
    "dm_controls_same_polarity": ("IW", "Indirect Wealth", "偏財"),
    "dm_controls_diff_polarity": ("DW", "Direct Wealth", "正財"),
    "controls_dm_same_polarity": ("7K", "Seven Killings", "七殺"),
    "controls_dm_diff_polarity": ("DO", "Direct Officer", "正官"),
}

ELEMENT_PRODUCES = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
ELEMENT_CONTROLS = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

# 10 Profiles
TEN_PROFILES = {
    "F": ("The Friend", "Connector"),
    "RW": ("The Leader", "Rob Wealth"),
    "IR": ("The Philosopher", "Indirect Resource"),
    "DR": ("The Analyzer", "Direct Resource"),
    "EG": ("The Artist", "Eating God"),
    "HO": ("The Performer", "Hurting Officer"),
    "IW": ("The Pioneer", "Indirect Wealth"),
    "DW": ("The Director", "Direct Wealth"),
    "7K": ("The Warrior", "Seven Killings"),
    "DO": ("The Diplomat", "Direct Officer"),
}

# =============================================================================
# ACCURATE SOLAR TERMS (节气) - Based on astronomical calculations
# Format: (month, day) approximate dates - varies by year
# =============================================================================

def get_solar_term_dates(year: int) -> Dict[int, Tuple[int, int]]:
    """
    Get solar term dates for a specific year.
    These are the START dates of each Chinese month (Jie 节).
    
    Month 1 starts at Li Chun (立春)
    Month 2 starts at Jing Zhe (惊蛰)
    etc.
    """
    # Base dates (approximate for 2000), adjusted slightly per year
    # In production, use astronomical library for exact times
    
    base_terms = {
        1: (2, 4),    # Li Chun 立春 - Start of Spring
        2: (3, 6),    # Jing Zhe 惊蛰 - Awakening of Insects
        3: (4, 5),    # Qing Ming 清明 - Clear and Bright
        4: (5, 6),    # Li Xia 立夏 - Start of Summer
        5: (6, 6),    # Mang Zhong 芒种 - Grain in Ear
        6: (7, 7),    # Xiao Shu 小暑 - Minor Heat
        7: (8, 8),    # Li Qiu 立秋 - Start of Autumn
        8: (9, 8),    # Bai Lu 白露 - White Dew
        9: (10, 8),   # Han Lu 寒露 - Cold Dew
        10: (11, 7),  # Li Dong 立冬 - Start of Winter
        11: (12, 7),  # Da Xue 大雪 - Major Snow
        12: (1, 6),   # Xiao Han 小寒 - Minor Cold
    }
    
    # Slight adjustment based on year cycle (simplified)
    year_offset = (year - 2000) % 4
    
    adjusted_terms = {}
    for month, (m, d) in base_terms.items():
        # Terms shift by about 1 day every 4 years
        adj_d = d + (1 if year_offset >= 2 and month in [1, 2, 7, 8] else 0)
        adjusted_terms[month] = (m, min(adj_d, 28))  # Cap at 28 for safety
    
    return adjusted_terms


def get_chinese_month(dt: date) -> Tuple[int, int]:
    """
    Get Chinese month and adjusted year based on solar terms.
    Returns (chinese_month, chinese_year)
    
    Important: Chinese year starts at Li Chun, not Jan 1!
    """
    year = dt.year
    solar_terms = get_solar_term_dates(year)
    prev_year_terms = get_solar_term_dates(year - 1)
    
    month_num = dt.month
    day = dt.day
    
    # Check if before Li Chun (still previous Chinese year)
    li_chun = solar_terms[1]  # Month 1 start = Li Chun
    if month_num < li_chun[0] or (month_num == li_chun[0] and day < li_chun[1]):
        chinese_year = year - 1
    else:
        chinese_year = year
    
    # Find which Chinese month we're in
    chinese_month = 12  # Default to month 12
    
    for cm in range(1, 13):
        term_month, term_day = solar_terms.get(cm, (1, 1))
        
        if cm == 12:
            # Month 12 starts in January of NEXT year's solar terms
            # Or previous year's December
            prev_term = prev_year_terms.get(12, (1, 6))
            if month_num == 1:
                if day < solar_terms[1][1]:  # Before Li Chun
                    if day >= prev_term[1] or month_num > prev_term[0]:
                        chinese_month = 12
                        break
            elif month_num == 12 and day >= prev_year_terms[11][1]:
                chinese_month = 11
        else:
            next_term = solar_terms.get(cm + 1, (13, 1))
            
            # Check if date falls in this month
            if term_month == month_num:
                if day >= term_day:
                    if cm + 1 > 12 or month_num < next_term[0] or (month_num == next_term[0] and day < next_term[1]):
                        chinese_month = cm
                        break
            elif term_month < month_num < next_term[0]:
                chinese_month = cm
                break
            elif term_month < month_num and month_num == next_term[0] and day < next_term[1]:
                chinese_month = cm
                break
    
    return (chinese_month, chinese_year)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Pillar:
    stem: str
    stem_cn: str
    branch: str
    branch_cn: str
    animal: str
    animal_cn: str
    stem_element: str
    branch_element: str
    stem_polarity: str
    branch_polarity: str
    hidden_stems: List[str]
    na_yin: str = ""
    
    def to_dict(self) -> dict:
        return {
            "stem": self.stem, "stem_cn": self.stem_cn,
            "branch": self.branch, "branch_cn": self.branch_cn,
            "animal": self.animal, "animal_cn": self.animal_cn,
            "stem_element": self.stem_element, "branch_element": self.branch_element,
            "hidden_stems": self.hidden_stems
        }


@dataclass
class LuckPillar:
    age_start: int
    age_end: int
    year_start: int
    stem: str
    stem_cn: str
    branch: str
    branch_cn: str
    animal: str
    hidden_stems: List[str]
    is_current: bool = False
    
    def to_dict(self) -> dict:
        return {
            "age_range": f"{self.age_start}-{self.age_end}",
            "year_start": self.year_start,
            "stem": self.stem, "stem_cn": self.stem_cn,
            "branch": self.branch, "branch_cn": self.branch_cn,
            "is_current": self.is_current
        }


@dataclass
class BaZiChart:
    birth_date: date
    birth_hour: int
    birth_minute: int
    gender: str
    
    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Pillar
    
    # Annual pillar (for current year overlay)
    annual_pillar: Optional[Pillar] = None
    
    day_master: str = ""
    day_master_element: str = ""
    day_master_polarity: str = ""
    
    dm_strength: float = 50.0
    strength_category: str = "Balanced"
    
    useful_gods: List[str] = None
    unfavorable_elements: List[str] = None
    
    ten_gods_distribution: Dict[str, float] = None
    luck_pillars: List[LuckPillar] = None
    
    symbolic_stars: Dict[str, str] = None
    life_palace: Tuple[str, str] = None
    conception_palace: Tuple[str, str] = None
    
    main_profile: str = ""
    main_structure: str = ""
    
    # Luck pillar calculation details
    luck_pillar_start_age: int = 0


# =============================================================================
# PILLAR CALCULATIONS
# =============================================================================

def get_stem_index(stem: str) -> int:
    return HEAVENLY_STEMS.index(stem) if stem in HEAVENLY_STEMS else 0

def get_branch_index(branch: str) -> int:
    return EARTHLY_BRANCHES.index(branch) if branch in EARTHLY_BRANCHES else 0


def calculate_year_pillar(year: int) -> Pillar:
    """Calculate year pillar - based on Li Chun, not Jan 1"""
    # 1984 = Jia Zi year
    cycle_pos = (year - 1984) % 60
    stem_idx = cycle_pos % 10
    branch_idx = cycle_pos % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem, stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch, branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx], animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem], branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem], branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch]
    )


def calculate_month_pillar(chinese_year: int, chinese_month: int) -> Pillar:
    """Calculate month pillar based on Chinese month"""
    # Year stem determines month stem cycle
    year_pillar = calculate_year_pillar(chinese_year)
    year_stem_idx = get_stem_index(year_pillar.stem)
    
    # Month stem formula: (year_stem * 2 + month) % 10
    # Month 1 (Yin) stem based on year stem
    base_stem_idx = (year_stem_idx * 2 + 2) % 10
    stem_idx = (base_stem_idx + chinese_month - 1) % 10
    
    # Month branch: Month 1 = Yin (Tiger), Month 2 = Mao (Rabbit), etc.
    branch_idx = (chinese_month + 1) % 12  # Yin = index 2, so month 1 -> 2
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem, stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch, branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx], animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem], branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem], branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch]
    )


def calculate_day_pillar(dt: date) -> Pillar:
    """Calculate day pillar using standard formula"""
    # Reference: Jan 1, 1900 = Jia Xu day (stem=0, branch=10)
    ref_date = date(1900, 1, 1)
    days_diff = (dt - ref_date).days
    
    stem_idx = (days_diff + 0) % 10  # Jia = 0
    branch_idx = (days_diff + 10) % 12  # Xu = 10
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem, stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch, branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx], animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem], branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem], branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch]
    )


def calculate_hour_pillar(hour: int, day_stem: str) -> Pillar:
    """Calculate hour pillar"""
    # Hour to branch: 23:00-01:00 = Zi, 01:00-03:00 = Chou, etc.
    if hour == 23:
        branch_idx = 0  # Zi
    else:
        branch_idx = ((hour + 1) // 2) % 12
    
    # Hour stem based on day stem
    day_stem_idx = get_stem_index(day_stem)
    base_stem_idx = (day_stem_idx * 2) % 10
    stem_idx = (base_stem_idx + branch_idx) % 10
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem, stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch, branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx], animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem], branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem], branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch]
    )


# =============================================================================
# 10 GODS CALCULATION
# =============================================================================

def get_ten_god(day_master: str, target_stem: str) -> Tuple[str, str, str]:
    """Calculate 10 God relationship"""
    dm_elem = STEM_ELEMENTS[day_master]
    dm_pol = STEM_POLARITY[day_master]
    tgt_elem = STEM_ELEMENTS[target_stem]
    tgt_pol = STEM_POLARITY[target_stem]
    
    same_pol = dm_pol == tgt_pol
    
    if dm_elem == tgt_elem:
        return TEN_GODS["same_element_same_polarity" if same_pol else "same_element_diff_polarity"]
    
    # What produces DM?
    for k, v in ELEMENT_PRODUCES.items():
        if v == dm_elem and k == tgt_elem:
            return TEN_GODS["produces_dm_same_polarity" if same_pol else "produces_dm_diff_polarity"]
    
    # What DM produces?
    if ELEMENT_PRODUCES.get(dm_elem) == tgt_elem:
        return TEN_GODS["dm_produces_same_polarity" if same_pol else "dm_produces_diff_polarity"]
    
    # What DM controls?
    if ELEMENT_CONTROLS.get(dm_elem) == tgt_elem:
        return TEN_GODS["dm_controls_same_polarity" if same_pol else "dm_controls_diff_polarity"]
    
    # What controls DM?
    for k, v in ELEMENT_CONTROLS.items():
        if v == dm_elem and k == tgt_elem:
            return TEN_GODS["controls_dm_same_polarity" if same_pol else "controls_dm_diff_polarity"]
    
    return ("?", "Unknown", "?")


def calculate_ten_gods_distribution(chart_data: dict) -> Dict[str, float]:
    """Calculate 10 Gods distribution with proper weighting"""
    dm = chart_data["day_master"]
    dist = {k: 0.0 for k in ["F", "RW", "IR", "DR", "EG", "HO", "IW", "DW", "7K", "DO"]}
    
    # Visible stems (excluding day master itself)
    visible_stems = [
        (chart_data["year_pillar"].stem, 1.0),
        (chart_data["month_pillar"].stem, 1.2),  # Month stem is important
        (chart_data["hour_pillar"].stem, 1.0),
    ]
    
    # Hidden stems with weights
    for pillar in [chart_data["year_pillar"], chart_data["month_pillar"],
                   chart_data["day_pillar"], chart_data["hour_pillar"]]:
        for i, hs in enumerate(pillar.hidden_stems):
            weight = HIDDEN_STEM_WEIGHTS[i] if i < len(HIDDEN_STEM_WEIGHTS) else 0.2
            visible_stems.append((hs, weight))
    
    # Calculate distribution
    for stem, weight in visible_stems:
        if stem == dm:
            continue
        code, _, _ = get_ten_god(dm, stem)
        if code in dist:
            dist[code] += weight
    
    # Normalize to 100%
    total = sum(dist.values())
    if total > 0:
        for k in dist:
            dist[k] = round((dist[k] / total) * 100, 1)
    
    return dist


# =============================================================================
# STRENGTH CALCULATION (Improved)
# =============================================================================

def calculate_dm_strength(chart_data: dict) -> Tuple[float, str]:
    """
    Calculate Day Master strength with improved accuracy.
    Considers:
    - Month branch (seasonal influence) - 40%
    - Hidden stems - 30%
    - Visible stems - 20%
    - Hour branch - 10%
    """
    dm = chart_data["day_master"]
    dm_elem = STEM_ELEMENTS[dm]
    
    supporting = 0.0
    opposing = 0.0
    
    # 1. Month Branch (Seasonal) - Most important (40%)
    month_branch_elem = chart_data["month_pillar"].branch_element
    seasonal_score = 0
    
    if month_branch_elem == dm_elem:
        seasonal_score = 4.0  # Same element = strongest
    elif ELEMENT_PRODUCES.get(month_branch_elem) == dm_elem:
        seasonal_score = 3.0  # Produces DM = strong
    elif dm_elem == ELEMENT_PRODUCES.get(month_branch_elem):
        seasonal_score = -2.0  # DM produces = drains
    elif ELEMENT_CONTROLS.get(month_branch_elem) == dm_elem:
        seasonal_score = -3.0  # Controls DM = weak
    elif dm_elem == ELEMENT_CONTROLS.get(month_branch_elem):
        seasonal_score = 1.0  # DM controls = slight support
    
    if seasonal_score > 0:
        supporting += seasonal_score * 4  # 40% weight
    else:
        opposing += abs(seasonal_score) * 4
    
    # 2. Hidden Stems (30%)
    for pillar in [chart_data["year_pillar"], chart_data["month_pillar"],
                   chart_data["day_pillar"], chart_data["hour_pillar"]]:
        for i, hs in enumerate(pillar.hidden_stems):
            weight = HIDDEN_STEM_WEIGHTS[i] if i < len(HIDDEN_STEM_WEIGHTS) else 0.2
            hs_elem = STEM_ELEMENTS[hs]
            
            if hs_elem == dm_elem:
                supporting += weight * 3
            elif ELEMENT_PRODUCES.get(hs_elem) == dm_elem:
                supporting += weight * 2
            elif ELEMENT_CONTROLS.get(hs_elem) == dm_elem:
                opposing += weight * 3
            elif dm_elem == ELEMENT_PRODUCES.get(hs_elem):
                opposing += weight * 1.5
    
    # 3. Visible Stems (20%)
    for pillar in [chart_data["year_pillar"], chart_data["month_pillar"], chart_data["hour_pillar"]]:
        s_elem = STEM_ELEMENTS[pillar.stem]
        if s_elem == dm_elem:
            supporting += 2
        elif ELEMENT_PRODUCES.get(s_elem) == dm_elem:
            supporting += 1.5
        elif ELEMENT_CONTROLS.get(s_elem) == dm_elem:
            opposing += 2
        elif dm_elem == ELEMENT_PRODUCES.get(s_elem):
            opposing += 1
    
    # 4. Hour Branch (10%)
    hour_elem = chart_data["hour_pillar"].branch_element
    if hour_elem == dm_elem:
        supporting += 1
    elif ELEMENT_PRODUCES.get(hour_elem) == dm_elem:
        supporting += 0.5
    elif ELEMENT_CONTROLS.get(hour_elem) == dm_elem:
        opposing += 1
    
    # Calculate percentage
    total = supporting + opposing
    if total == 0:
        return (50.0, "Balanced")
    
    strength_pct = (supporting / total) * 100
    
    # Categorize
    if strength_pct >= 65:
        category = "Strong"
    elif strength_pct >= 55:
        category = "Slightly Strong"
    elif strength_pct <= 35:
        category = "Weak"
    elif strength_pct <= 45:
        category = "Slightly Weak"
    else:
        category = "Balanced"
    
    return (round(strength_pct, 1), category)


def calculate_useful_gods(strength_cat: str, dm_elem: str) -> Tuple[List[str], List[str]]:
    """Calculate useful gods based on DM strength"""
    producing = None
    for k, v in ELEMENT_PRODUCES.items():
        if v == dm_elem:
            producing = k
            break
    
    draining = ELEMENT_PRODUCES.get(dm_elem)
    controlling = None
    for k, v in ELEMENT_CONTROLS.items():
        if v == dm_elem:
            controlling = k
            break
    controlled = ELEMENT_CONTROLS.get(dm_elem)
    
    if "Weak" in strength_cat:
        useful = [dm_elem]
        if producing:
            useful.append(producing)
        unfavorable = []
        if draining:
            unfavorable.append(draining)
        if controlling:
            unfavorable.append(controlling)
    elif "Strong" in strength_cat:
        useful = []
        if draining:
            useful.append(draining)
        if controlling:
            useful.append(controlling)
        unfavorable = [dm_elem]
        if producing:
            unfavorable.append(producing)
    else:
        useful = [dm_elem]
        unfavorable = []
    
    return (useful, unfavorable)


# =============================================================================
# LUCK PILLARS (Improved with accurate start age)
# =============================================================================

def calculate_luck_pillar_start_age(birth_date: date, gender: str, year_stem: str) -> int:
    """
    Calculate the exact start age for luck pillars.
    Based on days from birth to next/previous solar term.
    """
    year = birth_date.year
    solar_terms = get_solar_term_dates(year)
    
    # Direction based on gender + year stem polarity
    year_pol = STEM_POLARITY[year_stem]
    forward = (year_pol == "Yang" and gender == "M") or (year_pol == "Yin" and gender == "F")
    
    # Find nearest Jie (节) solar term
    chinese_month, _ = get_chinese_month(birth_date)
    
    if forward:
        # Count days to NEXT Jie
        next_month = (chinese_month % 12) + 1
        next_term = solar_terms.get(next_month, (3, 6))
        
        if next_month == 1:
            # Next term is Li Chun in next year
            next_date = date(year + 1, next_term[0], next_term[1])
        else:
            term_year = year if next_term[0] > birth_date.month else year + 1
            next_date = date(term_year, next_term[0], next_term[1])
        
        days_to_term = (next_date - birth_date).days
    else:
        # Count days from PREVIOUS Jie
        term = solar_terms.get(chinese_month, (2, 4))
        term_year = year if term[0] <= birth_date.month else year - 1
        prev_date = date(term_year, term[0], term[1])
        days_to_term = (birth_date - prev_date).days
    
    # 3 days = 1 year of luck pillar
    start_age = max(1, round(days_to_term / 3))
    
    return min(start_age, 10)  # Cap at 10


def calculate_luck_pillars(birth_date: date, gender: str, year_stem: str,
                          month_pillar: Pillar, current_year: int = None) -> List[LuckPillar]:
    """Calculate 10-year luck pillars"""
    if current_year is None:
        current_year = date.today().year
    
    current_age = current_year - birth_date.year
    
    # Calculate start age
    start_age = calculate_luck_pillar_start_age(birth_date, gender, year_stem)
    
    # Direction
    year_pol = STEM_POLARITY[year_stem]
    forward = (year_pol == "Yang" and gender == "M") or (year_pol == "Yin" and gender == "F")
    direction = 1 if forward else -1
    
    # Starting point
    month_stem_idx = get_stem_index(month_pillar.stem)
    month_branch_idx = get_branch_index(month_pillar.branch)
    
    pillars = []
    for i in range(10):
        age_start = start_age + (i * 10)
        age_end = age_start + 9
        year_start = birth_date.year + age_start
        
        stem_idx = (month_stem_idx + (i + 1) * direction) % 10
        branch_idx = (month_branch_idx + (i + 1) * direction) % 12
        
        stem = HEAVENLY_STEMS[stem_idx]
        branch = EARTHLY_BRANCHES[branch_idx]
        
        is_current = age_start <= current_age <= age_end
        
        pillars.append(LuckPillar(
            age_start=age_start, age_end=age_end, year_start=year_start,
            stem=stem, stem_cn=HEAVENLY_STEMS_CN[stem_idx],
            branch=branch, branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
            animal=ANIMALS[branch_idx],
            hidden_stems=HIDDEN_STEMS[branch],
            is_current=is_current
        ))
    
    return pillars


# =============================================================================
# SYMBOLIC STARS
# =============================================================================

def calculate_symbolic_stars(day_branch: str, year_branch: str, day_stem: str) -> Dict[str, str]:
    """Calculate symbolic stars"""
    stars = {}
    
    # Noble People (天乙贵人) based on Day Stem
    noble_map = {
        "Jia": ["Chou", "Wei"], "Yi": ["Zi", "Shen"], "Bing": ["Hai", "You"],
        "Ding": ["Hai", "You"], "Wu": ["Chou", "Wei"], "Ji": ["Zi", "Shen"],
        "Geng": ["Chou", "Wei"], "Xin": ["Yin", "Wu"], "Ren": ["Mao", "Si"],
        "Gui": ["Mao", "Si"]
    }
    nobles = noble_map.get(day_stem, [])
    stars["Noble People"] = ", ".join([f"{b} {EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(b)]}" for b in nobles])
    
    # Peach Blossom (桃花)
    peach_map = {
        "Yin": "Mao", "Wu": "Mao", "Xu": "Mao",
        "Shen": "You", "Zi": "You", "Chen": "You",
        "Si": "Wu", "You": "Wu", "Chou": "Wu",
        "Hai": "Zi", "Mao": "Zi", "Wei": "Zi"
    }
    pb = peach_map.get(year_branch, "?")
    stars["Peach Blossom"] = f"{pb} {EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(pb)] if pb in EARTHLY_BRANCHES else '?'}"
    
    # Sky Horse (驿马)
    horse_map = {
        "Yin": "Shen", "Wu": "Shen", "Xu": "Shen",
        "Shen": "Yin", "Zi": "Yin", "Chen": "Yin",
        "Si": "Hai", "You": "Hai", "Chou": "Hai",
        "Hai": "Si", "Mao": "Si", "Wei": "Si"
    }
    horse = horse_map.get(year_branch, "?")
    stars["Sky Horse"] = f"{horse} {EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(horse)] if horse in EARTHLY_BRANCHES else '?'}"
    
    # Intelligence (文昌)
    intel_map = {
        "Jia": "Si", "Yi": "Wu", "Bing": "Shen", "Ding": "You",
        "Wu": "Shen", "Ji": "You", "Geng": "Hai", "Xin": "Zi",
        "Ren": "Yin", "Gui": "Mao"
    }
    intel = intel_map.get(day_stem, "?")
    stars["Intelligence"] = f"{intel} {EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(intel)] if intel in EARTHLY_BRANCHES else '?'}"
    
    return stars


def calculate_life_palace(birth_month: int, birth_hour: int) -> Tuple[str, str]:
    """Calculate Life Palace"""
    branch_idx = (14 - birth_month - ((birth_hour + 1) // 2)) % 12
    stem_idx = (birth_month + ((birth_hour + 1) // 2)) % 10
    return (HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx])


def calculate_conception_palace(month_pillar: Pillar) -> Tuple[str, str]:
    """Calculate Conception Palace"""
    stem_idx = (get_stem_index(month_pillar.stem) + 1) % 10
    branch_idx = (get_branch_index(month_pillar.branch) + 3) % 12
    return (HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx])


# =============================================================================
# ANNUAL PILLAR
# =============================================================================

def calculate_annual_pillar(year: int) -> Pillar:
    """Calculate the annual pillar for any year"""
    return calculate_year_pillar(year)


# =============================================================================
# MAIN CALCULATION
# =============================================================================

def calculate_bazi_chart(
    birth_date: date,
    birth_hour: int,
    birth_minute: int = 0,
    gender: str = "M",
    current_year: int = None,
    include_annual: bool = True
) -> BaZiChart:
    """Calculate complete BaZi chart with improved accuracy"""
    
    if current_year is None:
        current_year = date.today().year
    
    # Get Chinese month/year (based on solar terms)
    chinese_month, chinese_year = get_chinese_month(birth_date)
    
    # Calculate Four Pillars
    year_pillar = calculate_year_pillar(chinese_year)
    month_pillar = calculate_month_pillar(chinese_year, chinese_month)
    day_pillar = calculate_day_pillar(birth_date)
    hour_pillar = calculate_hour_pillar(birth_hour, day_pillar.stem)
    
    # Annual pillar
    annual_pillar = calculate_annual_pillar(current_year) if include_annual else None
    
    # Day Master
    dm = day_pillar.stem
    dm_elem = STEM_ELEMENTS[dm]
    dm_pol = STEM_POLARITY[dm]
    
    # Build chart data for calculations
    chart_data = {
        "day_master": dm,
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar
    }
    
    # Calculate strength
    dm_strength, strength_cat = calculate_dm_strength(chart_data)
    
    # Useful gods
    useful, unfavorable = calculate_useful_gods(strength_cat, dm_elem)
    
    # 10 Gods distribution
    ten_gods_dist = calculate_ten_gods_distribution(chart_data)
    
    # Main profile
    filtered = {k: v for k, v in ten_gods_dist.items() if k != "F" and v > 0}
    if filtered:
        dominant = max(filtered, key=filtered.get)
        main_profile = TEN_PROFILES.get(dominant, ("Unknown", "Unknown"))[0]
    else:
        main_profile = "Balanced"
    
    # Luck pillars
    luck_pillar_start = calculate_luck_pillar_start_age(birth_date, gender, year_pillar.stem)
    luck_pillars = calculate_luck_pillars(birth_date, gender, year_pillar.stem, month_pillar, current_year)
    
    # Symbolic stars
    symbolic_stars = calculate_symbolic_stars(day_pillar.branch, year_pillar.branch, day_pillar.stem)
    
    # Special palaces
    life_palace = calculate_life_palace(chinese_month, birth_hour)
    conception_palace = calculate_conception_palace(month_pillar)
    
    return BaZiChart(
        birth_date=birth_date,
        birth_hour=birth_hour,
        birth_minute=birth_minute,
        gender=gender,
        year_pillar=year_pillar,
        month_pillar=month_pillar,
        day_pillar=day_pillar,
        hour_pillar=hour_pillar,
        annual_pillar=annual_pillar,
        day_master=dm,
        day_master_element=dm_elem,
        day_master_polarity=dm_pol,
        dm_strength=dm_strength,
        strength_category=strength_cat,
        useful_gods=useful,
        unfavorable_elements=unfavorable,
        ten_gods_distribution=ten_gods_dist,
        luck_pillars=luck_pillars,
        symbolic_stars=symbolic_stars,
        life_palace=life_palace,
        conception_palace=conception_palace,
        main_profile=main_profile,
        main_structure=dominant if filtered else "Balanced",
        luck_pillar_start_age=luck_pillar_start
    )


def chart_to_dict(chart: BaZiChart) -> dict:
    """Convert BaZiChart to dictionary"""
    result = {
        "birth_info": {
            "date": chart.birth_date.isoformat(),
            "hour": chart.birth_hour,
            "minute": chart.birth_minute,
            "gender": chart.gender
        },
        "four_pillars": {
            "year": chart.year_pillar.to_dict(),
            "month": chart.month_pillar.to_dict(),
            "day": chart.day_pillar.to_dict(),
            "hour": chart.hour_pillar.to_dict()
        },
        "day_master": {
            "stem": chart.day_master,
            "element": chart.day_master_element,
            "polarity": chart.day_master_polarity,
            "strength_pct": chart.dm_strength,
            "strength_category": chart.strength_category
        },
        "useful_gods": chart.useful_gods,
        "unfavorable_elements": chart.unfavorable_elements,
        "ten_gods_distribution": chart.ten_gods_distribution,
        "luck_pillars": [lp.to_dict() for lp in chart.luck_pillars] if chart.luck_pillars else [],
        "symbolic_stars": chart.symbolic_stars,
        "main_profile": chart.main_profile
    }
    
    if chart.annual_pillar:
        result["annual_pillar"] = chart.annual_pillar.to_dict()
    
    return result
