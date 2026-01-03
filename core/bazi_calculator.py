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

# Hidden Stems in each Branch (Joey Yap order - VERIFIED against Joey Yap chart)
# This order is CRITICAL for correct display
HIDDEN_STEMS = {
    'Zi': ['Gui'],                    # 子 Rat: 癸
    'Chou': ['Ji', 'Gui', 'Xin'],    # 丑 Ox: 己癸辛
    'Yin': ['Jia', 'Bing', 'Wu'],    # 寅 Tiger: 甲丙戊
    'Mao': ['Yi'],                    # 卯 Rabbit: 乙
    'Chen': ['Wu', 'Yi', 'Gui'],     # 辰 Dragon: 戊乙癸
    'Si': ['Bing', 'Wu', 'Geng'],    # 巳 Snake: 丙戊庚
    'Wu': ['Ding', 'Ji'],            # 午 Horse: 丁己 ✓ Joey Yap verified
    'Wei': ['Ji', 'Ding', 'Yi'],     # 未 Goat: 己丁乙
    'Shen': ['Wu', 'Geng', 'Ren'],   # 申 Monkey: 戊庚壬 ✓ Joey Yap verified
    'You': ['Xin'],                   # 酉 Rooster: 辛
    'Xu': ['Ding', 'Wu', 'Xin'],     # 戌 Dog: 丁戊辛 ✓ Joey Yap verified
    'Hai': ['Ren', 'Jia'],           # 亥 Pig: 壬甲
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
# SYMBOLIC STARS (神煞)
# =============================================================================

# Noble People 贵人 (Tian Yi Gui Ren) - Based on Day Stem
NOBLE_PEOPLE = {
    'Jia': ['Chou', 'Wei'],   # 甲 → 丑未
    'Yi': ['Zi', 'Shen'],     # 乙 → 子申
    'Bing': ['Hai', 'You'],   # 丙 → 亥酉
    'Ding': ['Hai', 'You'],   # 丁 → 亥酉
    'Wu': ['Chou', 'Wei'],    # 戊 → 丑未
    'Ji': ['Zi', 'Shen'],     # 己 → 子申
    'Geng': ['Chou', 'Wei'],  # 庚 → 丑未 ← Ben's
    'Xin': ['Yin', 'Wu'],     # 辛 → 寅午
    'Ren': ['Mao', 'Si'],     # 壬 → 卯巳
    'Gui': ['Mao', 'Si'],     # 癸 → 卯巳
}

# Peach Blossom 桃花 (Tao Hua) - Based on Day Branch (or Year Branch)
# Uses the "Three Harmony Frame" - find the Mao/You/Wu/Zi of your frame
PEACH_BLOSSOM = {
    'Yin': 'Mao', 'Wu': 'Mao', 'Xu': 'Mao',      # Fire frame → Mao
    'Shen': 'You', 'Zi': 'You', 'Chen': 'You',   # Water frame → You ← Ben (申)
    'Si': 'Wu', 'You': 'Wu', 'Chou': 'Wu',       # Metal frame → Wu
    'Hai': 'Zi', 'Mao': 'Zi', 'Wei': 'Zi',       # Wood frame → Zi
}

# Intelligence Star 文昌 (Wen Chang) - Based on Day Stem
INTELLIGENCE_STAR = {
    'Jia': 'Si',    # 甲 → 巳
    'Yi': 'Wu',     # 乙 → 午
    'Bing': 'Shen', # 丙 → 申
    'Ding': 'You',  # 丁 → 酉
    'Wu': 'Shen',   # 戊 → 申
    'Ji': 'You',    # 己 → 酉
    'Geng': 'Hai',  # 庚 → 亥 ← Ben's
    'Xin': 'Zi',    # 辛 → 子
    'Ren': 'Yin',   # 壬 → 寅
    'Gui': 'Mao',   # 癸 → 卯
}

# Sky Horse 驿马 (Yi Ma) - Based on Day Branch (or Year Branch)
SKY_HORSE = {
    'Yin': 'Shen', 'Wu': 'Shen', 'Xu': 'Shen',   # Fire frame → Shen
    'Shen': 'Yin', 'Zi': 'Yin', 'Chen': 'Yin',   # Water frame → Yin ← Ben (申)
    'Si': 'Hai', 'You': 'Hai', 'Chou': 'Hai',    # Metal frame → Hai
    'Hai': 'Si', 'Mao': 'Si', 'Wei': 'Si',       # Wood frame → Si
}

# Solitary Star 孤辰 (Gu Chen) - Based on DAY Branch (not Year!)
# Formula groups:
# 寅卯辰 (Tiger, Rabbit, Dragon) → Solitary at 巳 Si (Snake)
# 巳午未 (Snake, Horse, Goat) → Solitary at 申 Shen (Monkey)
# 申酉戌 (Monkey, Rooster, Dog) → Solitary at 亥 Hai (Pig)
# 亥子丑 (Pig, Rat, Ox) → Solitary at 寅 Yin (Tiger)
SOLITARY_STAR = {
    'Yin': 'Si', 'Mao': 'Si', 'Chen': 'Si',
    'Si': 'Shen', 'Wu': 'Shen', 'Wei': 'Shen',
    'Shen': 'Hai', 'You': 'Hai', 'Xu': 'Hai',  # Ben's Day Branch Shen → Hai
    'Hai': 'Yin', 'Zi': 'Yin', 'Chou': 'Yin',
}

# Widow Star 寡宿 (Gua Su) - Based on Year Branch
WIDOW_STAR = {
    'Yin': 'Chou', 'Mao': 'Chou', 'Chen': 'Chou',
    'Si': 'Chen', 'Wu': 'Chen', 'Wei': 'Chen',
    'Shen': 'Wei', 'You': 'Wei', 'Xu': 'Wei',
    'Hai': 'Xu', 'Zi': 'Xu', 'Chou': 'Xu',
}

# =============================================================================
# LIFE PALACE & CONCEPTION PALACE
# =============================================================================

def calculate_life_palace(year_stem: str, month_branch: str, hour_branch: str) -> Tuple[str, str]:
    """
    Calculate Life Palace 命宫 (stem and branch)
    
    Formula for branch:
    Count from Yin (month 1) to birth month, then count backwards from that point by hour.
    Formula: Life Palace Branch = 14 - month_index - hour_index (mod 12)
    
    Formula for stem:
    Uses the year stem with 5-Tiger formula
    
    Ben's case: Month=Wu(Horse), Hour=Xu(Dog)
    Month index (from Yin): Wu=4, Hour index: Xu=10
    Life Palace = (14 - 4 - 10) % 12 = 0 = Zi (Rat) ✓
    """
    # Month branch order starting from Yin (Tiger) = index 0
    month_order = ['Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 
                   'Shen', 'You', 'Xu', 'Hai', 'Zi', 'Chou']
    
    # Get month index (Yin=0, Mao=1, ... Wu=4, etc.)
    m_idx = month_order.index(month_branch) if month_branch in month_order else 0
    
    # Get hour index using standard branch order (Zi=0, Chou=1, ...)
    h_idx = EARTHLY_BRANCHES.index(hour_branch)
    
    # Life palace branch calculation
    life_idx = (14 - m_idx - h_idx) % 12
    life_branch = EARTHLY_BRANCHES[life_idx]
    
    # Life palace stem calculation using 5-Tiger formula
    # Based on year stem, determine the starting stem for Yin month
    year_stem_idx = HEAVENLY_STEMS.index(year_stem)
    
    # 5-Tiger formula: Year stem determines Yin month stem
    # Jia/Ji -> Bing (index 2), Yi/Geng -> Wu (index 4), 
    # Bing/Xin -> Geng (index 6), Ding/Ren -> Ren (index 8), Wu/Gui -> Jia (index 0)
    base_stems = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
    yin_stem_idx = base_stems.get(year_stem_idx, 0)
    
    # Find the life palace branch's position in month order
    life_month_idx = month_order.index(life_branch) if life_branch in month_order else 0
    
    # Calculate stem for life palace
    life_stem_idx = (yin_stem_idx + life_month_idx) % 10
    life_stem = HEAVENLY_STEMS[life_stem_idx]
    
    return life_stem, life_branch

def calculate_conception_palace(month_stem: str, month_branch: str) -> Tuple[str, str]:
    """
    Calculate Conception Palace 胎元
    Formula: Month Stem + 1, Month Branch + 3
    """
    stem_idx = HEAVENLY_STEMS.index(month_stem)
    branch_idx = EARTHLY_BRANCHES.index(month_branch)
    
    # Add 1 to stem, add 3 to branch
    conception_stem = HEAVENLY_STEMS[(stem_idx + 1) % 10]
    conception_branch = EARTHLY_BRANCHES[(branch_idx + 3) % 12]
    
    return conception_stem, conception_branch

# =============================================================================
# 12 LIFE STAGES (十二长生)
# =============================================================================

# Life stages in order
TWELVE_STAGES = [
    ('長生', 'Chang Sheng', 'Birth'),
    ('沐浴', 'Mu Yu', 'Bath'),
    ('冠帶', 'Guan Dai', 'Youth'),
    ('臨官', 'Lin Guan', 'Maturity'),
    ('帝旺', 'Di Wang', 'Prosperous'),
    ('衰', 'Shuai', 'Weakening'),
    ('病', 'Bing', 'Sickness'),
    ('死', 'Si', 'Death'),
    ('墓', 'Mu', 'Grave'),
    ('絕', 'Jue', 'Extinction'),
    ('胎', 'Tai', 'Conceived'),
    ('養', 'Yang', 'Nourishing'),
]

# Starting branch for each stem's life cycle (where 長生 begins)
LIFE_STAGE_START = {
    'Jia': 'Hai',   # Yang Wood starts at Pig
    'Yi': 'Wu',     # Yin Wood starts at Horse (reverse)
    'Bing': 'Yin',  # Yang Fire starts at Tiger
    'Ding': 'You',  # Yin Fire starts at Rooster (reverse)
    'Wu': 'Yin',    # Yang Earth starts at Tiger
    'Ji': 'You',    # Yin Earth starts at Rooster (reverse)
    'Geng': 'Si',   # Yang Metal starts at Snake
    'Xin': 'Zi',    # Yin Metal starts at Rat (reverse)
    'Ren': 'Shen',  # Yang Water starts at Monkey
    'Gui': 'Mao',   # Yin Water starts at Rabbit (reverse)
}

def get_life_stage(stem: str, branch: str) -> Tuple[str, str, str]:
    """
    Get the 12 Life Stage for a stem in a particular branch
    Returns: (Chinese, Pinyin, English)
    """
    if stem not in LIFE_STAGE_START:
        return ('', '', '')
    
    start_branch = LIFE_STAGE_START[stem]
    start_idx = EARTHLY_BRANCHES.index(start_branch)
    branch_idx = EARTHLY_BRANCHES.index(branch)
    
    # Yang stems go forward, Yin stems go backward
    polarity = STEM_POLARITY[stem]
    if polarity == 'Yang':
        stage_idx = (branch_idx - start_idx) % 12
    else:
        stage_idx = (start_idx - branch_idx) % 12
    
    return TWELVE_STAGES[stage_idx]

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
# ANNUAL PILLAR & ANALYSIS
# =============================================================================

def calculate_annual_pillar(year: int) -> Dict:
    """
    Calculate the Annual Pillar for a given year.
    
    2026 = 丙午 Bing Wu (Fire Horse)
    """
    # Year stem cycle: starts from Jia (index 0) at year 4 (e.g., 1984, 1994, 2004)
    stem_idx = (year - 4) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    stem_cn = HEAVENLY_STEMS_CN[stem_idx]
    
    # Year branch cycle: starts from Zi (index 0) at year 4 (e.g., 1984, 1996, 2008)
    branch_idx = (year - 4) % 12
    branch = EARTHLY_BRANCHES[branch_idx]
    branch_cn = EARTHLY_BRANCHES_CN[branch_idx]
    animal = BRANCH_ANIMALS[branch_idx]
    
    element = STEM_ELEMENTS[stem]
    polarity = STEM_POLARITY[stem]
    hidden = HIDDEN_STEMS.get(branch, [])
    
    return {
        'year': year,
        'stem': stem,
        'stem_cn': stem_cn,
        'branch': branch,
        'branch_cn': branch_cn,
        'animal': animal,
        'element': element,
        'polarity': polarity,
        'chinese': f"{stem_cn}{branch_cn}",
        'hidden_stems': hidden
    }


def calculate_annual_ten_gods(day_master: str, annual_pillar: Dict) -> Dict[str, str]:
    """
    Calculate Ten Gods for the annual pillar relative to Day Master.
    """
    stem_god = get_ten_god(day_master, annual_pillar['stem'])
    
    hidden_gods = []
    for hs in annual_pillar['hidden_stems']:
        hidden_gods.append({
            'stem': hs,
            'god': get_ten_god(day_master, hs)
        })
    
    return {
        'stem_god': stem_god,
        'hidden_gods': hidden_gods
    }


def calculate_annual_profile_influence(natal_profiles: Dict[str, int], annual_pillar: Dict, day_master: str) -> Dict[str, float]:
    """
    Calculate how the annual pillar influences Ten Profiles.
    Combines natal profile with annual pillar influence.
    
    Joey Yap shows both Natal % and Annual % side by side.
    """
    # Get the annual stem's ten god
    annual_stem_god = get_ten_god(day_master, annual_pillar['stem'])
    
    # Get hidden stems' ten gods
    annual_hidden_gods = [get_ten_god(day_master, hs) for hs in annual_pillar['hidden_stems']]
    
    # Start with natal counts
    annual_counts = natal_profiles.copy()
    
    # Add annual pillar influence
    # Visible stem adds weight
    if annual_stem_god in annual_counts:
        annual_counts[annual_stem_god] = annual_counts.get(annual_stem_god, 0) + 2
    
    # Hidden stems add weight
    for god in annual_hidden_gods:
        if god in annual_counts:
            annual_counts[god] = annual_counts.get(god, 0) + 1
    
    # Calculate percentages using Joey Yap position-weighted method
    # (simplified version - adds annual pillar influence to natal)
    ten_gods = [
        'Direct Officer', 'Indirect Resource', 'Seven Killings', 'Direct Resource',
        'Friend', 'Eating God', 'Rob Wealth', 'Direct Wealth', 'Indirect Wealth', 'Hurting Officer'
    ]
    
    max_count = max(annual_counts.values()) if annual_counts.values() else 1
    if max_count == 0:
        max_count = 1
    
    percentages = {}
    for god in ten_gods:
        count = annual_counts.get(god, 0)
        if count > 0:
            pct = (count / max_count) * 100
            percentages[god] = round(pct, 0)
        else:
            percentages[god] = 0
    
    return percentages


# =============================================================================
# SIX ASPECTS ANALYSIS (六神)
# =============================================================================

SIX_ASPECTS_INFO = {
    'Life Purpose': {
        'chinese': '事業',
        'description': 'Career direction, life mission, sense of purpose',
        'gods': ['Direct Officer', 'Seven Killings'],
        'element': 'Fire'
    },
    'Financial': {
        'chinese': '財運',
        'description': 'Wealth potential, money management, financial opportunities',
        'gods': ['Direct Wealth', 'Indirect Wealth'],
        'element': 'Wood'
    },
    'Relationship': {
        'chinese': '感情',
        'description': 'Romance, partnerships, social connections',
        'gods': ['Rob Wealth', 'Friend'],
        'element': 'Metal'
    },
    'Family': {
        'chinese': '家庭',
        'description': 'Family harmony, home life, parental relationships',
        'gods': ['Direct Resource', 'Indirect Resource'],
        'element': 'Earth'
    },
    'Wellness': {
        'chinese': '健康',
        'description': 'Physical health, mental wellbeing, vitality',
        'gods': ['Eating God'],
        'element': 'Water'
    },
    'Contribution': {
        'chinese': '貢獻',
        'description': 'Creative output, legacy, impact on others',
        'gods': ['Hurting Officer', 'Eating God'],
        'element': 'Water'
    }
}


def calculate_six_aspects(profile_percentages: Dict[str, float]) -> Dict[str, Dict]:
    """
    Calculate Six Aspects scores from Ten Profiles.
    
    Each aspect is derived from specific Ten Gods:
    - Life Purpose: Direct Officer + Seven Killings (Influence/官)
    - Financial: Direct Wealth + Indirect Wealth (Wealth/財)
    - Relationship: Rob Wealth + Friend (Companion/比)
    - Family: Direct Resource + Indirect Resource (Resource/印)
    - Wellness: Eating God (Output/食)
    - Contribution: Hurting Officer + Eating God (Output/食)
    """
    aspects = {}
    
    for aspect_name, info in SIX_ASPECTS_INFO.items():
        gods = info['gods']
        
        # Calculate score as average of related gods' percentages
        total = sum(profile_percentages.get(god, 0) for god in gods)
        score = total / len(gods) if gods else 0
        
        aspects[aspect_name] = {
            'score': round(score, 0),
            'chinese': info['chinese'],
            'description': info['description'],
            'element': info['element'],
            'related_gods': gods
        }
    
    return aspects


def calculate_annual_six_aspects(natal_aspects: Dict, annual_profile_pcts: Dict[str, float]) -> Dict[str, Dict]:
    """
    Calculate Six Aspects for annual comparison.
    """
    annual_aspects = {}
    
    for aspect_name, info in SIX_ASPECTS_INFO.items():
        gods = info['gods']
        
        total = sum(annual_profile_pcts.get(god, 0) for god in gods)
        score = total / len(gods) if gods else 0
        
        natal_score = natal_aspects.get(aspect_name, {}).get('score', 0)
        change = score - natal_score
        
        annual_aspects[aspect_name] = {
            'score': round(score, 0),
            'natal_score': natal_score,
            'change': round(change, 0),
            'chinese': info['chinese'],
            'element': info['element']
        }
    
    return annual_aspects


# =============================================================================
# MONTHLY INFLUENCE
# =============================================================================

MONTHLY_STEMS_2026 = {
    # 2026 is 丙午 year, so month stems follow the pattern
    # Month stem = (Year stem index * 2 + month index) % 10
    1: ('Geng', 'Yin'),    # Feb 4 - Tiger month
    2: ('Xin', 'Mao'),     # Mar 5 - Rabbit month  
    3: ('Ren', 'Chen'),    # Apr 5 - Dragon month
    4: ('Gui', 'Si'),      # May 5 - Snake month
    5: ('Jia', 'Wu'),      # Jun 5 - Horse month
    6: ('Yi', 'Wei'),      # Jul 7 - Goat month
    7: ('Bing', 'Shen'),   # Aug 7 - Monkey month
    8: ('Ding', 'You'),    # Sep 7 - Rooster month
    9: ('Wu', 'Xu'),       # Oct 8 - Dog month
    10: ('Ji', 'Hai'),     # Nov 7 - Pig month
    11: ('Geng', 'Zi'),    # Dec 7 - Rat month
    12: ('Xin', 'Chou'),   # Jan 5 (2027) - Ox month
}


def calculate_monthly_influence(year: int, day_master: str) -> List[Dict]:
    """
    Calculate monthly pillar influence for a given year.
    """
    months = []
    
    # Get year stem for calculating month stems
    year_stem_idx = (year - 4) % 10
    
    month_names = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 
                   'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan+']
    
    for month_num in range(1, 13):
        # Calculate month stem (Five Tiger formula)
        # Base: Jia/Ji year starts with Bing Yin
        base_stem_idx = (year_stem_idx % 5) * 2
        month_stem_idx = (base_stem_idx + month_num - 1) % 10
        month_stem = HEAVENLY_STEMS[month_stem_idx]
        
        # Month branch is fixed: Yin(Feb), Mao(Mar), etc.
        month_branch_idx = (month_num + 1) % 12  # Yin=2 for Feb
        month_branch = EARTHLY_BRANCHES[month_branch_idx]
        
        # Get hidden stems
        hidden = HIDDEN_STEMS.get(month_branch, [])
        
        # Calculate ten gods
        stem_god = get_ten_god(day_master, month_stem)
        hidden_gods = [{'stem': hs, 'god': get_ten_god(day_master, hs)} for hs in hidden]
        
        months.append({
            'month': month_num,
            'name': month_names[month_num - 1],
            'stem': month_stem,
            'stem_cn': HEAVENLY_STEMS_CN[HEAVENLY_STEMS.index(month_stem)],
            'branch': month_branch,
            'branch_cn': EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(month_branch)],
            'animal': BRANCH_ANIMALS[EARTHLY_BRANCHES.index(month_branch)],
            'element': STEM_ELEMENTS[month_stem],
            'stem_god': stem_god,
            'hidden_stems': hidden,
            'hidden_gods': hidden_gods
        })
    
    return months

