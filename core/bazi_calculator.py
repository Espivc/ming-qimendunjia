"""
===============================================================================
BAZI CALCULATOR - Core Calculation Engine
===============================================================================
Ming QiMenDunJia 明奇门 - Four Pillars of Destiny

This module provides accurate BaZi calculations following classical methodology:
- Solar term-based month pillar calculation
- Proper day pillar algorithm
- Luck pillar age calculation (days to solar term / 3)
- Day Master strength with weighted algorithm
- Ten Gods relationship mapping
- Clash, Combine, and Harmony detection

Version: 1.0
Updated: 2026-01-03
===============================================================================
"""

from datetime import date, datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum

# =============================================================================
# CONSTANTS - HEAVENLY STEMS & EARTHLY BRANCHES
# =============================================================================

HEAVENLY_STEMS = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
HEAVENLY_STEMS_CN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

EARTHLY_BRANCHES = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
EARTHLY_BRANCHES_CN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

BRANCH_ANIMALS = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 
                  'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']

# BaZi month branches (Month 1 = Yin/Tiger)
MONTH_BRANCHES = ['Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 
                  'Shen', 'You', 'Xu', 'Hai', 'Zi', 'Chou']

# =============================================================================
# ELEMENT MAPPINGS
# =============================================================================

STEM_ELEMENTS = {
    'Jia': 'Wood', 'Yi': 'Wood',
    'Bing': 'Fire', 'Ding': 'Fire',
    'Wu': 'Earth', 'Ji': 'Earth',
    'Geng': 'Metal', 'Xin': 'Metal',
    'Ren': 'Water', 'Gui': 'Water'
}

STEM_POLARITY = {
    'Jia': 'Yang', 'Yi': 'Yin',
    'Bing': 'Yang', 'Ding': 'Yin',
    'Wu': 'Yang', 'Ji': 'Yin',
    'Geng': 'Yang', 'Xin': 'Yin',
    'Ren': 'Yang', 'Gui': 'Yin'
}

BRANCH_ELEMENTS = {
    'Zi': 'Water', 'Chou': 'Earth', 'Yin': 'Wood', 'Mao': 'Wood',
    'Chen': 'Earth', 'Si': 'Fire', 'Wu': 'Fire', 'Wei': 'Earth',
    'Shen': 'Metal', 'You': 'Metal', 'Xu': 'Earth', 'Hai': 'Water'
}

BRANCH_POLARITY = {
    'Zi': 'Yang', 'Chou': 'Yin', 'Yin': 'Yang', 'Mao': 'Yin',
    'Chen': 'Yang', 'Si': 'Yin', 'Wu': 'Yang', 'Wei': 'Yin',
    'Shen': 'Yang', 'You': 'Yin', 'Xu': 'Yang', 'Hai': 'Yin'
}

# Hidden Stems in each Branch (Main, Secondary, Residual order)
HIDDEN_STEMS = {
    'Zi': ['Gui'],                    # Rat
    'Chou': ['Ji', 'Gui', 'Xin'],    # Ox
    'Yin': ['Jia', 'Bing', 'Wu'],    # Tiger
    'Mao': ['Yi'],                    # Rabbit
    'Chen': ['Wu', 'Yi', 'Gui'],     # Dragon
    'Si': ['Bing', 'Wu', 'Geng'],    # Snake
    'Wu': ['Ding', 'Ji'],            # Horse
    'Wei': ['Ji', 'Ding', 'Yi'],     # Goat
    'Shen': ['Geng', 'Ren', 'Wu'],   # Monkey
    'You': ['Xin'],                   # Rooster
    'Xu': ['Wu', 'Xin', 'Ding'],     # Dog
    'Hai': ['Ren', 'Jia'],           # Pig
}

# =============================================================================
# SOLAR TERMS (Jie 节 - Month Transition Dates)
# =============================================================================

SOLAR_TERMS = {
    1: (2, 4),    # 立春 Li Chun → Month 1 (寅 Tiger)
    2: (3, 6),    # 惊蛰 Jing Zhe → Month 2 (卯 Rabbit)
    3: (4, 5),    # 清明 Qing Ming → Month 3 (辰 Dragon)
    4: (5, 6),    # 立夏 Li Xia → Month 4 (巳 Snake)
    5: (6, 6),    # 芒种 Mang Zhong → Month 5 (午 Horse)
    6: (7, 7),    # 小暑 Xiao Shu → Month 6 (未 Goat)
    7: (8, 8),    # 立秋 Li Qiu → Month 7 (申 Monkey)
    8: (9, 8),    # 白露 Bai Lu → Month 8 (酉 Rooster)
    9: (10, 8),   # 寒露 Han Lu → Month 9 (戌 Dog)
    10: (11, 7),  # 立冬 Li Dong → Month 10 (亥 Pig)
    11: (12, 7),  # 大雪 Da Xue → Month 11 (子 Rat)
    12: (1, 6),   # 小寒 Xiao Han → Month 12 (丑 Ox)
}

