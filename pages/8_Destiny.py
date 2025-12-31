# Ming QiMenDunJia v8.0 - QMDJ Destiny Analysis (Hybrid)
# pages/8_Destiny.py
"""
QI MEN DESTINY ANALYSIS (奇门命盘) - HYBRID

Your birth chart in Qi Men Dun Jia system.
- Shows useful insights (component meanings, brief archetypes)
- "Analyze with AI" button for full personalized reading
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
    .component-card {
        background: #1a2744;
        border-radius: 10px;
        padding: 18px;
        border: 1px solid #2d3748;
        margin: 8px 0;
    }
    .component-star { border-left: 4px solid #f6e05e; }
    .component-door { border-left: 4px solid #48bb78; }
    .component-deity { border-left: 4px solid #9f7aea; }
    .palace-cell {
        background: #1a2744;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        border: 1px solid #2d3748;
        min-height: 70px;
    }
    .palace-birth {
        border: 2px solid #FFD700 !important;
        background: linear-gradient(135deg, #2d3748 0%, #1a2744 100%);
    }
    .trait-tag {
        display: inline-block;
        background: #2d3748;
        padding: 4px 10px;
        border-radius: 15px;
        margin: 3px;
        font-size: 0.85em;
    }
    .trait-good { background: #1a3728; color: #48bb78; }
    .trait-challenge { background: #371a1a; color: #f56565; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# COMPONENT DATA (Brief insights, not full interpretations)
# =============================================================================

STAR_DATA = {
    "Canopy": {
        "chinese": "天蓬", "element": "Water", "archetype": "The Strategist",
        "brief": "Strategic mind, resourceful, works behind the scenes",
        "strengths": ["Strategic thinking", "Adaptability", "Intuition"],
        "challenges": ["Trust issues", "Secrecy tendency"]
    },
    "Grass": {
        "chinese": "天芮", "element": "Earth", "archetype": "The Healer",
        "brief": "Caring nature, patient, drawn to helping professions",
        "strengths": ["Nurturing", "Medical intuition", "Patience"],
        "challenges": ["Health sensitivity", "Over-giving"]
    },
    "Impulse": {
        "chinese": "天冲", "element": "Wood", "archetype": "The Pioneer",
        "brief": "Courageous, takes initiative, natural leader",
        "strengths": ["Courage", "Initiative", "Athletic ability"],
        "challenges": ["Impatience", "Injury-prone"]
    },
    "Assistant": {
        "chinese": "天辅", "element": "Wood", "archetype": "The Scholar",
        "brief": "Wise, excellent teacher, diplomatic advisor",
        "strengths": ["Wisdom", "Teaching ability", "Diplomacy"],
        "challenges": ["Overthinking", "Indecision"]
    },
    "Connect": {
        "chinese": "天禽", "element": "Earth", "archetype": "The Connector",
        "brief": "Versatile, connects people and ideas, central role",
        "strengths": ["Versatility", "Networking", "Balance"],
        "challenges": ["Scattered energy", "Identity confusion"]
    },
    "Heart": {
        "chinese": "天心", "element": "Metal", "archetype": "The Authority",
        "brief": "Precise, authoritative, skilled problem-solver",
        "strengths": ["Precision", "Authority", "Technical skill"],
        "challenges": ["Over-analytical", "Coldness"]
    },
    "Pillar": {
        "chinese": "天柱", "element": "Metal", "archetype": "The Critic",
        "brief": "Sharp insight, truth-seeker, independent thinker",
        "strengths": ["Discernment", "Independence", "Truth-seeking"],
        "challenges": ["Harsh criticism", "Isolation"]
    },
    "Ren": {
        "chinese": "天任", "element": "Earth", "archetype": "The Diplomat",
        "brief": "Stable, trustworthy, builds lasting foundations",
        "strengths": ["Stability", "Trustworthiness", "Diplomacy"],
        "challenges": ["Stubbornness", "Slow adaptation"]
    },
    "Hero": {
        "chinese": "天英", "element": "Fire", "archetype": "The Performer",
        "brief": "Creative, charismatic, born to inspire others",
        "strengths": ["Creativity", "Charisma", "Expression"],
        "challenges": ["Attention-seeking", "Drama"]
    }
}

DOOR_DATA = {
    "Open": {
        "chinese": "开门", "element": "Metal", "theme": "Leadership & Authority",
        "brief": "Opens doors for self and others, natural authority",
        "gifts": ["Natural authority", "Career success", "Opening opportunities"]
    },
    "Rest": {
        "chinese": "休门", "element": "Water", "theme": "Prosperity & Ease",
        "brief": "Attracts wealth through relationships and timing",
        "gifts": ["Attracting wealth", "Networking", "Strategic timing"]
    },
    "Life": {
        "chinese": "生门", "element": "Earth", "theme": "Creation & Growth",
        "brief": "Natural creator, business sense, builds abundance",
        "gifts": ["Wealth creation", "Business acumen", "Nurturing growth"]
    },
    "Harm": {
        "chinese": "伤门", "element": "Wood", "theme": "Competition & Transformation",
        "brief": "Grows through challenges, competitive spirit",
        "gifts": ["Competitive drive", "Breakthrough power", "Transformation"]
    },
    "Delusion": {
        "chinese": "杜门", "element": "Wood", "theme": "Strategy & Secrets",
        "brief": "Works best behind scenes, strategic mind",
        "gifts": ["Strategic thinking", "Secret-keeping", "Hidden influence"]
    },
    "Scenery": {
        "chinese": "景门", "element": "Fire", "theme": "Recognition & Expression",
        "brief": "Meant to be seen, artistic expression, fame potential",
        "gifts": ["Public recognition", "Artistic expression", "Visibility"]
    },
    "Death": {
        "chinese": "死门", "element": "Earth", "theme": "Transformation & Endings",
        "brief": "Masters endings and transitions, deep transformer",
        "gifts": ["Completing cycles", "Major transitions", "Deep wisdom"]
    },
    "Fear": {
        "chinese": "惊门", "element": "Metal", "theme": "Awareness & Protection",
        "brief": "Heightened awareness, protective instincts, legal mind",
        "gifts": ["Heightened awareness", "Legal mind", "Protection"]
    }
}

DEITY_DATA = {
    "Chief": {"chinese": "值符", "brief": "Authority backing, people follow you naturally"},
    "Serpent": {"chinese": "腾蛇", "brief": "Mystical perception, strong intuition and dreams"},
    "Moon": {"chinese": "太阴", "brief": "Hidden support, benefactors work behind scenes"},
    "Six Harmony": {"chinese": "六合", "brief": "Relationship blessing, harmonious connections"},
    "Hook": {"chinese": "勾陈", "brief": "Grounding force, stability in chaos"},
    "Tiger": {"chinese": "白虎", "brief": "Fierce protection, competitive edge"},
    "Emptiness": {"chinese": "玄武", "brief": "Hidden wisdom, unconventional paths"},
    "Nine Earth": {"chinese": "九地", "brief": "Deep grounding, patience, foundation building"},
    "Nine Heaven": {"chinese": "九天", "brief": "Upward energy, ambition, high aspirations"}
}

PALACE_DATA = {
    1: ("Kan 坎", "North", "Water", "Career, wisdom, flow"),
    2: ("Kun 坤", "Southwest", "Earth", "Relationships, nurturing"),
    3: ("Zhen 震", "East", "Wood", "Action, new beginnings"),
    4: ("Xun 巽", "Southeast", "Wood", "Wealth, growth, wind"),
    5: ("Center 中", "Center", "Earth", "Balance, health, core"),
    6: ("Qian 乾", "Northwest", "Metal", "Authority, leadership"),
    7: ("Dui 兑", "West", "Metal", "Joy, communication"),
    8: ("Gen 艮", "Northeast", "Earth", "Knowledge, stability"),
    9: ("Li 离", "South", "Fire", "Fame, recognition, clarity")
}

# Hour branch to palace mapping
BRANCH_TO_PALACE = {
    "Zi": 1, "Chou": 8, "Yin": 8, "Mao": 3,
    "Chen": 4, "Si": 4, "Wu": 9, "Wei": 2,
    "Shen": 2, "You": 7, "Xu": 6, "Hai": 6
}


# =============================================================================
# CALCULATION
# =============================================================================

def get_hour_branch(hour: int) -> str:
    """Get earthly branch from hour."""
    branches = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", 
                "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
    if hour == 23:
        return "Zi"
    return branches[(hour + 1) // 2 % 12]


def calculate_destiny(birth_dt: datetime) -> dict:
    """Calculate QMDJ destiny chart."""
    if not IMPORTS_OK:
        return {
            "palace": 6, "star": "Heart", "door": "Open", "deity": "Chief",
            "heaven_stem": "Geng", "earth_stem": "Xin",
            "formations": [], "formation_score": 0
        }
    
    try:
        chart = generate_qmdj_chart(birth_dt)
        hour_branch = get_hour_branch(birth_dt.hour)
        birth_palace = BRANCH_TO_PALACE.get(hour_branch, 5)
        
        palace_data = chart.get("palaces", {}).get(str(birth_palace), {})
        
        formations = detect_formations(palace_data)
        f_score, _ = get_formation_score(formations)
        
        return {
            "palace": birth_palace,
            "star": palace_data.get("star", "Unknown"),
            "door": palace_data.get("door", "Unknown"),
            "deity": palace_data.get("deity", "Unknown"),
            "heaven_stem": palace_data.get("heaven_stem", "?"),
            "earth_stem": palace_data.get("earth_stem", "?"),
            "formations": [{"name": f.name, "category": f.category.value} for f in formations],
            "formation_score": f_score,
            "chart": chart
        }
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# AI PROMPT GENERATOR
# =============================================================================

def generate_ai_prompt(birth_info: dict, destiny: dict, user_bazi: dict = None) -> str:
    """Generate a ready-to-paste prompt for full reading."""
    
    star_data = STAR_DATA.get(destiny['star'], {})
    door_data = DOOR_DATA.get(destiny['door'], {})
    deity_data = DEITY_DATA.get(destiny['deity'], {})
    palace_info = PALACE_DATA.get(destiny['palace'], ("?", "?", "?", "?"))
    
    formations_text = ""
    if destiny.get('formations'):
        formations_text = "\n**Natal Formations:**\n" + "\n".join([
            f"- {f['name']} ({f['category']})" for f in destiny['formations']
        ])
    
    bazi_text = ""
    if user_bazi:
        bazi_text = f"""