ELEMENT_COLORS = {
    'Wood': '#228B22',   # Forest Green
    'Fire': '#DC143C',   # Crimson
    'Earth': '#DAA520',  # Goldenrod
    'Metal': '#C0C0C0',  # Silver
    'Water': '#1E90FF',  # Dodger Blue
}

# =============================================================================
# LIFE STAR / GUA NUMBER (風水命卦)
# =============================================================================

GUA_INFO = {
    1: {
        'number': 1,
        'name': 'Kan',
        'chinese': '坎',
        'element': 'Water',
        'color': 'White',
        'color_cn': '一白',
        'direction': 'North',
        'trigram': '☵',
        'group': 'East',
        'description': 'The Abysmal, Water. Represents adaptability, wisdom, and flow. Associated with career and life path.'
    },
    2: {
        'number': 2,
        'name': 'Kun',
        'chinese': '坤',
        'element': 'Earth',
        'color': 'Black',
        'color_cn': '二黑',
        'direction': 'Southwest',
        'trigram': '☷',
        'group': 'West',
        'description': 'The Receptive, Earth. Represents nurturing, relationships, and motherhood. Associated with partnerships.'
    },
    3: {
        'number': 3,
        'name': 'Zhen',
        'chinese': '震',
        'element': 'Wood',
        'color': 'Jade',
        'color_cn': '三碧',
        'direction': 'East',
        'trigram': '☳',
        'group': 'East',
        'description': 'The Arousing, Thunder. Represents growth, new beginnings, and ambition. Associated with family and health.'
    },
    4: {
        'number': 4,
        'name': 'Xun',
        'chinese': '巽',
        'element': 'Wood',
        'color': 'Green',
        'color_cn': '四綠',
        'direction': 'Southeast',
        'trigram': '☴',
        'group': 'East',
        'description': 'The Gentle, Wind. Represents flexibility, communication, and wealth accumulation. Associated with prosperity and romance.'
    },
    5: {
        'number': 5,
        'name': 'Center',
        'chinese': '中',
        'element': 'Earth',
        'color': 'Yellow',
        'color_cn': '五黃',
        'direction': 'Center',
        'trigram': '',
        'group': 'Variable',
        'description': 'The Center. Males default to Kun (2), females default to Gen (8). Represents balance and central authority.'
    },
    6: {
        'number': 6,
        'name': 'Qian',
        'chinese': '乾',
        'element': 'Metal',
        'color': 'White',
        'color_cn': '六白',
        'direction': 'Northwest',
        'trigram': '☰',
        'group': 'West',
        'description': 'The Creative, Heaven. Represents leadership, authority, and fatherhood. Associated with mentors and helpful people.'
    },
    7: {
        'number': 7,
        'name': 'Dui',
        'chinese': '兌',
        'element': 'Metal',
        'color': 'Red',
        'color_cn': '七赤',
        'direction': 'West',
        'trigram': '☱',
        'group': 'West',
        'description': 'The Joyous, Lake. Represents joy, pleasure, and communication. Associated with children and creativity.'
    },
    8: {
        'number': 8,
        'name': 'Gen',
        'chinese': '艮',
        'element': 'Earth',
        'color': 'White',
        'color_cn': '八白',
        'direction': 'Northeast',
        'trigram': '☶',
        'group': 'West',
        'description': 'The Still, Mountain. Represents stability, knowledge, and self-cultivation. Associated with education and spirituality.'
    },
    9: {
        'number': 9,
        'name': 'Li',
        'chinese': '離',
        'element': 'Fire',
        'color': 'Purple',
        'color_cn': '九紫',
        'direction': 'South',
        'trigram': '☲',
        'group': 'East',
        'description': 'The Clinging, Fire. Represents fame, recognition, and illumination. Associated with reputation and visibility.'
    }
}

