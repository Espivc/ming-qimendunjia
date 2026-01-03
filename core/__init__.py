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
    calculate_profile_percentages_joey_yap,
    get_dominant_profile,
    get_dominant_profile_joey_yap,
    
    # Luck Pillars
    calculate_luck_pillars,
    calculate_luck_pillar_start_age,
    get_luck_direction,
    
    # Symbolic Stars (NEW!)
    calculate_symbolic_stars,
    calculate_life_palace,
    calculate_conception_palace,
    
    # Life Stages (NEW!)
    get_life_stage,
    calculate_life_stages_for_chart,
    
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
    # Symbolic Stars constants
    NOBLE_PEOPLE,
    PEACH_BLOSSOM,
    INTELLIGENCE_STAR,
    SKY_HORSE,
    SOLITARY_STAR,
    TWELVE_STAGES,
)

__version__ = "1.1.0"
__all__ = [
    'analyze_bazi',
    'calculate_four_pillars',
    'calculate_dm_strength',
    'calculate_ten_profiles',
    'calculate_profile_percentages_joey_yap',
    'calculate_luck_pillars',
    'calculate_symbolic_stars',
    'calculate_life_stages_for_chart',
    'Pillar',
    'LuckPillar',
    'DMStrength',
]
