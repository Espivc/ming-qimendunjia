# Ming QiMenDunJia v8.0 - Core Module
# core/__init__.py
"""
Core calculation engines for Ming QiMenDunJia.

Modules:
- qmdj_engine: Complete QMDJ calculations with all indicators
- bazi_calculator: BaZi Four Pillars calculation
- formations: Formation database and detection (NEW in v8.0)
- destiny_engine: QMDJ Destiny Analysis (coming soon)

v8.0 Changes:
- Added formations module with 50+ formations
- Added formation detection and scoring
- Added export functions for Universal Schema v2.0
"""

__version__ = "8.0"

# Try to import from qmdj_engine (may not exist if user is just using formations)
try:
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
    QMDJ_ENGINE_AVAILABLE = True
except ImportError:
    QMDJ_ENGINE_AVAILABLE = False

# Import formations module (always available)
from .formations import (
    # Main classes
    Formation,
    FormationCategory,
    
    # Detection functions
    detect_formations,
    get_formation_score,
    
    # Display functions
    format_formation_display,
    get_formation_card,
    
    # Export functions
    export_formations_for_schema,
    
    # Database queries
    get_formation_by_name,
    get_formations_by_category,
    get_all_formations,
    get_database_stats,
    
    # Constants
    FORMATIONS_DATABASE,
    DOOR_ELEMENTS,
    ELEMENT_CONTROLS,
)

__all__ = [
    # Version
    "__version__",
    "QMDJ_ENGINE_AVAILABLE",
    
    # Formations (v8.0)
    "Formation",
    "FormationCategory",
    "detect_formations",
    "get_formation_score",
    "format_formation_display",
    "get_formation_card",
    "export_formations_for_schema",
    "get_formation_by_name",
    "get_formations_by_category",
    "get_all_formations",
    "get_database_stats",
    "FORMATIONS_DATABASE",
    "DOOR_ELEMENTS",
    "ELEMENT_CONTROLS",
]

# Add QMDJ engine exports if available
if QMDJ_ENGINE_AVAILABLE:
    __all__.extend([
        "generate_qmdj_chart",
        "calculate_qmdj_pillars",
        "calculate_death_emptiness",
        "calculate_horse_star",
        "calculate_nobleman",
        "calculate_lead_indicators",
        "PALACE_INFO",
        "LUOSHU_GRID",
        "NINE_STARS",
        "EIGHT_DOORS",
        "EIGHT_DEITIES",
    ])