**User's BaZi Profile (for comparison):**
- Day Master: {user_bazi.get('day_master', '?')} ({user_bazi.get('element', '?')})
- Strength: {user_bazi.get('strength', '?')}
- Useful Gods: {', '.join(user_bazi.get('useful_gods', []))}
- Ten God Profile: {user_bazi.get('profile', '?')}
"""
    
    prompt = f"""Provide a complete Qi Men Dun Jia Destiny reading for this birth chart:

**Birth Information:**
- Date: {birth_info['date']}
- Time: {birth_info['time']}
- Timezone: {birth_info.get('timezone', 'Asia/Singapore')}

**Birth Palace:** Palace {destiny['palace']} - {palace_info[0]}
- Direction: {palace_info[1]}
- Element: {palace_info[2]}
- Theme: {palace_info[3]}

**Natal Star:** {destiny['star']} ({star_data.get('chinese', '?')})
- Element: {star_data.get('element', '?')}
- Archetype: {star_data.get('archetype', '?')}

**Natal Door:** {destiny['door']} ({door_data.get('chinese', '?')})
- Element: {door_data.get('element', '?')}
- Life Theme: {door_data.get('theme', '?')}

**Natal Deity:** {destiny['deity']} ({deity_data.get('chinese', '?')})

**Stems:** Heaven {destiny.get('heaven_stem', '?')} / Earth {destiny.get('earth_stem', '?')}
{formations_text}
{bazi_text}
---

