# -*- coding: utf-8 -*-
"""
Ming Qimen 明奇门 - QMDJ Engine v6.0
Complete QMDJ calculations with all indicators

Features:
- QMDJ Four Pillars (from chart time, NOT user's BaZi)
- Death & Emptiness (空亡)
- Lead Stem Palace (值符宫)
- Lead Door / Envoy (直使)
- Lead Star (直符)
- Horse Star (驿马)
- Day/Hour Nobleman (贵人)
- Ju Number (局数)
- Structure (Yin/Yang Dun)
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
import math

# ============================================================================
# TIMEZONE
# ============================================================================
SGT = timezone(timedelta(hours=8))  # Singapore/China timezone

# ============================================================================
# CONSTANTS - STEMS & BRANCHES
# ============================================================================

HEAVENLY_STEMS = ["Jia 甲", "Yi 乙", "Bing 丙", "Ding 丁", "Wu 戊", 
                  "Ji 己", "Geng 庚", "Xin 辛", "Ren 壬", "Gui 癸"]

EARTHLY_BRANCHES = ["Zi 子", "Chou 丑", "Yin 寅", "Mao 卯", "Chen 辰", "Si 巳",
                    "Wu 午", "Wei 未", "Shen 申", "You 酉", "Xu 戌", "Hai 亥"]

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

BRANCH_ELEMENTS = {
    "Zi": "Water", "Chou": "Earth", "Yin": "Wood", "Mao": "Wood",
    "Chen": "Earth", "Si": "Fire", "Wu": "Fire", "Wei": "Earth",
    "Shen": "Metal", "You": "Metal", "Xu": "Earth", "Hai": "Water"
}

# Chinese hour mapping (each Chinese hour = 2 Western hours)
CHINESE_HOURS = {
    (23, 1): ("Zi 子", 0),    # 23:00-00:59
    (1, 3): ("Chou 丑", 1),   # 01:00-02:59
    (3, 5): ("Yin 寅", 2),    # 03:00-04:59
    (5, 7): ("Mao 卯", 3),    # 05:00-06:59
    (7, 9): ("Chen 辰", 4),   # 07:00-08:59
    (9, 11): ("Si 巳", 5),    # 09:00-10:59
    (11, 13): ("Wu 午", 6),   # 11:00-12:59
    (13, 15): ("Wei 未", 7),  # 13:00-14:59
    (15, 17): ("Shen 申", 8), # 15:00-16:59
    (17, 19): ("You 酉", 9),  # 17:00-18:59
    (19, 21): ("Xu 戌", 10),  # 19:00-20:59
    (21, 23): ("Hai 亥", 11), # 21:00-22:59
}

# ============================================================================
# PALACE CONSTANTS
# ============================================================================

PALACE_INFO = {
    1: {"name": "Kan", "chinese": "坎", "direction": "N", "element": "Water", "trigram": "☵"},
    2: {"name": "Kun", "chinese": "坤", "direction": "SW", "element": "Earth", "trigram": "☷"},
    3: {"name": "Zhen", "chinese": "震", "direction": "E", "element": "Wood", "trigram": "☳"},
    4: {"name": "Xun", "chinese": "巽", "direction": "SE", "element": "Wood", "trigram": "☴"},
    5: {"name": "Center", "chinese": "中", "direction": "C", "element": "Earth", "trigram": ""},
    6: {"name": "Qian", "chinese": "乾", "direction": "NW", "element": "Metal", "trigram": "☰"},
    7: {"name": "Dui", "chinese": "兑", "direction": "W", "element": "Metal", "trigram": "☱"},
    8: {"name": "Gen", "chinese": "艮", "direction": "NE", "element": "Earth", "trigram": "☶"},
    9: {"name": "Li", "chinese": "离", "direction": "S", "element": "Fire", "trigram": "☲"}
}

# Luoshu grid positions (for display)
LUOSHU_GRID = [
    [4, 9, 2],  # Top row: SE, S, SW
    [3, 5, 7],  # Middle: E, Center, W
    [8, 1, 6]   # Bottom: NE, N, NW
]

# ============================================================================
# QMDJ COMPONENTS - STARS, DOORS, DEITIES
# ============================================================================

# Nine Stars (九星) - Joey Yap terminology
NINE_STARS = {
    1: {"name": "Canopy", "chinese": "天蓬", "element": "Water", "nature": "Inauspicious"},
    2: {"name": "Grass", "chinese": "天芮", "element": "Earth", "nature": "Inauspicious"},
    3: {"name": "Impulse", "chinese": "天冲", "element": "Wood", "nature": "Auspicious"},
    4: {"name": "Assistant", "chinese": "天辅", "element": "Wood", "nature": "Auspicious"},
    5: {"name": "Connect", "chinese": "天禽", "element": "Earth", "nature": "Neutral"},
    6: {"name": "Heart", "chinese": "天心", "element": "Metal", "nature": "Auspicious"},
    7: {"name": "Pillar", "chinese": "天柱", "element": "Metal", "nature": "Neutral"},
    8: {"name": "Ren", "chinese": "天任", "element": "Earth", "nature": "Auspicious"},
    9: {"name": "Hero", "chinese": "天英", "element": "Fire", "nature": "Neutral"}
}

# Eight Doors (八门)
EIGHT_DOORS = {
    1: {"name": "Rest", "chinese": "休门", "element": "Water", "nature": "Auspicious"},
    2: {"name": "Death", "chinese": "死门", "element": "Earth", "nature": "Inauspicious"},
    3: {"name": "Harm", "chinese": "伤门", "element": "Wood", "nature": "Inauspicious"},
    4: {"name": "Delusion", "chinese": "杜门", "element": "Wood", "nature": "Neutral"},
    5: {"name": "Center", "chinese": "中门", "element": "Earth", "nature": "Neutral"},
    6: {"name": "Open", "chinese": "开门", "element": "Metal", "nature": "Auspicious"},
    7: {"name": "Fear", "chinese": "惊门", "element": "Metal", "nature": "Inauspicious"},
    8: {"name": "Life", "chinese": "生门", "element": "Earth", "nature": "Auspicious"},
    9: {"name": "Scenery", "chinese": "景门", "element": "Fire", "nature": "Neutral"}
}

# Eight Deities (八神)
EIGHT_DEITIES = {
    1: {"name": "Chief", "chinese": "值符", "nature": "Auspicious", "function": "Authority, leadership"},
    2: {"name": "Serpent", "chinese": "腾蛇", "nature": "Inauspicious", "function": "Worry, entanglement"},
    3: {"name": "Moon", "chinese": "太阴", "nature": "Auspicious", "function": "Hidden help, secrets"},
    4: {"name": "Six Harmony", "chinese": "六合", "nature": "Auspicious", "function": "Cooperation, agreements"},
    5: {"name": "Hook", "chinese": "勾陈", "nature": "Neutral", "function": "Delays, obstacles"},
    6: {"name": "Tiger", "chinese": "白虎", "nature": "Inauspicious", "function": "Danger, aggression"},
    7: {"name": "Emptiness", "chinese": "玄武", "nature": "Inauspicious", "function": "Deception, loss"},
    8: {"name": "Nine Earth", "chinese": "九地", "nature": "Auspicious", "function": "Stability, hiding"},
    9: {"name": "Nine Heaven", "chinese": "九天", "nature": "Auspicious", "function": "Expansion, boldness"}
}

# ============================================================================
# DEATH & EMPTINESS (空亡) CALCULATION
# ============================================================================

# The 60 Jiazi cycle is divided into 6 groups of 10
# Each group has 2 "empty" branches (the ones not paired with stems)
DEATH_EMPTINESS_MAP = {
    # Stems 0-9 paired with branches 0-9 → branches 10,11 are empty
    "Jia-Zi": ["Xu", "Hai"],      # 甲子旬: 戌亥空
    "Jia-Xu": ["Shen", "You"],    # 甲戌旬: 申酉空
    "Jia-Shen": ["Wu", "Wei"],    # 甲申旬: 午未空
    "Jia-Wu": ["Chen", "Si"],     # 甲午旬: 辰巳空
    "Jia-Chen": ["Yin", "Mao"],   # 甲辰旬: 寅卯空
    "Jia-Yin": ["Zi", "Chou"],    # 甲寅旬: 子丑空
}

def get_jiazi_cycle(stem_idx: int, branch_idx: int) -> str:
    """Determine which Jiazi cycle (旬) a stem-branch combination belongs to"""
    # Calculate the start of the current 10-day cycle
    diff = (branch_idx - stem_idx) % 12
    
    if diff == 0:
        return "Jia-Zi"
    elif diff == 10:
        return "Jia-Xu"
    elif diff == 8:
        return "Jia-Shen"
    elif diff == 6:
        return "Jia-Wu"
    elif diff == 4:
        return "Jia-Chen"
    elif diff == 2:
        return "Jia-Yin"
    else:
        # Fallback - calculate based on stem
        return "Jia-Zi"

def calculate_death_emptiness(day_stem: str, day_branch: str) -> Dict:
    """
    Calculate Death & Emptiness (空亡) for a given day pillar.
    
    Returns dict with:
    - empty_branches: List of 2 branches that are "empty"
    - affected_palaces: List of palace numbers affected
    """
    # Get indices
    stem_name = day_stem.split()[0] if " " in day_stem else day_stem
    branch_name = day_branch.split()[0] if " " in day_branch else day_branch
    
    stem_names = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    branch_names = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
    
    try:
        stem_idx = stem_names.index(stem_name)
        branch_idx = branch_names.index(branch_name)
    except ValueError:
        return {"empty_branches": [], "affected_palaces": [], "cycle": "Unknown"}
    
    # Find the Jiazi cycle
    cycle = get_jiazi_cycle(stem_idx, branch_idx)
    empty_branches = DEATH_EMPTINESS_MAP.get(cycle, [])
    
    # Map empty branches to palaces
    branch_to_palace = {
        "Zi": 1, "Chou": 8, "Yin": 8, "Mao": 3, "Chen": 4, "Si": 4,
        "Wu": 9, "Wei": 2, "Shen": 2, "You": 7, "Xu": 6, "Hai": 6
    }
    
    affected_palaces = []
    for branch in empty_branches:
        if branch in branch_to_palace:
            palace = branch_to_palace[branch]
            if palace not in affected_palaces:
                affected_palaces.append(palace)
    
    return {
        "empty_branches": empty_branches,
        "empty_branches_chinese": [f"{b} {branch_names.index(b)+1}" for b in empty_branches],
        "affected_palaces": affected_palaces,
        "cycle": cycle,
        "cycle_chinese": cycle.replace("Jia", "甲").replace("-", "").replace("Zi", "子").replace("Xu", "戌").replace("Shen", "申").replace("Wu", "午").replace("Chen", "辰").replace("Yin", "寅")
    }

# ============================================================================
# HORSE STAR (驿马) CALCULATION
# ============================================================================

HORSE_STAR_MAP = {
    # Year/Day branch group → Horse Star location
    "Yin-Wu-Xu": "Shen",    # 寅午戌 → 申 (Tiger, Horse, Dog → Monkey)
    "Shen-Zi-Chen": "Yin",  # 申子辰 → 寅 (Monkey, Rat, Dragon → Tiger)
    "Si-You-Chou": "Hai",   # 巳酉丑 → 亥 (Snake, Rooster, Ox → Pig)
    "Hai-Mao-Wei": "Si",    # 亥卯未 → 巳 (Pig, Rabbit, Goat → Snake)
}

def calculate_horse_star(year_branch: str) -> Dict:
    """
    Calculate Horse Star (驿马) position based on year branch.
    Horse Star indicates travel, mobility, fast results.
    """
    branch_name = year_branch.split()[0] if " " in year_branch else year_branch
    
    # Determine which group
    if branch_name in ["Yin", "Wu", "Xu"]:
        horse_branch = "Shen"
        group = "Yin-Wu-Xu"
    elif branch_name in ["Shen", "Zi", "Chen"]:
        horse_branch = "Yin"
        group = "Shen-Zi-Chen"
    elif branch_name in ["Si", "You", "Chou"]:
        horse_branch = "Hai"
        group = "Si-You-Chou"
    elif branch_name in ["Hai", "Mao", "Wei"]:
        horse_branch = "Si"
        group = "Hai-Mao-Wei"
    else:
        return {"horse_branch": None, "horse_palace": None, "group": None}
    
    # Map branch to palace
    branch_to_palace = {
        "Shen": 2, "Yin": 8, "Hai": 6, "Si": 4
    }
    
    branch_chinese = {
        "Shen": "申", "Yin": "寅", "Hai": "亥", "Si": "巳"
    }
    
    return {
        "horse_branch": horse_branch,
        "horse_branch_chinese": branch_chinese.get(horse_branch, ""),
        "horse_palace": branch_to_palace.get(horse_branch),
        "group": group,
        "meaning": "Travel, mobility, fast results in this palace"
    }

# ============================================================================
# NOBLEMAN STAR (贵人) CALCULATION
# ============================================================================

# Day Nobleman based on Day Stem
DAY_NOBLEMAN_MAP = {
    "Jia": ["Chou", "Wei"],   # 甲 → 丑未
    "Yi": ["Zi", "Shen"],     # 乙 → 子申
    "Bing": ["Hai", "You"],   # 丙 → 亥酉
    "Ding": ["Hai", "You"],   # 丁 → 亥酉
    "Wu": ["Chou", "Wei"],    # 戊 → 丑未
    "Ji": ["Zi", "Shen"],     # 己 → 子申
    "Geng": ["Chou", "Wei"],  # 庚 → 丑未
    "Xin": ["Yin", "Wu"],     # 辛 → 寅午
    "Ren": ["Mao", "Si"],     # 壬 → 卯巳
    "Gui": ["Mao", "Si"],     # 癸 → 卯巳
}

def calculate_nobleman(day_stem: str, hour_stem: str = None) -> Dict:
    """
    Calculate Nobleman Stars (贵人) based on Day and Hour stems.
    Nobleman indicates helpful people, support, guidance.
    """
    stem_name = day_stem.split()[0] if " " in day_stem else day_stem
    
    day_nobleman_branches = DAY_NOBLEMAN_MAP.get(stem_name, [])
    
    # Map branches to palaces
    branch_to_palace = {
        "Zi": 1, "Chou": 8, "Yin": 8, "Mao": 3, "Chen": 4, "Si": 4,
        "Wu": 9, "Wei": 2, "Shen": 2, "You": 7, "Xu": 6, "Hai": 6
    }
    
    branch_chinese = {
        "Zi": "子", "Chou": "丑", "Yin": "寅", "Mao": "卯", "Chen": "辰", "Si": "巳",
        "Wu": "午", "Wei": "未", "Shen": "申", "You": "酉", "Xu": "戌", "Hai": "亥"
    }
    
    day_nobleman_palaces = [branch_to_palace.get(b) for b in day_nobleman_branches if b in branch_to_palace]
    
    result = {
        "day_nobleman_branches": day_nobleman_branches,
        "day_nobleman_chinese": [branch_chinese.get(b, "") for b in day_nobleman_branches],
        "day_nobleman_palaces": day_nobleman_palaces,
        "meaning": "Palaces with Nobleman bring helpful people and support"
    }
    
    # Hour nobleman (if hour stem provided)
    if hour_stem:
        hour_stem_name = hour_stem.split()[0] if " " in hour_stem else hour_stem
        hour_nobleman_branches = DAY_NOBLEMAN_MAP.get(hour_stem_name, [])
        hour_nobleman_palaces = [branch_to_palace.get(b) for b in hour_nobleman_branches if b in branch_to_palace]
        result["hour_nobleman_branches"] = hour_nobleman_branches
        result["hour_nobleman_palaces"] = hour_nobleman_palaces
    
    return result

# ============================================================================
# QMDJ FOUR PILLARS CALCULATION (Chart Time, NOT BaZi)
# ============================================================================

def calculate_year_pillar(year: int) -> Tuple[str, str]:
    """Calculate Year Pillar stem and branch"""
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_month_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """
    Calculate Month Pillar using solar terms (simplified).
    Note: For production, should use actual solar term dates.
    """
    # Simplified: Use month directly (solar month starts ~4-6th)
    # Adjust if before ~5th of month
    solar_month = month
    if day < 5:
        solar_month = month - 1 if month > 1 else 12
    
    # Branch: Tiger (Yin) is month 1, etc.
    branch_idx = (solar_month + 1) % 12  # Month 1 = Yin (index 2)
    
    # Stem: Based on year stem
    year_stem_idx = (year - 4) % 10
    # Formula: (year_stem % 5) * 2 + month
    stem_idx = ((year_stem_idx % 5) * 2 + solar_month) % 10
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_day_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """
    Calculate Day Pillar using the standard formula.
    Reference date: Jan 1, 1900 was Jia-Chen (甲辰)
    """
    from datetime import date
    ref_date = date(1900, 1, 1)
    target_date = date(year, month, day)
    days_diff = (target_date - ref_date).days
    
    # Jan 1, 1900 was Stem index 0 (Jia), Branch index 4 (Chen)
    stem_idx = (days_diff + 0) % 10
    branch_idx = (days_diff + 4) % 12
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]

def calculate_hour_pillar(day_stem: str, hour: int) -> Tuple[str, str]:
    """
    Calculate Hour Pillar based on day stem and hour.
    """
    # Find Chinese hour branch
    hour_branch_idx = 0
    hour_branch_name = "Zi 子"
    
    for (start, end), (branch, idx) in CHINESE_HOURS.items():
        if start == 23:
            if hour >= 23 or hour < end:
                hour_branch_idx = idx
                hour_branch_name = branch
                break
        elif start <= hour < end:
            hour_branch_idx = idx
            hour_branch_name = branch
            break
    
    # Calculate hour stem based on day stem
    day_stem_name = day_stem.split()[0] if " " in day_stem else day_stem
    stem_names = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    
    try:
        day_stem_idx = stem_names.index(day_stem_name)
    except ValueError:
        day_stem_idx = 0
    
    # Hour stem formula
    hour_stem_idx = ((day_stem_idx % 5) * 2 + hour_branch_idx) % 10
    
    return HEAVENLY_STEMS[hour_stem_idx], EARTHLY_BRANCHES[hour_branch_idx]

def calculate_qmdj_pillars(dt: datetime) -> Dict:
    """
    Calculate all Four Pillars for a QMDJ chart time.
    This is different from natal BaZi - these are the pillars of the moment being analyzed.
    """
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    
    year_stem, year_branch = calculate_year_pillar(year)
    month_stem, month_branch = calculate_month_pillar(year, month, day)
    day_stem, day_branch = calculate_day_pillar(year, month, day)
    hour_stem, hour_branch = calculate_hour_pillar(day_stem, hour)
    
    return {
        "Year": {
            "stem": year_stem,
            "branch": year_branch,
            "stem_element": STEM_ELEMENTS.get(year_stem.split()[0], ""),
            "branch_element": BRANCH_ELEMENTS.get(year_branch.split()[0], "")
        },
        "Month": {
            "stem": month_stem,
            "branch": month_branch,
            "stem_element": STEM_ELEMENTS.get(month_stem.split()[0], ""),
            "branch_element": BRANCH_ELEMENTS.get(month_branch.split()[0], "")
        },
        "Day": {
            "stem": day_stem,
            "branch": day_branch,
            "stem_element": STEM_ELEMENTS.get(day_stem.split()[0], ""),
            "branch_element": BRANCH_ELEMENTS.get(day_branch.split()[0], "")
        },
        "Hour": {
            "stem": hour_stem,
            "branch": hour_branch,
            "stem_element": STEM_ELEMENTS.get(hour_stem.split()[0], ""),
            "branch_element": BRANCH_ELEMENTS.get(hour_branch.split()[0], "")
        }
    }

# ============================================================================
# JU NUMBER & STRUCTURE CALCULATION
# ============================================================================

def get_chinese_hour_info(hour: int) -> Dict:
    """Get Chinese hour name and index"""
    for (start, end), (name, idx) in CHINESE_HOURS.items():
        if start == 23:
            if hour >= 23 or hour < end:
                return {"name": name, "index": idx, "range": f"{start}:00-{end}:59"}
        elif start <= hour < end:
            return {"name": name, "index": idx, "range": f"{start}:00-{end+1}:59"}
    return {"name": "Zi 子", "index": 0, "range": "23:00-00:59"}

def calculate_structure_and_ju(dt: datetime) -> Dict:
    """
    Calculate Yin/Yang Structure and Ju Number.
    
    Yang Dun (阳遁): Winter Solstice to Summer Solstice
    Yin Dun (阴遁): Summer Solstice to Winter Solstice
    
    Simplified calculation - for production, use solar terms.
    """
    month = dt.month
    day = dt.day
    
    # Simplified: Yang Dun roughly Dec 22 - Jun 21, Yin Dun Jun 22 - Dec 21
    if (month == 12 and day >= 22) or (month < 6) or (month == 6 and day < 22):
        structure = "Yang Dun"
        structure_chinese = "阳遁"
        is_yang = True
    else:
        structure = "Yin Dun"
        structure_chinese = "阴遁"
        is_yang = False
    
    # Ju number (1-9) based on solar term and day
    # Simplified calculation - in production use actual solar term ju mapping
    day_of_year = dt.timetuple().tm_yday
    
    if is_yang:
        # Yang Dun: Ju increases
        ju_base = ((day_of_year - 355) % 45) // 5  # Rough calculation
        ju_number = (ju_base % 9) + 1
    else:
        # Yin Dun: Ju decreases
        ju_base = ((day_of_year - 172) % 45) // 5
        ju_number = 9 - (ju_base % 9)
        if ju_number == 0:
            ju_number = 9
    
    # Ensure ju is 1-9
    ju_number = max(1, min(9, ju_number))
    
    return {
        "structure": structure,
        "structure_chinese": structure_chinese,
        "is_yang_dun": is_yang,
        "ju_number": ju_number,
        "ju_display": f"{structure} Ju {ju_number} ({structure_chinese}{ju_number}局)"
    }

# ============================================================================
# LEAD STEM, LEAD STAR, LEAD DOOR CALCULATION
# ============================================================================

def calculate_lead_indicators(ju_number: int, hour_branch_idx: int, is_yang: bool) -> Dict:
    """
    Calculate Lead Stem Palace (值符宫), Lead Star (直符), and Lead Door (直使).
    
    Lead Stem Palace: Where Jia 甲 is hidden in the current chart
    Lead Star: The star that governs the current hour
    Lead Door: The door that commands the current hour
    """
    # Base palace for each Ju
    ju_base_palace = {
        1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9
    }
    
    base = ju_base_palace.get(ju_number, 1)
    
    # Lead Stem Palace moves based on hour
    # Yang Dun: forward, Yin Dun: backward
    if is_yang:
        lead_stem_palace = ((base - 1 + hour_branch_idx) % 9) + 1
    else:
        lead_stem_palace = ((base - 1 - hour_branch_idx) % 9) + 1
    
    if lead_stem_palace == 0:
        lead_stem_palace = 9
    
    # Lead Star follows Lead Stem Palace
    lead_star = NINE_STARS.get(lead_stem_palace, NINE_STARS[1])
    
    # Lead Door (Envoy) - based on Lead Star position
    # The door that was originally in the Lead Stem Palace
    lead_door = EIGHT_DOORS.get(lead_stem_palace, EIGHT_DOORS[1])
    
    return {
        "lead_stem_palace": lead_stem_palace,
        "lead_stem_palace_name": PALACE_INFO[lead_stem_palace]["name"],
        "lead_stem_palace_chinese": PALACE_INFO[lead_stem_palace]["chinese"],
        "lead_star": lead_star,
        "lead_door": lead_door,
        "hidden_jia_location": f"Palace {lead_stem_palace} ({PALACE_INFO[lead_stem_palace]['name']})"
    }

# ============================================================================
# COMPONENT STRENGTH CALCULATION
# ============================================================================

ELEMENT_STRENGTH = {
    # Element in Palace → Strength
    # (component_element, palace_element): strength_name, score
    ("Wood", "Water"): ("Prosperous", 2),   # Water produces Wood
    ("Wood", "Wood"): ("Timely", 3),         # Same element
    ("Wood", "Fire"): ("Resting", 0),        # Wood produces Fire (draining)
    ("Wood", "Earth"): ("Confined", -1),     # Wood controls Earth (effort)
    ("Wood", "Metal"): ("Dead", -3),         # Metal controls Wood
    
    ("Fire", "Wood"): ("Prosperous", 2),
    ("Fire", "Fire"): ("Timely", 3),
    ("Fire", "Earth"): ("Resting", 0),
    ("Fire", "Metal"): ("Confined", -1),
    ("Fire", "Water"): ("Dead", -3),
    
    ("Earth", "Fire"): ("Prosperous", 2),
    ("Earth", "Earth"): ("Timely", 3),
    ("Earth", "Metal"): ("Resting", 0),
    ("Earth", "Water"): ("Confined", -1),
    ("Earth", "Wood"): ("Dead", -3),
    
    ("Metal", "Earth"): ("Prosperous", 2),
    ("Metal", "Metal"): ("Timely", 3),
    ("Metal", "Water"): ("Resting", 0),
    ("Metal", "Wood"): ("Confined", -1),
    ("Metal", "Fire"): ("Dead", -3),
    
    ("Water", "Metal"): ("Prosperous", 2),
    ("Water", "Water"): ("Timely", 3),
    ("Water", "Wood"): ("Resting", 0),
    ("Water", "Fire"): ("Confined", -1),
    ("Water", "Earth"): ("Dead", -3),
}

def calculate_component_strength(component_element: str, palace_element: str) -> Dict:
    """Calculate strength of a component based on palace element."""
    key = (component_element, palace_element)
    strength_name, score = ELEMENT_STRENGTH.get(key, ("Neutral", 0))
    
    # Friendly names for beginners
    friendly_names = {
        "Timely": "🔥 Peak Energy - Best Time to Act",
        "Prosperous": "💪 Strong Energy - Good Support",
        "Resting": "😴 Rest Energy - Wait & Reflect",
        "Confined": "🔒 Blocked Energy - Face Challenges",
        "Dead": "💀 Weak Energy - Avoid Action"
    }
    
    return {
        "strength": strength_name,
        "strength_score": score,
        "friendly_name": friendly_names.get(strength_name, strength_name)
    }

# ============================================================================
# MAIN QMDJ CHART GENERATION
# ============================================================================

def generate_qmdj_chart(dt: datetime = None, palace_focus: int = None) -> Dict:
    """
    Generate complete QMDJ chart with all indicators.
    
    Args:
        dt: DateTime for the chart (default: now in SGT)
        palace_focus: Optional palace number (1-9) to focus analysis on
    
    Returns:
        Complete chart data with all v6.0 features
    """
    if dt is None:
        dt = datetime.now(SGT)
    
    # Ensure timezone
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=SGT)
    
    # Calculate QMDJ Four Pillars (chart time, not BaZi!)
    qmdj_pillars = calculate_qmdj_pillars(dt)
    
    # Get key pillar data
    day_stem = qmdj_pillars["Day"]["stem"]
    day_branch = qmdj_pillars["Day"]["branch"]
    hour_stem = qmdj_pillars["Hour"]["stem"]
    year_branch = qmdj_pillars["Year"]["branch"]
    
    # Chinese hour info
    chinese_hour = get_chinese_hour_info(dt.hour)
    
    # Structure and Ju
    structure_info = calculate_structure_and_ju(dt)
    
    # Lead indicators
    lead_info = calculate_lead_indicators(
        structure_info["ju_number"],
        chinese_hour["index"],
        structure_info["is_yang_dun"]
    )
    
    # Death & Emptiness
    death_emptiness = calculate_death_emptiness(day_stem, day_branch)
    
    # Horse Star
    horse_star = calculate_horse_star(year_branch)
    
    # Nobleman
    nobleman = calculate_nobleman(day_stem, hour_stem)
    
    # Build palace data (simplified - in production, use actual flying star positions)
    palaces = {}
    for palace_num in range(1, 10):
        palace_info = PALACE_INFO[palace_num]
        
        # Determine components (simplified rotation based on Ju)
        star_idx = ((palace_num - 1 + structure_info["ju_number"]) % 9) + 1
        door_idx = ((palace_num - 1 + chinese_hour["index"]) % 8) + 1
        deity_idx = ((palace_num - 1 + structure_info["ju_number"] + chinese_hour["index"]) % 8) + 1
        
        star = NINE_STARS.get(star_idx, NINE_STARS[1])
        door = EIGHT_DOORS.get(door_idx, EIGHT_DOORS[1])
        deity = EIGHT_DEITIES.get(deity_idx, EIGHT_DEITIES[1])
        
        # Calculate component strengths
        star_strength = calculate_component_strength(star["element"], palace_info["element"])
        door_strength = calculate_component_strength(door["element"], palace_info["element"])
        
        # Check special indicators for this palace
        is_empty = palace_num in death_emptiness["affected_palaces"]
        has_horse = palace_num == horse_star.get("horse_palace")
        has_nobleman = palace_num in nobleman.get("day_nobleman_palaces", [])
        is_lead_palace = palace_num == lead_info["lead_stem_palace"]
        
        palaces[palace_num] = {
            "palace_info": palace_info,
            "star": {**star, **star_strength},
            "door": {**door, **door_strength},
            "deity": deity,
            "indicators": {
                "is_empty": is_empty,
                "has_horse_star": has_horse,
                "has_nobleman": has_nobleman,
                "is_lead_palace": is_lead_palace
            }
        }
    
    # Compile full chart
    chart = {
        "metadata": {
            "datetime": dt.isoformat(),
            "date_display": dt.strftime("%Y-%m-%d"),
            "time_display": dt.strftime("%H:%M"),
            "chinese_hour": chinese_hour,
            "timezone": "UTC+8"
        },
        "structure": structure_info,
        "qmdj_pillars": qmdj_pillars,
        "lead_indicators": lead_info,
        "death_emptiness": death_emptiness,
        "horse_star": horse_star,
        "nobleman": nobleman,
        "palaces": palaces,
        "palace_focus": palace_focus
    }
    
    return chart

# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MING QIMEN v6.0 - QMDJ ENGINE TEST")
    print("=" * 60)
    
    # Test with current time
    chart = generate_qmdj_chart()
    
    print(f"\n📅 Chart Time: {chart['metadata']['date_display']} {chart['metadata']['time_display']}")
    print(f"⏰ Chinese Hour: {chart['metadata']['chinese_hour']['name']}")
    print(f"\n🔮 Structure: {chart['structure']['ju_display']}")
    
    print(f"\n📜 QMDJ PILLARS (Chart Time):")
    for pillar, data in chart['qmdj_pillars'].items():
        print(f"  {pillar}: {data['stem']} / {data['branch']}")
    
    print(f"\n🎯 LEAD INDICATORS:")
    print(f"  Lead Stem Palace: {chart['lead_indicators']['hidden_jia_location']}")
    print(f"  Lead Star: {chart['lead_indicators']['lead_star']['name']} {chart['lead_indicators']['lead_star']['chinese']}")
    print(f"  Lead Door: {chart['lead_indicators']['lead_door']['name']} {chart['lead_indicators']['lead_door']['chinese']}")
    
    print(f"\n💀 DEATH & EMPTINESS:")
    print(f"  Cycle: {chart['death_emptiness']['cycle']}")
    print(f"  Empty Branches: {chart['death_emptiness']['empty_branches']}")
    print(f"  Affected Palaces: {chart['death_emptiness']['affected_palaces']}")
    
    print(f"\n🐴 HORSE STAR:")
    print(f"  Location: Palace {chart['horse_star']['horse_palace']} ({chart['horse_star']['horse_branch']})")
    
    print(f"\n👑 NOBLEMAN:")
    print(f"  Day Nobleman Palaces: {chart['nobleman']['day_nobleman_palaces']}")
    
    print(f"\n🏛️ PALACE SUMMARY:")
    for num, palace in chart['palaces'].items():
        indicators = []
        if palace['indicators']['is_lead_palace']:
            indicators.append("⭐LEAD")
        if palace['indicators']['has_horse_star']:
            indicators.append("🐴HORSE")
        if palace['indicators']['has_nobleman']:
            indicators.append("👑NOBLE")
        if palace['indicators']['is_empty']:
            indicators.append("💀EMPTY")
        
        ind_str = " ".join(indicators) if indicators else ""
        print(f"  P{num} {palace['palace_info']['name']}: {palace['star']['name']} + {palace['door']['name']} {ind_str}")
    
    print("\n✅ Engine test complete!")