SOLAR_TERM_NAMES = {
    1: ('立春', 'Li Chun', 'Spring Begins'),
    2: ('惊蛰', 'Jing Zhe', 'Insects Awaken'),
    3: ('清明', 'Qing Ming', 'Clear and Bright'),
    4: ('立夏', 'Li Xia', 'Summer Begins'),
    5: ('芒种', 'Mang Zhong', 'Grain in Ear'),
    6: ('小暑', 'Xiao Shu', 'Minor Heat'),
    7: ('立秋', 'Li Qiu', 'Autumn Begins'),
    8: ('白露', 'Bai Lu', 'White Dew'),
    9: ('寒露', 'Han Lu', 'Cold Dew'),
    10: ('立冬', 'Li Dong', 'Winter Begins'),
    11: ('大雪', 'Da Xue', 'Heavy Snow'),
    12: ('小寒', 'Xiao Han', 'Minor Cold'),
}

# =============================================================================
# FIVE ELEMENTS CYCLES
# =============================================================================

# Productive Cycle: Wood → Fire → Earth → Metal → Water → Wood
PRODUCTIVE_CYCLE = {
    'Wood': 'Fire',
    'Fire': 'Earth',
    'Earth': 'Metal',
    'Metal': 'Water',
    'Water': 'Wood',
}

# What produces this element (Resource)
PRODUCED_BY = {
    'Wood': 'Water',
    'Fire': 'Wood',
    'Earth': 'Fire',
    'Metal': 'Earth',
    'Water': 'Metal',
}

# Controlling Cycle: Wood → Earth → Water → Fire → Metal → Wood
CONTROLLING_CYCLE = {
    'Wood': 'Earth',
    'Earth': 'Water',
    'Water': 'Fire',
    'Fire': 'Metal',
    'Metal': 'Wood',
}

# What controls this element (Power)
CONTROLLED_BY = {
    'Wood': 'Metal',
    'Fire': 'Water',
    'Earth': 'Wood',
    'Metal': 'Fire',
    'Water': 'Earth',
}

# =============================================================================
# TEN GODS (十神)
# =============================================================================

TEN_GODS_CN = {
    'Friend': '比肩',
    'Rob Wealth': '劫财',
    'Eating God': '食神',
    'Hurting Officer': '伤官',
    'Indirect Wealth': '偏财',
    'Direct Wealth': '正财',
    'Seven Killings': '七杀',
    'Direct Officer': '正官',
    'Indirect Resource': '偏印',
    'Direct Resource': '正印',
}

# Profile names for the 10 Gods
PROFILE_NAMES = {
    'Friend': 'The Leader',
    'Rob Wealth': 'The Competitor',
    'Eating God': 'The Artist',
    'Hurting Officer': 'The Performer',
    'Indirect Wealth': 'The Pioneer',
    'Direct Wealth': 'The Director',
    'Seven Killings': 'The Warrior',
    'Direct Officer': 'The Diplomat',
    'Indirect Resource': 'The Analyzer',
    'Direct Resource': 'The Philosopher',
}

# =============================================================================
# CLASHES, COMBINES & HARMONY
# =============================================================================

# Six Clashes (六冲)
SIX_CLASHES = {
    'Zi': 'Wu', 'Wu': 'Zi',
    'Chou': 'Wei', 'Wei': 'Chou',
    'Yin': 'Shen', 'Shen': 'Yin',
    'Mao': 'You', 'You': 'Mao',
    'Chen': 'Xu', 'Xu': 'Chen',
    'Si': 'Hai', 'Hai': 'Si',
}

# Six Combines (六合) - (partner, result_element)
SIX_COMBINES = {
    'Zi': ('Chou', 'Earth'),
    'Chou': ('Zi', 'Earth'),
    'Yin': ('Hai', 'Wood'),
    'Hai': ('Yin', 'Wood'),
    'Mao': ('Xu', 'Fire'),
    'Xu': ('Mao', 'Fire'),
    'Chen': ('You', 'Metal'),
    'You': ('Chen', 'Metal'),
    'Si': ('Shen', 'Water'),
    'Shen': ('Si', 'Water'),
    'Wu': ('Wei', 'Fire'),
    'Wei': ('Wu', 'Fire'),
}