# =============================================================================
# EIGHT MANSIONS (八宅) - Directions for each Gua
# =============================================================================

# Direction meanings
DIRECTION_MEANINGS = {
    'Sheng Qi': {
        'chinese': '生氣',
        'english': 'Life Generating',
        'type': 'Favorable',
        'rank': 1,
        'description': 'Best for main door, bedroom, and study. Brings vitality, success, and good fortune. Excellent for career advancement and wealth generation.',
        'use_for': ['Main entrance', 'Master bedroom', 'Home office', 'Important meetings']
    },
    'Tian Yi': {
        'chinese': '天醫',
        'english': 'Heavenly Doctor',
        'type': 'Favorable',
        'rank': 2,
        'description': 'Healing energy. Good for bedroom if you have health issues. Attracts helpful people and improves relationships with authority figures.',
        'use_for': ['Bedroom for health recovery', 'Kitchen', 'Dining area', 'Medical consultations']
    },
    'Yan Nian': {
        'chinese': '延年',
        'english': 'Longevity',
        'type': 'Favorable',
        'rank': 3,
        'description': 'Promotes harmonious relationships and longevity. Excellent for romance and marriage luck. Stabilizes existing relationships.',
        'use_for': ['Couple bedroom', 'Living room', 'Family gatherings', 'Relationship discussions']
    },
    'Fu Wei': {
        'chinese': '伏位',
        'english': 'Stability',
        'type': 'Favorable',
        'rank': 4,
        'description': 'Provides stability and peace. Good for meditation and personal development. Not the strongest but reliable and calming.',
        'use_for': ['Meditation space', 'Study', 'Personal retreat', 'Quiet contemplation']
    },
    'Huo Hai': {
        'chinese': '禍害',
        'english': 'Mishaps',
        'type': 'Unfavorable',
        'rank': 5,
        'description': 'Causes minor setbacks, arguments, and frustrations. Avoid for important activities. Can lead to misunderstandings and small accidents.',
        'avoid_for': ['Main door', 'Bedroom', 'Important work', 'Negotiations']
    },
    'Wu Gui': {
        'chinese': '五鬼',
        'english': 'Five Ghosts',
        'type': 'Unfavorable',
        'rank': 6,
        'description': 'Brings backstabbing, betrayal, and fire hazards. Can cause theft and loss of money. Be cautious of people from this direction.',
        'avoid_for': ['Storing valuables', 'Trusting strangers', 'Financial dealings', 'Fire placement']
    },
    'Liu Sha': {
        'chinese': '六煞',
        'english': 'Six Killings',
        'type': 'Unfavorable',
        'rank': 7,
        'description': 'Affects relationships negatively. Can cause scandals, affairs, and legal problems. Impacts reputation and romantic relationships.',
        'avoid_for': ['Bedroom', 'Romantic encounters', 'Legal matters', 'Public appearances']
    },
    'Jue Ming': {
        'chinese': '絕命',
        'english': 'Life Threatening',
        'type': 'Unfavorable',
        'rank': 8,
        'description': 'The worst direction. Brings serious misfortune, health problems, and financial disasters. Absolutely avoid for sleeping or main door.',
        'avoid_for': ['Everything important', 'Sleeping', 'Main entrance', 'Business activities']
    }
}

# Eight Mansions direction mapping for each Gua
# Format: {gua_number: {direction_name: compass_direction}}
EIGHT_MANSIONS = {
    1: {  # Kan - Water
        'Sheng Qi': 'Southeast', 'Tian Yi': 'East', 'Yan Nian': 'South', 'Fu Wei': 'North',
        'Huo Hai': 'West', 'Wu Gui': 'Northeast', 'Liu Sha': 'Northwest', 'Jue Ming': 'Southwest'
    },
    2: {  # Kun - Earth
        'Sheng Qi': 'Northeast', 'Tian Yi': 'West', 'Yan Nian': 'Northwest', 'Fu Wei': 'Southwest',
        'Huo Hai': 'East', 'Wu Gui': 'Southeast', 'Liu Sha': 'South', 'Jue Ming': 'North'
    },
    3: {  # Zhen - Wood
        'Sheng Qi': 'South', 'Tian Yi': 'North', 'Yan Nian': 'Southeast', 'Fu Wei': 'East',
        'Huo Hai': 'Southwest', 'Wu Gui': 'Northwest', 'Liu Sha': 'Northeast', 'Jue Ming': 'West'
    },
    4: {  # Xun - Wood (Ben's Gua)
        'Sheng Qi': 'North', 'Tian Yi': 'South', 'Yan Nian': 'East', 'Fu Wei': 'Southeast',
        'Huo Hai': 'Northwest', 'Wu Gui': 'Southwest', 'Liu Sha': 'West', 'Jue Ming': 'Northeast'
    },
    6: {  # Qian - Metal
        'Sheng Qi': 'West', 'Tian Yi': 'Northeast', 'Yan Nian': 'Southwest', 'Fu Wei': 'Northwest',
        'Huo Hai': 'Southeast', 'Wu Gui': 'East', 'Liu Sha': 'South', 'Jue Ming': 'North'
    },
    7: {  # Dui - Metal
        'Sheng Qi': 'Northwest', 'Tian Yi': 'Southwest', 'Yan Nian': 'Northeast', 'Fu Wei': 'West',
        'Huo Hai': 'South', 'Wu Gui': 'North', 'Liu Sha': 'East', 'Jue Ming': 'Southeast'
    },
    8: {  # Gen - Earth
        'Sheng Qi': 'Southwest', 'Tian Yi': 'Northwest', 'Yan Nian': 'West', 'Fu Wei': 'Northeast',
        'Huo Hai': 'North', 'Wu Gui': 'South', 'Liu Sha': 'Southeast', 'Jue Ming': 'East'
    },
    9: {  # Li - Fire
        'Sheng Qi': 'East', 'Tian Yi': 'Southeast', 'Yan Nian': 'North', 'Fu Wei': 'South',
        'Huo Hai': 'Northeast', 'Wu Gui': 'West', 'Liu Sha': 'Southwest', 'Jue Ming': 'Northwest'
    }
}

# =============================================================================
# HIDDEN STEMS MEANINGS (藏干解释)
# =============================================================================

HIDDEN_STEM_ROLES = {
    0: {'name': 'Main Qi', 'chinese': '主气', 'description': 'The dominant energy of the branch. This is the primary influence and carries the most weight.'},
    1: {'name': 'Middle Qi', 'chinese': '中气', 'description': 'The secondary energy. This represents transitional or supporting influence.'},
    2: {'name': 'Residual Qi', 'chinese': '余气', 'description': 'The residual or leftover energy from the previous season. Subtle but present influence.'}
}

def explain_hidden_stems(day_master: str, branch: str, hidden_stems: List[str]) -> List[Dict]:
    """
    Generate detailed explanations for hidden stems in a branch.
    
    For each hidden stem, explains:
    - What element it is
    - Its role (Main Qi, Middle Qi, Residual Qi)
    - What Ten God it represents relative to Day Master
    - What this means practically
    """
    explanations = []
    
    for i, stem in enumerate(hidden_stems):
        stem_element = STEM_ELEMENTS[stem]
        stem_polarity = STEM_POLARITY[stem]
        stem_cn = HEAVENLY_STEMS_CN[HEAVENLY_STEMS.index(stem)]
        
        # Get Ten God relationship
        ten_god = get_ten_god(day_master, stem)
        ten_god_cn = TEN_GODS_CN.get(ten_god, '')
        
        # Get role based on position
        role = HIDDEN_STEM_ROLES.get(i, HIDDEN_STEM_ROLES[2])
        
        # Generate practical meaning based on Ten God
        meaning = get_ten_god_meaning(ten_god)
        
        explanations.append({
            'stem': stem,
            'stem_cn': stem_cn,
            'element': stem_element,
            'polarity': stem_polarity,
            'role': role['name'],
            'role_cn': role['chinese'],
            'role_description': role['description'],
            'ten_god': ten_god,
            'ten_god_cn': ten_god_cn,
            'meaning': meaning,
            'position': i
        })
    
    return explanations


