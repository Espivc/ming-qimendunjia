# Ming Qimen v6.0 - Core Module
"""
Core calculation engines for Ming Qimen.

Modules:
- qmdj_engine: Complete QMDJ calculations with all indicators
- bazi_calculator: BaZi Four Pillars calculation (existing)
- formations: Formation database and detection (coming soon)
- destiny_engine: QMDJ Destiny Analysis (coming soon)
"""

from .qmdj_engine import (
    # Main function
    generate_qmdj_chart,
    
    # Pillar calculations
    calculate_qmdj_pillars,
    calculate_year_pillar,
    calculate_month_pillar,
    calculate_day_pillar,
    calculate_hour_pillar,
    
    # Indicator calculations
    calculate_death_emptiness,
    calculate_horse_star,
    calculate_nobleman,
    calculate_lead_indicators,
    calculate_structure_and_ju,
    calculate_component_strength,
    
    # Utility functions
    get_chinese_hour_info,
    
    # Constants
    PALACE_INFO,
    LUOSHU_GRID,
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    NINE_STARS,
    EIGHT_DOORS,
    EIGHT_DEITIES,
    STEM_ELEMENTS,
    STEM_POLARITY,
    BRANCH_ELEMENTS,
    SGT,
)

__version__ = "6.0"
__all__ = [
    "generate_qmdj_chart",
    "calculate_qmdj_pillars",
    "calculate_death_emptiness",
    "calculate_horse_star",
    "calculate_nobleman",
    "calculate_lead_indicators",
    "calculate_structure_and_ju",
    "PALACE_INFO",
    "LUOSHU_GRID",
    "NINE_STARS",
    "EIGHT_DOORS",
    "EIGHT_DEITIES",
]
