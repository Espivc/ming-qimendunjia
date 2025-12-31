# Ming QiMenDunJia v10.0 - QMDJ Destiny Analysis
# pages/8_Destiny.py
"""
QI MEN DESTINY ANALYSIS (奇门命盘)
Fixed version - uses native Streamlit components
"""

import streamlit as st
from datetime import datetime, date
import pytz

# Import from core modules
import sys
sys.path.insert(0, '..')

try:
    from core.qmdj_engine import generate_qmdj_chart
    from core.formations import detect_formations, get_formation_score
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False

st.set_page_config(page_title="Destiny Analysis | Ming Qimen", page_icon="⭐", layout="wide")

# =============================================================================
# DATA
# =============================================================================

STAR_DATA = {
    "Canopy": {"cn": "天蓬", "elem": "Water", "arch": "The Strategist", "brief": "Strategic mind, resourceful", "str": ["Strategic thinking", "Adaptability", "Intuition"], "ch": ["Trust issues", "Secrecy"]},
    "Grass": {"cn": "天芮", "elem": "Earth", "arch": "The Healer", "brief": "Caring nature, patient", "str": ["Nurturing", "Medical intuition", "Patience"], "ch": ["Health sensitivity", "Over-giving"]},
    "Impulse": {"cn": "天冲", "elem": "Wood", "arch": "The Pioneer", "brief": "Courageous, takes initiative", "str": ["Courage", "Initiative", "Athletic"], "ch": ["Impatience", "Injury-prone"]},
    "Assistant": {"cn": "天辅", "elem": "Wood", "arch": "The Scholar", "brief": "Wise, excellent teacher", "str": ["Wisdom", "Teaching", "Diplomacy"], "ch": ["Overthinking", "Indecision"]},
    "Connect": {"cn": "天禽", "elem": "Earth", "arch": "The Connector", "brief": "Versatile, central role", "str": ["Versatility", "Networking", "Balance"], "ch": ["Scattered energy"]},
    "Heart": {"cn": "天心", "elem": "Metal", "arch": "The Authority", "brief": "Precise, authoritative", "str": ["Precision", "Authority", "Technical skill"], "ch": ["Over-analytical", "Coldness"]},
    "Pillar": {"cn": "天柱", "elem": "Metal", "arch": "The Critic", "brief": "Sharp insight, truth-seeker", "str": ["Discernment", "Independence"], "ch": ["Harsh criticism", "Isolation"]},
    "Ren": {"cn": "天任", "elem": "Earth", "arch": "The Diplomat", "brief": "Stable, trustworthy", "str": ["Stability", "Trustworthiness"], "ch": ["Stubbornness"]},
    "Hero": {"cn": "天英", "elem": "Fire", "arch": "The Performer", "brief": "Creative, charismatic", "str": ["Creativity", "Charisma", "Expression"], "ch": ["Attention-seeking"]}
}

DOOR_DATA = {
    "Open": {"cn": "开门", "elem": "Metal", "theme": "Leadership & Authority", "brief": "Opens doors, natural authority", "gifts": ["Authority", "Career success", "Opportunities"]},
    "Rest": {"cn": "休门", "elem": "Water", "theme": "Prosperity & Ease", "brief": "Attracts wealth through timing", "gifts": ["Wealth", "Networking", "Timing"]},
    "Life": {"cn": "生门", "elem": "Earth", "theme": "Creation & Growth", "brief": "Natural creator, business sense", "gifts": ["Wealth creation", "Business acumen"]},
    "Harm": {"cn": "伤门", "elem": "Wood", "theme": "Competition & Transformation", "brief": "Grows through challenges", "gifts": ["Competitive drive", "Breakthrough"]},
    "Delusion": {"cn": "杜门", "elem": "Wood", "theme": "Strategy & Secrets", "brief": "Works best behind scenes", "gifts": ["Strategy", "Hidden influence"]},
    "Scenery": {"cn": "景门", "elem": "Fire", "theme": "Recognition & Expression", "brief": "Meant to be seen, artistic", "gifts": ["Recognition", "Expression"]},
    "Death": {"cn": "死门", "elem": "Earth", "theme": "Transformation & Endings", "brief": "Masters transitions", "gifts": ["Completing cycles", "Deep wisdom"]},
    "Fear": {"cn": "惊门", "elem": "Metal", "theme": "Awareness & Protection", "brief": "Heightened awareness", "gifts": ["Awareness", "Legal mind"]}
}

DEITY_DATA = {
    "Chief": {"cn": "值符", "brief": "Authority backing, people follow you"},
    "Serpent": {"cn": "腾蛇", "brief": "Mystical perception, intuition"},
    "Moon": {"cn": "太阴", "brief": "Hidden support, benefactors"},
    "Six Harmony": {"cn": "六合", "brief": "Relationship blessing"},
    "Hook": {"cn": "勾陈", "brief": "Grounding force, stability"},
    "Tiger": {"cn": "白虎", "brief": "Fierce protection"},
    "Emptiness": {"cn": "玄武", "brief": "Hidden wisdom"},
    "Nine Earth": {"cn": "九地", "brief": "Deep grounding, patience"},
    "Nine Heaven": {"cn": "九天", "brief": "Upward energy, ambition"}
}

