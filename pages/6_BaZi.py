# pages/6_BaZi.py - Ming QiMenDunJia v10.5 PRO - FIXED
# Complete BaZi Analysis with Full Interpretations
# FIXED: Month pillar now uses solar terms correctly!
import streamlit as st
from datetime import datetime, date
import json

st.set_page_config(page_title="BaZi Pro | Ming Qimen", page_icon="🎴", layout="wide")

# =============================================================================
# CONSTANTS & DATA
# =============================================================================

STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
STEMS_CN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
BRANCHES_CN = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

STEM_ELEM = {"Jia":"Wood","Yi":"Wood","Bing":"Fire","Ding":"Fire","Wu":"Earth","Ji":"Earth","Geng":"Metal","Xin":"Metal","Ren":"Water","Gui":"Water"}
STEM_POL = {"Jia":"Yang","Yi":"Yin","Bing":"Yang","Ding":"Yin","Wu":"Yang","Ji":"Yin","Geng":"Yang","Xin":"Yin","Ren":"Yang","Gui":"Yin"}
BRANCH_ELEM = {"Zi":"Water","Chou":"Earth","Yin":"Wood","Mao":"Wood","Chen":"Earth","Si":"Fire","Wu":"Fire","Wei":"Earth","Shen":"Metal","You":"Metal","Xu":"Earth","Hai":"Water"}

HIDDEN = {"Zi":["Gui"],"Chou":["Ji","Gui","Xin"],"Yin":["Jia","Bing","Wu"],"Mao":["Yi"],"Chen":["Wu","Yi","Gui"],
          "Si":["Bing","Wu","Geng"],"Wu":["Ding","Ji"],"Wei":["Ji","Ding","Yi"],"Shen":["Geng","Ren","Wu"],
          "You":["Xin"],"Xu":["Wu","Xin","Ding"],"Hai":["Ren","Jia"]}

# =============================================================================
# 1. DAY MASTER INTERPRETATIONS
# =============================================================================