# Three Harmony (三合)
THREE_HARMONY = {
    'Wood': ['Hai', 'Mao', 'Wei'],   # Pig, Rabbit, Goat
    'Fire': ['Yin', 'Wu', 'Xu'],     # Tiger, Horse, Dog
    'Metal': ['Si', 'You', 'Chou'],  # Snake, Rooster, Ox
    'Water': ['Shen', 'Zi', 'Chen'], # Monkey, Rat, Dragon
}

# =============================================================================
# SEASONAL STRENGTH TABLE
# =============================================================================

SEASONAL_STRENGTH = {
    # Spring months (Wood prosperous)
    'Yin': {'Wood': 1.0, 'Fire': 0.6, 'Earth': 0.1, 'Metal': 0.0, 'Water': 0.3},
    'Mao': {'Wood': 1.0, 'Fire': 0.6, 'Earth': 0.1, 'Metal': 0.0, 'Water': 0.3},
    'Chen': {'Wood': 0.8, 'Fire': 0.5, 'Earth': 0.4, 'Metal': 0.1, 'Water': 0.2},
    # Summer months (Fire prosperous)
    'Si': {'Fire': 1.0, 'Earth': 0.6, 'Metal': 0.1, 'Water': 0.0, 'Wood': 0.3},
    'Wu': {'Fire': 1.0, 'Earth': 0.6, 'Metal': 0.1, 'Water': 0.0, 'Wood': 0.3},
    'Wei': {'Fire': 0.8, 'Earth': 0.7, 'Metal': 0.2, 'Water': 0.1, 'Wood': 0.2},
    # Autumn months (Metal prosperous)
    'Shen': {'Metal': 1.0, 'Water': 0.6, 'Wood': 0.1, 'Fire': 0.0, 'Earth': 0.3},
    'You': {'Metal': 1.0, 'Water': 0.6, 'Wood': 0.1, 'Fire': 0.0, 'Earth': 0.3},
    'Xu': {'Metal': 0.8, 'Water': 0.5, 'Wood': 0.1, 'Fire': 0.1, 'Earth': 0.5},
    # Winter months (Water prosperous)
    'Hai': {'Water': 1.0, 'Wood': 0.6, 'Fire': 0.1, 'Earth': 0.0, 'Metal': 0.3},
    'Zi': {'Water': 1.0, 'Wood': 0.6, 'Fire': 0.1, 'Earth': 0.0, 'Metal': 0.3},
    'Chou': {'Water': 0.8, 'Wood': 0.4, 'Fire': 0.1, 'Earth': 0.5, 'Metal': 0.2},
}

# =============================================================================
# ELEMENT COLORS (for UI)
# =============================================================================

ELEMENT_COLORS = {
    'Wood': '#228B22',   # Forest Green
    'Fire': '#DC143C',   # Crimson
    'Earth': '#DAA520',  # Goldenrod
    'Metal': '#C0C0C0',  # Silver
    'Water': '#1E90FF',  # Dodger Blue
}

# =============================================================================
# ENUMS
# =============================================================================

class DMStrength(Enum):
    """Day Master Strength Categories"""
    VERY_WEAK = "Very Weak"
    WEAK = "Weak"
    NEUTRAL = "Neutral"
    STRONG = "Strong"
    VERY_STRONG = "Very Strong"

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Pillar:
    """Represents a single BaZi pillar"""
    stem: str
    branch: str
    name: str = ""
    
    def __post_init__(self):
        self._stem_idx = HEAVENLY_STEMS.index(self.stem) if self.stem in HEAVENLY_STEMS else -1
        self._branch_idx = EARTHLY_BRANCHES.index(self.branch) if self.branch in EARTHLY_BRANCHES else -1
    
    @property
    def stem_cn(self) -> str:
        return HEAVENLY_STEMS_CN[self._stem_idx] if self._stem_idx >= 0 else ""
    
    @property
    def branch_cn(self) -> str:
        return EARTHLY_BRANCHES_CN[self._branch_idx] if self._branch_idx >= 0 else ""
    
    @property
    def chinese(self) -> str:
        return f"{self.stem_cn}{self.branch_cn}"
    
    @property
    def element(self) -> str:
        return STEM_ELEMENTS.get(self.stem, "")
    
    @property
    def polarity(self) -> str:
        return STEM_POLARITY.get(self.stem, "")
    
    @property
    def animal(self) -> str:
        return BRANCH_ANIMALS[self._branch_idx] if self._branch_idx >= 0 else ""
    
    @property
    def hidden_stems(self) -> List[str]:
        return HIDDEN_STEMS.get(self.branch, [])
    
    @property
    def branch_element(self) -> str:
        return BRANCH_ELEMENTS.get(self.branch, "")
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'stem': self.stem,
            'branch': self.branch,
            'stem_cn': self.stem_cn,
            'branch_cn': self.branch_cn,
            'chinese': self.chinese,
            'element': self.element,
            'polarity': self.polarity,
            'animal': self.animal,
            'hidden_stems': self.hidden_stems,
            'branch_element': self.branch_element,
        }

