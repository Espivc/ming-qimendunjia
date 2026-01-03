# utils/bazi_calculator.py - Ming QiMenDunJia v10.4
# Accurate BaZi Calculations - Fixed Month Pillar with Solar Terms
# Validated against Joey Yap charts

from datetime import date, datetime

# =============================================================================
# CONSTANTS
# =============================================================================

STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
STEMS_CN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
BRANCHES_CN = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

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

# Hidden Stems for each branch
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

# =============================================================================
# SOLAR TERMS - Critical for accurate month calculation
# Format: (month, day) approximate dates - varies by year
# These are the JIE (节) solar terms that START each month
# =============================================================================

# Solar term approximate dates (Jie terms that start each BaZi month)
# Month 1 (Yin/Tiger) starts at Li Chun (Start of Spring)
SOLAR_TERMS_APPROX = {
    1: (2, 4),    # 立春 Li Chun - Start of Spring → Month 1 (寅 Tiger)
    2: (3, 6),    # 惊蛰 Jing Zhe - Awakening of Insects → Month 2 (卯 Rabbit)
    3: (4, 5),    # 清明 Qing Ming - Clear and Bright → Month 3 (辰 Dragon)
    4: (5, 6),    # 立夏 Li Xia - Start of Summer → Month 4 (巳 Snake)
    5: (6, 6),    # 芒种 Mang Zhong - Grain in Ear → Month 5 (午 Horse)
    6: (7, 7),    # 小暑 Xiao Shu - Minor Heat → Month 6 (未 Goat)
    7: (8, 8),    # 立秋 Li Qiu - Start of Autumn → Month 7 (申 Monkey)
    8: (9, 8),    # 白露 Bai Lu - White Dew → Month 8 (酉 Rooster)
    9: (10, 8),   # 寒露 Han Lu - Cold Dew → Month 9 (戌 Dog)
    10: (11, 7),  # 立冬 Li Dong - Start of Winter → Month 10 (亥 Pig)
    11: (12, 7),  # 大雪 Da Xue - Major Snow → Month 11 (子 Rat)
    12: (1, 6),   # 小寒 Xiao Han - Minor Cold → Month 12 (丑 Ox)
}

# Month branches in order (starting from month 1 = Yin/Tiger)
MONTH_BRANCHES = ["Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai", "Zi", "Chou"]

# =============================================================================
# YEAR PILLAR CALCULATION
# =============================================================================

def calc_year_pillar(year, month, day):
    """
    Calculate year pillar.
    Note: Year changes at Li Chun (Start of Spring), not Jan 1!
    """
    # Check if before Li Chun (around Feb 4)
    li_chun_month, li_chun_day = SOLAR_TERMS_APPROX[1]
    
    # If before Li Chun, use previous year
    if month < li_chun_month or (month == li_chun_month and day < li_chun_day):
        year = year - 1
    
    # Calculate stem and branch
    # Reference: 1984 = Jia Zi (甲子) year
    # Stem: (year - 4) % 10
    # Branch: (year - 4) % 12
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    
    return STEMS[stem_idx], BRANCHES[branch_idx]


# =============================================================================
# MONTH PILLAR CALCULATION - FIXED with Solar Terms
# =============================================================================

def get_bazi_month(year, month, day):
    """
    Determine which BaZi month based on solar terms.
    Returns month number (1-12) where 1=Tiger, 2=Rabbit, etc.
    """
    # Check each solar term boundary
    for bazi_month in range(12, 0, -1):
        solar_month, solar_day = SOLAR_TERMS_APPROX[bazi_month]
        
        # Handle month 12 which starts in January
        if bazi_month == 12:
            if month == 1 and day >= solar_day:
                return 12
            elif month == 12:
                # Check if after Da Xue (month 11)
                m11_month, m11_day = SOLAR_TERMS_APPROX[11]
                if month > m11_month or (month == m11_month and day >= m11_day):
                    return 11
        else:
            if month > solar_month or (month == solar_month and day >= solar_day):
                return bazi_month
    
    # Default to month 12 (Chou) for early January
    return 12


def calc_month_pillar(year, month, day):
    """
    Calculate month pillar using solar terms.
    
    Month stem is derived from year stem using the formula:
    - 甲己 year → Month 1 starts with 丙 (Bing)
    - 乙庚 year → Month 1 starts with 戊 (Wu)
    - 丙辛 year → Month 1 starts with 庚 (Geng)
    - 丁壬 year → Month 1 starts with 壬 (Ren)
    - 戊癸 year → Month 1 starts with 甲 (Jia)
    """
    # Get the BaZi month (1-12)
    bazi_month = get_bazi_month(year, month, day)
    
    # Get month branch
    month_branch = MONTH_BRANCHES[bazi_month - 1]
    
    # Get year stem (considering Li Chun boundary)
    year_stem, _ = calc_year_pillar(year, month, day)
    year_stem_idx = STEMS.index(year_stem)
    
    # Calculate month stem based on year stem
    # Formula: First month (Tiger) stem = (year_stem_idx * 2 + 2) % 10
    # Then add (bazi_month - 1) for subsequent months
    first_month_stem_idx = (year_stem_idx * 2 + 2) % 10
    month_stem_idx = (first_month_stem_idx + bazi_month - 1) % 10
    month_stem = STEMS[month_stem_idx]
    
    return month_stem, month_branch