DAY_MASTER_INFO = {
    "Jia": {
        "cn": "甲", "element": "Wood", "polarity": "Yang",
        "image": "🌲 The Tall Tree / The General",
        "personality": """**Jia Wood** is the mighty oak tree - tall, upright, and unwavering. You possess natural leadership qualities and strong principles. Like a tree that grows straight toward the sun, you have clear ambitions and the determination to achieve them.

**Core Traits:**
- Strong sense of justice and fairness
- Natural leader who inspires others
- Stubborn but reliable and trustworthy
- Needs space to grow and expand
- Values integrity above all else

**Strengths:** Leadership, vision, integrity, perseverance, ambition
**Challenges:** Inflexibility, stubbornness, difficulty adapting, can be too rigid""",
        "career": "Leadership roles, management, entrepreneurship, law, military, forestry, education",
        "relationship": "Needs a partner who respects your independence. Best with supportive Earth or nurturing Water types."
    },
    "Yi": {
        "cn": "乙", "element": "Wood", "polarity": "Yin",
        "image": "🌿 The Vine / The Diplomat",
        "personality": """**Yi Wood** is the flexible vine or flower - adaptable, graceful, and resilient. You possess the ability to navigate complex situations with elegance. Like a vine that finds its way around obstacles, you excel at finding creative solutions.

**Core Traits:**
- Highly adaptable and flexible
- Excellent at networking and relationships
- Artistic and creative nature
- Can appear gentle but has inner strength
- Skilled at diplomacy and negotiation

**Strengths:** Adaptability, creativity, diplomacy, charm, resilience
**Challenges:** Can be indecisive, overly dependent on others, may lack direction""",
        "career": "Arts, design, diplomacy, counseling, beauty industry, fashion, public relations",
        "relationship": "Seeks harmony and connection. Compatible with protective Metal or supportive Water types."
    },
    "Bing": {
        "cn": "丙", "element": "Fire", "polarity": "Yang",
        "image": "☀️ The Sun / The Inspirer",
        "personality": """**Bing Fire** is the blazing sun - warm, generous, and impossible to ignore. You radiate energy and enthusiasm that naturally draws others to you. Like the sun that shines on everyone equally, you're generous and open-hearted.

**Core Traits:**
- Charismatic and magnetic personality
- Generous and warm-hearted
- Natural optimist with infectious enthusiasm
- Needs to be seen and appreciated
- Can illuminate any situation

**Strengths:** Charisma, generosity, optimism, leadership, inspiration
**Challenges:** Can be attention-seeking, burns out easily, may lack depth""",
        "career": "Entertainment, media, politics, public speaking, marketing, hospitality",
        "relationship": "Needs admiration and appreciation. Best with grounding Earth or appreciative Wood types."
    },
    "Ding": {
        "cn": "丁", "element": "Fire", "polarity": "Yin",
        "image": "🕯️ The Candle / The Thinker",
        "personality": """**Ding Fire** is the gentle candlelight - focused, thoughtful, and illuminating. You possess deep intuition and the ability to see what others miss. Like a candle that lights the darkness, you bring clarity to complex situations.

**Core Traits:**
- Highly intuitive and perceptive
- Thoughtful and contemplative
- Warm but focused energy
- Excellent at detailed work
- Inner fire that sustains through challenges

**Strengths:** Intuition, focus, warmth, perception, dedication
**Challenges:** Can be moody, overly sensitive, may burn out from within""",
        "career": "Research, writing, counseling, spirituality, detailed crafts, psychology",
        "relationship": "Seeks deep connection. Compatible with supportive Wood or stable Earth types."
    },
    "Wu": {
        "cn": "戊", "element": "Earth", "polarity": "Yang",
        "image": "🏔️ The Mountain / The Stabilizer",
        "personality": """**Wu Earth** is the mighty mountain - solid, reliable, and unmovable. You provide stability and security to everyone around you. Like a mountain that has stood for millennia, you're patient and enduring.

**Core Traits:**
- Extremely reliable and trustworthy
- Patient and steady in all situations
- Provides security and stability to others
- Can be stubborn but always dependable
- Natural mediator and peacekeeper

**Strengths:** Reliability, patience, stability, trustworthiness, endurance
**Challenges:** Stubbornness, resistance to change, can be too passive""",
        "career": "Real estate, agriculture, management, banking, construction, HR",
        "relationship": "Provides security and stability. Best with dynamic Fire or grounded Metal types."
    },
    "Ji": {
        "cn": "己", "element": "Earth", "polarity": "Yin",
        "image": "🌾 The Garden / The Nurturer",
        "personality": """**Ji Earth** is fertile garden soil - nurturing, productive, and life-giving. You have the ability to help others grow and flourish. Like soil that supports all plants, you're adaptable and supportive.

**Core Traits:**
- Nurturing and supportive nature
- Highly adaptable to different situations
- Productive and practical minded
- Excellent at bringing out the best in others
- Humble but essential presence

**Strengths:** Nurturing, adaptability, productivity, humility, support
**Challenges:** Can be too self-sacrificing, may lack personal boundaries""",
        "career": "Education, healthcare, agriculture, food industry, childcare, social work",
        "relationship": "Nurtures and supports partners. Compatible with appreciative Wood or passionate Fire types."
    },
    "Geng": {
        "cn": "庚", "element": "Metal", "polarity": "Yang",
        "image": "⚔️ The Sword / The Warrior",
        "personality": """**Geng Metal** is the sharp sword - decisive, principled, and powerful. You cut through confusion with clarity and make tough decisions others avoid. Like a sword that must be forged through fire, you grow stronger through challenges.

**Core Traits:**
- Decisive and action-oriented
- Strong sense of justice and fairness
- Courageous and willing to fight for beliefs
- Values loyalty and honor
- Direct communication style

**Strengths:** Decisiveness, courage, loyalty, justice, strength
**Challenges:** Can be harsh, inflexible, may hurt others unintentionally""",
        "career": "Military, law enforcement, surgery, engineering, sports, martial arts, management",
        "relationship": "Needs respect and loyalty. Best with softening Water or supportive Earth types."
    },
    "Xin": {
        "cn": "辛", "element": "Metal", "polarity": "Yin",
        "image": "💎 The Jewel / The Perfectionist",
        "personality": """**Xin Metal** is the precious jewel - refined, beautiful, and valuable. You have high standards and an eye for quality in everything. Like a jewel that must be polished, you continuously refine yourself.

**Core Traits:**
- High standards and attention to detail
- Refined taste and aesthetic sense
- Sensitive and emotionally deep
- Values quality over quantity
- Can be critical but seeks perfection

**Strengths:** Refinement, sensitivity, attention to detail, aesthetic sense
**Challenges:** Can be overly critical, perfectionist, may appear cold""",
        "career": "Jewelry, finance, law, luxury goods, beauty, quality control, arts",
        "relationship": "Seeks refinement and appreciation. Compatible with nurturing Earth or warming Fire types."
    },
    "Ren": {
        "cn": "壬", "element": "Water", "polarity": "Yang",
        "image": "🌊 The Ocean / The Philosopher",
        "personality": """**Ren Water** is the vast ocean - deep, powerful, and containing infinite wisdom. You possess great intellectual capacity and the ability to understand complex systems. Like the ocean that connects all continents, you see the big picture.

**Core Traits:**
- Deep intellectual capacity
- Excellent strategic thinking
- Adaptable yet powerful
- Natural wisdom and insight
- Can be overwhelming in intensity

**Strengths:** Wisdom, strategy, adaptability, depth, vision
**Challenges:** Can be scattered, emotionally turbulent, may lack focus""",
        "career": "Philosophy, research, shipping, travel, consulting, strategic planning, import/export",
        "relationship": "Needs intellectual connection. Best with grounding Earth or inspiring Wood types."
    },
    "Gui": {
        "cn": "癸", "element": "Water", "polarity": "Yin",
        "image": "💧 The Rain / The Intuitive",
        "personality": """**Gui Water** is gentle rain or morning dew - subtle, nourishing, and life-giving. You possess deep intuition and the ability to nurture growth in others. Like rain that falls everywhere equally, you're compassionate and giving.

**Core Traits:**
- Highly intuitive and psychic
- Gentle and compassionate nature
- Nourishing presence for others
- Deep emotional understanding
- Subtle but persistent influence

**Strengths:** Intuition, compassion, gentleness, emotional intelligence
**Challenges:** Can be overly emotional, may lack assertiveness, easily influenced""",
        "career": "Spirituality, counseling, healthcare, writing, music, psychology, caregiving",
        "relationship": "Seeks emotional depth. Compatible with protective Metal or stable Earth types."
    }
}