def get_ten_god_meaning(ten_god: str) -> Dict:
    """
    Get practical meaning and interpretation for each Ten God.
    """
    meanings = {
        'Friend': {
            'keyword': 'Self, Peers, Competition',
            'represents': 'Same element, same polarity as Day Master',
            'people': 'Friends, siblings, colleagues at same level',
            'traits': 'Independence, self-reliance, competition',
            'positive': 'Strong sense of self, confident, independent',
            'negative': 'Stubborn, competitive, reluctant to ask for help',
            'life_aspect': 'Personal identity and peer relationships'
        },
        'Rob Wealth': {
            'keyword': 'Rivalry, Boldness, Action',
            'represents': 'Same element, opposite polarity as Day Master',
            'people': 'Competitors, rivals, assertive friends',
            'traits': 'Bold action, risk-taking, competitive spirit',
            'positive': 'Courageous, decisive, willing to take risks',
            'negative': 'Impulsive, aggressive, may lose money through competition',
            'life_aspect': 'Competition and bold ventures'
        },
        'Eating God': {
            'keyword': 'Creativity, Expression, Enjoyment',
            'represents': 'Element produced by Day Master, same polarity',
            'people': 'Children (especially daughters for men), students',
            'traits': 'Creativity, self-expression, appreciation of life',
            'positive': 'Artistic, enjoys life, good with food/arts',
            'negative': 'May be too relaxed, indulgent, lacks drive',
            'life_aspect': 'Creative output and life enjoyment'
        },
        'Hurting Officer': {
            'keyword': 'Rebellion, Innovation, Expression',
            'represents': 'Element produced by Day Master, opposite polarity',
            'people': 'Children (especially sons for men), unconventional people',
            'traits': 'Innovation, challenging authority, strong expression',
            'positive': 'Creative genius, innovative, breaks new ground',
            'negative': 'Rebellious, conflicts with authority, sharp tongue',
            'life_aspect': 'Innovation and challenging the status quo'
        },
        'Direct Wealth': {
            'keyword': 'Stable Income, Spouse, Control',
            'represents': 'Element controlled by Day Master, opposite polarity',
            'people': 'Wife (for men), stable business partners',
            'traits': 'Financial stability, management, tangible assets',
            'positive': 'Good money manager, stable income, practical',
            'negative': 'May be too focused on money, materialistic',
            'life_aspect': 'Stable finances and marriage'
        },
        'Indirect Wealth': {
            'keyword': 'Windfall, Opportunities, Father',
            'represents': 'Element controlled by Day Master, same polarity',
            'people': 'Father, mistress, speculative partners',
            'traits': 'Unexpected income, opportunities, risk for reward',
            'positive': 'Good at seizing opportunities, lucky with money',
            'negative': 'Unstable finances, gambling tendencies',
            'life_aspect': 'Opportunities and unexpected gains'
        },
        'Direct Officer': {
            'keyword': 'Authority, Discipline, Husband',
            'represents': 'Element that controls Day Master, opposite polarity',
            'people': 'Husband (for women), bosses, government officials',
            'traits': 'Discipline, following rules, proper conduct',
            'positive': 'Respected, disciplined, good reputation',
            'negative': 'Too rigid, pressured by authority, conservative',
            'life_aspect': 'Career authority and proper conduct'
        },
        'Seven Killings': {
            'keyword': 'Power, Pressure, Ambition',
            'represents': 'Element that controls Day Master, same polarity',
            'people': 'Competitors in authority, demanding bosses',
            'traits': 'Ambition, drive, pressure to succeed',
            'positive': 'Powerful, ambitious, can handle pressure',
            'negative': 'Aggressive, ruthless, health issues from stress',
            'life_aspect': 'Power struggles and ambition'
        },
        'Direct Resource': {
            'keyword': 'Mother, Education, Support',
            'represents': 'Element that produces Day Master, opposite polarity',
            'people': 'Mother, teachers, mentors, helpful elders',
            'traits': 'Learning, nurturing support, traditional knowledge',
            'positive': 'Well-educated, supported, good memory',
            'negative': 'Dependent, too passive, over-protected',
            'life_aspect': 'Education and nurturing support'
        },
        'Indirect Resource': {
            'keyword': 'Unconventional Learning, Intuition',
            'represents': 'Element that produces Day Master, same polarity',
            'people': 'Step-mother, alternative teachers, spiritual guides',
            'traits': 'Intuition, unconventional wisdom, spiritual learning',
            'positive': 'Intuitive, creative thinking, spiritual insight',
            'negative': 'Scattered thinking, impractical ideas, loneliness',
            'life_aspect': 'Unconventional wisdom and intuition'
        }
    }
    
    return meanings.get(ten_god, {
        'keyword': 'Unknown',
        'represents': 'Unknown relationship',
        'people': 'Unknown',
        'traits': 'Unknown',
        'positive': 'Unknown',
        'negative': 'Unknown',
        'life_aspect': 'Unknown'
    })


def get_pillar_hidden_stem_analysis(pillars: Dict, day_master: str) -> Dict[str, List[Dict]]:
    """
    Get complete hidden stem analysis for all four pillars.
    """
    analysis = {}
    
    pillar_meanings = {
        'year': {
            'name': 'Year Pillar',
            'chinese': '年柱',
            'represents': 'Ancestors, grandparents, early childhood (0-16)',
            'influence': 'Social environment, family background, inherited traits'
        },
        'month': {
            'name': 'Month Pillar',
            'chinese': '月柱',
            'represents': 'Parents, young adulthood (17-32)',
            'influence': 'Career foundation, parental influence, education period'
        },
        'day': {
            'name': 'Day Pillar',
            'chinese': '日柱',
            'represents': 'Self and spouse, middle age (33-48)',
            'influence': 'Marriage, personal identity, core self'
        },
        'hour': {
            'name': 'Hour Pillar',
            'chinese': '时柱',
            'represents': 'Children, later life (49+)',
            'influence': 'Children, legacy, later achievements, subconscious'
        }
    }
    
    for name, pillar in pillars.items():
        hidden_explanations = explain_hidden_stems(day_master, pillar.branch, pillar.hidden_stems)
        
        analysis[name] = {
            'pillar_info': pillar_meanings[name],
            'branch': pillar.branch,
            'branch_cn': EARTHLY_BRANCHES_CN[EARTHLY_BRANCHES.index(pillar.branch)],
            'animal': BRANCH_ANIMALS[EARTHLY_BRANCHES.index(pillar.branch)],
            'hidden_stems': hidden_explanations
        }
    
    return analysis


# =============================================================================
# 12 LIFE STAGES DISPLAY (十二长生)
# =============================================================================

TWELVE_STAGES_INFO = {
    '長生': {'pinyin': 'Chang Sheng', 'english': 'Growth', 'meaning': 'Birth of energy, new beginnings, fresh start', 'quality': 'Favorable'},
    '沐浴': {'pinyin': 'Mu Yu', 'english': 'Bath', 'meaning': 'Cleansing, vulnerability, exposed, romantic', 'quality': 'Unfavorable'},
    '冠帶': {'pinyin': 'Guan Dai', 'english': 'Youth', 'meaning': 'Coming of age, maturity approaching, preparation', 'quality': 'Favorable'},
    '臨官': {'pinyin': 'Lin Guan', 'english': 'Maturity', 'meaning': 'Career advancement, official position, authority', 'quality': 'Favorable'},
    '帝旺': {'pinyin': 'Di Wang', 'english': 'Prosperous', 'meaning': 'Peak power, maximum strength, emperor stage', 'quality': 'Favorable'},
    '衰': {'pinyin': 'Shuai', 'english': 'Weakening', 'meaning': 'Decline begins, energy reducing, caution needed', 'quality': 'Unfavorable'},
    '病': {'pinyin': 'Bing', 'english': 'Sickness', 'meaning': 'Illness, weakness, need for rest and recovery', 'quality': 'Unfavorable'},
    '死': {'pinyin': 'Si', 'english': 'Death', 'meaning': 'End of cycle, transformation, letting go', 'quality': 'Unfavorable'},
    '墓': {'pinyin': 'Mu', 'english': 'Grave', 'meaning': 'Storage, hidden resources, accumulation', 'quality': 'Neutral'},
    '絕': {'pinyin': 'Jue', 'english': 'Extinction', 'meaning': 'Complete end, void, spiritual transformation', 'quality': 'Unfavorable'},
    '胎': {'pinyin': 'Tai', 'english': 'Conceived', 'meaning': 'Conception, potential forming, planning stage', 'quality': 'Neutral'},
    '養': {'pinyin': 'Yang', 'english': 'Nourishing', 'meaning': 'Nurturing, preparation for birth, incubation', 'quality': 'Favorable'}
}

def get_twelve_stages_wheel(day_master: str) -> List[Dict]:
    """
    Get the 12 Life Stages wheel starting from Day Master's Growth position.
    Returns stages mapped to all 12 branches in order.
    """
    # Starting branch for Growth (長生) for each Day Master
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    
    start_branch = LIFE_STAGE_START.get(day_master, 'Yin')
    start_idx = EARTHLY_BRANCHES.index(start_branch)
    
    # Direction: Yang goes forward, Yin goes backward
    direction = 1 if dm_polarity == 'Yang' else -1
    
    wheel = []
    
    for i, stage_tuple in enumerate(TWELVE_STAGES):
        stage_cn, stage_pinyin, stage_english = stage_tuple
        
        branch_idx = (start_idx + (i * direction)) % 12
        branch = EARTHLY_BRANCHES[branch_idx]
        branch_cn = EARTHLY_BRANCHES_CN[branch_idx]
        animal = BRANCH_ANIMALS[branch_idx]
        
        stage_info = TWELVE_STAGES_INFO.get(stage_cn, {})
        
        wheel.append({
            'stage_cn': stage_cn,
            'stage_pinyin': stage_pinyin,
            'stage_english': stage_english,
            'meaning': stage_info.get('meaning', ''),
            'quality': stage_info.get('quality', 'Neutral'),
            'branch': branch,
            'branch_cn': branch_cn,
            'animal': animal,
            'position': i + 1
        })
    
    return wheel


# =============================================================================
# 6 ASPECTS CHART (六项分析)
# =============================================================================

SIX_ASPECTS_INFO = {
    'life_purpose': {
        'name': 'Life Purpose',
        'chinese': '事業',
        'description': 'Your mission, calling, and what drives you',
        'ten_gods': ['Direct Officer', 'Seven Killings'],
        'element': 'Fire'
    },
    'wealth': {
        'name': 'Wealth & Finance',
        'chinese': '財運',
        'description': 'Money, assets, and financial opportunities',
        'ten_gods': ['Direct Wealth', 'Indirect Wealth'],
        'element': 'Wood'
    },
    'relationship': {
        'name': 'Relationships',
        'chinese': '感情',
        'description': 'Marriage, romance, and partnerships',
        'ten_gods': ['Direct Wealth', 'Direct Officer'],  # DW for men, DO for women
        'element': 'Water'
    },
    'health': {
        'name': 'Health & Wellness',
        'chinese': '健康',
        'description': 'Physical vitality and mental wellbeing',
        'ten_gods': ['Friend', 'Rob Wealth'],
        'element': 'Metal'
    },
    'career': {
        'name': 'Career & Status',
        'chinese': '官位',
        'description': 'Professional advancement and social status',
        'ten_gods': ['Direct Officer', 'Seven Killings'],
        'element': 'Fire'
    },
    'creativity': {
        'name': 'Creativity & Output',
        'chinese': '創作',
        'description': 'Self-expression, children, and creative works',
        'ten_gods': ['Eating God', 'Hurting Officer'],
        'element': 'Water'
    }
}