# =============================================================================
# DAY PILLAR CALCULATION
# =============================================================================

def calc_day_pillar(year, month, day):
    """
    Calculate day pillar using the standard algorithm.
    Reference: January 1, 1900 = 甲戌 (Jia Xu), stem=0, branch=10
    """
    # Calculate Julian Day Number
    def to_julian(y, m, d):
        if m <= 2:
            y -= 1
            m += 12
        A = y // 100
        B = 2 - A + A // 4
        return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524
    
    # Reference: January 1, 1900
    ref_jd = to_julian(1900, 1, 1)
    target_jd = to_julian(year, month, day)
    
    days_diff = target_jd - ref_jd
    
    # January 1, 1900 = 甲戌 (Jia Xu) = stem index 0, branch index 10
    # But we need to verify this reference
    # Actually, January 1, 1900 = 甲戌 (Jia Xu)
    ref_stem = 0   # Jia
    ref_branch = 10  # Xu
    
    stem_idx = (ref_stem + days_diff) % 10
    branch_idx = (ref_branch + days_diff) % 12
    
    return STEMS[stem_idx], BRANCHES[branch_idx]


# =============================================================================
# HOUR PILLAR CALCULATION
# =============================================================================

def get_hour_branch(hour):
    """
    Convert hour (0-23) to earthly branch.
    23:00-00:59 = Zi (子)
    01:00-02:59 = Chou (丑)
    ...and so on
    """
    if hour == 23:
        return "Zi", 0
    branch_idx = ((hour + 1) // 2) % 12
    return BRANCHES[branch_idx], branch_idx


def calc_hour_pillar(hour, day_stem):
    """
    Calculate hour pillar based on hour and day stem.
    
    Hour stem formula based on day stem:
    - 甲己 day → Hour starts with 甲 at Zi
    - 乙庚 day → Hour starts with 丙 at Zi
    - 丙辛 day → Hour starts with 戊 at Zi
    - 丁壬 day → Hour starts with 庚 at Zi
    - 戊癸 day → Hour starts with 壬 at Zi
    """
    hour_branch, branch_idx = get_hour_branch(hour)
    day_stem_idx = STEMS.index(day_stem)
    
    # Calculate starting stem for Zi hour based on day stem
    # Formula: (day_stem_idx % 5) * 2
    zi_hour_stem_idx = (day_stem_idx % 5) * 2
    
    # Add branch index to get hour stem
    hour_stem_idx = (zi_hour_stem_idx + branch_idx) % 10
    hour_stem = STEMS[hour_stem_idx]
    
    return hour_stem, hour_branch


# =============================================================================
# COMPLETE BAZI CALCULATION
# =============================================================================

def calculate_bazi(birth_date, birth_hour):
    """
    Calculate complete BaZi four pillars.
    
    Args:
        birth_date: date object or (year, month, day) tuple
        birth_hour: int 0-23
    
    Returns:
        dict with all four pillars and metadata
    """
    if isinstance(birth_date, date):
        year, month, day = birth_date.year, birth_date.month, birth_date.day
    else:
        year, month, day = birth_date
    
    # Calculate all pillars
    year_stem, year_branch = calc_year_pillar(year, month, day)
    month_stem, month_branch = calc_month_pillar(year, month, day)
    day_stem, day_branch = calc_day_pillar(year, month, day)
    hour_stem, hour_branch = calc_hour_pillar(birth_hour, day_stem)
    
    # Build result
    pillars = {
        "year": {
            "stem": year_stem,
            "stem_cn": STEMS_CN[STEMS.index(year_stem)],
            "branch": year_branch,
            "branch_cn": BRANCHES_CN[BRANCHES.index(year_branch)],
            "animal": ANIMALS[BRANCHES.index(year_branch)],
            "element": STEM_ELEMENTS[year_stem],
            "hidden_stems": HIDDEN_STEMS[year_branch]
        },
        "month": {
            "stem": month_stem,
            "stem_cn": STEMS_CN[STEMS.index(month_stem)],
            "branch": month_branch,
            "branch_cn": BRANCHES_CN[BRANCHES.index(month_branch)],
            "animal": ANIMALS[BRANCHES.index(month_branch)],
            "element": STEM_ELEMENTS[month_stem],
            "hidden_stems": HIDDEN_STEMS[month_branch]
        },
        "day": {
            "stem": day_stem,
            "stem_cn": STEMS_CN[STEMS.index(day_stem)],
            "branch": day_branch,
            "branch_cn": BRANCHES_CN[BRANCHES.index(day_branch)],
            "animal": ANIMALS[BRANCHES.index(day_branch)],
            "element": STEM_ELEMENTS[day_stem],
            "hidden_stems": HIDDEN_STEMS[day_branch],
            "is_day_master": True
        },
        "hour": {
            "stem": hour_stem,
            "stem_cn": STEMS_CN[STEMS.index(hour_stem)],
            "branch": hour_branch,
            "branch_cn": BRANCHES_CN[BRANCHES.index(hour_branch)],
            "animal": ANIMALS[BRANCHES.index(hour_branch)],
            "element": STEM_ELEMENTS[hour_stem],
            "hidden_stems": HIDDEN_STEMS[hour_branch]
        }
    }
    
    return {
        "birth_info": {
            "date": f"{year}-{month:02d}-{day:02d}",
            "hour": birth_hour,
            "bazi_month": get_bazi_month(year, month, day)
        },
        "pillars": pillars,
        "day_master": {
            "stem": day_stem,
            "stem_cn": STEMS_CN[STEMS.index(day_stem)],
            "element": STEM_ELEMENTS[day_stem],
            "polarity": STEM_POLARITY[day_stem]
        }
    }


# =============================================================================
# TEN GODS CALCULATION
# =============================================================================

def get_ten_god(day_master, stem):
    """Calculate the Ten God relationship between day master and a stem."""
    if day_master == stem:
        return "F", "比肩", "Friend"
    
    dm_elem = STEM_ELEMENTS[day_master]
    dm_pol = STEM_POLARITY[day_master]
    s_elem = STEM_ELEMENTS[stem]
    s_pol = STEM_POLARITY[stem]
    
    same_polarity = (dm_pol == s_pol)
    
    # Five elements relationships
    produces = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
    controls = {"Wood": "Earth", "Fire": "Metal", "Earth": "Water", "Metal": "Wood", "Water": "Fire"}
    
    # Same element
    if dm_elem == s_elem:
        if same_polarity:
            return "F", "比肩", "Friend"
        else:
            return "RW", "劫财", "Rob Wealth"
    
    # I produce (Output)
    if produces[dm_elem] == s_elem:
        if same_polarity:
            return "EG", "食神", "Eating God"
        else:
            return "HO", "伤官", "Hurting Officer"
    
    # I am produced by (Resource)
    if produces[s_elem] == dm_elem:
        if same_polarity:
            return "IR", "偏印", "Indirect Resource"
        else:
            return "DR", "正印", "Direct Resource"
    
    # I control (Wealth)
    if controls[dm_elem] == s_elem:
        if same_polarity:
            return "IW", "偏财", "Indirect Wealth"
        else:
            return "DW", "正财", "Direct Wealth"
    
    # I am controlled by (Influence)
    if controls[s_elem] == dm_elem:
        if same_polarity:
            return "7K", "七杀", "Seven Killings"
        else:
            return "DO", "正官", "Direct Officer"
    
    return "?", "?", "Unknown"


# =============================================================================
# VALIDATION TEST
# =============================================================================

def test_ben_chart():
    """
    Test with Ben's birth data against Joey Yap chart.
    Birth: June 27, 1978, 20:08 (8:08 PM)
    
    Joey Yap shows:
    - Year: 戊午 Wu Wu (Earth Horse)
    - Month: 戊午 Wu Wu (Earth Horse) 
    - Day: 庚申 Geng Shen (Metal Monkey)
    - Hour: 丙戌 Bing Xu (Fire Dog)
    """
    result = calculate_bazi(date(1978, 6, 27), 20)
    
    print("=" * 60)
    print("VALIDATION TEST: Ben's Chart (1978-06-27 20:00)")
    print("=" * 60)
    
    expected = {
        "year": ("Wu", "Wu"),      # 戊午
        "month": ("Wu", "Wu"),     # 戊午 - This is the key fix!
        "day": ("Geng", "Shen"),   # 庚申
        "hour": ("Bing", "Xu")     # 丙戌
    }
    
    pillars = result["pillars"]
    all_pass = True
    
    for pillar_name in ["year", "month", "day", "hour"]:
        p = pillars[pillar_name]
        exp_stem, exp_branch = expected[pillar_name]
        
        stem_ok = p["stem"] == exp_stem
        branch_ok = p["branch"] == exp_branch
        status = "✅" if (stem_ok and branch_ok) else "❌"
        
        if not (stem_ok and branch_ok):
            all_pass = False
        
        print(f"{status} {pillar_name.upper():6} | Got: {p['stem_cn']}{p['branch_cn']} ({p['stem']} {p['branch']}) | Expected: {exp_stem} {exp_branch}")
    
    print("=" * 60)
    print(f"RESULT: {'ALL TESTS PASSED ✅' if all_pass else 'SOME TESTS FAILED ❌'}")
    print("=" * 60)
    
    # Print full chart
    print("\nFULL CHART:")
    for pname in ["year", "month", "day", "hour"]:
        p = pillars[pname]
        hidden = ", ".join([f"{h} {STEMS_CN[STEMS.index(h)]}" for h in p["hidden_stems"]])
        print(f"  {pname.upper():6}: {p['stem_cn']}{p['branch_cn']} ({p['stem']} {p['branch']}) - {p['animal']} - Hidden: [{hidden}]")
    
    return all_pass, result


if __name__ == "__main__":
    test_ben_chart()