# =============================================================================
# 2-4. DIRECTIONS DATA
# =============================================================================

ELEMENT_DIRECTIONS = {
    "Wood": {"favorable": ["East", "Southeast"], "direction_cn": "東、東南", "color": "Green", "number": "3, 4"},
    "Fire": {"favorable": ["South"], "direction_cn": "南", "color": "Red/Purple", "number": "9"},
    "Earth": {"favorable": ["Northeast", "Southwest", "Center"], "direction_cn": "東北、西南、中", "color": "Yellow/Brown", "number": "2, 5, 8"},
    "Metal": {"favorable": ["West", "Northwest"], "direction_cn": "西、西北", "color": "White/Gold", "number": "6, 7"},
    "Water": {"favorable": ["North"], "direction_cn": "北", "color": "Black/Blue", "number": "1"}
}

# =============================================================================
# 10. SIX ASPECTS
# =============================================================================

SIX_ASPECTS = {
    "Wealth": {"gods": ["DW", "IW"], "area": "财运", "meaning": "Money, assets, business income, financial opportunities"},
    "Career": {"gods": ["DO", "7K"], "area": "事业", "meaning": "Job, position, authority, recognition, government relations"},
    "Resource": {"gods": ["DR", "IR"], "area": "贵人", "meaning": "Support, education, mentors, helpful people, knowledge"},
    "Output": {"gods": ["EG", "HO"], "area": "表现", "meaning": "Expression, creativity, children, ideas, performance"},
    "Companion": {"gods": ["F", "RW"], "area": "人际", "meaning": "Friends, siblings, peers, competition, networking"},
    "Health": {"gods": ["7K", "HO"], "area": "健康", "meaning": "Physical wellness, stress, pressure, vitality"}
}

# =============================================================================
# 12-13. STRUCTURES & PROFILES
# =============================================================================

FIVE_STRUCTURES = {
    "Wealth": {
        "gods": ["DW", "IW"], "element": "Wood", "cn": "財型",
        "description": "Wealth Structure indicates strong focus on financial matters, material acquisition, and resource management.",
        "strengths": "Good at making money, practical, goal-oriented, business-minded",
        "careers": "Business, sales, finance, investment, real estate, trading"
    },
    "Influence": {
        "gods": ["DO", "7K"], "element": "Fire", "cn": "官型", 
        "description": "Influence Structure shows natural authority, leadership ability, and desire for recognition and status.",
        "strengths": "Leadership, discipline, responsibility, ambition, status-conscious",
        "careers": "Government, management, politics, law, military, corporate leadership"
    },
    "Resource": {
        "gods": ["DR", "IR"], "element": "Earth", "cn": "印型",
        "description": "Resource Structure indicates love of learning, need for support, and connection to knowledge and wisdom.",
        "strengths": "Intellectual, thoughtful, supported by others, good learner, wise",
        "careers": "Education, research, consulting, writing, advisory, academics"
    },
    "Companion": {
        "gods": ["F", "RW"], "element": "Metal", "cn": "比型",
        "description": "Companion Structure shows strong peer relationships, competition awareness, and collaborative nature.",
        "strengths": "Networking, teamwork, competitive, loyal, social",
        "careers": "Partnerships, team sports, networking businesses, franchises"
    },
    "Output": {
        "gods": ["EG", "HO"], "element": "Water", "cn": "食傷型",
        "description": "Output Structure indicates creativity, self-expression, and desire to share ideas with the world.",
        "strengths": "Creative, expressive, innovative, artistic, communicative",
        "careers": "Arts, entertainment, writing, teaching, marketing, media"
    }
}

