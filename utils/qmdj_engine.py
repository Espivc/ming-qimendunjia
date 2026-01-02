"""
QMDJ Engine v10.3 - Real kinqimen Integration
Proper implementation of kinqimen library for accurate QMDJ calculations
"""

from datetime import datetime
import sxtwl

try:
    import kinqimen as kq
    KINQIMEN_AVAILABLE = True
except ImportError:
    KINQIMEN_AVAILABLE = False
    print("⚠️ kinqimen not available, using fallback calculations")

# ============================================================================
# MAPPING DICTIONARIES
# ============================================================================

# Heaven Stems (天干)
STEM_MAP = {
    '甲': 'Jia', '乙': 'Yi', '丙': 'Bing', '丁': 'Ding', '戊': 'Wu',
    '己': 'Ji', '庚': 'Geng', '辛': 'Xin', '壬': 'Ren', '癸': 'Gui'
}

# Earth Branches (地支)
BRANCH_MAP = {
    '子': 'Zi', '丑': 'Chou', '寅': 'Yin', '卯': 'Mao', '辰': 'Chen', '巳': 'Si',
    '午': 'Wu', '未': 'Wei', '申': 'Shen', '酉': 'You', '戌': 'Xu', '亥': 'Hai'
}

# Stars (九星)
STAR_MAP = {
    '天蓬': 'Canopy', '天芮': 'Grass', '天冲': 'Impulse',
    '天辅': 'Assistant', '天禽': 'Connect', '天心': 'Heart',
    '天柱': 'Pillar', '天任': 'Ren', '天英': 'Hero'
}

# Doors (八门)
DOOR_MAP = {
    '开门': 'Open', '休门': 'Rest', '生门': 'Life',
    '伤门': 'Harm', '杜门': 'Delusion', '景门': 'Scenery',
    '死门': 'Death', '惊门': 'Fear'
}

# Deities (八神)
DEITY_MAP = {
    '值符': 'Chief', '腾蛇': 'Serpent', '太阴': 'Moon',
    '六合': 'Six Harmony', '勾陈': 'Hook', '白虎': 'Tiger',
    '玄武': 'Emptiness', '九地': 'Nine Earth', '九天': 'Nine Heaven'
}

# Element mappings
STEM_ELEMENTS = {
    'Jia': 'Wood', 'Yi': 'Wood', 'Bing': 'Fire', 'Ding': 'Fire',
    'Wu': 'Earth', 'Ji': 'Earth', 'Geng': 'Metal', 'Xin': 'Metal',
    'Ren': 'Water', 'Gui': 'Water'
}

STAR_ELEMENTS = {
    'Canopy': 'Water', 'Grass': 'Earth', 'Impulse': 'Wood',
    'Assistant': 'Wood', 'Connect': 'Earth', 'Heart': 'Metal',
    'Pillar': 'Metal', 'Ren': 'Earth', 'Hero': 'Fire'
}

DOOR_ELEMENTS = {
    'Open': 'Metal', 'Rest': 'Water', 'Life': 'Earth',
    'Harm': 'Wood', 'Delusion': 'Wood', 'Scenery': 'Fire',
    'Death': 'Earth', 'Fear': 'Metal'
}

# ============================================================================
# CORE QMDJ CALCULATION FUNCTIONS
# ============================================================================