def calculate_six_aspects(profile_counts: Dict[str, int], gender: str = 'male') -> Dict[str, Dict]:
    """
    Calculate the 6 Aspects scores based on Ten Gods distribution.
    """
    aspects = {}
    
    for aspect_key, info in SIX_ASPECTS_INFO.items():
        # Calculate score based on relevant ten gods
        score = sum(profile_counts.get(god, 0) for god in info['ten_gods'])
        
        # Normalize to percentage (assuming max possible is ~6)
        max_possible = 6
        percentage = min(100, (score / max_possible) * 100)
        
        aspects[aspect_key] = {
            'name': info['name'],
            'chinese': info['chinese'],
            'description': info['description'],
            'score': score,
            'percentage': round(percentage, 0),
            'element': info['element'],
            'strength': 'Strong' if percentage >= 60 else 'Moderate' if percentage >= 30 else 'Weak'
        }
    
    return aspects


# =============================================================================
# ANNUAL ANALYSIS (年度分析)
# =============================================================================

def calculate_annual_pillar(year: int) -> Dict:
    """
    Calculate the Annual Pillar for a given year.
    """
    # Stem cycle: starts with Jia (0) at year 4 (e.g., 1984, 1994, 2004)
    stem_idx = (year - 4) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    stem_cn = HEAVENLY_STEMS_CN[stem_idx]
    
    # Branch cycle: starts with Zi (0) at year 4 (e.g., 1984 = Rat)
    branch_idx = (year - 4) % 12
    branch = EARTHLY_BRANCHES[branch_idx]
    branch_cn = EARTHLY_BRANCHES_CN[branch_idx]
    animal = BRANCH_ANIMALS[branch_idx]
    
    hidden = HIDDEN_STEMS.get(branch, [])
    
    return {
        'year': year,
        'stem': stem,
        'stem_cn': stem_cn,
        'branch': branch,
        'branch_cn': branch_cn,
        'animal': animal,
        'element': STEM_ELEMENTS[stem],
        'polarity': STEM_POLARITY[stem],
        'hidden_stems': hidden,
        'chinese': f"{stem_cn}{branch_cn}"
    }


def calculate_annual_analysis(day_master: str, natal_profiles: Dict[str, int], year: int = 2026) -> Dict:
    """
    Calculate annual influence comparing natal chart to annual pillar.
    """
    annual_pillar = calculate_annual_pillar(year)
    
    # Calculate Ten Gods for annual stem and hidden stems
    annual_stem_god = get_ten_god(day_master, annual_pillar['stem'])
    annual_hidden_gods = [get_ten_god(day_master, hs) for hs in annual_pillar['hidden_stems']]
    
    # Calculate annual profile influence
    annual_profiles = {}
    for god in TEN_GODS_CN.keys():
        annual_profiles[god] = 0
    
    # Add annual stem (weight 2)
    annual_profiles[annual_stem_god] = annual_profiles.get(annual_stem_god, 0) + 2
    
    # Add hidden stems (weight 1 each)
    for god in annual_hidden_gods:
        annual_profiles[god] = annual_profiles.get(god, 0) + 1
    
    # Combine natal and annual for comparison
    combined_profiles = {}
    for god in TEN_GODS_CN.keys():
        natal_score = natal_profiles.get(god, 0)
        annual_score = annual_profiles.get(god, 0)
        combined_profiles[god] = {
            'natal': natal_score,
            'annual': annual_score,
            'combined': natal_score + annual_score
        }
    
    # Determine annual theme based on strongest annual gods
    annual_theme = max(annual_profiles.items(), key=lambda x: x[1])[0] if annual_profiles else 'Friend'
    
    return {
        'year': year,
        'pillar': annual_pillar,
        'stem_god': annual_stem_god,
        'hidden_gods': annual_hidden_gods,
        'profiles': combined_profiles,
        'theme': annual_theme,
        'theme_name': PROFILE_NAMES.get(annual_theme, annual_theme)
    }


# =============================================================================
# MONTHLY INFLUENCE (月度分析)
# =============================================================================

# Month stems follow 5-Tiger rule based on Year Stem
MONTH_STEM_START = {
    'Jia': 'Bing', 'Ji': 'Bing',    # 甲/己年 → 丙寅月始
    'Yi': 'Wu', 'Geng': 'Wu',       # 乙/庚年 → 戊寅月始
    'Bing': 'Geng', 'Xin': 'Geng',  # 丙/辛年 → 庚寅月始
    'Ding': 'Ren', 'Ren': 'Ren',    # 丁/壬年 → 壬寅月始
    'Wu': 'Jia', 'Gui': 'Jia'       # 戊/癸年 → 甲寅月始
}

MONTH_BRANCHES = ['Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai', 'Zi', 'Chou']

def calculate_monthly_influence(day_master: str, year: int = 2026) -> List[Dict]:
    """
    Calculate monthly pillars and their influence for a given year.
    """
    # Get year stem to determine month stem cycle
    annual_pillar = calculate_annual_pillar(year)
    year_stem = annual_pillar['stem']
    
    # Get starting month stem
    start_stem = MONTH_STEM_START.get(year_stem, 'Jia')
    start_stem_idx = HEAVENLY_STEMS.index(start_stem)
    
    months = []
    month_names = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    
    for i in range(12):
        stem_idx = (start_stem_idx + i) % 10
        stem = HEAVENLY_STEMS[stem_idx]
        stem_cn = HEAVENLY_STEMS_CN[stem_idx]
        
        branch = MONTH_BRANCHES[i]
        branch_idx = EARTHLY_BRANCHES.index(branch)
        branch_cn = EARTHLY_BRANCHES_CN[branch_idx]
        animal = BRANCH_ANIMALS[branch_idx]
        
        hidden = HIDDEN_STEMS.get(branch, [])
        
        # Calculate Ten Gods
        stem_god = get_ten_god(day_master, stem)
        hidden_gods = [(hs, get_ten_god(day_master, hs)) for hs in hidden]
        
        # Get life stage for this month
        stage = get_life_stage(day_master, branch)
        
        months.append({
            'month_num': i + 1,
            'month_name': month_names[i],
            'year': year if i < 11 else year + 1,  # Jan is next year
            'stem': stem,
            'stem_cn': stem_cn,
            'branch': branch,
            'branch_cn': branch_cn,
            'animal': animal,
            'element': STEM_ELEMENTS[stem],
            'chinese': f"{stem_cn}{branch_cn}",
            'stem_god': stem_god,
            'stem_god_cn': TEN_GODS_CN.get(stem_god, ''),
            'hidden_stems': hidden_gods,
            'life_stage': {
                'chinese': stage[0],
                'pinyin': stage[1],
                'english': stage[2]
            }
        })
    
    return months


# =============================================================================
# CURRENT LUCK PILLAR DETECTION
# =============================================================================

def get_current_luck_pillar(luck_pillars: List[Dict], birth_year: int, current_year: int = 2026) -> Dict:
    """
    Determine which luck pillar is currently active based on age.
    """
    age = current_year - birth_year
    
    current_pillar = None
    pillar_index = -1
    
    for i, lp in enumerate(luck_pillars):
        start_age = lp.get('start_age', 0)
        end_age = start_age + 9
        
        if start_age <= age <= end_age:
            current_pillar = lp
            pillar_index = i
            break
    
    return {
        'current_age': age,
        'pillar': current_pillar,
        'pillar_index': pillar_index,
        'years_remaining': (current_pillar.get('start_age', 0) + 10 - age) if current_pillar else 0
    }


# =============================================================================
# FIVE STRUCTURES (五型格)
# =============================================================================