TEN_PROFILES = {
    "F": {"name": "The Friend 比肩", "cn": "比肩", "brief": "Collaborative, loyal, peer-focused",
          "description": "Friends value relationships with peers and equals. You work well in teams and value fairness and reciprocity.",
          "strengths": "Loyal, fair, cooperative, supportive", "challenges": "Can be too dependent on peers, competitive"},
    "RW": {"name": "The Leader 劫财", "cn": "劫财", "brief": "Ambitious, competitive, action-oriented",
           "description": "Rob Wealth types are natural competitors who drive hard for success. You're action-oriented and ambitious.",
           "strengths": "Driven, ambitious, competitive, bold", "challenges": "Can be aggressive, overspending, risky"},
    "EG": {"name": "The Artist 食神", "cn": "食神", "brief": "Creative, expressive, pleasure-seeking",
           "description": "Eating Gods are creative souls who enjoy life's pleasures. You express yourself through art, food, or lifestyle.",
           "strengths": "Creative, joyful, expressive, talented", "challenges": "Can be indulgent, unfocused, lazy"},
    "HO": {"name": "The Performer 伤官", "cn": "伤官", "brief": "Innovative, rebellious, outspoken",
           "description": "Hurting Officers are innovators who challenge the status quo. You're not afraid to speak your mind.",
           "strengths": "Innovative, brave, talented, expressive", "challenges": "Can be rebellious, critical, disruptive"},
    "DW": {"name": "The Director 正财", "cn": "正财", "brief": "Practical, steady, financially focused",
           "description": "Direct Wealth types are practical money managers. You build wealth steadily through hard work.",
           "strengths": "Practical, reliable, hardworking, stable", "challenges": "Can be materialistic, workaholic"},
    "IW": {"name": "The Pioneer 偏财", "cn": "偏财", "brief": "Opportunistic, risk-taking, entrepreneurial",
           "description": "Indirect Wealth types spot opportunities others miss. You're entrepreneurial and willing to take calculated risks.",
           "strengths": "Opportunistic, bold, visionary, adaptable", "challenges": "Can be risky, unstable, speculative"},
    "DO": {"name": "The Diplomat 正官", "cn": "正官", "brief": "Disciplined, responsible, status-conscious",
           "description": "Direct Officers value order, rules, and proper conduct. You excel in structured environments.",
           "strengths": "Disciplined, responsible, respected, ethical", "challenges": "Can be rigid, status-obsessed"},
    "7K": {"name": "The Warrior 七杀", "cn": "七杀", "brief": "Powerful, intense, transformative",
           "description": "Seven Killings types are intense and powerful. You transform through pressure and challenge.",
           "strengths": "Powerful, determined, resilient, transformative", "challenges": "Can be aggressive, stressed"},
    "DR": {"name": "The Analyzer 正印", "cn": "正印", "brief": "Thoughtful, supported, knowledge-seeking",
           "description": "Direct Resource types love learning and are supported by others. You analyze before acting.",
           "strengths": "Thoughtful, supported, wise, caring", "challenges": "Can be passive, overthinking"},
    "IR": {"name": "The Philosopher 偏印", "cn": "偏印", "brief": "Unconventional, intuitive, independent",
           "description": "Indirect Resource types think differently. You have unique insights and unconventional wisdom.",
           "strengths": "Innovative, intuitive, independent, unique", "challenges": "Can be isolated, eccentric"}
}

# =============================================================================
# 11. MONTHLY ELEMENTS 2025
# =============================================================================

MONTHLY_STEMS_2025 = {
    1: ("Ding", "Chou", "丁丑", "Yin Fire on Earth"), 2: ("Wu", "Yin", "戊寅", "Yang Earth on Wood"),
    3: ("Ji", "Mao", "己卯", "Yin Earth on Wood"), 4: ("Geng", "Chen", "庚辰", "Yang Metal on Earth"),
    5: ("Xin", "Si", "辛巳", "Yin Metal on Fire"), 6: ("Ren", "Wu", "壬午", "Yang Water on Fire"),
    7: ("Gui", "Wei", "癸未", "Yin Water on Earth"), 8: ("Jia", "Shen", "甲申", "Yang Wood on Metal"),
    9: ("Yi", "You", "乙酉", "Yin Wood on Metal"), 10: ("Bing", "Xu", "丙戌", "Yang Fire on Earth"),
    11: ("Ding", "Hai", "丁亥", "Yin Fire on Water"), 12: ("Wu", "Zi", "戊子", "Yang Earth on Water")
}

# =============================================================================
# CALCULATION FUNCTIONS - FIXED with Solar Terms!
# =============================================================================

# Solar term dates (Jie terms that START each BaZi month)
SOLAR_TERMS = {
    1: (2, 4),    # 立春 → Month 1 (寅 Tiger)
    2: (3, 6),    # 惊蛰 → Month 2 (卯 Rabbit)
    3: (4, 5),    # 清明 → Month 3 (辰 Dragon)
    4: (5, 6),    # 立夏 → Month 4 (巳 Snake)
    5: (6, 6),    # 芒种 → Month 5 (午 Horse) ← June 27 is HERE!
    6: (7, 7),    # 小暑 → Month 6 (未 Goat)
    7: (8, 8),    # 立秋 → Month 7 (申 Monkey)
    8: (9, 8),    # 白露 → Month 8 (酉 Rooster)
    9: (10, 8),   # 寒露 → Month 9 (戌 Dog)
    10: (11, 7),  # 立冬 → Month 10 (亥 Pig)
    11: (12, 7),  # 大雪 → Month 11 (子 Rat)
    12: (1, 6),   # 小寒 → Month 12 (丑 Ox)
}

MONTH_BRANCHES = ["Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai", "Zi", "Chou"]

def calc_year_pillar(year, month=6, day=15):
    """Calculate year pillar - year changes at Li Chun (Feb 4), not Jan 1!"""
    li_chun_month, li_chun_day = SOLAR_TERMS[1]
    if month < li_chun_month or (month == li_chun_month and day < li_chun_day):
        year = year - 1
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return STEMS[stem_idx], BRANCHES[branch_idx]