PALACE_DATA = {
    1: ("Kan", "North", "Water"), 2: ("Kun", "Southwest", "Earth"), 3: ("Zhen", "East", "Wood"),
    4: ("Xun", "Southeast", "Wood"), 5: ("Center", "Center", "Earth"), 6: ("Qian", "Northwest", "Metal"),
    7: ("Dui", "West", "Metal"), 8: ("Gen", "Northeast", "Earth"), 9: ("Li", "South", "Fire")
}

# Default components per palace
DEFAULT_COMP = {
    1: ("Canopy", "Rest", "Emptiness"), 2: ("Grass", "Death", "Nine Earth"), 3: ("Impulse", "Harm", "Six Harmony"),
    4: ("Assistant", "Delusion", "Moon"), 5: ("Connect", "Life", "Hook"), 6: ("Heart", "Open", "Chief"),
    7: ("Pillar", "Fear", "Tiger"), 8: ("Ren", "Life", "Nine Heaven"), 9: ("Hero", "Scenery", "Serpent")
}

BRANCH_PALACE = {"Zi": 1, "Chou": 8, "Yin": 8, "Mao": 3, "Chen": 4, "Si": 4, "Wu": 9, "Wei": 2, "Shen": 2, "You": 7, "Xu": 6, "Hai": 6}