FIVE_STRUCTURES_INFO = {
    'Wealth': {
        'element': 'Wood',
        'chinese': '財',
        'structure_name': '管理型',
        'english_name': 'Manager',
        'gods': ['Direct Wealth', 'Indirect Wealth'],
        'description': 'Wealth structure people are natural managers and entrepreneurs. They excel at identifying opportunities, managing resources, and creating value. Strong focus on financial success and material achievement.',
        'strengths': ['Business acumen', 'Resource management', 'Opportunity recognition', 'Practical decision-making'],
        'challenges': ['May prioritize money over relationships', 'Risk of overwork', 'Can be too materialistic'],
        'careers': ['Business owner', 'Manager', 'Investor', 'Sales', 'Real estate', 'Finance'],
        'advice': 'Balance wealth pursuit with relationships and personal fulfillment. Your ability to create value is a gift - use it wisely.'
    },
    'Influence': {
        'element': 'Fire',
        'chinese': '官',
        'structure_name': '忠誠型',
        'english_name': 'Supporters',
        'gods': ['Direct Officer', 'Seven Killings'],
        'description': 'Influence structure people are natural leaders with authority and charisma. They command respect and can mobilize others effectively. Strong sense of duty and responsibility.',
        'strengths': ['Leadership ability', 'Authority presence', 'Strategic thinking', 'Discipline'],
        'challenges': ['Can be too controlling', 'Pressure from responsibilities', 'May struggle with flexibility'],
        'careers': ['Government', 'Military', 'Law enforcement', 'Corporate executive', 'Politics', 'Judge'],
        'advice': 'Your natural authority attracts followers. Lead with integrity and remember that true power comes from serving others.'
    },
    'Resources': {
        'element': 'Earth',
        'chinese': '印',
        'structure_name': '智慧型',
        'english_name': 'Thinkers',
        'gods': ['Direct Resource', 'Indirect Resource'],
        'description': 'Resource structure people are deep thinkers and knowledge seekers. They excel at learning, analysis, and providing wisdom to others. Strong intellectual and spiritual orientation.',
        'strengths': ['Analytical thinking', 'Knowledge acquisition', 'Teaching ability', 'Patience'],
        'challenges': ['May overthink', 'Can be too passive', 'Risk of analysis paralysis'],
        'careers': ['Teacher', 'Professor', 'Researcher', 'Writer', 'Consultant', 'Spiritual guide'],
        'advice': 'Your wisdom is valuable - share it generously. Balance thinking with action, and trust your intuition alongside your analysis.'
    },
    'Companion': {
        'element': 'Metal',
        'chinese': '比',
        'structure_name': '交際型',
        'english_name': 'Connectors',
        'gods': ['Friend', 'Rob Wealth'],
        'description': 'Companion structure people are natural networkers and team players. They build strong relationships and thrive in collaborative environments. Strong sense of loyalty and camaraderie.',
        'strengths': ['Networking', 'Team building', 'Loyalty', 'Social intelligence'],
        'challenges': ['May be too dependent on others', 'Competition with peers', 'Boundary issues'],
        'careers': ['HR', 'Public relations', 'Team sports', 'Community organizing', 'Partnerships', 'Networking roles'],
        'advice': 'Your strength lies in connections. Choose your allies wisely and maintain healthy boundaries while building your network.'
    },
    'Output': {
        'element': 'Water',
        'chinese': '食',
        'structure_name': '創作型',
        'english_name': 'Creators',
        'gods': ['Eating God', 'Hurting Officer'],
        'description': 'Output structure people are natural creators and expressers. They have strong artistic abilities and need outlets for self-expression. Innovative and often unconventional.',
        'strengths': ['Creativity', 'Expression', 'Innovation', 'Artistic talent'],
        'challenges': ['May be too unconventional', 'Emotional sensitivity', 'Can be undisciplined'],
        'careers': ['Artist', 'Designer', 'Writer', 'Performer', 'Inventor', 'Content creator', 'Chef'],
        'advice': 'Your creative gifts are meant to be shared. Find healthy outlets for expression and dont let criticism dim your light.'
    }
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


# Map each Ten God to its corresponding Heavenly Stem (relative to Day Master)
def get_stem_for_ten_god(day_master: str, ten_god: str) -> str:
    """
    Get the Heavenly Stem that represents a specific Ten God for a given Day Master.
    """
    dm_element = STEM_ELEMENTS[day_master]
    dm_polarity = STEM_POLARITY[day_master]
    
    # Element relationships
    same = dm_element
    produces = PRODUCTIVE_CYCLE[dm_element]  # Output
    controls = CONTROLLING_CYCLE[dm_element]  # Wealth
    controlled_by = CONTROLLED_BY[dm_element]  # Power
    produced_by = PRODUCED_BY[dm_element]  # Resource
    
    # Find the stem based on Ten God type
    target_element = None
    same_polarity = True
    
    if ten_god == 'Friend':
        target_element, same_polarity = same, True
    elif ten_god == 'Rob Wealth':
        target_element, same_polarity = same, False
    elif ten_god == 'Eating God':
        target_element, same_polarity = produces, True
    elif ten_god == 'Hurting Officer':
        target_element, same_polarity = produces, False
    elif ten_god == 'Indirect Wealth':
        target_element, same_polarity = controls, True
    elif ten_god == 'Direct Wealth':
        target_element, same_polarity = controls, False
    elif ten_god == 'Seven Killings':
        target_element, same_polarity = controlled_by, True
    elif ten_god == 'Direct Officer':
        target_element, same_polarity = controlled_by, False
    elif ten_god == 'Indirect Resource':
        target_element, same_polarity = produced_by, True
    elif ten_god == 'Direct Resource':
        target_element, same_polarity = produced_by, False
    
    if not target_element:
        return ''
    
    # Find the stem with matching element and polarity
    target_pol = dm_polarity if same_polarity else ('Yin' if dm_polarity == 'Yang' else 'Yang')
    
    for stem in HEAVENLY_STEMS:
        if STEM_ELEMENTS[stem] == target_element and STEM_POLARITY[stem] == target_pol:
            return stem
    
    return ''


# 12 Life Stages percentage mapping (from strongest to weakest)
LIFE_STAGE_PERCENTAGES = {
    '帝旺': 100,  # Prosperous (Di Wang) - Peak
    '臨官': 90,   # Maturity (Lin Guan) - also called 祿 Lu/Thriving
    '冠帶': 80,   # Youth (Guan Dai)
    '沐浴': 70,   # Bath (Mu Yu)
    '長生': 60,   # Birth (Chang Sheng)
    '養': 50,     # Nourishing (Yang)
    '胎': 40,     # Conceived (Tai)
    '絕': 30,     # Extinction (Jue)
    '墓': 20,     # Grave (Mu)
    '死': 10,     # Death (Si)
    '病': 5,      # Sickness (Bing)
    '衰': 3,      # Weakening (Shuai)
}


def calculate_profile_percentages_joey_yap(pillars: Dict[str, Pillar]) -> Dict[str, float]:
    """
    Calculate profile percentages using Joey Yap's methodology.
    
    Analysis shows Joey Yap weights:
    - Hidden stems in Year/Month = highest weight (these are foundation)
    - Hidden stems in Day/Hour = medium weight
    - Visible stems = base weight
    
    The Main Profile is typically the one with most hidden stem presence
    in the Year/Month pillars (the "root" of the chart).
    """
    day_master = pillars['day'].stem
    
    # Initialize scores for each Ten God
    ten_gods = [
        'Direct Officer', 'Indirect Resource', 'Seven Killings', 'Direct Resource',
        'Friend', 'Eating God', 'Rob Wealth', 'Direct Wealth', 'Indirect Wealth', 'Hurting Officer'
    ]
    scores = {god: 0.0 for god in ten_gods}
    
    # Position weights - Joey Yap heavily weights Year/Month hidden stems
    position_weights = {
        'year_visible': 0.15,
        'month_visible': 0.15,
        'hour_visible': 0.15,
        'year_hidden_main': 0.25,
        'year_hidden_secondary': 0.12,
        'year_hidden_residual': 0.06,
        'month_hidden_main': 0.25,
        'month_hidden_secondary': 0.12,
        'month_hidden_residual': 0.06,
        'day_hidden_main': 0.10,
        'day_hidden_secondary': 0.05,
        'day_hidden_residual': 0.03,
        'hour_hidden_main': 0.12,
        'hour_hidden_secondary': 0.06,
        'hour_hidden_residual': 0.03,
    }
    
    # Score visible stems (excluding Day Master)
    for name in ['year', 'month', 'hour']:
        stem = pillars[name].stem
        god = get_ten_god(day_master, stem)
        scores[god] += position_weights[f'{name}_visible']
    
    # Score hidden stems with position weighting
    for name in ['year', 'month', 'day', 'hour']:
        hidden_stems = pillars[name].hidden_stems
        for i, stem in enumerate(hidden_stems):
            god = get_ten_god(day_master, stem)
            if i == 0:
                weight_key = f'{name}_hidden_main'
            elif i == 1:
                weight_key = f'{name}_hidden_secondary'
            else:
                weight_key = f'{name}_hidden_residual'
            scores[god] += position_weights.get(weight_key, 0.05)
    
    # Convert scores to percentages (normalize)
    max_score = max(scores.values()) if scores.values() else 1
    
    percentages = {}
    for god, score in scores.items():
        if score > 0 and max_score > 0:
            # Scale to 0-100, with highest around 98%
            pct = (score / max_score) * 98
            percentages[god] = round(pct, 0)
        else:
            percentages[god] = 0
    
    return percentages


def calculate_profile_percentages(profile_counts: Dict[str, int]) -> Dict[str, float]:
    """
    Calculate profile percentages using weighted scoring.
    This is a fallback method - prefer calculate_profile_percentages_joey_yap for accuracy.
    """
    total = sum(profile_counts.values())
    if total == 0:
        return {k: 0.0 for k in profile_counts}
    
    # Calculate base percentage
    percentages = {}
    max_possible = total
    
    for profile, count in profile_counts.items():
        if count > 0:
            base_pct = (count / max_possible) * 100
            scaled_pct = min(100, base_pct * (100 / max(profile_counts.values())) * (count / total))
            percentages[profile] = round(scaled_pct, 0)
        else:
            percentages[profile] = 0.0
    
    if percentages:
        max_pct = max(percentages.values())
        if max_pct > 0:
            scale_factor = 100 / max_pct
            for profile in percentages:
                if percentages[profile] > 0:
                    percentages[profile] = round(min(100, percentages[profile] * scale_factor * 0.98), 0)
    
    return percentages


def get_dominant_profile(profile_counts: Dict[str, int]) -> Tuple[str, str]:
    """Get the dominant profile based on counts (fallback method)"""
    if not profile_counts:
        return 'Unknown', 'Unknown'
    
    dominant = max(profile_counts, key=profile_counts.get)
    profile_name = PROFILE_NAMES.get(dominant, dominant)
    return dominant, profile_name


def get_dominant_profile_joey_yap(percentages: Dict[str, float]) -> Tuple[str, str]:
    """Get the dominant profile based on Joey Yap's percentage method"""
    if not percentages:
        return 'Unknown', 'Unknown'
    
    dominant = max(percentages, key=percentages.get)
    profile_name = PROFILE_NAMES.get(dominant, dominant)
    return dominant, profile_name


def calculate_symbolic_stars(pillars: Dict[str, Pillar]) -> Dict[str, any]:
    """
    Calculate all symbolic stars based on the chart.
    """
    day_stem = pillars['day'].stem
    day_branch = pillars['day'].branch
    year_branch = pillars['year'].branch
    month_stem = pillars['month'].stem
    month_branch = pillars['month'].branch
    hour_branch = pillars['hour'].branch
    
    # Noble People 贵人 - from Day Stem
    noble_branches = NOBLE_PEOPLE.get(day_stem, [])
    noble_animals = [BRANCH_ANIMALS[EARTHLY_BRANCHES.index(b)] for b in noble_branches]
    
    # Peach Blossom 桃花 - from Day Branch
    peach_branch = PEACH_BLOSSOM.get(day_branch, '')
    peach_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(peach_branch)] if peach_branch else ''
    
    # Intelligence 文昌 - from Day Stem
    intel_branch = INTELLIGENCE_STAR.get(day_stem, '')
    intel_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(intel_branch)] if intel_branch else ''
    
    # Sky Horse 驿马 - from Day Branch
    horse_branch = SKY_HORSE.get(day_branch, '')
    horse_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(horse_branch)] if horse_branch else ''
    
    # Solitary 孤辰 - from DAY Branch (not Year!)
    solitary_branch = SOLITARY_STAR.get(day_branch, '')
    solitary_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(solitary_branch)] if solitary_branch else ''
    
    # Conception Palace 胎元
    conception_stem, conception_branch = calculate_conception_palace(month_stem, month_branch)
    conception_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(conception_branch)]
    
    # Life Palace 命宫
    year_stem = pillars['year'].stem
    life_stem, life_branch = calculate_life_palace(year_stem, month_branch, hour_branch)
    life_animal = BRANCH_ANIMALS[EARTHLY_BRANCHES.index(life_branch)]
    
    return {
        'noble_people': {
            'branches': noble_branches,
            'animals': noble_animals,
            'chinese': '贵人'
        },
        'peach_blossom': {
            'branch': peach_branch,
            'animal': peach_animal,
            'chinese': '桃花'
        },
        'intelligence': {
            'branch': intel_branch,
            'animal': intel_animal,
            'chinese': '文昌'
        },
        'sky_horse': {
            'branch': horse_branch,
            'animal': horse_animal,
            'chinese': '驿马'
        },
        'solitary': {
            'branch': solitary_branch,
            'animal': solitary_animal,
            'chinese': '孤辰'
        },
        'conception_palace': {
            'stem': conception_stem,
            'branch': conception_branch,
            'animal': conception_animal,
            'chinese': '胎元',
            'full': f"{conception_stem} {conception_branch}"
        },
        'life_palace': {
            'stem': life_stem,
            'branch': life_branch,
            'animal': life_animal,
            'chinese': '命宫',
            'full': f"{life_stem} {life_branch}"
        }
    }