def get_bazi_month(year, month, day):
    """Determine BaZi month (1-12) based on solar terms."""
    for bazi_month in range(12, 0, -1):
        solar_month, solar_day = SOLAR_TERMS[bazi_month]
        if bazi_month == 12:
            if month == 1 and day >= solar_day:
                return 12
            elif month == 12:
                m11_month, m11_day = SOLAR_TERMS[11]
                if month > m11_month or (month == m11_month and day >= m11_day):
                    return 11
        else:
            if month > solar_month or (month == solar_month and day >= solar_day):
                return bazi_month
    return 12

def calc_month_pillar(year, month, day):
    """Calculate month pillar using SOLAR TERMS - FIXED!"""
    bazi_month = get_bazi_month(year, month, day)
    month_branch = MONTH_BRANCHES[bazi_month - 1]
    
    # Get year stem (considering Li Chun boundary)
    year_stem, _ = calc_year_pillar(year, month, day)
    year_stem_idx = STEMS.index(year_stem)
    
    # Calculate month stem: First month starts at (year_stem * 2 + 2) % 10
    first_month_stem_idx = (year_stem_idx * 2 + 2) % 10
    month_stem_idx = (first_month_stem_idx + bazi_month - 1) % 10
    month_stem = STEMS[month_stem_idx]
    
    return month_stem, month_branch

def calc_day_pillar(dt):
    """Calculate day pillar."""
    ref = date(1900, 1, 1)
    days = (dt - ref).days
    return STEMS[days % 10], BRANCHES[(days + 10) % 12]

