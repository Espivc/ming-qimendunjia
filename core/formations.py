# Ming QiMenDunJia v8.0 - Formation Database
# core/formations.py
"""
Comprehensive QMDJ Formation Database
Based on Joey Yap methodology (#64 and #73 sources)

Contains 50+ formations organized by category:
- Auspicious Formations (吉格)
- Inauspicious Formations (凶格)
- Door-Stem Combinations
- Star-Door Combinations
- Special Formations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class FormationCategory(Enum):
    """Formation categories"""
    AUSPICIOUS = "Auspicious"
    INAUSPICIOUS = "Inauspicious"
    NEUTRAL = "Neutral"
    SPECIAL = "Special"


@dataclass
class Formation:
    """Formation data structure"""
    name_en: str
    name_cn: str
    category: FormationCategory
    components: Dict[str, str]  # What triggers this formation
    meaning: str
    advice: str
    source: str  # #64 or #73


# =============================================================================
# FORMATION DATABASE (50+ Formations)
# =============================================================================

FORMATIONS_DATABASE: List[Formation] = [
    # =========================================================================
    # AUSPICIOUS FORMATIONS (吉格) - 20+ formations
    # =========================================================================
    
    # --- Three Wonders Formations (三奇) ---
    Formation(
        name_en="Heaven's Three Wonders",
        name_cn="天三奇",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Yi-Bing-Ding sequence"},
        meaning="Yi 乙, Bing 丙, Ding 丁 appear in sequence. Ultimate blessing from heaven.",
        advice="Proceed with confidence. Heaven supports your actions.",
        source="#64"
    ),
    Formation(
        name_en="Earth's Three Wonders",
        name_cn="地三奇",
        category=FormationCategory.AUSPICIOUS,
        components={"earth_stem": "Yi-Bing-Ding sequence"},
        meaning="Yi 乙, Bing 丙, Ding 丁 in Earth position. Strong grounding support.",
        advice="Focus on tangible actions and earthly pursuits.",
        source="#64"
    ),
    
    # --- Yi Qi Formations (乙奇格) ---
    Formation(
        name_en="Yi + Open Door",
        name_cn="乙奇得使",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Yi", "door": "Open"},
        meaning="Wood Wonder meets Open Door. Excellent for negotiations, legal matters.",
        advice="Seek authority approval. Negotiations will succeed.",
        source="#64"
    ),
    Formation(
        name_en="Yi + Rest Door",
        name_cn="乙奇入休",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Yi", "door": "Rest"},
        meaning="Wood Wonder resting. Good for recovery, waiting, gathering strength.",
        advice="Pause and restore. Timing will improve.",
        source="#64"
    ),
    Formation(
        name_en="Yi + Life Door",
        name_cn="乙奇入生",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Yi", "door": "Life"},
        meaning="Wood Wonder generating. Excellent for starting businesses, new ventures.",
        advice="Begin new projects. Growth energy is strong.",
        source="#64"
    ),
    
    # --- Bing Qi Formations (丙奇格) ---
    Formation(
        name_en="Bing + Scenery Door",
        name_cn="丙奇入景",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Bing", "door": "Scenery"},
        meaning="Fire Wonder at Scenery. Excellent for exams, fame, recognition.",
        advice="Showcase your work. Public recognition awaits.",
        source="#64"
    ),
    Formation(
        name_en="Bing + Life Door",
        name_cn="丙奇入生",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Bing", "door": "Life"},
        meaning="Fire Wonder generating. Strong for wealth creation and expansion.",
        advice="Pursue financial opportunities aggressively.",
        source="#64"
    ),
    Formation(
        name_en="Bing + Open Door",
        name_cn="丙奇入开",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Bing", "door": "Open"},
        meaning="Fire illuminates authority. Government/official matters succeed.",
        advice="Approach authorities with confidence.",
        source="#64"
    ),
    
    # --- Ding Qi Formations (丁奇格) ---
    Formation(
        name_en="Ding + Rest Door",
        name_cn="丁奇入休",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Ding", "door": "Rest"},
        meaning="Yin Fire resting. Excellent for romance, relationships, secret matters.",
        advice="Focus on personal relationships. Hidden opportunities emerge.",
        source="#64"
    ),
    Formation(
        name_en="Ding + Scenery Door",
        name_cn="丁奇入景",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Ding", "door": "Scenery"},
        meaning="Intelligence shines. Perfect for study, documentation, creative work.",
        advice="Engage in intellectual pursuits. Learning is favored.",
        source="#64"
    ),
    Formation(
        name_en="Ding + Life Door",
        name_cn="丁奇入生",
        category=FormationCategory.AUSPICIOUS,
        components={"heaven_stem": "Ding", "door": "Life"},
        meaning="Subtle growth. Good for long-term investments, nurturing projects.",
        advice="Plant seeds for the future. Patient growth.",
        source="#64"
    ),
    
    # --- Star + Door Combinations (星门组合) ---
    Formation(
        name_en="Heart Star + Open Door",
        name_cn="天心遇开",
        category=FormationCategory.AUSPICIOUS,
        components={"star": "Heart", "door": "Open"},
        meaning="Medical/healing star with authority door. Excellent for health matters.",
        advice="Consult experts. Healing energy is present.",
        source="#73"
    ),
    Formation(
        name_en="Assistant Star + Life Door",
        name_cn="天辅遇生",
        category=FormationCategory.AUSPICIOUS,
        components={"star": "Assistant", "door": "Life"},
        meaning="Scholar star with growth door. Perfect for education, learning.",
        advice="Pursue knowledge. Teaching/learning excel.",
        source="#73"
    ),
    Formation(
        name_en="Ren Star + Rest Door",
        name_cn="天任遇休",
        category=FormationCategory.AUSPICIOUS,
        components={"star": "Ren", "door": "Rest"},
        meaning="Ambassador star resting. Good for real estate, property, stability.",
        advice="Focus on property matters. Stability favored.",
        source="#73"
    ),
    Formation(
        name_en="Hero Star + Scenery Door",
        name_cn="天英遇景",
        category=FormationCategory.AUSPICIOUS,
        components={"star": "Hero", "door": "Scenery"},
        meaning="Bright star at bright door. Fame, recognition, public success.",
        advice="Step into the spotlight. Recognition comes.",
        source="#73"
    ),
    
    # --- Deity + Door Combinations (神门组合) ---
    Formation(
        name_en="Chief + Open Door",
        name_cn="值符遇开",
        category=FormationCategory.AUSPICIOUS,
        components={"deity": "Chief", "door": "Open"},
        meaning="Highest authority blessing. Extremely auspicious for all official matters.",
        advice="This is a golden moment. Act decisively.",
        source="#73"
    ),
    Formation(
        name_en="Nine Heaven + Life Door",
        name_cn="九天遇生",
        category=FormationCategory.AUSPICIOUS,
        components={"deity": "Nine Heaven", "door": "Life"},
        meaning="Upward energy with growth. Excellent for expansion, reaching higher.",
        advice="Aim high. Growth and advancement favored.",
        source="#73"
    ),
    Formation(
        name_en="Six Harmony + Rest Door",
        name_cn="六合遇休",
        category=FormationCategory.AUSPICIOUS,
        components={"deity": "Six Harmony", "door": "Rest"},
        meaning="Harmony in rest. Perfect for partnerships, negotiations, agreements.",
        advice="Seek partnerships. Cooperation succeeds.",
        source="#73"
    ),
    Formation(
        name_en="Moon + Scenery Door",
        name_cn="太阴遇景",
        category=FormationCategory.AUSPICIOUS,
        components={"deity": "Moon", "door": "Scenery"},
        meaning="Hidden wisdom revealed. Good for strategy, planning.",
        advice="Use intuition. Hidden paths open up.",
        source="#73"
    ),
    
    # --- Special Auspicious (特吉格) ---
    Formation(
        name_en="Dragon Returns to Origin",
        name_cn="青龙返首",
        category=FormationCategory.AUSPICIOUS,
        components={"special": "Jia in Kun palace Yang Dun"},
        meaning="Green Dragon returns home. Major auspicious sign for new beginnings.",
        advice="Excellent timing. Fortune returns to you.",
        source="#64"
    ),
    Formation(
        name_en="Flying Bird Falls into Cave",
        name_cn="飞鸟跌穴",
        category=FormationCategory.AUSPICIOUS,
        components={"special": "Ding + Jia Zi Wu in palace"},
        meaning="Opportunity lands unexpectedly. Windfall, lucky discovery.",
        advice="Be receptive. Opportunities come to you.",
        source="#64"
    ),
    
    # =========================================================================
    # INAUSPICIOUS FORMATIONS (凶格) - 20+ formations
    # =========================================================================
    
    # --- Gate Oppression (门迫格) ---
    Formation(
        name_en="Door Oppression",
        name_cn="门迫",
        category=FormationCategory.INAUSPICIOUS,
        components={"condition": "Door element controlled by Palace element"},
        meaning="The door is suppressed by the palace. Opportunities blocked.",
        advice="Avoid forcing matters. Wait for better timing.",
        source="#64"
    ),
    
    # --- Stem Clashes (干冲格) ---
    Formation(
        name_en="Heaven Earth Clash",
        name_cn="天地相冲",
        category=FormationCategory.INAUSPICIOUS,
        components={"condition": "Heaven Stem clashes Earth Stem"},
        meaning="Upper and lower conflict. Internal contradiction, mixed signals.",
        advice="Resolve internal conflicts first. Don't proceed.",
        source="#64"
    ),
    
    # --- Geng Combinations (庚格) - The Obstacle Stem ---
    Formation(
        name_en="Geng + Open Door",
        name_cn="庚加开门",
        category=FormationCategory.INAUSPICIOUS,
        components={"heaven_stem": "Geng", "door": "Open"},
        meaning="Metal obstacle at authority. Official matters blocked.",
        advice="Avoid confronting authorities. Legal troubles possible.",
        source="#64"
    ),
    Formation(
        name_en="Geng + Life Door",
        name_cn="庚加生门",
        category=FormationCategory.INAUSPICIOUS,
        components={"heaven_stem": "Geng", "door": "Life"},
        meaning="Obstacle to growth. Business blockages, financial setbacks.",
        advice="Postpone investments. Growth energy blocked.",
        source="#64"
    ),
    Formation(
        name_en="Geng + Scenery Door",
        name_cn="庚加景门",
        category=FormationCategory.INAUSPICIOUS,
        components={"heaven_stem": "Geng", "door": "Scenery"},
        meaning="Metal clashes Fire. Exam failure, document problems.",
        advice="Avoid public exposure. Keep low profile.",
        source="#64"
    ),
    Formation(
        name_en="Geng + Rest Door",
        name_cn="庚加休门",
        category=FormationCategory.INAUSPICIOUS,
        components={"heaven_stem": "Geng", "door": "Rest"},
        meaning="Obstacle to rest. Cannot relax, hidden enemies.",
        advice="Stay vigilant. Rest is not safe.",
        source="#64"
    ),
    
    # --- Death Door Combinations (死门格) ---
    Formation(
        name_en="Death Door + Grass Star",
        name_cn="死门遇天芮",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Death", "star": "Grass"},
        meaning="Double illness energy. Severe health warning.",
        advice="Focus on health. Avoid risky activities.",
        source="#73"
    ),
    Formation(
        name_en="Death Door + Canopy Star",
        name_cn="死门遇天蓬",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Death", "star": "Canopy"},
        meaning="Thieves at death's door. Loss, theft, betrayal possible.",
        advice="Protect assets. Be wary of deceit.",
        source="#73"
    ),
    
    # --- Fear Door Combinations (惊门格) ---
    Formation(
        name_en="Fear Door + Tiger",
        name_cn="惊门遇白虎",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Fear", "deity": "Tiger"},
        meaning="Double fear energy. Legal troubles, accidents, shocking news.",
        advice="Stay calm. Avoid conflict and travel.",
        source="#73"
    ),
    Formation(
        name_en="Fear Door + Serpent",
        name_cn="惊门遇腾蛇",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Fear", "deity": "Serpent"},
        meaning="Frightening illusions. Anxiety, nightmares.",
        advice="Ground yourself. Don't trust first impressions.",
        source="#73"
    ),
    
    # --- Harm Door Combinations (伤门格) ---
    Formation(
        name_en="Harm Door + Impulse Star",
        name_cn="伤门遇天冲",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Harm", "star": "Impulse"},
        meaning="Double aggressive energy. Accidents, injuries, conflict.",
        advice="Avoid physical activities. Control temper.",
        source="#73"
    ),
    Formation(
        name_en="Harm Door + Tiger",
        name_cn="伤门遇白虎",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Harm", "deity": "Tiger"},
        meaning="Injury from metal. Surgery, accidents, violence.",
        advice="Be extremely careful. Postpone risky activities.",
        source="#73"
    ),
    
    # --- Delusion Door Combinations (杜门格) ---
    Formation(
        name_en="Delusion Door + Hook",
        name_cn="杜门遇勾陈",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Delusion", "deity": "Hook"},
        meaning="Trapped and stuck. Legal entanglement, unable to escape.",
        advice="Don't commit to anything. Seek exit strategies.",
        source="#73"
    ),
    Formation(
        name_en="Delusion Door + Emptiness",
        name_cn="杜门遇玄武",
        category=FormationCategory.INAUSPICIOUS,
        components={"door": "Delusion", "deity": "Emptiness"},
        meaning="Hidden deception blocked. Secrets will be exposed.",
        advice="Be honest. Hidden matters will surface.",
        source="#73"
    ),
    
    # --- Inauspicious Deity Combinations (凶神格) ---
    Formation(
        name_en="Tiger + Death Door",
        name_cn="白虎遇死门",
        category=FormationCategory.INAUSPICIOUS,
        components={"deity": "Tiger", "door": "Death"},
        meaning="Violent ending energy. Extreme caution required.",
        advice="Stay home. Avoid all risks.",
        source="#73"
    ),
    Formation(
        name_en="Serpent + Fear Door",
        name_cn="腾蛇遇惊门",
        category=FormationCategory.INAUSPICIOUS,
        components={"deity": "Serpent", "door": "Fear"},
        meaning="Nightmarish fears. Psychological distress.",
        advice="Seek calm. Ground yourself in reality.",
        source="#73"
    ),
    Formation(
        name_en="Hook + Harm Door",
        name_cn="勾陈遇伤门",
        category=FormationCategory.INAUSPICIOUS,
        components={"deity": "Hook", "door": "Harm"},
        meaning="Legal injury. Lawsuits, disputes, official trouble.",
        advice="Settle disputes quickly. Avoid litigation.",
        source="#73"
    ),
    
    # --- Special Inauspicious (特凶格) ---
    Formation(
        name_en="Fan Yin - Reversed Chart",
        name_cn="反吟",
        category=FormationCategory.INAUSPICIOUS,
        components={"special": "All components return to opposite position"},
        meaning="Everything reversed. Plans backfire, opposite results.",
        advice="Reconsider everything. Your assumptions are wrong.",
        source="#64"
    ),
    Formation(
        name_en="Fu Yin - Hidden Chart",
        name_cn="伏吟",
        category=FormationCategory.INAUSPICIOUS,
        components={"special": "Components in home palace"},
        meaning="Hidden/stagnant. Nothing moves, stuck situation.",
        advice="Be patient. Forcing will make things worse.",
        source="#64"
    ),
    Formation(
        name_en="Empty Death & Emptiness",
        name_cn="空亡落空",
        category=FormationCategory.INAUSPICIOUS,
        components={"condition": "Key component in Death & Emptiness"},
        meaning="Void energy. Plans will not materialize.",
        advice="Abandon current approach. Seek alternatives.",
        source="#64"
    ),
    
    # =========================================================================
    # NEUTRAL FORMATIONS (平格) - 10+ formations
    # =========================================================================
    
    Formation(
        name_en="Scenery Door + Hero Star",
        name_cn="景门遇天英",
        category=FormationCategory.NEUTRAL,
        components={"door": "Scenery", "star": "Hero"},
        meaning="Fire meets Fire. Intense but balanced. Good for short-term.",
        advice="Use for quick actions. Don't overextend.",
        source="#73"
    ),
    Formation(
        name_en="Rest Door + Canopy Star",
        name_cn="休门遇天蓬",
        category=FormationCategory.NEUTRAL,
        components={"door": "Rest", "star": "Canopy"},
        meaning="Water resting with water. Quiet scheming. Can go either way.",
        advice="Depends on your intentions. Use wisely.",
        source="#73"
    ),
    Formation(
        name_en="Life Door + Grass Star",
        name_cn="生门遇天芮",
        category=FormationCategory.NEUTRAL,
        components={"door": "Life", "star": "Grass"},
        meaning="Growth with illness. Recovery possible but slow.",
        advice="Focus on healing. Growth comes after recovery.",
        source="#73"
    ),
    Formation(
        name_en="Open Door + Pillar Star",
        name_cn="开门遇天柱",
        category=FormationCategory.NEUTRAL,
        components={"door": "Open", "star": "Pillar"},
        meaning="Authority with criticism. Can gain position but face opposition.",
        advice="Expect challenges. Prepare for scrutiny.",
        source="#73"
    ),
    Formation(
        name_en="Nine Earth + Rest Door",
        name_cn="九地遇休门",
        category=FormationCategory.NEUTRAL,
        components={"deity": "Nine Earth", "door": "Rest"},
        meaning="Deep grounding in rest. Good for hiding, waiting.",
        advice="Lay low. Build strength quietly.",
        source="#73"
    ),
    Formation(
        name_en="Moon + Delusion Door",
        name_cn="太阴遇杜门",
        category=FormationCategory.NEUTRAL,
        components={"deity": "Moon", "door": "Delusion"},
        meaning="Hidden secrets. Good for private matters, not public.",
        advice="Keep things private. Don't reveal plans.",
        source="#73"
    ),
    Formation(
        name_en="Connect Star + Life Door",
        name_cn="天禽遇生门",
        category=FormationCategory.NEUTRAL,
        components={"star": "Connect", "door": "Life"},
        meaning="Center energy with growth. Depends on other factors.",
        advice="Context matters. Check other components.",
        source="#73"
    ),
    
    # =========================================================================
    # SPECIAL/TIMING FORMATIONS (时格)
    # =========================================================================
    
    Formation(
        name_en="Meeting the Chief",
        name_cn="遇值符",
        category=FormationCategory.SPECIAL,
        components={"condition": "Chief deity present"},
        meaning="The highest authority blesses this palace. Very auspicious modifier.",
        advice="This palace is especially favored.",
        source="#73"
    ),
    Formation(
        name_en="Horse Star Activation",
        name_cn="驿马动",
        category=FormationCategory.SPECIAL,
        components={"condition": "Horse Star in active palace"},
        meaning="Movement and travel energy. Good for journeys, changes.",
        advice="Travel is favored. Movement brings opportunity.",
        source="#73"
    ),
    Formation(
        name_en="Nobleman Arrives",
        name_cn="贵人至",
        category=FormationCategory.SPECIAL,
        components={"condition": "Nobleman in queried palace"},
        meaning="Helpful people appear. Support from authorities.",
        advice="Seek help. Nobles will assist you.",
        source="#73"
    ),
    Formation(
        name_en="Lead Door Active",
        name_cn="直使当位",
        category=FormationCategory.SPECIAL,
        components={"condition": "Lead Door in queried palace"},
        meaning="The Envoy is present. Strong timing energy.",
        advice="Act now. Timing is optimal.",
        source="#73"
    ),
    Formation(
        name_en="Lead Star Active",
        name_cn="直符当位",
        category=FormationCategory.SPECIAL,
        components={"condition": "Lead Star in queried palace"},
        meaning="The Chief Star is here. Authority energy concentrated.",
        advice="Leadership energy strong. Take charge.",
        source="#73"
    ),
]


# =============================================================================
# FORMATION DETECTION ENGINE
# =============================================================================

def detect_formations(
    palace_data: Dict,
    chart_data: Optional[Dict] = None
) -> List[Formation]:
    """
    Detect all applicable formations for a given palace.
    
    Args:
        palace_data: Dictionary containing palace components
        chart_data: Optional full chart data for special formations
        
    Returns:
        List of detected Formation objects
    """
    detected = []
    
    heaven_stem = palace_data.get("heaven_stem", "")
    earth_stem = palace_data.get("earth_stem", "")
    door = palace_data.get("door", "")
    star = palace_data.get("star", "")
    deity = palace_data.get("deity", "")
    palace_element = palace_data.get("palace_element", "")
    
    for formation in FORMATIONS_DATABASE:
        components = formation.components
        matches = True
        
        # Check direct component matches
        if "heaven_stem" in components and not components["heaven_stem"].endswith("sequence"):
            if components["heaven_stem"] != heaven_stem:
                matches = False
                
        if "earth_stem" in components and not components["earth_stem"].endswith("sequence"):
            if components["earth_stem"] != earth_stem:
                matches = False
                
        if "door" in components:
            if components["door"] != door:
                matches = False
                
        if "star" in components:
            if components["star"] != star:
                matches = False
                
        if "deity" in components:
            if components["deity"] != deity:
                matches = False
        
        # Check conditional formations
        if "condition" in components:
            condition = components["condition"]
            
            if condition == "Door element controlled by Palace element":
                door_element = DOOR_ELEMENTS.get(door, "")
                if not is_controlled(door_element, palace_element):
                    matches = False
                    
            elif condition == "Heaven Stem clashes Earth Stem":
                if not stems_clash(heaven_stem, earth_stem):
                    matches = False
                    
            elif condition == "Chief deity present":
                if deity != "Chief":
                    matches = False
                    
            elif condition == "Horse Star in active palace":
                if not palace_data.get("has_horse", False):
                    matches = False
                    
            elif condition == "Nobleman in queried palace":
                if not palace_data.get("has_nobleman", False):
                    matches = False
                    
            elif condition == "Lead Door in queried palace":
                if not palace_data.get("is_lead_palace", False):
                    matches = False
                    
            elif condition == "Lead Star in queried palace":
                if not palace_data.get("is_lead_star_palace", False):
                    matches = False
                    
            elif condition == "Key component in Death & Emptiness":
                if not palace_data.get("death_emptiness", False):
                    matches = False
            else:
                # Skip special conditions we can't verify without full chart
                if "special" in components:
                    matches = False
        
        # Skip special pattern formations (need full chart analysis)
        if "special" in components:
            matches = False
        
        if matches:
            detected.append(formation)
    
    return detected


def get_formation_score(formations: List[Formation]) -> Tuple[int, str]:
    """Calculate net formation score and summary."""
    if not formations:
        return (0, "No special formations detected")
    
    auspicious = sum(1 for f in formations if f.category == FormationCategory.AUSPICIOUS)
    inauspicious = sum(1 for f in formations if f.category == FormationCategory.INAUSPICIOUS)
    special = sum(1 for f in formations if f.category == FormationCategory.SPECIAL)
    
    score = auspicious - inauspicious + (1 if special > 0 else 0)
    score = max(-3, min(3, score))
    
    if score >= 2:
        summary = f"✨ Highly Auspicious ({auspicious} good formations)"
    elif score == 1:
        summary = f"✨ Auspicious ({auspicious} good formations)"
    elif score == 0:
        summary = "⚖️ Neutral (mixed formations)"
    elif score == -1:
        summary = f"⚠️ Inauspicious ({inauspicious} bad formations)"
    else:
        summary = f"⚠️ Highly Inauspicious ({inauspicious} bad formations)"
    
    return (score, summary)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

DOOR_ELEMENTS = {
    "Open": "Metal", "Rest": "Water", "Life": "Earth", "Harm": "Wood",
    "Delusion": "Wood", "Scenery": "Fire", "Death": "Earth", "Fear": "Metal"
}

ELEMENT_CONTROLS = {
    "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
    "Metal": "Wood", "Water": "Fire"
}

STEM_CLASHES = [
    ("Jia", "Geng"), ("Yi", "Xin"), ("Bing", "Ren"),
    ("Ding", "Gui"), ("Wu", "Jia"), ("Ji", "Yi")
]


def is_controlled(element1: str, element2: str) -> bool:
    """Check if element1 is controlled by element2."""
    return ELEMENT_CONTROLS.get(element2) == element1


def stems_clash(stem1: str, stem2: str) -> bool:
    """Check if two stems clash."""
    return (stem1, stem2) in STEM_CLASHES or (stem2, stem1) in STEM_CLASHES


def format_formation_display(formation: Formation) -> str:
    """Format formation for display."""
    emoji = {
        FormationCategory.AUSPICIOUS: "✨",
        FormationCategory.INAUSPICIOUS: "⚠️",
        FormationCategory.NEUTRAL: "⚖️",
        FormationCategory.SPECIAL: "🌟"
    }
    return f"{emoji.get(formation.category, '•')} **{formation.name_en}** ({formation.name_cn})"


def get_formation_card(formation: Formation) -> Dict:
    """Get formation as a display card dictionary."""
    colors = {
        FormationCategory.AUSPICIOUS: "#4CAF50",
        FormationCategory.INAUSPICIOUS: "#F44336",
        FormationCategory.NEUTRAL: "#9E9E9E",
        FormationCategory.SPECIAL: "#FF9800"
    }
    return {
        "name_en": formation.name_en,
        "name_cn": formation.name_cn,
        "category": formation.category.value,
        "color": colors.get(formation.category, "#9E9E9E"),
        "meaning": formation.meaning,
        "advice": formation.advice,
        "source": formation.source
    }


def export_formations_for_schema(detected: List[Formation]) -> Dict:
    """Export detected formations in Universal Schema v2.0 format."""
    if not detected:
        return {"primary_formation": None, "secondary_formations": []}
    
    # Primary = first auspicious, then inauspicious, then first overall
    primary = None
    for cat in [FormationCategory.AUSPICIOUS, FormationCategory.INAUSPICIOUS]:
        for f in detected:
            if f.category == cat:
                primary = f
                break
        if primary:
            break
    
    if not primary:
        primary = detected[0]
    
    secondary = [f for f in detected if f != primary][:3]
    
    return {
        "primary_formation": {
            "name": primary.name_en,
            "name_cn": primary.name_cn,
            "category": primary.category.value,
            "source_book": primary.source,
            "outcome_pattern": primary.meaning
        },
        "secondary_formations": [
            {"name": f.name_en, "name_cn": f.name_cn, "source_book": f.source}
            for f in secondary
        ]
    }


# =============================================================================
# DATABASE QUERIES
# =============================================================================

def get_formation_by_name(name: str) -> Optional[Formation]:
    """Look up formation by English or Chinese name."""
    name_lower = name.lower()
    for f in FORMATIONS_DATABASE:
        if f.name_en.lower() == name_lower or f.name_cn == name:
            return f
    return None


def get_formations_by_category(category: FormationCategory) -> List[Formation]:
    """Get all formations of a specific category."""
    return [f for f in FORMATIONS_DATABASE if f.category == category]


def get_all_formations() -> List[Formation]:
    """Get complete formation database."""
    return FORMATIONS_DATABASE.copy()


def get_database_stats() -> Dict:
    """Get formation database statistics."""
    return {
        "total": len(FORMATIONS_DATABASE),
        "auspicious": len(get_formations_by_category(FormationCategory.AUSPICIOUS)),
        "inauspicious": len(get_formations_by_category(FormationCategory.INAUSPICIOUS)),
        "neutral": len(get_formations_by_category(FormationCategory.NEUTRAL)),
        "special": len(get_formations_by_category(FormationCategory.SPECIAL))
    }


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("🏯 Ming QiMenDunJia v8.0 - Formation Database")
    print("=" * 50)
    
    stats = get_database_stats()
    print(f"Total Formations: {stats['total']}")
    for cat, count in stats.items():
        if cat != "total":
            print(f"  {cat.title()}: {count}")
    
    print("\n" + "=" * 50)
    print("Sample Detection Test:")
    
    test_palace = {
        "heaven_stem": "Yi",
        "door": "Open",
        "star": "Heart",
        "deity": "Chief",
        "palace_element": "Metal",
        "has_nobleman": True
    }
    
    detected = detect_formations(test_palace)
    print(f"Palace: Yi + Open + Heart + Chief")
    print(f"Detected {len(detected)} formations:")
    for f in detected:
        print(f"  {format_formation_display(f)}")
    
    score, summary = get_formation_score(detected)
    print(f"\nScore: {score:+d} - {summary}")