def calculate_life_stages_for_chart(pillars: Dict[str, Pillar]) -> Dict[str, Dict]:
    """
    Calculate 12 Life Stages for each pillar position.
    """
    stages = {}
    
    for name, pillar in pillars.items():
        stage = get_life_stage(pillar.stem, pillar.branch)
        stages[name] = {
            'chinese': stage[0],
            'pinyin': stage[1],
            'english': stage[2]
        }
    
    return stages


# =============================================================================
# GUA NUMBER CALCULATION (風水命卦)
# =============================================================================

def calculate_gua_number(birth_year: int, gender: str) -> int:
    """
    Calculate the Life Star / Gua Number (風水命卦).
    
    Formula for people born 1900-1999:
    - Male: (100 - last two digits) % 9, if 0 then 9, if 5 then 2
    - Female: (last two digits - 4) % 9, if 0 then 9, if 5 then 8
    
    Formula for people born 2000+:
    - Male: (100 - (year - 2000)) % 9, if 0 then 9, if 5 then 2
    - Female: ((year - 2000) + 6) % 9, if 0 then 9, if 5 then 8
    
    Ben's case: 1978, Male
    (100 - 78) % 9 = 22 % 9 = 4 ✓
    """
    is_male = gender.lower() == 'male'
    
    if birth_year >= 2000:
        year_offset = birth_year - 2000
        if is_male:
            gua = (100 - year_offset) % 9
        else:
            gua = (year_offset + 6) % 9
    else:
        last_two = birth_year % 100
        if is_male:
            gua = (100 - last_two) % 9
        else:
            gua = (last_two - 4) % 9
    
    # Handle special cases
    if gua == 0:
        gua = 9
    
    # Gua 5 doesn't exist - redirect
    if gua == 5:
        gua = 2 if is_male else 8
    
    return gua


def get_gua_info(gua_number: int) -> Dict:
    """Get detailed information about a Gua number."""
    return GUA_INFO.get(gua_number, GUA_INFO[1])


def calculate_eight_mansions(gua_number: int) -> Dict:
    """
    Calculate Eight Mansions directions for a given Gua.
    Returns favorable and unfavorable directions with details.
    """
    # Handle Gua 5 redirect
    if gua_number == 5:
        gua_number = 2  # Default to Kun for display
    
    directions = EIGHT_MANSIONS.get(gua_number, EIGHT_MANSIONS[1])
    
    favorable = []
    unfavorable = []
    
    for direction_name, compass in directions.items():
        info = DIRECTION_MEANINGS[direction_name].copy()
        info['compass'] = compass
        info['name'] = direction_name
        
        if info['type'] == 'Favorable':
            favorable.append(info)
        else:
            unfavorable.append(info)
    
    # Sort by rank
    favorable.sort(key=lambda x: x['rank'])
    unfavorable.sort(key=lambda x: x['rank'])
    
    return {
        'favorable': favorable,
        'unfavorable': unfavorable,
        'all_directions': directions
    }


# =============================================================================
# FIVE STRUCTURES CALCULATION (五型格)
# =============================================================================

def calculate_five_structures(profile_counts: Dict[str, int]) -> Dict[str, Dict]:
    """
    Calculate the Five Structures from Ten Gods distribution.
    
    Mapping:
    - Wood (財 Wealth) = Direct Wealth + Indirect Wealth
    - Fire (官 Influence) = Direct Officer + Seven Killings  
    - Earth (印 Resource) = Direct Resource + Indirect Resource
    - Metal (比 Companion) = Friend + Rob Wealth
    - Water (食 Output) = Eating God + Hurting Officer
    """
    structures = {
        'Wealth': {
            'score': profile_counts.get('Direct Wealth', 0) + profile_counts.get('Indirect Wealth', 0),
            'element': 'Wood',
            'chinese': '財',
            'structure_name': '管理型',
            'english_name': 'Manager'
        },
        'Influence': {
            'score': profile_counts.get('Direct Officer', 0) + profile_counts.get('Seven Killings', 0),
            'element': 'Fire',
            'chinese': '官',
            'structure_name': '忠誠型',
            'english_name': 'Supporters'
        },
        'Resources': {
            'score': profile_counts.get('Direct Resource', 0) + profile_counts.get('Indirect Resource', 0),
            'element': 'Earth',
            'chinese': '印',
            'structure_name': '智慧型',
            'english_name': 'Thinkers'
        },
        'Companion': {
            'score': profile_counts.get('Friend', 0) + profile_counts.get('Rob Wealth', 0),
            'element': 'Metal',
            'chinese': '比',
            'structure_name': '交際型',
            'english_name': 'Connectors'
        },
        'Output': {
            'score': profile_counts.get('Eating God', 0) + profile_counts.get('Hurting Officer', 0),
            'element': 'Water',
            'chinese': '食',
            'structure_name': '創作型',
            'english_name': 'Creators'
        }
    }
    
    # Calculate percentages (normalize to 100 for highest)
    max_score = max(s['score'] for s in structures.values()) if structures else 1
    if max_score == 0:
        max_score = 1
    
    for name, data in structures.items():
        data['percentage'] = round((data['score'] / max_score) * 100, 0) if max_score > 0 else 0
        data['info'] = FIVE_STRUCTURES_INFO.get(name, {})
    
    # Determine dominant structure
    dominant = max(structures.items(), key=lambda x: x[1]['score'])
    
    return {
        'structures': structures,
        'dominant': dominant[0],
        'dominant_info': FIVE_STRUCTURES_INFO.get(dominant[0], {}),
        'dominant_element': dominant[1]['element']
    }


# =============================================================================
# ANNUAL PILLAR CALCULATION
# =============================================================================

def calculate_annual_pillar(year: int) -> Dict:
    """
    Calculate the Annual Pillar for any given year.
    
    The cycle repeats every 60 years (Sexagenary cycle).
    Reference: 1984 = 甲子 Jia Zi (Wood Rat)
    
    2026 = 丙午 Bing Wu (Fire Horse)
    """
    # Reference year: 1984 = index 0 (Jia Zi)
    cycle_index = (year - 1984) % 60
    
    stem_index = cycle_index % 10
    branch_index = cycle_index % 12
    
    stem = HEAVENLY_STEMS[stem_index]
    stem_cn = HEAVENLY_STEMS_CN[stem_index]
    branch = EARTHLY_BRANCHES[branch_index]
    branch_cn = EARTHLY_BRANCHES_CN[branch_index]
    
    element = STEM_ELEMENTS[stem]
    polarity = STEM_POLARITY[stem]
    animal = BRANCH_ANIMALS[branch_index]
    hidden = HIDDEN_STEMS.get(branch, [])
    
    return {
        'year': year,
        'stem': stem,
        'stem_cn': stem_cn,
        'branch': branch,
        'branch_cn': branch_cn,
        'chinese': f"{stem_cn}{branch_cn}",
        'element': element,
        'polarity': polarity,
        'animal': animal,
        'hidden_stems': hidden,
        'description': f"{polarity} {element} {animal}"
    }


def analyze_annual_influence(natal_result: Dict, year: int) -> Dict:
    """
    Analyze how an annual pillar influences the natal chart.
    
    Returns comparison of:
    - Annual pillar details
    - Ten God relationship to Day Master
    - Impact on natal chart (clashes, combines)
    - Profile shift analysis
    """
    annual = calculate_annual_pillar(year)
    
    # Get Day Master from natal
    dm_stem = natal_result['day_master']['stem']
    dm_element = natal_result['day_master']['element']
    
    # Calculate Ten God for annual stem relative to Day Master
    annual_stem_god = get_ten_god(dm_stem, annual['stem'])
    
    # Calculate Ten Gods for annual hidden stems
    annual_hidden_gods = []
    for hs in annual['hidden_stems']:
        god = get_ten_god(dm_stem, hs)
        annual_hidden_gods.append({
            'stem': hs,
            'god': god,
            'chinese': TEN_GODS_CN.get(god, '')
        })
    
    # Check for clashes with natal branches
    natal_branches = [
        natal_result['four_pillars']['year']['branch'],
        natal_result['four_pillars']['month']['branch'],
        natal_result['four_pillars']['day']['branch'],
        natal_result['four_pillars']['hour']['branch']
    ]
    
    clashes = []
    for i, nb in enumerate(natal_branches):
        pillar_names = ['Year', 'Month', 'Day', 'Hour']
        if SIX_CLASHES.get(annual['branch']) == nb or SIX_CLASHES.get(nb) == annual['branch']:
            clashes.append({
                'natal_pillar': pillar_names[i],
                'natal_branch': nb,
                'annual_branch': annual['branch'],
                'description': f"{annual['animal']} clashes with {BRANCH_ANIMALS[EARTHLY_BRANCHES.index(nb)]}"
            })
    
    # Check for combines
    combines = []
    for i, nb in enumerate(natal_branches):
        pillar_names = ['Year', 'Month', 'Day', 'Hour']
        combine_result = SIX_COMBINES.get(annual['branch'])
        if combine_result and combine_result[0] == nb:
            combines.append({
                'natal_pillar': pillar_names[i],
                'natal_branch': nb,
                'annual_branch': annual['branch'],
                'result_element': combine_result[1],
                'description': f"{annual['animal']} combines with {BRANCH_ANIMALS[EARTHLY_BRANCHES.index(nb)]} → {combine_result[1]}"
            })
    
    # Determine if annual element is favorable or unfavorable
    useful_elements = natal_result['useful_gods']['useful']
    unfavorable_elements = natal_result['useful_gods']['unfavorable']
    
    annual_element = annual['element']
    is_favorable = annual_element in useful_elements
    is_unfavorable = annual_element in unfavorable_elements
    
    # Calculate annual profile influence (how annual changes the Ten Gods distribution)
    # This simulates adding the annual pillar to the natal chart
    annual_profiles = {}
    annual_profiles[annual_stem_god] = annual_profiles.get(annual_stem_god, 0) + 1
    for hg in annual_hidden_gods:
        annual_profiles[hg['god']] = annual_profiles.get(hg['god'], 0) + 1
    
    # Generate interpretation
    interpretation = generate_annual_interpretation(
        natal_result, annual, annual_stem_god, 
        is_favorable, is_unfavorable, clashes, combines
    )
    
    return {
        'annual_pillar': annual,
        'annual_stem_god': {
            'god': annual_stem_god,
            'chinese': TEN_GODS_CN.get(annual_stem_god, ''),
            'profile_name': PROFILE_NAMES.get(annual_stem_god, '')
        },
        'annual_hidden_gods': annual_hidden_gods,
        'element_analysis': {
            'annual_element': annual_element,
            'is_favorable': is_favorable,
            'is_unfavorable': is_unfavorable,
            'useful_elements': useful_elements,
            'unfavorable_elements': unfavorable_elements
        },
        'interactions': {
            'clashes': clashes,
            'combines': combines
        },
        'annual_profiles': annual_profiles,
        'interpretation': interpretation
    }


