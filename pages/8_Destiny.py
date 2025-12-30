# Ming QiMenDunJia v8.0 - QMDJ Destiny Analysis (Tiered)
# pages/8_Destiny.py
"""
QI MEN DESTINY ANALYSIS (奇门命盘) - QUICK TIER

Show your birth chart QMDJ components.
- Shows WHAT (Star, Door, Deity, Palace)
- For WHY (full interpretation), export to Project 1 (AI Analyst)
"""

import streamlit as st
from datetime import datetime, date
import pytz
import json

# Import from core modules
import sys
sys.path.insert(0, '..')

try:
    from core.qmdj_engine import (
        generate_qmdj_chart, calculate_qmdj_pillars,
        PALACE_INFO, NINE_STARS, EIGHT_DOORS, EIGHT_DEITIES,
        SGT
    )
    from core.formations import detect_formations, get_formation_score, FormationCategory
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False
    NINE_STARS = {"天蓬": "Canopy", "天芮": "Grass", "天冲": "Impulse", "天辅": "Assistant",
                  "天禽": "Connect", "天心": "Heart", "天柱": "Pillar", "天任": "Ren", "天英": "Hero"}
    EIGHT_DOORS = {"开门": "Open", "休门": "Rest", "生门": "Life", "伤门": "Harm",
                   "杜门": "Delusion", "景门": "Scenery", "死门": "Death", "惊门": "Fear"}
    EIGHT_DEITIES = {"值符": "Chief", "腾蛇": "Serpent", "太阴": "Moon", "六合": "Six Harmony",
                     "勾陈": "Hook", "白虎": "Tiger", "玄武": "Emptiness", "九地": "Nine Earth", "九天": "Nine Heaven"}


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Destiny Analysis | Ming Qimen",
    page_icon="⭐",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0a1628; }
    .destiny-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 2px solid #9f7aea;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .component-box {
        background: #1a2744;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border: 1px solid #2d3748;
        margin: 5px;
    }
    .component-star { border-color: #f6e05e; }
    .component-door { border-color: #48bb78; }
    .component-deity { border-color: #9f7aea; }
    .palace-cell {
        background: #1a2744;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        border: 1px solid #2d3748;
        min-height: 80px;
    }
    .palace-birth {
        border: 2px solid #FFD700 !important;
        background: linear-gradient(135deg, #2d3748 0%, #1a2744 100%);
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# BRIEF LABELS (Not full interpretations)
# =============================================================================

STAR_LABELS = {
    "Canopy": ("天蓬", "Water", "Strategist"),
    "Grass": ("天芮", "Earth", "Healer"),
    "Impulse": ("天冲", "Wood", "Pioneer"),
    "Assistant": ("天辅", "Wood", "Scholar"),
    "Connect": ("天禽", "Earth", "Connector"),
    "Heart": ("天心", "Metal", "Authority"),
    "Pillar": ("天柱", "Metal", "Critic"),
    "Ren": ("天任", "Earth", "Diplomat"),
    "Hero": ("天英", "Fire", "Performer")
}

DOOR_LABELS = {
    "Open": ("开门", "Metal", "Leadership"),
    "Rest": ("休门", "Water", "Prosperity"),
    "Life": ("生门", "Earth", "Creation"),
    "Harm": ("伤门", "Wood", "Competition"),
    "Delusion": ("杜门", "Wood", "Strategy"),
    "Scenery": ("景门", "Fire", "Recognition"),
    "Death": ("死门", "Earth", "Transformation"),
    "Fear": ("惊门", "Metal", "Awareness")
}

DEITY_LABELS = {
    "Chief": ("值符", "Authority backing"),
    "Serpent": ("腾蛇", "Mystical perception"),
    "Moon": ("太阴", "Hidden support"),
    "Six Harmony": ("六合", "Relationship blessing"),
    "Hook": ("勾陈", "Grounding force"),
    "Tiger": ("白虎", "Protection power"),
    "Emptiness": ("玄武", "Hidden wisdom"),
    "Nine Earth": ("九地", "Deep stability"),
    "Nine Heaven": ("九天", "Upward energy")
}

PALACE_NAMES = {
    1: ("Kan 坎", "North", "Water"),
    2: ("Kun 坤", "Southwest", "Earth"),
    3: ("Zhen 震", "East", "Wood"),
    4: ("Xun 巽", "Southeast", "Wood"),
    5: ("Center 中", "Center", "Earth"),
    6: ("Qian 乾", "Northwest", "Metal"),
    7: ("Dui 兑", "West", "Metal"),
    8: ("Gen 艮", "Northeast", "Earth"),
    9: ("Li 离", "South", "Fire")
}

# Hour branch to palace mapping (Luo Shu)
BRANCH_TO_PALACE = {
    "Zi": 1, "Chou": 8, "Yin": 8, "Mao": 3,
    "Chen": 4, "Si": 4, "Wu": 9, "Wei": 2,
    "Shen": 2, "You": 7, "Xu": 6, "Hai": 6
}


# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

def get_birth_palace(birth_dt: datetime) -> int:
    """Get birth palace from hour branch."""
    hour = birth_dt.hour
    
    # Map hour to branch
    branches = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", 
                "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
    
    if hour == 23:
        branch = "Zi"
    else:
        branch_idx = (hour + 1) // 2
        branch = branches[branch_idx % 12]
    
    return BRANCH_TO_PALACE.get(branch, 5)


def calculate_destiny_chart(birth_dt: datetime) -> dict:
    """Calculate QMDJ destiny chart for birth time."""
    if not IMPORTS_OK:
        # Demo data
        return {
            "palace": 6,
            "star": "Heart",
            "door": "Open",
            "deity": "Chief",
            "heaven_stem": "Geng",
            "earth_stem": "Xin",
            "formations": [],
            "formation_score": 0
        }
    
    try:
        # Generate chart for birth time
        chart = generate_qmdj_chart(birth_dt)
        birth_palace = get_birth_palace(birth_dt)
        
        palace_data = chart.get("palaces", {}).get(str(birth_palace), {})
        
        # Detect formations
        formations = detect_formations(palace_data)
        f_score, _ = get_formation_score(formations)
        
        return {
            "palace": birth_palace,
            "star": palace_data.get("star", "Unknown"),
            "door": palace_data.get("door", "Unknown"),
            "deity": palace_data.get("deity", "Unknown"),
            "heaven_stem": palace_data.get("heaven_stem", "?"),
            "earth_stem": palace_data.get("earth_stem", "?"),
            "formations": [f.name for f in formations],
            "formation_score": f_score,
            "full_chart": chart
        }
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# EXPORT FOR PROJECT 1
# =============================================================================

def generate_export_data(birth_info: dict, destiny: dict, user_bazi: dict = None) -> dict:
    """Generate JSON for Project 1 (AI Analyst) full interpretation."""
    return {
        "analysis_type": "QMDJ_DESTINY",
        "birth_info": birth_info,
        "destiny_components": {
            "palace": {
                "number": destiny["palace"],
                "name": PALACE_NAMES.get(destiny["palace"], ("?", "?", "?"))[0],
                "direction": PALACE_NAMES.get(destiny["palace"], ("?", "?", "?"))[1],
                "element": PALACE_NAMES.get(destiny["palace"], ("?", "?", "?"))[2]
            },
            "natal_star": {
                "name": destiny["star"],
                "chinese": STAR_LABELS.get(destiny["star"], ("?", "?", "?"))[0],
                "element": STAR_LABELS.get(destiny["star"], ("?", "?", "?"))[1]
            },
            "natal_door": {
                "name": destiny["door"],
                "chinese": DOOR_LABELS.get(destiny["door"], ("?", "?", "?"))[0],
                "element": DOOR_LABELS.get(destiny["door"], ("?", "?", "?"))[1]
            },
            "natal_deity": {
                "name": destiny["deity"],
                "chinese": DEITY_LABELS.get(destiny["deity"], ("?", "?"))[0]
            },
            "stems": {
                "heaven": destiny.get("heaven_stem", "?"),
                "earth": destiny.get("earth_stem", "?")
            },
            "formations": destiny.get("formations", [])
        },
        "user_bazi": user_bazi,
        "instruction": "Provide a complete QMDJ Destiny reading for this birth chart. Explain the natal Star archetype, Door life theme, and Deity blessing. Discuss how these components interact. If BaZi is provided, compare and contrast the two systems' insights. Include life path guidance and potential challenges."
    }


# =============================================================================
# MAIN PAGE
# =============================================================================

def main():
    st.title("⭐ QMDJ Destiny Analysis")
    st.caption("Your birth chart in Qi Men Dun Jia • Export for full reading")
    
    # Sidebar - Birth info input
    with st.sidebar:
        st.header("🎂 Birth Information")
        
        # Check if we have saved birth info
        saved_profile = st.session_state.get("user_profile", {})
        
        birth_date = st.date_input(
            "Birth Date",
            value=date(1990, 1, 1),
            min_value=date(1920, 1, 1),
            max_value=date.today()
        )
        
        col1, col2 = st.columns(2)
        with col1:
            birth_hour = st.selectbox("Hour", options=list(range(0, 24)), index=12)
        with col2:
            birth_minute = st.selectbox("Minute", options=[0, 15, 30, 45], index=0)
        
        st.divider()
        
        # Show BaZi if available
        if saved_profile:
            st.success(f"🎴 BaZi: {saved_profile.get('day_master', '?')} Day Master")
            st.caption(f"Useful: {', '.join(saved_profile.get('useful_gods', []))}")
        
        st.divider()
        analyze_btn = st.button("🔮 Reveal Destiny", type="primary", use_container_width=True)
    
    # Main content
    if analyze_btn:
        # Create birth datetime
        tz = pytz.timezone('Asia/Singapore')
        birth_dt = tz.localize(datetime.combine(birth_date, datetime.min.time().replace(hour=birth_hour, minute=birth_minute)))
        
        # Calculate destiny
        destiny = calculate_destiny_chart(birth_dt)
        
        if "error" in destiny:
            st.error(f"Calculation error: {destiny['error']}")
            return
        
        # Birth Info Summary
        st.markdown(f"""
        <div class="destiny-card">
            <div style="color: #9f7aea; font-size: 0.9em;">BIRTH CHART</div>
            <div style="color: #fff; font-size: 1.3em; margin: 5px 0;">
                {birth_date.strftime('%B %d, %Y')} at {birth_hour:02d}:{birth_minute:02d}
            </div>
            <div style="color: #FFD700;">
                Palace {destiny['palace']} • {PALACE_NAMES[destiny['palace']][0]} • {PALACE_NAMES[destiny['palace']][1]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 9 Palace Grid showing birth palace
        st.subheader("🏯 Birth Palace Position")
        
        grid = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        for row in grid:
            cols = st.columns(3)
            for idx, palace_num in enumerate(row):
                with cols[idx]:
                    is_birth = palace_num == destiny["palace"]
                    p_name, p_dir, p_elem = PALACE_NAMES[palace_num]
                    
                    cls = "palace-birth" if is_birth else ""
                    marker = "⭐ YOU" if is_birth else ""
                    
                    st.markdown(f"""
                    <div class="palace-cell {cls}">
                        <div style="color: {'#FFD700' if is_birth else '#a0aec0'}; font-size: 0.8em;">{p_dir}</div>
                        <div style="color: #fff; font-weight: bold;">P{palace_num}</div>
                        <div style="color: #718096; font-size: 0.8em;">{p_elem}</div>
                        <div style="color: #FFD700; font-size: 0.9em;">{marker}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        
        # Three Core Components
        st.subheader("🌟 Your Natal Components")
        
        col1, col2, col3 = st.columns(3)
        
        # Natal Star
        with col1:
            star = destiny["star"]
            s_cn, s_elem, s_label = STAR_LABELS.get(star, ("?", "?", "?"))
            st.markdown(f"""
            <div class="component-box component-star">
                <div style="color: #f6e05e; font-size: 0.8em;">NATAL STAR 星</div>
                <div style="color: #fff; font-size: 1.5em; margin: 10px 0;">{star}</div>
                <div style="color: #a0aec0;">{s_cn}</div>
                <div style="color: #718096; font-size: 0.9em;">{s_elem} • {s_label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Natal Door
        with col2:
            door = destiny["door"]
            d_cn, d_elem, d_label = DOOR_LABELS.get(door, ("?", "?", "?"))
            st.markdown(f"""
            <div class="component-box component-door">
                <div style="color: #48bb78; font-size: 0.8em;">NATAL DOOR 门</div>
                <div style="color: #fff; font-size: 1.5em; margin: 10px 0;">{door}</div>
                <div style="color: #a0aec0;">{d_cn}</div>
                <div style="color: #718096; font-size: 0.9em;">{d_elem} • {d_label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Natal Deity
        with col3:
            deity = destiny["deity"]
            de_cn, de_label = DEITY_LABELS.get(deity, ("?", "?"))
            st.markdown(f"""
            <div class="component-box component-deity">
                <div style="color: #9f7aea; font-size: 0.8em;">NATAL DEITY 神</div>
                <div style="color: #fff; font-size: 1.5em; margin: 10px 0;">{deity}</div>
                <div style="color: #a0aec0;">{de_cn}</div>
                <div style="color: #718096; font-size: 0.9em;">{de_label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Formations if any
        formations = destiny.get("formations", [])
        if formations:
            st.divider()
            st.subheader("📜 Natal Formations")
            f_score = destiny.get("formation_score", 0)
            verdict = "✨ Auspicious" if f_score > 0 else "⚠️ Challenging" if f_score < 0 else "⚖️ Neutral"
            
            st.markdown(f"**{verdict}** ({len(formations)} formation{'s' if len(formations) > 1 else ''})")
            for f in formations:
                st.markdown(f"• {f}")
        
        # Quick Summary Card
        st.divider()
        st.subheader("📊 Quick Summary")
        
        st.markdown(f"""
        | Component | Name | Element | Brief |
        |-----------|------|---------|-------|
        | Star | {destiny['star']} | {STAR_LABELS.get(destiny['star'], ('?','?','?'))[1]} | {STAR_LABELS.get(destiny['star'], ('?','?','?'))[2]} |
        | Door | {destiny['door']} | {DOOR_LABELS.get(destiny['door'], ('?','?','?'))[1]} | {DOOR_LABELS.get(destiny['door'], ('?','?','?'))[2]} |
        | Deity | {destiny['deity']} | - | {DEITY_LABELS.get(destiny['deity'], ('?','?'))[1]} |
        | Palace | P{destiny['palace']} | {PALACE_NAMES[destiny['palace']][2]} | {PALACE_NAMES[destiny['palace']][1]} |
        """)
        
        # =================================================================
        # EXPORT FOR FULL READING
        # =================================================================
        st.divider()
        st.subheader("🤖 Get Full Interpretation")
        st.caption("Export to AI Analyst for complete destiny reading")
        
        birth_info = {
            "date": birth_date.strftime("%Y-%m-%d"),
            "time": f"{birth_hour:02d}:{birth_minute:02d}",
            "timezone": "Asia/Singapore (UTC+8)"
        }
        
        export_data = generate_export_data(birth_info, destiny, saved_profile)
        export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        with st.expander("📋 View Export Data"):
            st.code(export_json, language="json")
        
        st.download_button(
            "💾 Download JSON for Full Reading",
            export_json,
            file_name=f"destiny_{birth_date.strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.info("💡 **Paste JSON to Claude:** *'Give me a complete QMDJ destiny reading. Explain my natal Star archetype, Door life theme, and Deity blessing.'*")
        
        # Note about BaZi vs QMDJ
        with st.expander("ℹ️ QMDJ vs BaZi Destiny"):
            st.markdown("""
            **QMDJ Destiny** and **BaZi** are complementary systems:
            
            | Aspect | QMDJ Destiny | BaZi |
            |--------|--------------|------|
            | Focus | Spiritual path, timing | Character, life phases |
            | Components | Star, Door, Deity | Day Master, Ten Gods |
            | Strength | Strategic guidance | Elemental balance |
            
            **Both together** give a complete picture of your destiny.
            """)
    
    else:
        st.info("👈 Enter your birth date and time, then click **Reveal Destiny**")
        
        st.markdown("""
        ### What You'll See
        
        | This App (Quick) | AI Analyst (Deep) |
        |------------------|-------------------|
        | Your natal Star, Door, Deity | Full archetype explanation |
        | Palace position | Life path interpretation |
        | Element labels | Strengths & challenges |
        | Formation names | Personalized guidance |
        
        **QMDJ Destiny** reveals your spiritual blueprint - different from BaZi!
        """)


if __name__ == "__main__":
    main()
