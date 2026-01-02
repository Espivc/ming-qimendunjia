# pages/1_Chart.py - Ming QiMenDunJia v10.3 PRO
# QMDJ Chart with Full Component Explanations
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="QMDJ Chart | Ming Qimen", page_icon="🎯", layout="wide")

# =============================================================================
# COMPONENT DATA WITH EXPLANATIONS
# =============================================================================

STAR_INFO = {
    "Canopy": {"cn": "天蓬", "elem": "Water", "nature": "Inauspicious",
        "meaning": "Strategic intelligence, working behind scenes, hidden power",
        "keywords": ["Strategy", "Secrecy", "Cunning", "Deep thinking"],
        "favorable": "Research, investigation, covert operations, planning",
        "caution": "Deception, hidden enemies, trust issues"},
    "Grass": {"cn": "天芮", "elem": "Earth", "nature": "Inauspicious",
        "meaning": "Illness, obstacles, but also healing and medical matters",
        "keywords": ["Health", "Obstacles", "Healing", "Patience"],
        "favorable": "Medical treatment, healthcare, addressing root problems",
        "caution": "Health issues, delays, sickness energy"},
    "Impulse": {"cn": "天冲", "elem": "Wood", "nature": "Auspicious",
        "meaning": "Breakthrough energy, action, initiative, speed",
        "keywords": ["Action", "Speed", "Breakthrough", "Courage"],
        "favorable": "Starting projects, competitions, sports, quick action",
        "caution": "Impulsiveness, accidents, rushing"},
    "Assistant": {"cn": "天辅", "elem": "Wood", "nature": "Auspicious",
        "meaning": "Wisdom, education, helpful guidance, scholarly pursuits",
        "keywords": ["Wisdom", "Teaching", "Guidance", "Learning"],
        "favorable": "Education, exams, consulting, seeking advice",
        "caution": "Over-analysis, indecision"},
    "Connect": {"cn": "天禽", "elem": "Earth", "nature": "Neutral",
        "meaning": "Central connector, versatility, bringing things together",
        "keywords": ["Connection", "Versatility", "Balance", "Integration"],
        "favorable": "Networking, mediation, bringing parties together",
        "caution": "Scattered energy, lack of focus"},
    "Heart": {"cn": "天心", "elem": "Metal", "nature": "Auspicious",
        "meaning": "Authority, precision, problem-solving, technical excellence",
        "keywords": ["Authority", "Precision", "Leadership", "Expertise"],
        "favorable": "Leadership decisions, technical work, medicine, engineering",
        "caution": "Coldness, over-criticism"},
    "Pillar": {"cn": "天柱", "elem": "Metal", "nature": "Inauspicious",
        "meaning": "Criticism, speaking truth, standing alone, discernment",
        "keywords": ["Truth", "Criticism", "Independence", "Standards"],
        "favorable": "Auditing, quality control, speaking truth, legal matters",
        "caution": "Harsh words, isolation, negativity"},
    "Ren": {"cn": "天任", "elem": "Earth", "nature": "Auspicious",
        "meaning": "Trust, reliability, carrying responsibilities, stability",
        "keywords": ["Trust", "Reliability", "Responsibility", "Stability"],
        "favorable": "Building trust, long-term commitments, steady progress",
        "caution": "Stubbornness, slow progress"},
    "Hero": {"cn": "天英", "elem": "Fire", "nature": "Neutral",
        "meaning": "Visibility, recognition, charisma, creative expression",
        "keywords": ["Fame", "Creativity", "Expression", "Visibility"],
        "favorable": "Public speaking, arts, marketing, seeking recognition",
        "caution": "Ego issues, attention-seeking, burnout"}
}