Please provide a comprehensive reading including:

1. **Natal Star Analysis** - What does {destiny['star']} Star reveal about core personality, natural talents, and life approach? What is the archetype in depth?

2. **Natal Door Analysis** - How does {destiny['door']} Door shape life opportunities and challenges? What is the life theme?

3. **Natal Deity Analysis** - What spiritual backing or energy pattern does {destiny['deity']} provide?

4. **Component Interactions** - How do the Star, Door, and Deity work together? Any notable combinations?

5. **Life Path Guidance** - Based on this chart, what are the key life lessons, optimal career paths, and areas to develop?

6. **Challenges to Navigate** - What potential pitfalls should be aware of based on this configuration?

{"7. **BaZi Comparison** - How does this QMDJ destiny complement or contrast with the BaZi profile? What insights emerge from combining both systems?" if user_bazi else ""}

Make the reading personal and actionable, not generic."""

    return prompt


# =============================================================================
# MAIN PAGE
# =============================================================================

def main():
    st.title("⭐ QMDJ Destiny Analysis")
    st.caption("Your Qi Men birth chart • Get AI-powered full reading")
    
    # Sidebar
    with st.sidebar:
        st.header("🎂 Birth Information")
        
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
        
        # BaZi profile
        saved_profile = st.session_state.get("user_profile", None)
        if saved_profile:
            st.success(f"🎴 BaZi: {saved_profile.get('day_master', '?')} Day Master")
        
        st.divider()
        analyze_btn = st.button("🔮 Reveal Destiny", type="primary", use_container_width=True)
    
    # Main content
    if analyze_btn:
        tz = pytz.timezone('Asia/Singapore')
        birth_dt = tz.localize(datetime.combine(birth_date, datetime.min.time().replace(hour=birth_hour, minute=birth_minute)))
        
        destiny = calculate_destiny(birth_dt)
        
        if "error" in destiny:
            st.error(f"Calculation error: {destiny['error']}")
            return
        
        # Store for AI prompt
        st.session_state.destiny_result = {
            "birth_info": {
                "date": birth_date.strftime("%Y-%m-%d"),
                "time": f"{birth_hour:02d}:{birth_minute:02d}",
                "timezone": "Asia/Singapore (UTC+8)"
            },
            "destiny": destiny,
            "profile": saved_profile
        }
        
        # Birth Summary Card
        palace_info = PALACE_DATA[destiny['palace']]
        st.markdown(f"""
        <div class="destiny-card">
            <div style="color: #9f7aea; font-size: 0.9em;">YOUR QI MEN BIRTH CHART</div>
            <div style="color: #fff; font-size: 1.2em; margin: 8px 0;">
                {birth_date.strftime('%B %d, %Y')} at {birth_hour:02d}:{birth_minute:02d}
            </div>
            <div style="color: #FFD700; font-size: 1.1em;">
                Palace {destiny['palace']} • {palace_info[0]} • {palace_info[1]}
            </div>
            <div style="color: #718096; font-size: 0.9em; margin-top: 5px;">
                {palace_info[2]} Element • {palace_info[3]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 9 Palace Grid
        st.subheader("🏯 Birth Palace Position")
        
        grid = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        
        for row in grid:
            cols = st.columns(3)
            for idx, p_num in enumerate(row):
                with cols[idx]:
                    is_birth = p_num == destiny["palace"]
                    p_name, p_dir, p_elem, _ = PALACE_DATA[p_num]
                    cls = "palace-birth" if is_birth else ""
                    
                    st.markdown(f"""
                    <div class="palace-cell {cls}">
                        <div style="color: {'#FFD700' if is_birth else '#718096'}; font-size: 0.75em;">{p_dir}</div>
                        <div style="color: #fff; font-weight: bold;">P{p_num}</div>
                        <div style="color: #a0aec0; font-size: 0.8em;">{p_elem}</div>
                        {"<div style='color: #FFD700;'>⭐ YOU</div>" if is_birth else ""}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        
        # Three Core Components with Brief Insights
        st.subheader("🌟 Your Natal Components")
        
        # Natal Star
        star = destiny["star"]
        star_info = STAR_DATA.get(star, {})
        st.markdown(f"""
        <div class="component-card component-star">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <div style="color: #f6e05e; font-size: 0.85em;">NATAL STAR 星</div>
                    <div style="color: #fff; font-size: 1.4em; margin: 5px 0;">{star} <span style="color: #718096; font-size: 0.7em;">{star_info.get('chinese', '')}</span></div>
                    <div style="color: #a0aec0; font-style: italic;">"{star_info.get('archetype', '?')}"</div>
                </div>
                <div style="color: #718096; font-size: 0.9em;">{star_info.get('element', '?')}</div>
            </div>
            <div style="color: #a0aec0; margin: 10px 0; font-size: 0.95em;">{star_info.get('brief', '')}</div>
            <div style="margin-top: 10px;">
                {''.join([f'<span class="trait-tag trait-good">✓ {s}</span>' for s in star_info.get('strengths', [])[:3]])}
            </div>
            <div style="margin-top: 5px;">
                {''.join([f'<span class="trait-tag trait-challenge">⚡ {c}</span>' for c in star_info.get('challenges', [])[:2]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Natal Door
        door = destiny["door"]
        door_info = DOOR_DATA.get(door, {})
        st.markdown(f"""
        <div class="component-card component-door">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <div style="color: #48bb78; font-size: 0.85em;">NATAL DOOR 门</div>
                    <div style="color: #fff; font-size: 1.4em; margin: 5px 0;">{door} <span style="color: #718096; font-size: 0.7em;">{door_info.get('chinese', '')}</span></div>
                    <div style="color: #a0aec0; font-style: italic;">"{door_info.get('theme', '?')}"</div>
                </div>
                <div style="color: #718096; font-size: 0.9em;">{door_info.get('element', '?')}</div>
            </div>
            <div style="color: #a0aec0; margin: 10px 0; font-size: 0.95em;">{door_info.get('brief', '')}</div>
            <div style="margin-top: 10px;">
                {''.join([f'<span class="trait-tag trait-good">🎁 {g}</span>' for g in door_info.get('gifts', [])[:3]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Natal Deity
        deity = destiny["deity"]
        deity_info = DEITY_DATA.get(deity, {})
        st.markdown(f"""
        <div class="component-card component-deity">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <div style="color: #9f7aea; font-size: 0.85em;">NATAL DEITY 神</div>
                    <div style="color: #fff; font-size: 1.4em; margin: 5px 0;">{deity} <span style="color: #718096; font-size: 0.7em;">{deity_info.get('chinese', '')}</span></div>
                </div>
            </div>
            <div style="color: #a0aec0; margin: 10px 0; font-size: 0.95em;">{deity_info.get('brief', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Formations
        if destiny.get('formations'):
            st.divider()
            st.subheader("📜 Natal Formations")
            
            f_score = destiny.get('formation_score', 0)
            verdict_emoji = "✨" if f_score > 0 else "⚠️" if f_score < 0 else "⚖️"
            verdict_text = "Auspicious patterns" if f_score > 0 else "Challenging patterns" if f_score < 0 else "Mixed patterns"
            
            st.markdown(f"**{verdict_emoji} {verdict_text}** ({len(destiny['formations'])} formation{'s' if len(destiny['formations']) > 1 else ''})")
            
            for f in destiny['formations']:
                emoji = "✨" if f['category'] == 'auspicious' else "⚠️" if f['category'] == 'inauspicious' else "📜"
                st.markdown(f"• {emoji} **{f['name']}** *({f['category']})*")
        
        # Quick Summary Table
        st.divider()
        st.subheader("📊 Quick Summary")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            | Component | Value |
            |-----------|-------|
            | Birth Palace | P{destiny['palace']} ({palace_info[1]}) |
            | Star | {destiny['star']} ({star_info.get('element', '?')}) |
            | Door | {destiny['door']} ({door_info.get('element', '?')}) |
            | Deity | {destiny['deity']} |
            """)
        
        with col2:
            st.markdown(f"""
            | Aspect | Info |
            |--------|------|
            | Star Archetype | {star_info.get('archetype', '?')} |
            | Door Theme | {door_info.get('theme', '?')} |
            | Heaven Stem | {destiny.get('heaven_stem', '?')} |
            | Earth Stem | {destiny.get('earth_stem', '?')} |
            """)
        
        # =================================================================
        # AI ANALYSIS BUTTON
        # =================================================================
        st.divider()
        st.subheader("🤖 Get Full Reading")
        
        st.markdown("""
        Get a comprehensive, personalized destiny interpretation including 
        **life path guidance**, **career insights**, and **BaZi comparison**.
        """)
        
        ai_prompt = generate_ai_prompt(
            st.session_state.destiny_result["birth_info"],
            destiny,
            saved_profile
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("📋 Copy Full Reading Prompt", type="primary", use_container_width=True):
                st.session_state.show_destiny_prompt = True
        
        with col2:
            st.download_button(
                "💾 Save as TXT",
                ai_prompt,
                file_name=f"destiny_{birth_date.strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        if st.session_state.get("show_destiny_prompt", False):
            st.code(ai_prompt, language="markdown")
            st.info("👆 Copy this prompt and paste it to Claude for a complete destiny reading")
        
        # QMDJ vs BaZi note
        with st.expander("ℹ️ QMDJ Destiny vs BaZi"):
            st.markdown("""
            **QMDJ Destiny** and **BaZi** are complementary systems that reveal different aspects:
            
            | Aspect | QMDJ Destiny | BaZi |
            |--------|--------------|------|
            | Focus | Spiritual path, timing mastery | Character, life phases |
            | Core Element | Star (archetype) | Day Master |
            | Life Theme | Door (opportunities) | Ten Gods (relationships) |
            | Support | Deity (spiritual backing) | Useful Gods (elements) |
            
            Using both together provides a **complete picture** of your destiny.
            """)
    
    else:
        st.info("👈 Enter your birth date and time, then click **Reveal Destiny**")
        
        st.markdown("""
        ### What You'll Discover
        
        **Quick Insights (App):**
        - Your natal Star, Door, and Deity
        - Brief archetype descriptions
        - Strengths and challenges
        - Formation patterns
        
        **Full Reading (AI):**
        - Deep archetype analysis
        - Life path guidance
        - Career and relationship insights
        - BaZi comparison (if profile set)
        - Personalized advice
        
        *QMDJ Destiny reveals your spiritual blueprint - different from BaZi!*
        """)


if __name__ == "__main__":
    main()