def calc_hour_pillar(hour, day_stem):
    """Calculate hour pillar."""
    branch_idx = 0 if hour == 23 else ((hour + 1) // 2) % 12
    day_idx = STEMS.index(day_stem)
    stem_idx = ((day_idx % 5) * 2 + branch_idx) % 10
    return STEMS[stem_idx], BRANCHES[branch_idx]

def get_10_god(dm, stem):
    """Calculate 10 God relationship."""
    dm_elem, dm_pol = STEM_ELEM[dm], STEM_POL[dm]
    s_elem, s_pol = STEM_ELEM[stem], STEM_POL[stem]
    same_pol = dm_pol == s_pol
    
    produces = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
    controls = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
    
    if dm_elem == s_elem:
        return "F" if same_pol else "RW"
    for k,v in produces.items():
        if v == dm_elem and k == s_elem:
            return "IR" if same_pol else "DR"
    if produces.get(dm_elem) == s_elem:
        return "EG" if same_pol else "HO"
    if controls.get(dm_elem) == s_elem:
        return "IW" if same_pol else "DW"
    for k,v in controls.items():
        if v == dm_elem and k == s_elem:
            return "7K" if same_pol else "DO"
    return "?"

def calc_dm_strength(pillars, dm):
    """Calculate Day Master strength."""
    dm_elem = STEM_ELEM[dm]
    support, oppose = 0, 0
    
    produces = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
    controls = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
    
    for p in pillars:
        s_elem = STEM_ELEM[p["stem"]]
        b_elem = BRANCH_ELEM[p["branch"]]
        
        for elem in [s_elem, b_elem]:
            if elem == dm_elem:
                support += 1.5
            elif produces.get(elem) == dm_elem:
                support += 1
            elif controls.get(elem) == dm_elem:
                oppose += 1.5
            elif produces.get(dm_elem) == elem:
                oppose += 1
    
    total = support + oppose
    pct = (support / total * 100) if total > 0 else 50
    
    if pct >= 60: cat = "Strong"
    elif pct >= 55: cat = "Slightly Strong"
    elif pct <= 40: cat = "Weak"
    elif pct <= 45: cat = "Slightly Weak"
    else: cat = "Balanced"
    
    return round(pct, 1), cat

def get_useful_gods(strength_cat, dm_elem):
    """Determine useful and unfavorable elements."""
    produces = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
    produced_by = {v:k for k,v in produces.items()}
    controls = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
    controlled_by = {v:k for k,v in controls.items()}
    
    if "Weak" in strength_cat:
        useful = [dm_elem, produced_by.get(dm_elem, "")]
        unfav = [produces.get(dm_elem, ""), controlled_by.get(dm_elem, "")]
    elif "Strong" in strength_cat:
        useful = [produces.get(dm_elem, ""), controlled_by.get(dm_elem, "")]
        unfav = [dm_elem, produced_by.get(dm_elem, "")]
    else:
        useful = [dm_elem]
        unfav = []
    
    return [u for u in useful if u], [u for u in unfav if u]

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    st.title("🎴 BaZi Pro Analysis")
    st.caption("Complete Four Pillars Analysis with Full Interpretations • v10.5 FIXED")
    
    # Sidebar
    with st.sidebar:
        st.header("🎂 Birth Information")
        
        saved = st.session_state.get("bazi_info", {})
        birth_date = st.date_input("Birth Date", saved.get("date", date(1978, 6, 27)))
        
        unknown_time = st.checkbox("Unknown birth time")
        if unknown_time:
            birth_hour = 12
            st.warning("⚠️ Using noon - Hour pillar may be inaccurate")
        else:
            birth_hour = st.selectbox("Hour", range(24), saved.get("hour", 20))
        
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        
        st.divider()
        calc_btn = st.button("🔮 Calculate BaZi", type="primary", use_container_width=True)
    
    # Main content
    if calc_btn or st.session_state.get("bazi_calc"):
        if calc_btn:
            # Calculate pillars - NOW USING FIXED FUNCTIONS!
            y_stem, y_branch = calc_year_pillar(birth_date.year, birth_date.month, birth_date.day)
            m_stem, m_branch = calc_month_pillar(birth_date.year, birth_date.month, birth_date.day)
            d_stem, d_branch = calc_day_pillar(birth_date)
            h_stem, h_branch = calc_hour_pillar(birth_hour, d_stem)
            
            pillars = [
                {"name": "Year", "stem": y_stem, "branch": y_branch},
                {"name": "Month", "stem": m_stem, "branch": m_branch},
                {"name": "Day", "stem": d_stem, "branch": d_branch},
                {"name": "Hour", "stem": h_stem, "branch": h_branch}
            ]
            
            dm = d_stem
            dm_elem = STEM_ELEM[dm]
            strength_pct, strength_cat = calc_dm_strength(pillars, dm)
            useful, unfav = get_useful_gods(strength_cat, dm_elem)
            
            # Calculate 10 Gods distribution
            gods_dist = {k: 0 for k in TEN_PROFILES.keys()}
            for p in pillars:
                if p["stem"] != dm:
                    god = get_10_god(dm, p["stem"])
                    if god in gods_dist:
                        gods_dist[god] += 10
                for hs in HIDDEN.get(p["branch"], []):
                    god = get_10_god(dm, hs)
                    if god in gods_dist:
                        gods_dist[god] += 5
            
            # Normalize
            total = sum(gods_dist.values())
            if total > 0:
                gods_dist = {k: round(v/total*100, 1) for k,v in gods_dist.items()}
            
            # Find main profile
            main_profile = max(gods_dist, key=gods_dist.get)
            
            # Save to session
            st.session_state.bazi_calc = True
            st.session_state.bazi_info = {"date": birth_date, "hour": birth_hour}
            st.session_state.bazi_data = {
                "pillars": pillars, "dm": dm, "dm_elem": dm_elem,
                "strength_pct": strength_pct, "strength_cat": strength_cat,
                "useful": useful, "unfav": unfav,
                "gods_dist": gods_dist, "main_profile": main_profile,
                "gender": gender
            }
            
            # Also save for other pages
            st.session_state.user_profile = {
                "day_master": dm, "element": dm_elem,
                "strength": strength_cat, "useful_gods": useful,
                "unfavorable": unfav, "profile": TEN_PROFILES[main_profile]["name"]
            }
            st.session_state.bazi_birth_info = {"date": birth_date, "hour": birth_hour}
        
        data = st.session_state.bazi_data
        pillars = data["pillars"]
        dm = data["dm"]
        dm_elem = data["dm_elem"]
        
        # =====================================================================
        # 1. DAY MASTER SECTION
        # =====================================================================
        st.header("1️⃣ DAY MASTER 日主")
        
        dm_info = DAY_MASTER_INFO.get(dm, {})
        dm_cn = STEMS_CN[STEMS.index(dm)]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            ### {dm_info.get('image', '')}
            ## {dm} {dm_cn}
            **{dm_elem} • {STEM_POL[dm]}**
            """)
            
            # Strength bar
            pct = data["strength_pct"]
            st.metric("Strength", f"{data['strength_cat']} ({pct}%)")
            st.progress(pct/100)
        
        with col2:
            st.markdown(dm_info.get("personality", ""))
            
            with st.expander("💼 Career & Relationship"):
                st.markdown(f"**Career:** {dm_info.get('career', '')}")
                st.markdown(f"**Relationship:** {dm_info.get('relationship', '')}")
        
        st.divider()
        
        # =====================================================================
        # 3-4. FAVORABLE & UNFAVORABLE DIRECTIONS
        # =====================================================================
        st.header("3️⃣ FAVORABLE & 4️⃣ UNFAVORABLE DIRECTIONS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Favorable 吉方")
            for elem in data["useful"]:
                dir_info = ELEMENT_DIRECTIONS.get(elem, {})
                st.success(f"""
                **{elem}** {dir_info.get('direction_cn', '')}
                - Directions: {', '.join(dir_info.get('favorable', []))}
                - Colors: {dir_info.get('color', '')}
                - Numbers: {dir_info.get('number', '')}
                """)
        
        with col2:
            st.subheader("❌ Unfavorable 凶方")
            for elem in data["unfav"]:
                dir_info = ELEMENT_DIRECTIONS.get(elem, {})
                st.error(f"""
                **{elem}** {dir_info.get('direction_cn', '')}
                - Directions: {', '.join(dir_info.get('favorable', []))}
                - Colors: {dir_info.get('color', '')}
                - Numbers: {dir_info.get('number', '')}
                """)
        
        st.divider()
        
        # =====================================================================
        # 5. FOUR PILLARS WITH HIDDEN STEMS
        # =====================================================================
        st.header("5️⃣ FOUR PILLARS & HIDDEN STEMS 四柱藏干")
        
        cols = st.columns(4)
        for i, p in enumerate(pillars):
            with cols[i]:
                s_idx = STEMS.index(p["stem"])
                b_idx = BRANCHES.index(p["branch"])
                s_elem = STEM_ELEM[p["stem"]]
                
                # 10 God
                if p["stem"] == dm:
                    god_display = "★ Day Master"
                else:
                    god = get_10_god(dm, p["stem"])
                    god_display = TEN_PROFILES.get(god, {}).get("name", god)
                
                st.markdown(f"### {p['name']} 柱")
                st.info(f"""
                **{STEMS_CN[s_idx]} {BRANCHES_CN[b_idx]}**
                
                {p['stem']} {p['branch']}
                
                {ANIMALS[b_idx]}
                """)
                
                st.caption(f"{s_elem} | {god_display}")
                
                # Hidden stems
                hidden = HIDDEN.get(p["branch"], [])
                st.markdown("**Hidden 藏干:**")
                for hs in hidden:
                    hs_god = get_10_god(dm, hs)
                    st.caption(f"• {hs} {STEMS_CN[STEMS.index(hs)]} ({hs_god})")
        
        st.divider()
        
        # =====================================================================
        # 6 & 8. ANNUAL PILLAR 2025
        # =====================================================================
        st.header("6️⃣ 2025 ANNUAL PILLAR 流年 & 8️⃣ ANNUAL STAR")
        
        annual_stem, annual_branch = "Yi", "Si"  # 2025 = Yi Si
        annual_god = get_10_god(dm, annual_stem)
        annual_info = TEN_PROFILES.get(annual_god, {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            ### 2025 乙巳 Yi Si (Wood Snake)
            
            **Annual Element:** Wood (Yin)
            
            **Your 10 God for 2025:** {annual_god} {annual_info.get('name', '')}
            """)
            
            # Is it favorable?
            if "Wood" in data["useful"]:
                st.success("✅ 2025's Wood element is FAVORABLE for you!")
            elif "Wood" in data["unfav"]:
                st.error("⚠️ 2025's Wood element is UNFAVORABLE - exercise caution")
            else:
                st.info("📌 2025's Wood element is NEUTRAL for you")
        
        with col2:
            st.markdown(f"""
            ### Annual Theme: {annual_info.get('name', '')}
            
            {annual_info.get('description', '')}
            
            **Strengths this year:** {annual_info.get('strengths', '')}
            
            **Watch out for:** {annual_info.get('challenges', '')}
            """)
        
        st.divider()
        
        # =====================================================================
        # 7. MOBILITY DIRECTIONS 2025
        # =====================================================================
        st.header("7️⃣ 2025 MOBILITY DIRECTIONS 出行方位")
        
        st.markdown("""
        Based on your useful elements and 2025's annual energy:
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"""
            ### ✅ GO TO
            **{', '.join(data['useful'])} directions**
            
            Best for: Travel, business, opportunities
            """)
        with col2:
            st.warning(f"""
            ### ⚡ CAUTION
            **Wood (East/SE) in 2025**
            
            Snake year energy - watch for obstacles
            """)
        with col3:
            st.error(f"""
            ### ❌ AVOID
            **{', '.join(data['unfav'])} directions**
            
            May bring challenges or setbacks
            """)
        
        st.divider()
        
        # =====================================================================
        # 10. SIX ASPECTS
        # =====================================================================
        st.header("🔟 SIX ASPECTS 六神")
        
        gods_dist = data["gods_dist"]
        
        cols = st.columns(3)
        for i, (aspect, info) in enumerate(SIX_ASPECTS.items()):
            with cols[i % 3]:
                score = sum(gods_dist.get(g, 0) for g in info["gods"])
                
                if score >= 20:
                    st.success(f"""
                    ### {aspect} {info['area']}
                    **Score: {score:.0f}%** ⬆️ Strong
                    
                    {info['meaning']}
                    """)
                elif score >= 10:
                    st.info(f"""
                    ### {aspect} {info['area']}
                    **Score: {score:.0f}%** ➡️ Moderate
                    
                    {info['meaning']}
                    """)
                else:
                    st.warning(f"""
                    ### {aspect} {info['area']}
                    **Score: {score:.0f}%** ⬇️ Weak
                    
                    {info['meaning']}
                    """)
        
        st.divider()
        
        # =====================================================================
        # 11. MONTHLY INFLUENCE 2025
        # =====================================================================
        st.header("1️⃣1️⃣ 2025 MONTHLY INFLUENCE 月运")
        
        st.markdown("How each month of 2025 affects you based on your Day Master:")
        
        cols = st.columns(4)
        for month in range(1, 13):
            with cols[(month-1) % 4]:
                m_stem, m_branch, m_cn, m_desc = MONTHLY_STEMS_2025[month]
                m_god = get_10_god(dm, m_stem)
                m_elem = STEM_ELEM[m_stem]
                
                # Determine favorability
                if m_elem in data["useful"]:
                    st.success(f"""
                    **{month}月 {m_cn}**
                    {m_god} - Favorable ✅
                    """)
                elif m_elem in data["unfav"]:
                    st.error(f"""
                    **{month}月 {m_cn}**
                    {m_god} - Caution ⚠️
                    """)
                else:
                    st.info(f"""
                    **{month}月 {m_cn}**
                    {m_god} - Neutral 📌
                    """)
        
        st.divider()
        
        # =====================================================================
        # 12. FIVE STRUCTURES
        # =====================================================================
        st.header("1️⃣2️⃣ FIVE STRUCTURES 五型格")
        
        # Calculate structure scores
        struct_scores = {}
        for name, info in FIVE_STRUCTURES.items():
            struct_scores[name] = sum(gods_dist.get(g, 0) for g in info["gods"])
        
        main_struct = max(struct_scores, key=struct_scores.get)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Structure Strength")
            for name, score in sorted(struct_scores.items(), key=lambda x: x[1], reverse=True):
                st.progress(score/100 if score <= 100 else 1.0)
                st.caption(f"{name}: {score:.0f}%")
        
        with col2:
            main_info = FIVE_STRUCTURES[main_struct]
            st.markdown(f"""
            ### Your Main Structure: {main_struct} {main_info['cn']}
            
            {main_info['description']}
            
            **Strengths:** {main_info['strengths']}
            
            **Best Careers:** {main_info['careers']}
            """)
        
        st.divider()
        
        # =====================================================================
        # 13. TEN PROFILES
        # =====================================================================
        st.header("1️⃣3️⃣ TEN PROFILES 十神格")
        
        # Sort by score
        sorted_profiles = sorted(gods_dist.items(), key=lambda x: x[1], reverse=True)
        main_profile = sorted_profiles[0][0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Profile Strength")
            for god, score in sorted_profiles:
                if score > 0:
                    info = TEN_PROFILES.get(god, {})
                    st.progress(score/100 if score <= 100 else 1.0)
                    st.caption(f"{god} {info.get('cn', '')}: {score:.0f}%")
        
        with col2:
            main_info = TEN_PROFILES[main_profile]
            st.markdown(f"""
            ### Your Main Profile: {main_info['name']}
            
            {main_info['description']}
            
            **Strengths:** {main_info['strengths']}
            
            **Challenges:** {main_info['challenges']}
            """)
            
            # Secondary profile
            if len(sorted_profiles) > 1 and sorted_profiles[1][1] > 5:
                sec_god = sorted_profiles[1][0]
                sec_info = TEN_PROFILES[sec_god]
                st.markdown(f"""
                ---
                **Secondary Profile:** {sec_info['name']}
                
                {sec_info['brief']}
                """)
        
        st.divider()
        
        # =====================================================================
        # EXPORT
        # =====================================================================
        st.header("📤 Export Analysis")
        
        if st.button("🤖 Generate AI Analysis Prompt", use_container_width=True):
            prompt = f"""Complete BaZi Analysis for {birth_date} at {birth_hour}:00

**DAY MASTER:** {dm} {STEMS_CN[STEMS.index(dm)]} ({dm_elem})
**Strength:** {data['strength_cat']} ({data['strength_pct']}%)

**FOUR PILLARS:**
- Year: {pillars[0]['stem']} {pillars[0]['branch']}
- Month: {pillars[1]['stem']} {pillars[1]['branch']}
- Day: {pillars[2]['stem']} {pillars[2]['branch']} ← Day Master
- Hour: {pillars[3]['stem']} {pillars[3]['branch']}

**USEFUL GODS:** {', '.join(data['useful'])}
**UNFAVORABLE:** {', '.join(data['unfav'])}

**MAIN PROFILE:** {TEN_PROFILES[main_profile]['name']}
**MAIN STRUCTURE:** {main_struct}

**10 GODS DISTRIBUTION:** {gods_dist}

**2025 OUTLOOK:**
- Annual Pillar: Yi Si (Wood Snake)
- 10 God for 2025: {annual_god} {annual_info.get('name', '')}
- Wood is {'FAVORABLE' if 'Wood' in data['useful'] else 'UNFAVORABLE' if 'Wood' in data['unfav'] else 'NEUTRAL'} for this chart

Please provide comprehensive analysis covering all 13 areas."""
            
            st.code(prompt, language="markdown")
    
    else:
        st.info("👈 Enter birth info and click **Calculate BaZi** to begin")
        
        with st.expander("📋 What This Page Covers"):
            st.markdown("""
            **Complete BaZi Analysis includes:**
            
            1. ✅ Day Master personality & traits
            2. ✅ Qi Men Destiny Palace (see Destiny page)
            3. ✅ Favorable directions based on useful gods
            4. ✅ Unfavorable directions to avoid
            5. ✅ Four Pillars with hidden stems
            6. ✅ 2025 Annual Pillar overlay
            7. ✅ 2025 Mobility directions
            8. ✅ Annual BaZi star for 2025
            9. ✅ 2025 Life Palace (see Destiny page)
            10. ✅ Six Aspects analysis
            11. ✅ 2025 Monthly influence
            12. ✅ Five Structures with explanations
            13. ✅ Ten Profiles with explanations
            """)


if __name__ == "__main__":
    main()