DOOR_INFO = {
    "Open": {"cn": "开门", "elem": "Metal", "nature": "Auspicious",
        "meaning": "Career opportunities, leadership, official matters, new beginnings",
        "keywords": ["Career", "Leadership", "Opportunity", "Authority"],
        "favorable": "Job interviews, promotions, government matters, starting businesses",
        "caution": "May attract attention from authorities"},
    "Rest": {"cn": "休门", "elem": "Water", "nature": "Auspicious",
        "meaning": "Prosperity, ease, helpful people, relaxation, wealth attraction",
        "keywords": ["Wealth", "Rest", "Support", "Ease"],
        "favorable": "Negotiations, seeking help, rest, attracting resources",
        "caution": "May lead to laziness or complacency"},
    "Life": {"cn": "生门", "elem": "Earth", "nature": "Auspicious",
        "meaning": "Wealth creation, growth, business success, property matters",
        "keywords": ["Wealth", "Growth", "Business", "Property"],
        "favorable": "Business deals, investments, property purchase, wealth building",
        "caution": "Greed, overextension"},
    "Harm": {"cn": "伤门", "elem": "Wood", "nature": "Inauspicious",
        "meaning": "Competition, conflict, transformation through struggle",
        "keywords": ["Competition", "Conflict", "Injury", "Breakthrough"],
        "favorable": "Competitive situations, sports, breaking obstacles, surgery",
        "caution": "Arguments, injuries, legal disputes"},
    "Delusion": {"cn": "杜门", "elem": "Wood", "nature": "Neutral",
        "meaning": "Hiding, secrecy, strategic concealment, blocked paths",
        "keywords": ["Secrecy", "Hiding", "Strategy", "Blockage"],
        "favorable": "Keeping secrets, covert operations, avoiding detection",
        "caution": "Blocked opportunities, confusion, deception"},
    "Scenery": {"cn": "景门", "elem": "Fire", "nature": "Neutral",
        "meaning": "Recognition, visibility, documents, examinations, fame",
        "keywords": ["Fame", "Documents", "Exams", "Visibility"],
        "favorable": "Exams, publishing, marketing, seeking recognition",
        "caution": "Gossip, unwanted exposure, document issues"},
    "Death": {"cn": "死门", "elem": "Earth", "nature": "Inauspicious",
        "meaning": "Endings, closures, funerals, transformation, letting go",
        "keywords": ["Ending", "Closure", "Death", "Transformation"],
        "favorable": "Ending relationships, funerals, closure matters, spiritual work",
        "caution": "Loss, endings, stagnation"},
    "Fear": {"cn": "惊门", "elem": "Metal", "nature": "Inauspicious",
        "meaning": "Anxiety, legal matters, warnings, heightened awareness",
        "keywords": ["Fear", "Legal", "Warning", "Awareness"],
        "favorable": "Legal matters, warnings, protective actions",
        "caution": "Anxiety, legal troubles, unexpected shocks"}
}

DEITY_INFO = {
    "Chief": {"cn": "值符", "nature": "Auspicious",
        "meaning": "Highest authority support, official backing, noble help",
        "keywords": ["Authority", "Support", "Backing", "Official"],
        "influence": "Support from authority figures and those in power"},
    "Serpent": {"cn": "腾蛇", "nature": "Inauspicious",
        "meaning": "Illusion, dreams, psychic perception, worry, strange events",
        "keywords": ["Dreams", "Illusion", "Worry", "Psychic"],
        "influence": "Dreams may be significant; watch for strange occurrences"},
    "Moon": {"cn": "太阴", "nature": "Auspicious",
        "meaning": "Hidden support, female benefactors, secret assistance",
        "keywords": ["Hidden help", "Female", "Secret", "Yin"],
        "influence": "Help comes from behind the scenes, often from women"},
    "Six Harmony": {"cn": "六合", "nature": "Auspicious",
        "meaning": "Partnerships, cooperation, harmony, matchmaking",
        "keywords": ["Partnership", "Harmony", "Cooperation", "Marriage"],
        "influence": "Excellent for partnerships, relationships, collaborations"},
    "Hook": {"cn": "勾陈", "nature": "Neutral",
        "meaning": "Grounding, stability, delays, bureaucracy",
        "keywords": ["Grounding", "Delay", "Stability", "Bureaucracy"],
        "influence": "Things may be slow but stable; expect paperwork"},
    "Tiger": {"cn": "白虎", "nature": "Inauspicious",
        "meaning": "Aggression, accidents, surgery, fierce energy, roads",
        "keywords": ["Danger", "Surgery", "Fierce", "Accident"],
        "influence": "Be cautious of accidents; good for surgery if needed"},
    "Emptiness": {"cn": "玄武", "nature": "Inauspicious",
        "meaning": "Theft, deception, loss, unconventional wisdom",
        "keywords": ["Theft", "Deception", "Loss", "Unconventional"],
        "influence": "Watch for theft or deception; verify everything"},
    "Nine Earth": {"cn": "九地", "nature": "Auspicious",
        "meaning": "Patience, grounding, defense, hiding, real estate",
        "keywords": ["Patience", "Defense", "Property", "Hiding"],
        "influence": "Patience wins; good for defensive strategies and property"},
    "Nine Heaven": {"cn": "九天", "nature": "Auspicious",
        "meaning": "Expansion, upward movement, ambition, taking action",
        "keywords": ["Expansion", "Ambition", "Action", "Rise"],
        "influence": "Excellent for expansion and bold moves; aim high"}
}