def generate_annual_interpretation(natal: Dict, annual: Dict, annual_god: str,
                                   is_favorable: bool, is_unfavorable: bool,
                                   clashes: list, combines: list) -> Dict:
    """Generate human-readable interpretation of annual influence."""
    
    dm_element = natal['day_master']['element']
    dm_strength = natal['day_master']['strength_category']
    annual_element = annual['element']
    
    # Overall rating
    if is_favorable and not clashes:
        rating = "Favorable"
        rating_emoji = "🟢"
        rating_score = 8
    elif is_unfavorable and clashes:
        rating = "Challenging"
        rating_emoji = "🔴"
        rating_score = 3
    elif clashes:
        rating = "Mixed - Watch for Conflicts"
        rating_emoji = "🟡"
        rating_score = 5
    elif combines:
        rating = "Harmonious"
        rating_emoji = "🟢"
        rating_score = 7
    else:
        rating = "Neutral"
        rating_emoji = "🟡"
        rating_score = 5
    
    # Element relationship description
    element_desc = ""
    if annual_element == dm_element:
        element_desc = f"The {annual_element} year brings similar energy to your {dm_element} Day Master - a year of peer connections and competition."
    elif annual_element in PRODUCTIVE_CYCLE and PRODUCTIVE_CYCLE[annual_element] == dm_element:
        element_desc = f"{annual_element} produces {dm_element} - this year brings support and resources to strengthen you."
    elif annual_element in CONTROLLING_CYCLE and CONTROLLING_CYCLE[annual_element] == dm_element:
        element_desc = f"{annual_element} controls {dm_element} - this year brings pressure, authority figures, and potential career opportunities."
    elif dm_element in PRODUCTIVE_CYCLE and PRODUCTIVE_CYCLE[dm_element] == annual_element:
        element_desc = f"Your {dm_element} produces {annual_element} - a year of output, expression, and creativity."
    elif dm_element in CONTROLLING_CYCLE and CONTROLLING_CYCLE[dm_element] == annual_element:
        element_desc = f"Your {dm_element} controls {annual_element} - a year of wealth opportunities and resource management."
    
    # God-specific interpretation
    god_interpretations = {
        'Direct Wealth': "Focus on stable income, managing assets, and financial planning. Good for traditional business and investments.",
        'Indirect Wealth': "Opportunities for windfall gains, side income, and speculative investments. Be alert to unexpected opportunities.",
        'Direct Officer': "Career advancement, recognition from authority, and taking on leadership roles. Good for promotions and official matters.",
        'Seven Killings': "Competitive pressure, need for decisive action. Good for bold moves and overcoming obstacles.",
        'Direct Resource': "Learning, certifications, and support from mentors. Good for education and self-improvement.",
        'Indirect Resource': "Unconventional learning, intuition, and spiritual growth. Good for creative problem-solving.",
        'Friend': "Collaboration, partnerships, and peer support. Good for teamwork but watch for competition.",
        'Rob Wealth': "Competition for resources, need to protect assets. Be cautious with partnerships.",
        'Eating God': "Creative expression, enjoyment, and leisure. Good for artistic pursuits and relaxation.",
        'Hurting Officer': "Breaking conventions, innovation, and speaking out. Good for change but watch your words."
    }
    
    god_desc = god_interpretations.get(annual_god, "")
    
    # Clash/Combine specific advice
    interaction_advice = ""
    if clashes:
        clash_pillars = [c['natal_pillar'] for c in clashes]
        interaction_advice = f"⚠️ The annual {annual['animal']} clashes with your {', '.join(clash_pillars)} pillar(s). "
        if 'Year' in clash_pillars:
            interaction_advice += "Watch your social relationships and public image. "
        if 'Month' in clash_pillars:
            interaction_advice += "Career changes possible - prepare for transitions. "
        if 'Day' in clash_pillars:
            interaction_advice += "Personal relationships need extra care. Health attention advised. "
        if 'Hour' in clash_pillars:
            interaction_advice += "Children/subordinates may face challenges. Investment caution advised. "
    elif combines:
        combine_pillars = [c['natal_pillar'] for c in combines]
        interaction_advice = f"✨ The annual {annual['animal']} harmonizes with your {', '.join(combine_pillars)} pillar(s), bringing smooth energy and opportunities."
    
    return {
        'rating': rating,
        'rating_emoji': rating_emoji,
        'rating_score': rating_score,
        'element_description': element_desc,
        'god_description': god_desc,
        'interaction_advice': interaction_advice,
        'summary': f"{rating_emoji} {annual['year']} is a **{rating}** year for you. {element_desc}"
    }

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
    
    # Ten Profiles - use Joey Yap's 12 Life Stages method
    profiles = calculate_ten_profiles(pillars)
    profile_percentages = calculate_profile_percentages_joey_yap(pillars)
    dominant_god, profile_name = get_dominant_profile_joey_yap(profile_percentages)
    
    # Luck Pillars
    year_polarity = pillars['year'].polarity
    luck_direction = get_luck_direction(gender, year_polarity)
    luck_pillars = calculate_luck_pillars(pillars, birth_date, gender)
    
    # Interactions
    clashes = detect_clashes(pillars)
    combines = detect_combines(pillars)
    harmonies = detect_three_harmony(pillars)
    
    # Symbolic Stars (NEW)
    symbolic_stars = calculate_symbolic_stars(pillars)
    
    # Life Stages (NEW)
    life_stages = calculate_life_stages_for_chart(pillars)
    
    # Celestial Animal (from Year Branch)
    year_branch_idx = EARTHLY_BRANCHES.index(pillars['year'].branch)
    celestial_animal = BRANCH_ANIMALS[year_branch_idx]
    
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
            'percentages': profile_percentages,
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
        },
        'symbolic_stars': symbolic_stars,
        'life_stages': life_stages,
        'celestial_animal': {
            'branch': pillars['year'].branch,
            'animal': celestial_animal,
            'chinese': '生肖'
        },
        # NEW: Life Star / Gua
        'life_star': {
            'gua_number': calculate_gua_number(birth_date.year, gender),
            'gua_info': get_gua_info(calculate_gua_number(birth_date.year, gender))
        },
        # NEW: Eight Mansions
        'eight_mansions': calculate_eight_mansions(calculate_gua_number(birth_date.year, gender)),
        # NEW: Five Structures
        'five_structures': calculate_five_structures(profiles),
        # NEW: Hidden Stems Analysis with explanations
        'hidden_stems_analysis': get_pillar_hidden_stem_analysis(pillars, day_master),
        # NEW: 12 Life Stages Wheel
        'twelve_stages_wheel': get_twelve_stages_wheel(day_master),
        # NEW: 6 Aspects Chart
        'six_aspects': calculate_six_aspects(profiles, gender),
        # NEW: Annual Analysis
        'annual_analysis': calculate_annual_analysis(day_master, profiles, 2026),
        # NEW: Monthly Influence
        'monthly_influence': calculate_monthly_influence(day_master, 2026),
        # NEW: Current Luck Pillar
        'current_luck': get_current_luck_pillar([lp.to_dict() for lp in luck_pillars], birth_date.year, 2026)
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
    print("BAZI CALCULATOR TEST - v10.7")
    print("=" * 60)
    print(f"\nFour Pillars:")
    for name in ['year', 'month', 'day', 'hour']:
        p = result['four_pillars'][name]
        print(f"  {name.title():6} | {p['stem']:4} {p['branch']:5} | {p['chinese']} | {p['animal']}")
        print(f"         Hidden: {', '.join(p['hidden_stems'])}")
    
    print(f"\nDay Master: {result['day_master']['stem']} ({result['day_master']['element']})")
    print(f"Strength: {result['day_master']['strength_pct']}% ({result['day_master']['strength_category']})")
    print(f"\nUseful: {', '.join(result['useful_gods']['useful'])}")
    print(f"Unfavorable: {', '.join(result['useful_gods']['unfavorable'])}")
    
    print(f"\n--- Ten Profiles ---")
    print(f"Dominant: {result['profiles']['dominant']} ({result['profiles']['profile_name']})")
    print(f"\nCounts:")
    for god, count in sorted(result['profiles']['counts'].items(), key=lambda x: -x[1]):
        if count > 0:
            pct = result['profiles']['percentages'].get(god, 0)
            print(f"  {god:20} | {count} | {pct:.0f}%")
    
    print(f"\n--- Luck Pillars ({result['luck_pillars']['direction']}, Start Age {result['luck_pillars']['start_age']}) ---")
    for lp in result['luck_pillars']['pillars'][:6]:
        print(f"  {lp['age_range']:8} | {lp['chinese']} | {lp['animal']}")
    
    print(f"\n--- Symbolic Stars ---")
    stars = result['symbolic_stars']
    print(f"  Celestial Animal: {result['celestial_animal']['animal']} ({result['celestial_animal']['branch']})")
    print(f"  Noble People: {', '.join(stars['noble_people']['animals'])} ({', '.join(stars['noble_people']['branches'])})")
    print(f"  Peach Blossom: {stars['peach_blossom']['animal']} ({stars['peach_blossom']['branch']})")
    print(f"  Intelligence: {stars['intelligence']['animal']} ({stars['intelligence']['branch']})")
    print(f"  Sky Horse: {stars['sky_horse']['animal']} ({stars['sky_horse']['branch']})")
    print(f"  Solitary: {stars['solitary']['animal']} ({stars['solitary']['branch']})")
    print(f"  Life Palace: {stars['life_palace']['full']} ({stars['life_palace']['animal']})")
    print(f"  Conception: {stars['conception_palace']['full']} ({stars['conception_palace']['animal']})")
    
    print(f"\n--- Life Stages ---")
    for name, stage in result['life_stages'].items():
        print(f"  {name.title():6} | {stage['chinese']} {stage['english']}")
    
    print("\n" + "=" * 60)
    print("EXPECTED (Joey Yap):")
    print("=" * 60)
    print("  Main Profile: The Diplomat (Direct Officer) 正官格")
    print("  Noble People: Goat (未), Ox (丑)")
    print("  Peach Blossom: Rooster (酉)")
    print("  Intelligence: Pig (亥)")
    print("  Sky Horse: Tiger (寅)")
    print("  Solitary: Pig (亥)")
    print("  Life Palace: 甲子 Jia Zi (Rat)")
    print("  Conception: 己酉 Ji You (Rooster)")
