# Ming QiMenDunJia v10.0 - Professional BaZi Calculator
# core/bazi_calculator.py
"""
Complete BaZi (Four Pillars) calculation engine
Based on Joey Yap methodology

Features:
- Four Pillars calculation (Year/Month/Day/Hour)
- Hidden Stems extraction
- 10-Year Luck Pillars
- Day Master strength analysis
- 10 Gods distribution
- Symbolic Stars
- Na Yin (納音)
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
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

# Stem elements
STEM_ELEMENTS = {
    "Jia": "Wood", "Yi": "Wood",
    "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth",
    "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water"
}

STEM_POLARITY = {
    "Jia": "Yang", "Yi": "Yin",
    "Bing": "Yang", "Ding": "Yin",
    "Wu": "Yang", "Ji": "Yin",
    "Geng": "Yang", "Xin": "Yin",
    "Ren": "Yang", "Gui": "Yin"
}

# Branch elements
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

# Hidden Stems in each Branch (Main, Middle, Residual)
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

# 10 Gods mapping based on Day Master
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

# Element production cycle
ELEMENT_PRODUCES = {
    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal", 
    "Metal": "Water", "Water": "Wood"
}

# Element control cycle
ELEMENT_CONTROLS = {
    "Wood": "Earth", "Earth": "Water", "Water": "Fire",
    "Fire": "Metal", "Metal": "Wood"
}

# Na Yin (納音) - 60 Jia Zi cycle
NA_YIN = {
    (0, 0): "Gold in the Sea", (0, 1): "Gold in the Sea",
    (2, 2): "Fire in the Furnace", (2, 3): "Fire in the Furnace",
    (4, 4): "Wood of the Forest", (4, 5): "Wood of the Forest",
    (6, 6): "Earth on the Road", (6, 7): "Earth on the Road",
    (8, 8): "Metal of the Sword", (8, 9): "Metal of the Sword",
    (0, 10): "Earth on the Roof", (0, 11): "Earth on the Roof",
    (2, 0): "Fire of the Lightning", (2, 1): "Fire of the Lightning",
    (4, 2): "Wood of the Pine", (4, 3): "Wood of the Pine",
    (6, 4): "Earth of the Sand", (6, 5): "Earth of the Sand",
    (8, 6): "Metal of the Hairpin", (8, 7): "Metal of the Hairpin",
    (0, 8): "Fire of the Mountain", (0, 9): "Fire of the Mountain",
    (2, 10): "Water of the Stream", (2, 11): "Water of the Stream",
    (4, 0): "Gold in the Sand", (4, 1): "Gold in the Sand",
    (6, 2): "Fire of the Sky", (6, 3): "Fire of the Sky",
    (8, 4): "Wood of the Flat Ground", (8, 5): "Wood of the Flat Ground",
    (0, 6): "Earth of the Wall", (0, 7): "Earth of the Wall",
    (2, 8): "Metal of the Mirror", (2, 9): "Metal of the Mirror",
    (4, 10): "Wood of the Willow", (4, 11): "Wood of the Willow",
    (6, 0): "Water of the Spring", (6, 1): "Water of the Spring",
    (8, 2): "Earth on the Roof", (8, 3): "Earth on the Roof",
    (0, 4): "Fire of the Thunder", (0, 5): "Fire of the Thunder",
    (2, 6): "Wood of the Mulberry", (2, 7): "Wood of the Mulberry",
    (4, 8): "Earth of the Great Post", (4, 9): "Earth of the Great Post",
    (6, 10): "Metal of the White Wax", (6, 11): "Metal of the White Wax",
    (8, 0): "Wood of the Poplar", (8, 1): "Wood of the Poplar",
    (0, 2): "Water of the Well", (0, 3): "Water of the Well",
    (2, 4): "Earth on the Roof", (2, 5): "Earth on the Roof",
    (4, 6): "Fire of the Sky", (4, 7): "Fire of the Sky",
    (6, 8): "Wood of the Pomegranate", (6, 9): "Wood of the Pomegranate",
    (8, 10): "Earth of the Great Station", (8, 11): "Earth of the Great Station",
}

# 12 Growth Phases (長生十二宮)
GROWTH_PHASES = ["Birth", "Bath", "Growth", "Thriving", "Prosperous", "Weakening", 
                 "Sickness", "Death", "Grave", "Extinction", "Conceived", "Nourishing"]
GROWTH_PHASES_CN = ["長生", "沐浴", "冠帶", "臨官", "帝旺", "衰", "病", "死", "墓", "絕", "胎", "養"]

# Growth phase starting positions for each Day Master
GROWTH_PHASE_START = {
    "Jia": 10, "Yi": 4, "Bing": 2, "Ding": 8, "Wu": 2,
    "Ji": 8, "Geng": 8, "Xin": 2, "Ren": 8, "Gui": 2
}

# 10 Profiles mapping
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
# DATA CLASSES
# =============================================================================

@dataclass
class Pillar:
    """Single pillar data"""
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
    na_yin: str
    
    def to_dict(self) -> dict:
        return {
            "stem": self.stem,
            "stem_cn": self.stem_cn,
            "branch": self.branch,
            "branch_cn": self.branch_cn,
            "animal": self.animal,
            "animal_cn": self.animal_cn,
            "stem_element": self.stem_element,
            "branch_element": self.branch_element,
            "stem_polarity": self.stem_polarity,
            "branch_polarity": self.branch_polarity,
            "hidden_stems": self.hidden_stems,
            "na_yin": self.na_yin
        }


@dataclass 
class LuckPillar:
    """10-Year Luck Pillar"""
    age_start: int
    age_end: int
    year_start: int
    stem: str
    stem_cn: str
    branch: str
    branch_cn: str
    animal: str
    hidden_stems: List[str]
    growth_phase: str
    is_current: bool = False
    
    def to_dict(self) -> dict:
        return {
            "age_range": f"{self.age_start}-{self.age_end}",
            "year_start": self.year_start,
            "stem": self.stem,
            "stem_cn": self.stem_cn,
            "branch": self.branch,
            "branch_cn": self.branch_cn,
            "animal": self.animal,
            "hidden_stems": self.hidden_stems,
            "growth_phase": self.growth_phase,
            "is_current": self.is_current
        }


@dataclass
class BaZiChart:
    """Complete BaZi chart"""
    birth_date: date
    birth_hour: int
    birth_minute: int
    gender: str  # "M" or "F"
    
    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Pillar
    
    day_master: str
    day_master_element: str
    day_master_polarity: str
    
    dm_strength: float  # 0-100%
    strength_category: str  # "Strong", "Weak", "Balanced"
    
    useful_gods: List[str]
    unfavorable_elements: List[str]
    
    ten_gods_distribution: Dict[str, float]
    luck_pillars: List[LuckPillar]
    
    symbolic_stars: Dict[str, str]
    life_palace: Tuple[str, str]  # (stem, branch)
    conception_palace: Tuple[str, str]
    
    main_profile: str
    main_structure: str


# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

def get_stem_index(stem: str) -> int:
    """Get index of heavenly stem"""
    return HEAVENLY_STEMS.index(stem) if stem in HEAVENLY_STEMS else 0


def get_branch_index(branch: str) -> int:
    """Get index of earthly branch"""
    return EARTHLY_BRANCHES.index(branch) if branch in EARTHLY_BRANCHES else 0


def calculate_year_pillar(year: int) -> Pillar:
    """Calculate year pillar from Gregorian year"""
    # 1984 is Jia Zi year
    base_year = 1984
    cycle_position = (year - base_year) % 60
    
    stem_idx = cycle_position % 10
    branch_idx = cycle_position % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    # Get Na Yin
    na_yin_key = (stem_idx % 10, branch_idx)
    na_yin = NA_YIN.get(na_yin_key, "Unknown")
    
    return Pillar(
        stem=stem,
        stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch,
        branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx],
        animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem],
        branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch],
        na_yin=na_yin
    )


def get_solar_term_month(dt: date) -> int:
    """Get Chinese month based on solar terms (simplified)"""
    # Solar term dates (approximate, varies by year)
    solar_terms = [
        (2, 4),   # Li Chun - Start of Spring (Month 1)
        (3, 6),   # Jing Zhe - Month 2
        (4, 5),   # Qing Ming - Month 3
        (5, 6),   # Li Xia - Month 4
        (6, 6),   # Mang Zhong - Month 5
        (7, 7),   # Xiao Shu - Month 6
        (8, 8),   # Li Qiu - Month 7
        (9, 8),   # Bai Lu - Month 8
        (10, 8),  # Han Lu - Month 9
        (11, 7),  # Li Dong - Month 10
        (12, 7),  # Da Xue - Month 11
        (1, 6),   # Xiao Han - Month 12
    ]
    
    month, day = dt.month, dt.day
    
    for i, (term_month, term_day) in enumerate(solar_terms):
        if month == term_month and day >= term_day:
            return (i % 12) + 1
        elif month == term_month and day < term_day:
            return ((i - 1) % 12) + 1
    
    # Fallback
    if month == 1 and day < 6:
        return 12
    return ((month + 9) % 12) + 1


def calculate_month_pillar(year: int, month: int, year_stem: str) -> Pillar:
    """Calculate month pillar"""
    # Month stem based on year stem
    year_stem_idx = get_stem_index(year_stem)
    base_stem_idx = (year_stem_idx * 2 + 2) % 10
    stem_idx = (base_stem_idx + month - 1) % 10
    
    # Month branch: Yin(Tiger) = Month 1, etc.
    branch_idx = (month + 1) % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem,
        stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch,
        branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx],
        animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem],
        branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch],
        na_yin="varies"
    )


def calculate_day_pillar(dt: date) -> Pillar:
    """Calculate day pillar using formula"""
    # Reference: Jan 1, 1900 = Jia Xu day
    # Days since reference
    ref_date = date(1900, 1, 1)
    days_diff = (dt - ref_date).days
    
    # Jan 1, 1900 is stem index 0 (Jia), branch index 10 (Xu)
    stem_idx = (days_diff + 0) % 10
    branch_idx = (days_diff + 10) % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem,
        stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch,
        branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx],
        animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem],
        branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch],
        na_yin="varies"
    )


def calculate_hour_pillar(hour: int, day_stem: str) -> Pillar:
    """Calculate hour pillar"""
    # Hour to branch mapping
    if hour == 23:
        branch_idx = 0  # Zi hour starts at 23:00
    else:
        branch_idx = ((hour + 1) // 2) % 12
    
    # Hour stem based on day stem
    day_stem_idx = get_stem_index(day_stem)
    base_stem_idx = (day_stem_idx * 2) % 10
    stem_idx = (base_stem_idx + branch_idx) % 10
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return Pillar(
        stem=stem,
        stem_cn=HEAVENLY_STEMS_CN[stem_idx],
        branch=branch,
        branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
        animal=ANIMALS[branch_idx],
        animal_cn=ANIMALS_CN[branch_idx],
        stem_element=STEM_ELEMENTS[stem],
        branch_element=BRANCH_ELEMENTS[branch],
        stem_polarity=STEM_POLARITY[stem],
        branch_polarity=BRANCH_POLARITY[branch],
        hidden_stems=HIDDEN_STEMS[branch],
        na_yin="varies"
    )


def get_ten_god(day_master: str, target_stem: str) -> Tuple[str, str, str]:
    """Calculate 10 God relationship between Day Master and another stem"""
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    target_element = STEM_ELEMENTS[target_stem]
    target_polarity = STEM_POLARITY[target_stem]
    
    same_polarity = dm_polarity == target_polarity
    
    # Same element
    if dm_element == target_element:
        if same_polarity:
            return TEN_GODS["same_element_same_polarity"]
        else:
            return TEN_GODS["same_element_diff_polarity"]
    
    # Element that produces DM
    if ELEMENT_PRODUCES[target_element] == dm_element:
        if same_polarity:
            return TEN_GODS["produces_dm_same_polarity"]
        else:
            return TEN_GODS["produces_dm_diff_polarity"]
    
    # Element that DM produces
    if ELEMENT_PRODUCES[dm_element] == target_element:
        if same_polarity:
            return TEN_GODS["dm_produces_same_polarity"]
        else:
            return TEN_GODS["dm_produces_diff_polarity"]
    
    # Element that DM controls
    if ELEMENT_CONTROLS[dm_element] == target_element:
        if same_polarity:
            return TEN_GODS["dm_controls_same_polarity"]
        else:
            return TEN_GODS["dm_controls_diff_polarity"]
    
    # Element that controls DM
    if ELEMENT_CONTROLS[target_element] == dm_element:
        if same_polarity:
            return TEN_GODS["controls_dm_same_polarity"]
        else:
            return TEN_GODS["controls_dm_diff_polarity"]
    
    return ("?", "Unknown", "?")


def calculate_dm_strength(chart_data: dict) -> Tuple[float, str]:
    """Calculate Day Master strength percentage"""
    dm = chart_data["day_master"]
    dm_element = STEM_ELEMENTS[dm]
    
    # Count supporting vs opposing elements
    supporting = 0
    opposing = 0
    
    # Check all stems
    all_stems = [
        chart_data["year_pillar"].stem,
        chart_data["month_pillar"].stem,
        chart_data["hour_pillar"].stem,
    ]
    
    # Add hidden stems
    for pillar in [chart_data["year_pillar"], chart_data["month_pillar"], 
                   chart_data["day_pillar"], chart_data["hour_pillar"]]:
        all_stems.extend(pillar.hidden_stems)
    
    for stem in all_stems:
        elem = STEM_ELEMENTS[stem]
        if elem == dm_element:  # Same element
            supporting += 1.5
        elif ELEMENT_PRODUCES[elem] == dm_element:  # Produces DM
            supporting += 1
        elif ELEMENT_CONTROLS[elem] == dm_element:  # Controls DM
            opposing += 1.5
        elif ELEMENT_PRODUCES[dm_element] == elem:  # DM produces (drains)
            opposing += 1
        elif ELEMENT_CONTROLS[dm_element] == elem:  # DM controls (effort)
            opposing += 0.5
    
    # Check branch elements (seasonal influence)
    month_branch_elem = chart_data["month_pillar"].branch_element
    if month_branch_elem == dm_element:
        supporting += 2
    elif ELEMENT_PRODUCES[month_branch_elem] == dm_element:
        supporting += 1.5
    elif ELEMENT_CONTROLS[month_branch_elem] == dm_element:
        opposing += 2
    
    total = supporting + opposing
    if total == 0:
        return (50.0, "Balanced")
    
    strength_pct = (supporting / total) * 100
    
    if strength_pct >= 60:
        category = "Strong"
    elif strength_pct <= 40:
        category = "Weak"
    else:
        category = "Balanced"
    
    return (round(strength_pct, 1), category)


def calculate_ten_gods_distribution(chart_data: dict) -> Dict[str, float]:
    """Calculate distribution of 10 Gods in chart"""
    dm = chart_data["day_master"]
    distribution = {
        "F": 0, "RW": 0, "IR": 0, "DR": 0, "EG": 0,
        "HO": 0, "IW": 0, "DW": 0, "7K": 0, "DO": 0
    }
    
    # Count from all visible stems
    stems_to_check = [
        chart_data["year_pillar"].stem,
        chart_data["month_pillar"].stem,
        chart_data["hour_pillar"].stem,
    ]
    
    # Add hidden stems with reduced weight
    for pillar in [chart_data["year_pillar"], chart_data["month_pillar"],
                   chart_data["day_pillar"], chart_data["hour_pillar"]]:
        for i, hs in enumerate(pillar.hidden_stems):
            weight = 1.0 if i == 0 else (0.5 if i == 1 else 0.3)
            god_code, _, _ = get_ten_god(dm, hs)
            if god_code in distribution:
                distribution[god_code] += weight
    
    # Main stems
    for stem in stems_to_check:
        god_code, _, _ = get_ten_god(dm, stem)
        if god_code in distribution:
            distribution[god_code] += 2
    
    # Normalize to percentages
    total = sum(distribution.values())
    if total > 0:
        for key in distribution:
            distribution[key] = round((distribution[key] / total) * 100, 1)
    
    return distribution


def calculate_luck_pillars(birth_date: date, gender: str, year_stem: str, 
                          month_pillar: Pillar, current_year: int = None) -> List[LuckPillar]:
    """Calculate 10-Year Luck Pillars"""
    if current_year is None:
        current_year = date.today().year
    
    current_age = current_year - birth_date.year
    
    # Direction based on gender and year stem polarity
    year_stem_polarity = STEM_POLARITY[year_stem]
    
    # Yang male or Yin female = forward, otherwise backward
    if (year_stem_polarity == "Yang" and gender == "M") or \
       (year_stem_polarity == "Yin" and gender == "F"):
        direction = 1  # Forward
    else:
        direction = -1  # Backward
    
    # Starting stem and branch from month pillar
    month_stem_idx = get_stem_index(month_pillar.stem)
    month_branch_idx = get_branch_index(month_pillar.branch)
    
    # Calculate first luck pillar start age (simplified: use 3)
    first_age = 3
    
    luck_pillars = []
    for i in range(10):  # 10 luck pillars
        age_start = first_age + (i * 10)
        age_end = age_start + 9
        year_start = birth_date.year + age_start
        
        # Calculate stem and branch
        stem_idx = (month_stem_idx + (i + 1) * direction) % 10
        branch_idx = (month_branch_idx + (i + 1) * direction) % 12
        
        stem = HEAVENLY_STEMS[stem_idx]
        branch = EARTHLY_BRANCHES[branch_idx]
        
        is_current = age_start <= current_age <= age_end
        
        luck_pillars.append(LuckPillar(
            age_start=age_start,
            age_end=age_end,
            year_start=year_start,
            stem=stem,
            stem_cn=HEAVENLY_STEMS_CN[stem_idx],
            branch=branch,
            branch_cn=EARTHLY_BRANCHES_CN[branch_idx],
            animal=ANIMALS[branch_idx],
            hidden_stems=HIDDEN_STEMS[branch],
            growth_phase="varies",
            is_current=is_current
        ))
    
    return luck_pillars


def calculate_symbolic_stars(day_branch: str, year_branch: str) -> Dict[str, str]:
    """Calculate major symbolic stars"""
    stars = {}
    
    # Noble People (貴人) - based on Day Master
    noble_mapping = {
        "Zi": ["Chou", "Wei"], "Chou": ["Zi", "Shen"],
        "Yin": ["Hai", "Mao"], "Mao": ["Yin", "Xu"],
        "Chen": ["Chou", "Wei"], "Si": ["Zi", "Shen"],
        "Wu": ["Hai", "Mao"], "Wei": ["Yin", "Xu"],
        "Shen": ["Chou", "Wei"], "You": ["Zi", "Shen"],
        "Xu": ["Hai", "Mao"], "Hai": ["Yin", "Xu"]
    }
    stars["Noble People"] = ", ".join(noble_mapping.get(day_branch, []))
    
    # Peach Blossom (桃花) - based on Year/Day Branch
    peach_mapping = {
        "Yin": "Mao", "Wu": "Mao", "Xu": "Mao",
        "Shen": "You", "Zi": "You", "Chen": "You",
        "Si": "Wu", "You": "Wu", "Chou": "Wu",
        "Hai": "Zi", "Mao": "Zi", "Wei": "Zi"
    }
    stars["Peach Blossom"] = peach_mapping.get(year_branch, "?")
    
    # Travelling Horse (驛馬) - based on Year/Day Branch
    horse_mapping = {
        "Yin": "Shen", "Wu": "Shen", "Xu": "Shen",
        "Shen": "Yin", "Zi": "Yin", "Chen": "Yin",
        "Si": "Hai", "You": "Hai", "Chou": "Hai",
        "Hai": "Si", "Mao": "Si", "Wei": "Si"
    }
    stars["Sky Horse"] = horse_mapping.get(year_branch, "?")
    
    # Intelligence Star (文昌)
    intelligence_mapping = {
        "Jia": "Si", "Yi": "Wu", "Bing": "Shen", "Ding": "You",
        "Wu": "Shen", "Ji": "You", "Geng": "Hai", "Xin": "Zi",
        "Ren": "Yin", "Gui": "Mao"
    }
    # Need day stem for this
    stars["Intelligence"] = "varies"
    
    return stars


def calculate_life_palace(birth_month: int, birth_hour: int) -> Tuple[str, str]:
    """Calculate Life Palace (命宮)"""
    # Simplified calculation
    branch_idx = (14 - birth_month - ((birth_hour + 1) // 2)) % 12
    stem_idx = 0  # Simplified
    
    return (HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx])


def calculate_conception_palace(month_pillar: Pillar) -> Tuple[str, str]:
    """Calculate Conception Palace (胎元)"""
    stem_idx = (get_stem_index(month_pillar.stem) + 1) % 10
    branch_idx = (get_branch_index(month_pillar.branch) + 3) % 12
    
    return (HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx])


def calculate_useful_gods(dm_strength: str, dm_element: str) -> Tuple[List[str], List[str]]:
    """Calculate Useful Gods and Unfavorable Elements"""
    if dm_strength == "Weak":
        # Weak DM needs support: same element + element that produces it
        producing = [k for k, v in ELEMENT_PRODUCES.items() if v == dm_element][0]
        useful = [dm_element, producing]
        # Unfavorable: what drains (produces) and what controls
        draining = ELEMENT_PRODUCES[dm_element]
        controlling = [k for k, v in ELEMENT_CONTROLS.items() if v == dm_element][0]
        unfavorable = [draining, controlling]
    elif dm_strength == "Strong":
        # Strong DM needs draining: what it produces + what controls it
        draining = ELEMENT_PRODUCES[dm_element]
        controlling = [k for k, v in ELEMENT_CONTROLS.items() if v == dm_element][0]
        useful = [draining, controlling]
        # Unfavorable: same element + what produces it
        producing = [k for k, v in ELEMENT_PRODUCES.items() if v == dm_element][0]
        unfavorable = [dm_element, producing]
    else:
        # Balanced - context dependent
        useful = [dm_element]
        unfavorable = []
    
    return (useful, unfavorable)


def get_main_profile(ten_gods_dist: Dict[str, float]) -> Tuple[str, str]:
    """Get main profile based on highest 10 God"""
    # Exclude F (Friend) for profile determination
    filtered = {k: v for k, v in ten_gods_dist.items() if k != "F"}
    if not filtered:
        return ("Unknown", "Balanced")
    
    dominant = max(filtered, key=filtered.get)
    profile_name, structure = TEN_PROFILES.get(dominant, ("Unknown", "Unknown"))
    
    return (profile_name, dominant)


# =============================================================================
# MAIN CALCULATION FUNCTION
# =============================================================================

def calculate_bazi_chart(
    birth_date: date,
    birth_hour: int,
    birth_minute: int = 0,
    gender: str = "M",
    current_year: int = None
) -> BaZiChart:
    """
    Calculate complete BaZi chart
    
    Args:
        birth_date: Date of birth
        birth_hour: Hour of birth (0-23)
        birth_minute: Minute of birth (0-59)
        gender: "M" for male, "F" for female
        current_year: Year for luck pillar calculation
    
    Returns:
        Complete BaZiChart object
    """
    if current_year is None:
        current_year = date.today().year
    
    # Calculate Four Pillars
    year_pillar = calculate_year_pillar(birth_date.year)
    
    solar_month = get_solar_term_month(birth_date)
    month_pillar = calculate_month_pillar(birth_date.year, solar_month, year_pillar.stem)
    
    day_pillar = calculate_day_pillar(birth_date)
    hour_pillar = calculate_hour_pillar(birth_hour, day_pillar.stem)
    
    # Day Master info
    day_master = day_pillar.stem
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    
    # Create chart data dict for calculations
    chart_data = {
        "day_master": day_master,
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar
    }
    
    # Calculate DM Strength
    dm_strength_pct, strength_category = calculate_dm_strength(chart_data)
    
    # Calculate Useful Gods
    useful_gods, unfavorable = calculate_useful_gods(strength_category, dm_element)
    
    # Calculate 10 Gods Distribution
    ten_gods_dist = calculate_ten_gods_distribution(chart_data)
    
    # Calculate Luck Pillars
    luck_pillars = calculate_luck_pillars(
        birth_date, gender, year_pillar.stem, month_pillar, current_year
    )
    
    # Calculate Symbolic Stars
    symbolic_stars = calculate_symbolic_stars(day_pillar.branch, year_pillar.branch)
    
    # Calculate Special Palaces
    life_palace = calculate_life_palace(solar_month, birth_hour)
    conception_palace = calculate_conception_palace(month_pillar)
    
    # Get Main Profile
    main_profile, main_structure = get_main_profile(ten_gods_dist)
    
    return BaZiChart(
        birth_date=birth_date,
        birth_hour=birth_hour,
        birth_minute=birth_minute,
        gender=gender,
        year_pillar=year_pillar,
        month_pillar=month_pillar,
        day_pillar=day_pillar,
        hour_pillar=hour_pillar,
        day_master=day_master,
        day_master_element=dm_element,
        day_master_polarity=dm_polarity,
        dm_strength=dm_strength_pct,
        strength_category=strength_category,
        useful_gods=useful_gods,
        unfavorable_elements=unfavorable,
        ten_gods_distribution=ten_gods_dist,
        luck_pillars=luck_pillars,
        symbolic_stars=symbolic_stars,
        life_palace=life_palace,
        conception_palace=conception_palace,
        main_profile=main_profile,
        main_structure=main_structure
    )


def chart_to_dict(chart: BaZiChart) -> dict:
    """Convert BaZiChart to dictionary for export"""
    return {
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
        "luck_pillars": [lp.to_dict() for lp in chart.luck_pillars],
        "symbolic_stars": chart.symbolic_stars,
        "life_palace": {
            "stem": chart.life_palace[0],
            "branch": chart.life_palace[1]
        },
        "conception_palace": {
            "stem": chart.conception_palace[0],
            "branch": chart.conception_palace[1]
        },
        "main_profile": chart.main_profile,
        "main_structure": chart.main_structure
    }