def get_hour_branch(hour):
    branches = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
    return "Zi" if hour == 23 else branches[(hour + 1) // 2 % 12]

def calculate_destiny(birth_dt):
    hour_branch = get_hour_branch(birth_dt.hour)
    palace = BRANCH_PALACE.get(hour_branch, 6)
    
    # Try QMDJ engine first
    if IMPORTS_OK:
        try:
            chart = generate_qmdj_chart(birth_dt)
            pd = chart.get("palaces", {}).get(str(palace), {})
            star, door, deity = pd.get("star", ""), pd.get("door", ""), pd.get("deity", "")
            if star in STAR_DATA and door in DOOR_DATA:
                formations = detect_formations(pd)
                return {"palace": palace, "star": star, "door": door, "deity": deity, 
                        "formations": [{"name": f.name_en, "cat": f.category.value} for f in formations]}
        except:
            pass
    
    # Fallback to defaults
    star, door, deity = DEFAULT_COMP.get(palace, ("Heart", "Open", "Chief"))
    return {"palace": palace, "star": star, "door": door, "deity": deity, "formations": []}

# =============================================================================
# MAIN
# =============================================================================

def main():
    st.title("⭐ QMDJ Destiny Analysis")
    
    bazi_birth = st.session_state.get("bazi_birth_info", {})
    saved_profile = st.session_state.get("user_profile", None)
    
    with st.sidebar:
        st.header("🎂 Birth Information")
        
        if bazi_birth:
            st.success("🔗 Synced from BaZi")
            use_bazi = st.checkbox("Use BaZi birth info", value=True)
        else:
            use_bazi = False
            st.info("💡 Set BaZi first to auto-sync")
        
        if use_bazi and bazi_birth:
            birth_date = bazi_birth.get("date", date(1990, 1, 1))
            if isinstance(birth_date, str):
                birth_date = date.fromisoformat(birth_date)
            birth_hour = bazi_birth.get("hour", 12)
            birth_minute = bazi_birth.get("minute", 0)
            st.write(f"**Date:** {birth_date}")
            st.write(f"**Time:** {birth_hour:02d}:{birth_minute:02d}")
        else:
            birth_date = st.date_input("Birth Date", value=date(1990, 1, 1))
            col1, col2 = st.columns(2)
            with col1:
                birth_hour = st.selectbox("Hour", range(24), index=12, format_func=lambda x: f"{x:02d}")
            with col2:
                birth_minute = st.selectbox("Min", range(60), index=0, format_func=lambda x: f"{x:02d}")
        
        st.divider()
        if saved_profile:
            st.success(f"🎴 {saved_profile.get('day_master', '?')} {saved_profile.get('day_master_cn', '')} DM")
        
        analyze_btn = st.button("🔮 Reveal Destiny", type="primary", use_container_width=True)
    
    if analyze_btn:
        if isinstance(birth_date, str):
            birth_date = date.fromisoformat(birth_date)
        
        tz = pytz.timezone('Asia/Singapore')
        birth_dt = tz.localize(datetime.combine(birth_date, datetime.min.time().replace(hour=birth_hour, minute=birth_minute)))
        
        destiny = calculate_destiny(birth_dt)
        palace_info = PALACE_DATA[destiny['palace']]
        
        # Header
        st.markdown(f"### 🏯 Birth: {birth_date.strftime('%B %d, %Y')} at {birth_hour:02d}:{birth_minute:02d}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Palace", f"P{destiny['palace']} {palace_info[0]}")
        col2.metric("Direction", palace_info[1])
        col3.metric("Element", palace_info[2])
        
        st.divider()
        
        # 9 Palace Grid
        st.subheader("🏯 Birth Palace Position")
        grid = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        for row in grid:
            cols = st.columns(3)
            for i, p in enumerate(row):
                with cols[i]:
                    pn, pd, pe = PALACE_DATA[p]
                    if p == destiny["palace"]:
                        st.success(f"**P{p}** ⭐ YOU\n\n{pd} • {pe}")
                    else:
                        st.info(f"**P{p}**\n\n{pd} • {pe}")
        
        st.divider()
        
        # Components
        st.subheader("🌟 Your Natal Components")
        
        # Star
        star = destiny["star"]
        sd = STAR_DATA.get(star, {})
        st.markdown("---")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### ⭐ NATAL STAR: {star} {sd.get('cn', '')}")
            st.markdown(f"**\"{sd.get('arch', '')}\"** — {sd.get('brief', '')}")
        with col2:
            st.metric("Element", sd.get('elem', '?'))
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✓ Strengths:**")
            for s in sd.get('str', []):
                st.markdown(f"- {s}")
        with c2:
            st.markdown("**⚡ Challenges:**")
            for c in sd.get('ch', []):
                st.markdown(f"- {c}")
        
        # Door
        door = destiny["door"]
        dd = DOOR_DATA.get(door, {})
        st.markdown("---")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### 🚪 NATAL DOOR: {door} {dd.get('cn', '')}")
            st.markdown(f"**\"{dd.get('theme', '')}\"** — {dd.get('brief', '')}")
        with col2:
            st.metric("Element", dd.get('elem', '?'))
        
        st.markdown("**🎁 Life Gifts:**")
        for g in dd.get('gifts', []):
            st.markdown(f"- {g}")
        
        # Deity
        deity = destiny["deity"]
        de = DEITY_DATA.get(deity, {})
        st.markdown("---")
        st.markdown(f"### 👑 NATAL DEITY: {deity} {de.get('cn', '')}")
        st.markdown(f"*{de.get('brief', '')}*")
        
        # Formations
        if destiny.get('formations'):
            st.divider()
            st.subheader("📜 Natal Formations")
            for f in destiny['formations']:
                emoji = "✨" if f['cat'] == 'Auspicious' else "⚠️"
                st.markdown(f"• {emoji} **{f['name']}** ({f['cat']})")
        
        # Summary table
        st.divider()
        st.subheader("📊 Quick Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
| Component | Value |
|-----------|-------|
| Palace | P{destiny['palace']} ({palace_info[1]}) |
| Star | {star} ({sd.get('elem', '?')}) |
| Door | {door} ({dd.get('elem', '?')}) |
| Deity | {deity} |
""")
        with col2:
            st.markdown(f"""
| Aspect | Info |
|--------|------|
| Archetype | {sd.get('arch', '?')} |
| Theme | {dd.get('theme', '?')} |
| Blessing | {de.get('brief', '?')[:25]}... |
""")
        
        # AI Prompt
        st.divider()
        st.subheader("🤖 Get Full Reading")
        
        prompt = f"""Analyze this QMDJ Destiny chart:

**Birth:** {birth_date} at {birth_hour:02d}:{birth_minute:02d}
**Palace:** P{destiny['palace']} - {palace_info[0]} ({palace_info[1]}, {palace_info[2]})

**Natal Star:** {star} {sd.get('cn','')} - {sd.get('arch','')} ({sd.get('elem','')})
**Natal Door:** {door} {dd.get('cn','')} - {dd.get('theme','')} ({dd.get('elem','')})
**Natal Deity:** {deity} {de.get('cn','')}
"""
        if saved_profile:
            prompt += f"""
**BaZi Profile:** {saved_profile.get('day_master','')} {saved_profile.get('day_master_cn','')} Day Master
- Strength: {saved_profile.get('strength','')} ({saved_profile.get('strength_pct','')}%)
- Useful Gods: {', '.join(saved_profile.get('useful_gods',[]))}
"""
        prompt += """
Please provide:
1. Natal Star personality analysis
2. Natal Door life opportunities
3. Natal Deity spiritual backing
4. How components interact together
5. Life path guidance and career insights
6. Key challenges to navigate"""
        
        if st.button("📋 Show AI Prompt", type="primary"):
            st.code(prompt, language="markdown")
            st.info("Copy and paste to Claude for full reading")
        
        st.download_button("💾 Save Prompt", prompt, f"destiny_{birth_date}.txt", "text/plain")
    
    else:
        st.info("👈 Enter birth info and click **Reveal Destiny**")
        if bazi_birth:
            st.success("✅ Birth info ready from BaZi - just click Reveal!")

if __name__ == "__main__":
    main()