@dataclass
class LuckPillar:
    """Represents a 10-year Luck Pillar period"""
    pillar: Pillar
    start_age: int
    end_age: int
    
    @property
    def age_range(self) -> str:
        return f"{self.start_age}-{self.end_age}"
    
    def to_dict(self) -> Dict:
        return {
            **self.pillar.to_dict(),
            'start_age': self.start_age,
            'end_age': self.end_age,
            'age_range': self.age_range,
        }

# =============================================================================
# CORE CALCULATION FUNCTIONS
# =============================================================================

def get_bazi_year(year: int, month: int, day: int) -> int:
    """
    Get the BaZi year considering Li Chun boundary.
    BaZi year changes at Li Chun (~Feb 4), not Jan 1.
    """
    li_chun_month, li_chun_day = SOLAR_TERMS[1]
    if month < li_chun_month or (month == li_chun_month and day < li_chun_day):
        return year - 1
    return year


def get_bazi_month(year: int, month: int, day: int) -> int:
    """
    Determine BaZi month (1-12) based on solar terms.
    This is CRITICAL for correct month pillar calculation.
    """
    for bazi_month in range(12, 0, -1):
        solar_month, solar_day = SOLAR_TERMS[bazi_month]
        
        if bazi_month == 12:
            # Month 12 starts Jan 6
            if month == 1 and day >= solar_day:
                return 12
        else:
            if month > solar_month or (month == solar_month and day >= solar_day):
                return bazi_month
    
    # Before Jan 6 = still Month 11 of previous year
    return 11


def calc_year_pillar(year: int, month: int, day: int) -> Pillar:
    """Calculate the Year Pillar"""
    bazi_year = get_bazi_year(year, month, day)
    stem_idx = (bazi_year - 4) % 10
    branch_idx = (bazi_year - 4) % 12
    return Pillar(HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx], "Year")


def calc_month_pillar(year: int, month: int, day: int) -> Pillar:
    """
    Calculate the Month Pillar using solar terms.
    Uses the 5-Tiger Formula for month stem.
    """
    bazi_month = get_bazi_month(year, month, day)
    month_branch = MONTH_BRANCHES[bazi_month - 1]
    
    # Get year stem (considering Li Chun boundary)
    year_pillar = calc_year_pillar(year, month, day)
    year_stem_idx = HEAVENLY_STEMS.index(year_pillar.stem)
    
    # 5-Tiger Formula
    first_month_stem_idx = (year_stem_idx * 2 + 2) % 10
    month_stem_idx = (first_month_stem_idx + bazi_month - 1) % 10
    
    return Pillar(HEAVENLY_STEMS[month_stem_idx], month_branch, "Month")


def calc_day_pillar(birth_date: date) -> Pillar:
    """
    Calculate the Day Pillar.
    Reference: 1900-01-01 = 甲戌 (Jia Xu)
    """
    reference = date(1900, 1, 1)
    days_diff = (birth_date - reference).days
    
    stem_idx = days_diff % 10
    branch_idx = (days_diff + 10) % 12
    
    return Pillar(HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx], "Day")


