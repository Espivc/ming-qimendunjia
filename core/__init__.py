"""
===============================================================================
Ming QiMenDunJia - Core Calculation Module
===============================================================================

This module contains the core calculation engines for:
- BaZi (Four Pillars of Destiny)
- QMDJ (Qi Men Dun Jia) - Coming soon
- Formations - Coming soon

Usage:
    from core.bazi_calculator import analyze_bazi, calculate_four_pillars
"""

from .bazi_calculator import (
    # Main analysis function
    analyze_bazi,
    
    # Four Pillars calculation
    calculate_four_pillars,
    calc_year_pillar,
    calc_month_pillar,
    calc_day_pillar,
    calc_hour_pillar,
    
    # Day Master analysis
    calculate_dm_strength,
    determine_useful_gods,
    
    # Ten Gods / Profiles
    get_ten_god,
    calculate_ten_profiles,
    get_dominant_profile,
    
    # Luck Pillars
    calculate_luck_pillars,
    calculate_luck_pillar_start_age,
    get_luck_direction,
    
    # Interactions
    detect_clashes,
    detect_combines,
    detect_three_harmony,
    
    # Solar terms
    get_bazi_year,
    get_bazi_month,
    
    # Utilities
    pillars_to_dict,
    validate_calculation,
    
    # Data classes
    Pillar,
    LuckPillar,
    DMStrength,
    
    # Constants
    HEAVENLY_STEMS,
    HEAVENLY_STEMS_CN,
    EARTHLY_BRANCHES,
    EARTHLY_BRANCHES_CN,
    BRANCH_ANIMALS,
    STEM_ELEMENTS,
    STEM_POLARITY,
    BRANCH_ELEMENTS,
    HIDDEN_STEMS,
    SOLAR_TERMS,
    ELEMENT_COLORS,
    TEN_GODS_CN,
    PROFILE_NAMES,
    PRODUCTIVE_CYCLE,
    PRODUCED_BY,
    CONTROLLING_CYCLE,
    CONTROLLED_BY,
    SIX_CLASHES,
    SIX_COMBINES,
    THREE_HARMONY,
    SEASONAL_STRENGTH,
)

__version__ = "1.0.0"
__all__ = [
    'analyze_bazi',
    'calculate_four_pillars',
    'calculate_dm_strength',
    'calculate_ten_profiles',
    'calculate_luck_pillars',
    'Pillar',
    'LuckPillar',
    'DMStrength',
]