def generate_qmdj_chart(chart_datetime: datetime, method: str = "Chai Bu"):
    """
    Generate QMDJ chart using real kinqimen library
    
    Args:
        chart_datetime: DateTime object for chart generation
        method: "Chai Bu" (default) - fixed arrangement method
    
    Returns:
        dict: Complete QMDJ chart data with all palaces
    """
    if not KINQIMEN_AVAILABLE:
        return generate_fallback_chart(chart_datetime)
    
    try:
        # Use kinqimen's built-in chart generation
        kq_chart = kq.QiMen(chart_datetime)
        
        # Extract structure info
        structure = "Yang Dun" if kq_chart.yang else "Yin Dun"
        ju_number = kq_chart.ju
        
        # Calculate Four Pillars from CHART TIME (not user's natal BaZi)
        pillars = calculate_four_pillars_from_chart(chart_datetime)
        
        # Generate all 9 palaces
        palaces = {}
        for palace_num in range(1, 10):
            palaces[palace_num] = extract_palace_data(kq_chart, palace_num)
        
        # Phase A indicators
        phase_a = calculate_phase_a_indicators(kq_chart, pillars)
        
        return {
            "chart_datetime": chart_datetime.strftime("%Y-%m-%d %H:%M"),
            "structure": structure,
            "ju_number": ju_number,
            "palaces": palaces,
            "four_pillars": pillars,
            "phase_a_indicators": phase_a,
            "method": method,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error generating QMDJ chart: {e}")
        return generate_fallback_chart(chart_datetime)


def extract_palace_data(kq_chart, palace_num: int):
    """
    Extract all components for a specific palace from kinqimen chart
    
    Args:
        kq_chart: kinqimen QiMen object
        palace_num: Palace number (1-9)
    
    Returns:
        dict: Palace data with all components
    """
    # Palace mapping
    palace_names = {
        1: "Kan", 2: "Kun", 3: "Zhen", 4: "Xun", 5: "Center",
        6: "Qian", 7: "Dui", 8: "Gen", 9: "Li"
    }
    
    palace_chinese = {
        1: "坎", 2: "坤", 3: "震", 4: "巽", 5: "中",
        6: "乾", 7: "兑", 8: "艮", 9: "离"
    }
    
    directions = {
        1: "N", 2: "SW", 3: "E", 4: "SE", 5: "Center",
        6: "NW", 7: "W", 8: "NE", 9: "S"
    }
    
    elements = {
        1: "Water", 2: "Earth", 3: "Wood", 4: "Wood", 5: "Earth",
        6: "Metal", 7: "Metal", 8: "Earth", 9: "Fire"
    }
    
    # Get palace data from kinqimen
    palace = kq_chart.ju_arr[palace_num - 1]
    
    # Extract components (kinqimen uses Chinese, need to map)
    heaven_stem_cn = palace.get('天干', '?')
    earth_stem_cn = palace.get('地盘', '?')
    star_cn = palace.get('星', '?')
    door_cn = palace.get('门', '?')
    deity_cn = palace.get('神', '?')
    
    # Map to English
    heaven_stem_en = STEM_MAP.get(heaven_stem_cn, heaven_stem_cn)
    earth_stem_en = STEM_MAP.get(earth_stem_cn, earth_stem_cn)
    star_en = STAR_MAP.get(star_cn, star_cn)
    door_en = DOOR_MAP.get(door_cn, door_cn)
    deity_en = DEITY_MAP.get(deity_cn, deity_cn)
    
    return {
        "number": palace_num,
        "name": palace_names[palace_num],
        "chinese": palace_chinese[palace_num],
        "direction": directions[palace_num],
        "element": elements[palace_num],
        "components": {
            "heaven_stem": {
                "character": heaven_stem_en,
                "chinese": heaven_stem_cn,
                "element": STEM_ELEMENTS.get(heaven_stem_en, 'Unknown'),
                "polarity": get_stem_polarity(heaven_stem_en)
            },
            "earth_stem": {
                "character": earth_stem_en,
                "chinese": earth_stem_cn,
                "element": STEM_ELEMENTS.get(earth_stem_en, 'Unknown'),
                "polarity": get_stem_polarity(earth_stem_en)
            },
            "star": {
                "name": star_en,
                "chinese": star_cn,
                "element": STAR_ELEMENTS.get(star_en, 'Unknown'),
                "category": get_star_category(star_en)
            },
            "door": {
                "name": door_en,
                "chinese": door_cn,
                "element": DOOR_ELEMENTS.get(door_en, 'Unknown'),
                "category": get_door_category(door_en)
            },
            "deity": {
                "name": deity_en,
                "chinese": deity_cn,
                "nature": get_deity_nature(deity_en)
            }
        }
    }


def calculate_phase_a_indicators(kq_chart, pillars):
    """
    Calculate Phase A indicators (Death/Emptiness, Lead Palace, etc.)
    
    Args:
        kq_chart: kinqimen chart object
        pillars: Four Pillars from chart time
    
    Returns:
        dict: Phase A indicator data
    """
    try:
        # Death & Emptiness (空亡)
        day_branch = pillars['day']['branch']
        death_emptiness = calculate_death_emptiness(day_branch)
        
        # Lead Stem Palace (值符宫) - find where Chief deity is
        lead_palace = find_lead_stem_palace(kq_chart)
        
        # Lead Star & Door - from the lead palace
        if lead_palace > 0 and lead_palace <= 9:
            palace_data = kq_chart.ju_arr[lead_palace - 1]
            lead_star = STAR_MAP.get(palace_data.get('星', ''), 'Unknown')
            lead_door = DOOR_MAP.get(palace_data.get('门', ''), 'Unknown')
        else:
            lead_star = 'Unknown'
            lead_door = 'Unknown'
        
        # Horse Star (驿马星)
        horse_star = calculate_horse_star(pillars)
        
        # Nobleman Star (天乙贵人)
        nobleman = calculate_nobleman_star(pillars['day']['stem'])
        
        return {
            "death_emptiness": death_emptiness,
            "lead_stem_palace": lead_palace,
            "lead_star": lead_star,
            "lead_door": lead_door,
            "horse_star": horse_star,
            "nobleman_star": nobleman
        }
    except Exception as e:
        print(f"⚠️ Phase A calculation error: {e}")
        return {
            "death_emptiness": {"branches": [], "palaces": []},
            "lead_stem_palace": 5,
            "lead_star": "Unknown",
            "lead_door": "Unknown",
            "horse_star": {"branch": "", "palace": 0},
            "nobleman_star": {"branches": [], "palaces": []}
        }


def calculate_four_pillars_from_chart(chart_datetime: datetime):
    """
    CRITICAL: Calculate Four Pillars from CHART TIME, not user's natal BaZi
    
    This was a major bug in earlier versions - QMDJ uses the moment of
    chart creation, not the user's birth time.
    
    Args:
        chart_datetime: DateTime when chart is being generated
    
    Returns:
        dict: Four pillars (year, month, day, hour) with stems and branches
    """
    lunar = sxtwl.Lunar()
    
    year = chart_datetime.year
    month = chart_datetime.month
    day = chart_datetime.day
    hour = chart_datetime.hour
    
    # Get solar terms for accurate month pillar
    day_data = lunar.getDayBySolar(year, month, day)
    
    # Calculate pillars
    year_pillar = get_year_pillar(year, day_data)
    month_pillar = get_month_pillar(year, month, day_data)
    day_pillar = get_day_pillar(day_data)
    hour_pillar = get_hour_pillar(day_pillar['stem'], hour)
    
    return {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_stem_polarity(stem):
    """Get polarity from stem"""
    yang_stems = ['Jia', 'Bing', 'Wu', 'Geng', 'Ren']
    return "Yang" if stem in yang_stems else "Yin"


def get_star_category(star):
    """Categorize star as auspicious/neutral/inauspicious"""
    auspicious = ['Assistant', 'Heart', 'Ren', 'Hero']
    inauspicious = ['Canopy', 'Grass']
    return "Auspicious" if star in auspicious else "Inauspicious" if star in inauspicious else "Neutral"


def get_door_category(door):
    """Categorize door as auspicious/neutral/inauspicious"""
    auspicious = ['Open', 'Rest', 'Life']
    inauspicious = ['Death', 'Fear', 'Harm']
    return "Auspicious" if door in auspicious else "Inauspicious" if door in inauspicious else "Neutral"


def get_deity_nature(deity):
    """Get nature of deity"""
    auspicious = ['Chief', 'Moon', 'Six Harmony', 'Nine Heaven']
    inauspicious = ['Serpent', 'Tiger', 'Emptiness']
    return "Auspicious" if deity in auspicious else "Inauspicious" if deity in inauspicious else "Neutral"


def calculate_death_emptiness(day_branch):
    """
    Calculate Death & Emptiness branches based on day branch
    Uses Jia-Zi cycle method
    """
    # Simplified implementation - full version needs 60 Jia-Zi cycle
    death_map = {
        'Zi': ['Xu', 'Hai'], 'Chou': ['Xu', 'Hai'], 'Yin': ['Zi', 'Chou'],
        'Mao': ['Zi', 'Chou'], 'Chen': ['Yin', 'Mao'], 'Si': ['Yin', 'Mao'],
        'Wu': ['Chen', 'Si'], 'Wei': ['Chen', 'Si'], 'Shen': ['Wu', 'Wei'],
        'You': ['Wu', 'Wei'], 'Xu': ['Shen', 'You'], 'Hai': ['Shen', 'You']
    }
    
    branches = death_map.get(day_branch, [])
    # Map branches to palaces (simplified)
    palace_map = {
        'Zi': 1, 'Chou': 8, 'Yin': 8, 'Mao': 3, 'Chen': 4, 'Si': 4,
        'Wu': 9, 'Wei': 2, 'Shen': 2, 'You': 7, 'Xu': 6, 'Hai': 6
    }
    palaces = [palace_map.get(b, 0) for b in branches]
    
    return {"branches": branches, "palaces": palaces}


def find_lead_stem_palace(kq_chart):
    """Find the palace containing the Lead Stem (值符)"""
    try:
        for i, palace in enumerate(kq_chart.ju_arr):
            if palace.get('神', '') == '值符':
                return i + 1
    except:
        pass
    return 5  # Default to center if not found


def calculate_horse_star(pillars):
    """Calculate Horse Star based on day branch"""
    horse_map = {
        'Yin': 'Shen', 'Wu': 'Yin', 'Xu': 'Shen',
        'Shen': 'Yin', 'Zi': 'Yin', 'Chen': 'Yin',
        'Si': 'Hai', 'You': 'Hai', 'Chou': 'Hai',
        'Hai': 'Si', 'Mao': 'Si', 'Wei': 'Si'
    }
    
    day_branch = pillars['day']['branch']
    horse_branch = horse_map.get(day_branch, '')
    
    # Map to palace number
    palace_map = {
        'Zi': 1, 'Chou': 8, 'Yin': 8, 'Mao': 3, 'Chen': 4, 'Si': 4,
        'Wu': 9, 'Wei': 2, 'Shen': 2, 'You': 7, 'Xu': 6, 'Hai': 6
    }
    horse_palace = palace_map.get(horse_branch, 0)
    
    return {"branch": horse_branch, "palace": horse_palace}


def calculate_nobleman_star(day_stem):
    """Calculate Nobleman Star based on day stem"""
    nobleman_map = {
        'Jia': ['Chou', 'Wei'], 'Yi': ['Zi', 'Shen'],
        'Bing': ['Hai', 'You'], 'Ding': ['Hai', 'You'],
        'Wu': ['Chou', 'Wei'], 'Ji': ['Zi', 'Shen'],
        'Geng': ['Chou', 'Wei'], 'Xin': ['Yin', 'Wu'],
        'Ren': ['Mao', 'Si'], 'Gui': ['Mao', 'Si']
    }
    
    branches = nobleman_map.get(day_stem, [])
    
    # Map to palaces
    palace_map = {
        'Zi': 1, 'Chou': 8, 'Yin': 8, 'Mao': 3, 'Chen': 4, 'Si': 4,
        'Wu': 9, 'Wei': 2, 'Shen': 2, 'You': 7, 'Xu': 6, 'Hai': 6
    }
    palaces = [palace_map.get(b, 0) for b in branches]
    
    return {"branches": branches, "palaces": palaces}


def get_year_pillar(year, day_data):
    """Calculate year pillar from year"""
    gan = day_data.getYearGZ().tg  # Heavenly stem index
    zhi = day_data.getYearGZ().dz  # Earthly branch index
    
    stems = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
    branches = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
    
    return {
        "stem": stems[gan],
        "branch": branches[zhi]
    }


def get_month_pillar(year, month, day_data):
    """Calculate month pillar with solar term consideration"""
    gan = day_data.getMonthGZ().tg
    zhi = day_data.getMonthGZ().dz
    
    stems = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
    branches = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
    
    return {
        "stem": stems[gan],
        "branch": branches[zhi]
    }


def get_day_pillar(day_data):
    """Extract day pillar from sxtwl day data"""
    gan = day_data.getDayGZ().tg
    zhi = day_data.getDayGZ().dz
    
    stems = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
    branches = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
    
    return {
        "stem": stems[gan],
        "branch": branches[zhi]
    }


def get_hour_pillar(day_stem, hour):
    """Calculate hour pillar from day stem and hour"""
    # Hour branch calculation
    hour_branches = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 
                     'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai']
    
    # Hour to branch index
    hour_index = (hour + 1) // 2 % 12
    hour_branch = hour_branches[hour_index]
    
    # Hour stem calculation (based on day stem)
    day_stem_index = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'].index(day_stem)
    
    # Hour stem formula
    hour_stem_base = (day_stem_index % 5) * 2
    hour_stem_index = (hour_stem_base + hour_index) % 10
    
    hour_stems = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui']
    hour_stem = hour_stems[hour_stem_index]
    
    return {
        "stem": hour_stem,
        "branch": hour_branch
    }


def generate_fallback_chart(chart_datetime):
    """Generate basic fallback chart if kinqimen fails"""
    print("⚠️ Using fallback QMDJ chart - kinqimen integration failed")
    
    # Create basic 9 palace structure
    palace_names = {
        1: "Kan", 2: "Kun", 3: "Zhen", 4: "Xun", 5: "Center",
        6: "Qian", 7: "Dui", 8: "Gen", 9: "Li"
    }
    
    palaces = {}
    for i in range(1, 10):
        palaces[i] = {
            "number": i,
            "name": palace_names[i],
            "components": {
                "heaven_stem": {"character": "Unknown", "element": "Unknown"},
                "earth_stem": {"character": "Unknown", "element": "Unknown"},
                "star": {"name": "Unknown", "element": "Unknown"},
                "door": {"name": "Unknown", "element": "Unknown"},
                "deity": {"name": "Unknown"}
            }
        }
    
    return {
        "chart_datetime": chart_datetime.strftime("%Y-%m-%d %H:%M"),
        "structure": "Yang Dun",
        "ju_number": 1,
        "palaces": palaces,
        "four_pillars": {
            "year": {"stem": "Unknown", "branch": "Unknown"},
            "month": {"stem": "Unknown", "branch": "Unknown"},
            "day": {"stem": "Unknown", "branch": "Unknown"},
            "hour": {"stem": "Unknown", "branch": "Unknown"}
        },
        "phase_a_indicators": {},
        "status": "fallback",
        "error": "kinqimen not available - using fallback data"
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_palace_name(palace_num):
    """Get palace name from number"""
    names = {
        1: "Kan", 2: "Kun", 3: "Zhen", 4: "Xun", 5: "Center",
        6: "Qian", 7: "Dui", 8: "Gen", 9: "Li"
    }
    return names.get(palace_num, "Unknown")


def get_palace_direction(palace_num):
    """Get direction from palace number"""
    directions = {
        1: "N", 2: "SW", 3: "E", 4: "SE", 5: "Center",
        6: "NW", 7: "W", 8: "NE", 9: "S"
    }
    return directions.get(palace_num, "Unknown")


def get_palace_element(palace_num):
    """Get element from palace number"""
    elements = {
        1: "Water", 2: "Earth", 3: "Wood", 4: "Wood", 5: "Earth",
        6: "Metal", 7: "Metal", 8: "Earth", 9: "Fire"
    }
    return elements.get(palace_num, "Unknown")