PALACE_INFO = {
    1: {"name": "Kan", "cn": "坎", "dir": "N", "elem": "Water"},
    2: {"name": "Kun", "cn": "坤", "dir": "SW", "elem": "Earth"},
    3: {"name": "Zhen", "cn": "震", "dir": "E", "elem": "Wood"},
    4: {"name": "Xun", "cn": "巽", "dir": "SE", "elem": "Wood"},
    5: {"name": "Center", "cn": "中", "dir": "C", "elem": "Earth"},
    6: {"name": "Qian", "cn": "乾", "dir": "NW", "elem": "Metal"},
    7: {"name": "Dui", "cn": "兑", "dir": "W", "elem": "Metal"},
    8: {"name": "Gen", "cn": "艮", "dir": "NE", "elem": "Earth"},
    9: {"name": "Li", "cn": "离", "dir": "S", "elem": "Fire"}
}

# Simplified default components (real app uses kinqimen library)
DEFAULT_COMP = {
    1: ("Canopy", "Rest", "Emptiness"), 2: ("Grass", "Death", "Nine Earth"),
    3: ("Impulse", "Harm", "Six Harmony"), 4: ("Assistant", "Delusion", "Moon"),
    5: ("Connect", "Life", "Hook"), 6: ("Heart", "Open", "Chief"),
    7: ("Pillar", "Fear", "Tiger"), 8: ("Ren", "Life", "Nine Heaven"),
    9: ("Hero", "Scenery", "Serpent")
}