def calc_hour_pillar(hour: int, day_stem: str) -> Pillar:
    """
    Calculate the Hour Pillar.
    Uses the 5-Rat Formula for hour stem.
    
    Hour branches:
    - Zi (子): 23:00-00:59
    - Chou (丑): 01:00-02:59
    - etc.
    """
    if hour == 23:
        branch_idx = 0  # Zi hour (late)
    else:
        branch_idx = ((hour + 1) // 2) % 12
    
    # 5-Rat Formula
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    zi_hour_stem_idx = (day_stem_idx % 5) * 2
    hour_stem_idx = (zi_hour_stem_idx + branch_idx) % 10
    
    return Pillar(HEAVENLY_STEMS[hour_stem_idx], EARTHLY_BRANCHES[branch_idx], "Hour")


def calculate_four_pillars(birth_date: date, birth_hour: int) -> Dict[str, Pillar]:
    """
    Calculate all Four Pillars of Destiny.
    
    Returns dict with keys: 'year', 'month', 'day', 'hour'
    """
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    
    year_pillar = calc_year_pillar(year, month, day)
    month_pillar = calc_month_pillar(year, month, day)
    day_pillar = calc_day_pillar(birth_date)
    hour_pillar = calc_hour_pillar(birth_hour, day_pillar.stem)
    
    return {
        'year': year_pillar,
        'month': month_pillar,
        'day': day_pillar,
        'hour': hour_pillar,
    }


def pillars_to_dict(pillars: Dict[str, Pillar]) -> Dict[str, Dict]:
    """Convert pillars dict to serializable format"""
    return {name: p.to_dict() for name, p in pillars.items()}

# =============================================================================
# TEN GODS CALCULATION
# =============================================================================

def get_ten_god(day_master: str, other_stem: str) -> str:
    """
    Calculate the Ten God relationship between Day Master and another stem.
    """
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    other_element = STEM_ELEMENTS[other_stem]
    other_polarity = STEM_POLARITY[other_stem]
    
    same_polarity = (dm_polarity == other_polarity)
    
    # Same element
    if other_element == dm_element:
        return 'Friend' if same_polarity else 'Rob Wealth'
    
    # DM produces (Output)
    if PRODUCTIVE_CYCLE[dm_element] == other_element:
        return 'Eating God' if same_polarity else 'Hurting Officer'
    
    # DM controls (Wealth)
    if CONTROLLING_CYCLE[dm_element] == other_element:
        return 'Indirect Wealth' if same_polarity else 'Direct Wealth'
    
    # Controls DM (Power)
    if CONTROLLED_BY[dm_element] == other_element:
        return 'Seven Killings' if same_polarity else 'Direct Officer'
    
    # Produces DM (Resource)
    if PRODUCED_BY[dm_element] == other_element:
        return 'Indirect Resource' if same_polarity else 'Direct Resource'
    
    return 'Unknown'


def calculate_ten_profiles(pillars: Dict[str, Pillar]) -> Dict[str, int]:
    """
    Calculate the distribution of Ten Gods in the chart.
    Counts visible stems and hidden stems.
    """
    day_master = pillars['day'].stem
    profile_counts = {
        'Friend': 0, 'Rob Wealth': 0,
        'Eating God': 0, 'Hurting Officer': 0,
        'Indirect Wealth': 0, 'Direct Wealth': 0,
        'Seven Killings': 0, 'Direct Officer': 0,
        'Indirect Resource': 0, 'Direct Resource': 0,
    }
    
    # Count visible stems (excluding Day Master)
    for name, pillar in pillars.items():
        if name == 'day':
            continue
        god = get_ten_god(day_master, pillar.stem)
        profile_counts[god] += 1
    
    # Count hidden stems in all branches
    for pillar in pillars.values():
        for hidden in pillar.hidden_stems:
            god = get_ten_god(day_master, hidden)
            profile_counts[god] += 1
    
    return profile_counts


def get_dominant_profile(profile_counts: Dict[str, int]) -> Tuple[str, str]:
    """Get the dominant profile and its name"""
    if not profile_counts:
        return 'Unknown', 'Unknown'
    
    dominant = max(profile_counts, key=profile_counts.get)
    profile_name = PROFILE_NAMES.get(dominant, dominant)
    return dominant, profile_name

# =============================================================================
# DAY MASTER STRENGTH
# =============================================================================

def calculate_dm_strength(pillars: Dict[str, Pillar]) -> Tuple[float, DMStrength]:
    """
    Calculate Day Master strength using weighted algorithm.
    
    Weights:
    - Seasonal (Month branch): 40%
    - Hidden Stems: 30%
    - Visible Stems: 20%
    - Hour Branch: 10%
    
    Returns (percentage, category)
    """
    day_master = pillars['day'].stem
    dm_element = STEM_ELEMENTS[day_master]
    producing = PRODUCED_BY[dm_element]
    
    score = 0.0
    
    # 1. SEASONAL STRENGTH (40%)
    month_branch = pillars['month'].branch
    if month_branch in SEASONAL_STRENGTH:
        seasonal_score = SEASONAL_STRENGTH[month_branch].get(dm_element, 0.0)
        score += seasonal_score * 0.40
    
    # 2. HIDDEN STEMS (30%)
    hidden_support = 0
    hidden_total = 0
    
    for pillar in pillars.values():
        for hidden in pillar.hidden_stems:
            hidden_total += 1
            hidden_element = STEM_ELEMENTS[hidden]
            if hidden_element == dm_element:
                hidden_support += 1.0
            elif hidden_element == producing:
                hidden_support += 0.7
    
    if hidden_total > 0:
        score += (hidden_support / hidden_total) * 0.30
    
    # 3. VISIBLE STEMS (20%)
    visible_support = 0
    visible_count = 0
    
    for name, pillar in pillars.items():
        if name == 'day':
            continue
        visible_count += 1
        stem_element = STEM_ELEMENTS[pillar.stem]
        if stem_element == dm_element:
            visible_support += 1.0
        elif stem_element == producing:
            visible_support += 0.7
    
    if visible_count > 0:
        score += (visible_support / visible_count) * 0.20
    
    # 4. HOUR BRANCH (10%)
    hour_element = BRANCH_ELEMENTS[pillars['hour'].branch]
    if hour_element == dm_element:
        score += 0.10
    elif hour_element == producing:
        score += 0.07
    
    percentage = min(score * 100, 100)
    
    # Map to categories
    if percentage <= 20:
        category = DMStrength.VERY_WEAK
    elif percentage <= 40:
        category = DMStrength.WEAK
    elif percentage <= 60:
        category = DMStrength.NEUTRAL
    elif percentage <= 80:
        category = DMStrength.STRONG
    else:
        category = DMStrength.VERY_STRONG
    
    return round(percentage, 1), category


def determine_useful_gods(dm_element: str, strength: DMStrength) -> Dict:
    """
    Determine Useful Gods based on Day Master element and strength.
    """
    producing = PRODUCED_BY[dm_element]
    controls = CONTROLLING_CYCLE[dm_element]
    controlled_by = CONTROLLED_BY[dm_element]
    output = PRODUCTIVE_CYCLE[dm_element]
    
    if strength in [DMStrength.VERY_WEAK, DMStrength.WEAK]:
        return {
            'useful': [dm_element, producing],
            'unfavorable': [controlled_by, output, controls],
            'explanation': f'As a {strength.value} {dm_element} Day Master, you need strengthening from {dm_element} (same element) and {producing} (resource).'
        }
    elif strength == DMStrength.NEUTRAL:
        return {
            'useful': [dm_element, producing, controls],
            'unfavorable': [controlled_by],
            'explanation': f'As a Neutral {dm_element} Day Master, you can handle most elements. Focus on {controls} for wealth opportunities.'
        }
    else:
        return {
            'useful': [controlled_by, output, controls],
            'unfavorable': [dm_element, producing],
            'explanation': f'As a {strength.value} {dm_element} Day Master, you need draining through {output} (output) and {controls} (wealth).'
        }

# =============================================================================
# LUCK PILLARS
# =============================================================================

def calculate_luck_pillar_start_age(
    birth_date: date,
    gender: str,
    year_polarity: str
) -> int:
    """
    Calculate starting age for Luck Pillars.
    
    Algorithm:
    1. Direction: Yang Male / Yin Female = Forward; Yin Male / Yang Female = Reverse
    2. Count days to nearest solar term transition (in that direction)
    3. Divide by 3, round to nearest integer
    """
    is_forward = (
        (gender.lower() == 'male' and year_polarity == 'Yang') or
        (gender.lower() == 'female' and year_polarity == 'Yin')
    )
    
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    current_bazi_month = get_bazi_month(year, month, day)
    
    if is_forward:
        # Find NEXT solar term
        next_bazi_month = (current_bazi_month % 12) + 1
        next_solar_month, next_solar_day = SOLAR_TERMS[next_bazi_month]
        
        if next_solar_month < month or (next_solar_month == 1 and month >= 11):
            target_year = year + 1
        else:
            target_year = year
        
        target_date = date(target_year, next_solar_month, next_solar_day)
    else:
        # Find PREVIOUS solar term
        curr_solar_month, curr_solar_day = SOLAR_TERMS[current_bazi_month]
        target_date = date(year, curr_solar_month, curr_solar_day)
        
        if target_date > birth_date:
            prev_bazi_month = ((current_bazi_month - 2) % 12) + 1
            prev_solar_month, prev_solar_day = SOLAR_TERMS[prev_bazi_month]
            target_year = year - 1 if prev_solar_month > month else year
            target_date = date(target_year, prev_solar_month, prev_solar_day)
    
    days_diff = abs((target_date - birth_date).days)
    return round(days_diff / 3)


def calculate_luck_pillars(
    pillars: Dict[str, Pillar],
    birth_date: date,
    gender: str,
    num_pillars: int = 8
) -> List[LuckPillar]:
    """
    Calculate Luck Pillars (10-year periods).
    """
    month_pillar = pillars['month']
    year_pillar = pillars['year']
    year_polarity = year_pillar.polarity
    
    is_forward = (
        (gender.lower() == 'male' and year_polarity == 'Yang') or
        (gender.lower() == 'female' and year_polarity == 'Yin')
    )
    
    start_age = calculate_luck_pillar_start_age(birth_date, gender, year_polarity)
    
    stem_idx = HEAVENLY_STEMS.index(month_pillar.stem)
    branch_idx = EARTHLY_BRANCHES.index(month_pillar.branch)
    
    luck_pillars = []
    current_age = start_age
    
    for i in range(num_pillars):
        if is_forward:
            new_stem_idx = (stem_idx + i + 1) % 10
            new_branch_idx = (branch_idx + i + 1) % 12
        else:
            new_stem_idx = (stem_idx - i - 1) % 10
            new_branch_idx = (branch_idx - i - 1) % 12
        
        pillar = Pillar(
            HEAVENLY_STEMS[new_stem_idx],
            EARTHLY_BRANCHES[new_branch_idx],
            f"LP{i+1}"
        )
        
        luck_pillars.append(LuckPillar(
            pillar=pillar,
            start_age=current_age,
            end_age=current_age + 9
        ))
        
        current_age += 10
    
    return luck_pillars


def get_luck_direction(gender: str, year_polarity: str) -> str:
    """Get luck pillar direction as string"""
    is_forward = (
        (gender.lower() == 'male' and year_polarity == 'Yang') or
        (gender.lower() == 'female' and year_polarity == 'Yin')
    )
    return "Forward" if is_forward else "Reverse"

# =============================================================================
# CLASH & COMBINE DETECTION
# =============================================================================

def detect_clashes(pillars: Dict[str, Pillar]) -> List[Dict]:
    """Detect Six Clashes between pillars"""
    clashes = []
    pillar_names = list(pillars.keys())
    
    for i, name1 in enumerate(pillar_names):
        for name2 in pillar_names[i+1:]:
            branch1 = pillars[name1].branch
            branch2 = pillars[name2].branch
            
            if SIX_CLASHES.get(branch1) == branch2:
                clashes.append({
                    'pillar1': name1,
                    'pillar2': name2,
                    'branch1': branch1,
                    'branch2': branch2,
                    'animals': f"{pillars[name1].animal} vs {pillars[name2].animal}",
                    'description': f"{name1.title()} ↔ {name2.title()}"
                })
    
    return clashes


def detect_combines(pillars: Dict[str, Pillar]) -> List[Dict]:
    """Detect Six Combines between pillars"""
    combines = []
    pillar_names = list(pillars.keys())
    
    for i, name1 in enumerate(pillar_names):
        for name2 in pillar_names[i+1:]:
            branch1 = pillars[name1].branch
            branch2 = pillars[name2].branch
            
            combine_info = SIX_COMBINES.get(branch1)
            if combine_info and combine_info[0] == branch2:
                combines.append({
                    'pillar1': name1,
                    'pillar2': name2,
                    'branch1': branch1,
                    'branch2': branch2,
                    'result_element': combine_info[1],
                    'animals': f"{pillars[name1].animal} + {pillars[name2].animal}",
                    'description': f"{name1.title()} + {name2.title()} → {combine_info[1]}"
                })
    
    return combines


def detect_three_harmony(pillars: Dict[str, Pillar]) -> List[Dict]:
    """Detect Three Harmony combinations"""
    branches = [p.branch for p in pillars.values()]
    harmonies = []
    
    for element, trio in THREE_HARMONY.items():
        matches = [b for b in branches if b in trio]
        if len(matches) >= 2:
            harmonies.append({
                'element': element,
                'branches': matches,
                'complete': len(matches) == 3,
                'description': f"{element} {'(Complete)' if len(matches) == 3 else '(Partial)'}"
            })
    
    return harmonies

# =============================================================================
# COMPLETE ANALYSIS
# =============================================================================

def analyze_bazi(
    birth_date: date,
    birth_hour: int,
    gender: str = 'male'
) -> Dict:
    """
    Perform complete BaZi analysis.
    
    Returns comprehensive analysis dictionary.
    """
    # Calculate Four Pillars
    pillars = calculate_four_pillars(birth_date, birth_hour)
    day_master = pillars['day'].stem
    dm_element = pillars['day'].element
    
    # Calculate strength
    strength_pct, strength_category = calculate_dm_strength(pillars)
    
    # Useful gods
    useful_gods = determine_useful_gods(dm_element, strength_category)
    
    # Ten Profiles
    profiles = calculate_ten_profiles(pillars)
    dominant_god, profile_name = get_dominant_profile(profiles)
    
    # Luck Pillars
    year_polarity = pillars['year'].polarity
    luck_direction = get_luck_direction(gender, year_polarity)
    luck_pillars = calculate_luck_pillars(pillars, birth_date, gender)
    
    # Interactions
    clashes = detect_clashes(pillars)
    combines = detect_combines(pillars)
    harmonies = detect_three_harmony(pillars)
    
    return {
        'birth_info': {
            'date': birth_date.isoformat(),
            'hour': birth_hour,
            'gender': gender
        },
        'four_pillars': pillars_to_dict(pillars),
        'day_master': {
            'stem': day_master,
            'stem_cn': pillars['day'].stem_cn,
            'element': dm_element,
            'polarity': pillars['day'].polarity,
            'strength_pct': strength_pct,
            'strength_category': strength_category.value
        },
        'useful_gods': useful_gods,
        'profiles': {
            'counts': profiles,
            'dominant': dominant_god,
            'profile_name': profile_name
        },
        'luck_pillars': {
            'direction': luck_direction,
            'start_age': luck_pillars[0].start_age if luck_pillars else 0,
            'pillars': [lp.to_dict() for lp in luck_pillars]
        },
        'interactions': {
            'clashes': clashes,
            'combines': combines,
            'three_harmony': harmonies
        }
    }

# =============================================================================
# VALIDATION / TESTING
# =============================================================================

def validate_calculation(birth_date: date, birth_hour: int, expected: Dict) -> bool:
    """
    Validate calculation against expected results.
    
    Args:
        birth_date: Date of birth
        birth_hour: Hour of birth
        expected: Dict with keys 'year', 'month', 'day', 'hour' each containing (stem, branch)
    
    Returns:
        True if all match
    """
    pillars = calculate_four_pillars(birth_date, birth_hour)
    
    all_match = True
    for name in ['year', 'month', 'day', 'hour']:
        if name in expected:
            exp_stem, exp_branch = expected[name]
            actual = pillars[name]
            if actual.stem != exp_stem or actual.branch != exp_branch:
                print(f"MISMATCH {name}: Expected {exp_stem} {exp_branch}, Got {actual.stem} {actual.branch}")
                all_match = False
    
    return all_match


if __name__ == "__main__":
    # Test with Ben's profile
    result = analyze_bazi(date(1978, 6, 27), 20, 'male')
    
    print("=" * 60)
    print("BAZI CALCULATOR TEST")
    print("=" * 60)
    print(f"\nFour Pillars:")
    for name, p in result['four_pillars'].items():
        print(f"  {name.title():6} | {p['stem']:4} {p['branch']:5} | {p['chinese']} | {p['animal']}")
    
    print(f"\nDay Master: {result['day_master']['stem']} ({result['day_master']['element']})")
    print(f"Strength: {result['day_master']['strength_pct']}% ({result['day_master']['strength_category']})")
    print(f"\nUseful: {', '.join(result['useful_gods']['useful'])}")
    print(f"Unfavorable: {', '.join(result['useful_gods']['unfavorable'])}")
    
    print(f"\nDominant Profile: {result['profiles']['dominant']} ({result['profiles']['profile_name']})")
    
    print(f"\nLuck Pillars ({result['luck_pillars']['direction']}, Start Age {result['luck_pillars']['start_age']}):")
    for lp in result['luck_pillars']['pillars'][:6]:
        print(f"  {lp['age_range']:8} | {lp['chinese']} | {lp['animal']}")