def nature_icon(n):
    return "🟢" if n == "Auspicious" else "🔴" if n == "Inauspicious" else "🟡"

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    st.title("🎯 QMDJ Chart")
    
    with st.sidebar:
        st.header("⏰ Time")
        use_now = st.checkbox("Use current time", True)
        if use_now:
            now = datetime.utcnow() + timedelta(hours=8)
            chart_dt = now
        else:
            d = st.date_input("Date", datetime.now())
            h = st.selectbox("Hour", range(24), datetime.now().hour)
            chart_dt = datetime.combine(d, datetime.min.time().replace(hour=h))
        
        st.info(f"📅 {chart_dt.strftime('%Y-%m-%d %H:%M')}")
        gen_btn = st.button("🔮 Generate", type="primary", use_container_width=True)
    
    if gen_btn or st.session_state.get("qmdj_generated"):
        if gen_btn:
            # Build chart
            structure = "Yang Dun" if chart_dt.month in [12,1,2,3,4,5] else "Yin Dun"
            structure_cn = "阳遁" if "Yang" in structure else "阴遁"
            ju = ((chart_dt.day - 1) % 9) + 1
            
            chart = {
                "datetime": chart_dt.strftime("%Y-%m-%d %H:%M"),
                "structure": structure, "structure_cn": structure_cn, "ju": ju,
                "palaces": {}
            }
            
            for p in range(1, 10):
                pi = PALACE_INFO[p]
                star, door, deity = DEFAULT_COMP.get(p, DEFAULT_COMP[5])
                chart["palaces"][p] = {
                    "number": p, "name": pi["name"], "cn": pi["cn"],
                    "dir": pi["dir"], "elem": pi["elem"],
                    "star": star, "door": door, "deity": deity
                }
            
            st.session_state.qmdj_chart = chart
            st.session_state.qmdj_generated = True
        
        chart = st.session_state.qmdj_chart
        
        # Header
        st.markdown(f"### 📅 {chart['datetime']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Structure", f"{chart['structure']} {chart['structure_cn']}")
        c2.metric("Ju 局", chart['ju'])
        c3.metric("Hour", chart['datetime'].split()[1])
        
        st.divider()
        
        # Nine Palaces Grid
        st.subheader("🏯 Nine Palaces")
        
        for row in [[4,9,2], [3,5,7], [8,1,6]]:
            cols = st.columns(3)
            for i, pn in enumerate(row):
                with cols[i]:
                    p = chart["palaces"][pn]
                    si, di, dei = STAR_INFO.get(p["star"],{}), DOOR_INFO.get(p["door"],{}), DEITY_INFO.get(p["deity"],{})
                    
                    st.markdown(f"""
                    <div style="background:#1a1a2e; padding:12px; border-radius:8px; border:1px solid #0f3460;">
                        <div style="text-align:center; color:#888; font-size:11px;">P{pn}</div>
                        <div style="text-align:center; color:#e94560; font-weight:bold;">{p['name']} {p['cn']}</div>
                        <div style="text-align:center; color:#666; font-size:11px;">{p['elem']} • {p['dir']}</div>
                        <hr style="border-color:#0f3460; margin:8px 0;">
                        <div style="font-size:12px;">
                            {nature_icon(si.get('nature',''))} ★{p['star']} {si.get('cn','')}<br>
                            {nature_icon(di.get('nature',''))} 門{p['door']} {di.get('cn','')}<br>
                            {nature_icon(dei.get('nature',''))} 神{p['deity']} {dei.get('cn','')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        
        # Palace Analysis Selector
        st.subheader("🔍 Palace Analysis")
        
        sel = st.selectbox("Select palace", range(1,10),
            format_func=lambda x: f"P{x} - {PALACE_INFO[x]['name']} {PALACE_INFO[x]['cn']} ({PALACE_INFO[x]['dir']})")
        
        p = chart["palaces"][sel]
        pi = PALACE_INFO[sel]
        star, door, deity = STAR_INFO.get(p["star"],{}), DOOR_INFO.get(p["door"],{}), DEITY_INFO.get(p["deity"],{})
        
        # Quick Assessment
        ausp = sum([1 if star.get("nature")=="Auspicious" else 0,
                    1 if door.get("nature")=="Auspicious" else 0,
                    1 if deity.get("nature")=="Auspicious" else 0])
        
        if ausp >= 2:
            st.success(f"✅ **FAVORABLE** - {ausp}/3 auspicious components")
        elif ausp == 1:
            st.warning(f"⚡ **MIXED** - {ausp}/3 auspicious components")
        else:
            st.error(f"⚠️ **CAUTION** - {ausp}/3 auspicious components")
        
        st.divider()
        
        # Star Explanation
        st.markdown(f"### ⭐ Star: {p['star']} {star.get('cn','')}")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"**Element:** {star.get('elem','')}\n\n**Nature:** {nature_icon(star.get('nature',''))} {star.get('nature','')}")
            st.markdown("**Keywords:**")
            for k in star.get("keywords", []): st.markdown(f"• {k}")
        with c2:
            st.info(f"**Meaning:** {star.get('meaning','')}")
            st.success(f"**Favorable for:** {star.get('favorable','')}")
            st.warning(f"**Caution:** {star.get('caution','')}")
        
        st.divider()
        
        # Door Explanation
        st.markdown(f"### 🚪 Door: {p['door']} {door.get('cn','')}")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"**Element:** {door.get('elem','')}\n\n**Nature:** {nature_icon(door.get('nature',''))} {door.get('nature','')}")
            st.markdown("**Keywords:**")
            for k in door.get("keywords", []): st.markdown(f"• {k}")
        with c2:
            st.info(f"**Meaning:** {door.get('meaning','')}")
            st.success(f"**Favorable for:** {door.get('favorable','')}")
            st.warning(f"**Caution:** {door.get('caution','')}")
        
        st.divider()
        
        # Deity Explanation
        st.markdown(f"### 👑 Deity: {p['deity']} {deity.get('cn','')}")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"**Nature:** {nature_icon(deity.get('nature',''))} {deity.get('nature','')}")
            st.markdown("**Keywords:**")
            for k in deity.get("keywords", []): st.markdown(f"• {k}")
        with c2:
            st.info(f"**Meaning:** {deity.get('meaning','')}")
            st.success(f"**Influence:** {deity.get('influence','')}")
        
        st.divider()
        
        # Synthesis
        st.subheader("🔮 Palace Synthesis")
        st.markdown(f"""
**Palace {sel} ({pi['name']}) Analysis:**

• **Star ({p['star']})** brings: {star.get('meaning','').split(',')[0]}
• **Door ({p['door']})** opens: {door.get('favorable','').split(',')[0]}
• **Deity ({p['deity']})** provides: {deity.get('influence','').split(';')[0]}

**Best Uses:** {star.get('favorable','').split(',')[0]}, {door.get('favorable','').split(',')[0]}

**Watch Out For:** {star.get('caution','')}, {door.get('caution','')}
""")
        
        st.divider()
        
        # Buttons
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📤 Export", use_container_width=True):
                st.switch_page("pages/2_Export.py")
        with c2:
            if st.button("🤖 AI Prompt", use_container_width=True):
                st.code(f"""QMDJ Chart: {chart['datetime']}
Structure: {chart['structure']} | Ju: {chart['ju']}

Palace {sel} ({pi['name']} {pi['dir']}):
- Star: {p['star']} {star.get('cn','')} ({star.get('nature','')})
- Door: {p['door']} {door.get('cn','')} ({door.get('nature','')})
- Deity: {p['deity']} {deity.get('cn','')} ({deity.get('nature','')})

Analyze auspiciousness, best activities, timing, advice.""")
    
    else:
        st.info("👈 Click **Generate** to create a chart")
        
        with st.expander("📖 What is QMDJ?"):
            st.markdown("""
**Qi Men Dun Jia (奇门遁甲)** - Strategic timing and direction selection system.

**Nine Palaces** represent directions with unique energy:
- **Star (天星)**: Nature of energy (action, wisdom, authority)
- **Door (八门)**: Opportunities (wealth, career, travel)
- **Deity (八神)**: Spiritual support (authority, harmony)

**Reading:** 🟢 Auspicious | 🟡 Neutral | 🔴 Inauspicious
            """)
    
    st.divider()
    st.caption("🌟 Ming Qimen 明奇门 | Chart v10.3 | Schema v3.0")

if __name__ == "__main__":
    main()
