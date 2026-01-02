# pages/8_Destiny.py - Ming QiMenDunJia v10.2 PRO
import streamlit as st
from datetime import date

st.set_page_config(page_title="QMDJ Destiny | Ming Qimen", page_icon="⭐", layout="wide")

PALACE_INFO = {
    1: {"name": "Kan 坎", "dir": "North", "elem": "Water", "trigram": "☵",
        "meaning": "The Abyss - depth, hidden potential", "life_theme": "Navigating deep waters - emotional depth, hidden opportunities, flowing around obstacles.",
        "career": "Research, investigation, psychology, water industries", "challenge": "Hidden enemies, deception. Trust your intuition."},
    2: {"name": "Kun 坤", "dir": "Southwest", "elem": "Earth", "trigram": "☷",
        "meaning": "The Receptive - nurturing, supportive", "life_theme": "Support, nurturing others, building stable foundations.",
        "career": "Real estate, HR, caregiving, hospitality", "challenge": "Too self-sacrificing. Learn to receive."},
    3: {"name": "Zhen 震", "dir": "East", "elem": "Wood", "trigram": "☳",
        "meaning": "The Arousing - action, initiative", "life_theme": "Breakthrough moments, taking initiative, catalyst for change.",
        "career": "Sports, military, startups, activism", "challenge": "Act before thinking. Learn patience."},
    4: {"name": "Xun 巽", "dir": "Southeast", "elem": "Wood", "trigram": "☴",
        "meaning": "The Gentle - penetrating influence", "life_theme": "Subtle influence, spreading ideas, gentle persistence.",
        "career": "Communications, marketing, travel, consulting", "challenge": "Indecisive. Learn to commit."},
    5: {"name": "Center 中", "dir": "Center", "elem": "Earth", "trigram": "⊕",
        "meaning": "The Pivot - balance, integration", "life_theme": "Natural coordinator bringing elements together.",
        "career": "Management, mediation, logistics", "challenge": "Pulled in all directions. Set boundaries."},
    6: {"name": "Qian 乾", "dir": "Northwest", "elem": "Metal", "trigram": "☰",
        "meaning": "The Creative - heaven, authority", "life_theme": "Leadership and authority. Guide, decide, take responsibility.",
        "career": "Executive, government, military leadership", "challenge": "Too controlling. Learn flexibility."},
    7: {"name": "Dui 兑", "dir": "West", "elem": "Metal", "trigram": "☱",
        "meaning": "The Joyous - joy, communication", "life_theme": "Bringing joy and communication. Excel in social situations.",
        "career": "Entertainment, sales, hospitality, coaching", "challenge": "Excessive pleasure-seeking. Learn depth."},
    8: {"name": "Gen 艮", "dir": "Northeast", "elem": "Earth", "trigram": "☶",
        "meaning": "Keeping Still - meditation, stopping", "life_theme": "Knowing when to stop. Provide stability like a mountain.",
        "career": "Spiritual work, real estate, meditation", "challenge": "Too rigid. Learn when to move."},
    9: {"name": "Li 离", "dir": "South", "elem": "Fire", "trigram": "☲",
        "meaning": "The Clinging - fire, clarity", "life_theme": "Illumination, recognition, bringing clarity. Meant to be seen.",
        "career": "Media, arts, teaching, publishing", "challenge": "Too much attention-seeking. Learn substance."}
}

STAR_INFO = {
    "Canopy": {"cn": "天蓬", "elem": "Water", "arch": "🎭 The Strategist",
        "desc": "Deep strategic intelligence. Work behind scenes. Navigate complex situations with cunning.",
        "str": ["Strategic mind", "Adaptability", "Psychological insight"], "ch": ["Trust issues", "Secrecy"],
        "career": "Intelligence, research, strategy, psychology"},
    "Grass": {"cn": "天芮", "elem": "Earth", "arch": "💚 The Healer",
        "desc": "Natural connection to healing. Drawn to helping others through difficulties.",
        "str": ["Healing ability", "Empathy", "Medical intuition"], "ch": ["Health sensitivity", "Over-giving"],
        "career": "Healthcare, therapy, counseling, alternative medicine"},
    "Impulse": {"cn": "天冲", "elem": "Wood", "arch": "⚡ The Pioneer",
        "desc": "Break through barriers and lead charges. Herald change and new beginnings.",
        "str": ["Courage", "Initiative", "Action-oriented"], "ch": ["Impatience", "Recklessness"],
        "career": "Sports, military, entrepreneurship, activism"},
    "Assistant": {"cn": "天辅", "elem": "Wood", "arch": "📚 The Scholar",
        "desc": "Wisdom and gift of teaching. Help others see clearly.",
        "str": ["Wisdom", "Teaching ability", "Diplomacy"], "ch": ["Overthinking", "Indecision"],
        "career": "Education, consulting, diplomacy, research"},
    "Connect": {"cn": "天禽", "elem": "Earth", "arch": "🔗 The Connector",
        "desc": "Central hub connecting disparate elements. Bring together what couldn't meet.",
        "str": ["Networking", "Versatility", "Integration"], "ch": ["Scattered energy"],
        "career": "Networking, matchmaking, management"},
    "Heart": {"cn": "天心", "elem": "Metal", "arch": "⚔️ The Authority",
        "desc": "Natural authority and precision. Cut through confusion to find truth.",
        "str": ["Authority", "Precision", "Problem-solving"], "ch": ["Over-analytical", "Coldness"],
        "career": "Medicine, engineering, law, leadership"},
    "Pillar": {"cn": "天柱", "elem": "Metal", "arch": "👁️ The Critic",
        "desc": "See flaws and speak uncomfortable truths. Stand alone regardless of opinion.",
        "str": ["Discernment", "Truth-telling", "Independence"], "ch": ["Harsh criticism", "Isolation"],
        "career": "Quality control, auditing, legal, inspection"},
    "Ren": {"cn": "天任", "elem": "Earth", "arch": "🤝 The Diplomat",
        "desc": "Trust, reliability, carry responsibilities. Foundation of stability.",
        "str": ["Trustworthiness", "Reliability", "Stability"], "ch": ["Stubbornness"],
        "career": "Finance, insurance, diplomatic service, management"},
    "Hero": {"cn": "天英", "elem": "Fire", "arch": "🌟 The Performer",
        "desc": "Meant to be seen and inspire. Natural charisma and gift of expression.",
        "str": ["Charisma", "Creativity", "Expression"], "ch": ["Attention-seeking", "Ego"],
        "career": "Entertainment, arts, marketing, media"}
}

DOOR_INFO = {
    "Open": {"cn": "开门", "elem": "Metal", "theme": "🚪 Leadership & New Beginnings",
        "gifts": ["Career advancement", "Leadership roles", "Official recognition"],
        "advice": "Step confidently into leadership. Doors open for you."},
    "Rest": {"cn": "休门", "elem": "Water", "theme": "🌊 Prosperity & Ease",
        "gifts": ["Wealth attraction", "Beneficial connections", "Passive income"],
        "advice": "Trust that support will come. Your network is your net worth."},
    "Life": {"cn": "生门", "elem": "Earth", "theme": "🌱 Growth & Wealth Creation",
        "gifts": ["Business success", "Wealth building", "Property acquisition"],
        "advice": "Create actively. Build and grow wealth through action."},
    "Harm": {"cn": "伤门", "elem": "Wood", "theme": "⚔️ Competition & Transformation",
        "gifts": ["Competitive success", "Breakthrough moments", "Transformation"],
        "advice": "Embrace challenges as growth. Become stronger through struggle."},
    "Delusion": {"cn": "杜门", "elem": "Wood", "theme": "🌫️ Strategy & Hidden Influence",
        "gifts": ["Strategic success", "Behind-the-scenes influence", "Intelligence"],
        "advice": "Use discretion as power. Not everything needs to be visible."},
    "Scenery": {"cn": "景门", "elem": "Fire", "theme": "🎭 Recognition & Expression",
        "gifts": ["Public recognition", "Artistic success", "Fame"],
        "advice": "Step into the spotlight. Destiny involves being seen."},
    "Death": {"cn": "死门", "elem": "Earth", "theme": "☯️ Transformation & Endings",
        "gifts": ["Deep transformation", "Completing cycles", "Spiritual work"],
        "advice": "Embrace endings as new beginnings."},
    "Fear": {"cn": "惊门", "elem": "Metal", "theme": "⚡ Awareness & Protection",
        "gifts": ["Legal success", "Crisis management", "Protection"],
        "advice": "Trust your instincts about danger."}
}

DEITY_INFO = {
    "Chief": {"cn": "值符", "gift": "Authority figures support you naturally."},
    "Serpent": {"cn": "腾蛇", "gift": "Strong intuition and psychic perception."},
    "Moon": {"cn": "太阴", "gift": "Hidden support and benefactors work for you."},
    "Six Harmony": {"cn": "六合", "gift": "Blessed in partnerships and relationships."},
    "Hook": {"cn": "勾陈", "gift": "Grounding force keeping you stable."},
    "Tiger": {"cn": "白虎", "gift": "Fierce protection and competitive edge."},
    "Emptiness": {"cn": "玄武", "gift": "Unconventional wisdom, see through deceptions."},
    "Nine Earth": {"cn": "九地", "gift": "Deep patience, outlast through persistence."},
    "Nine Heaven": {"cn": "九天", "gift": "Upward mobility, you naturally rise."}
}

BRANCH_PALACE = {"Zi":1,"Chou":8,"Yin":8,"Mao":3,"Chen":4,"Si":4,"Wu":9,"Wei":2,"Shen":2,"You":7,"Xu":6,"Hai":6}
BRANCHES = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]
PALACE_COMP = {1:("Canopy","Rest","Emptiness"),2:("Connect","Death","Nine Earth"),3:("Impulse","Harm","Six Harmony"),
    4:("Assistant","Delusion","Moon"),5:("Connect","Life","Hook"),6:("Heart","Open","Chief"),
    7:("Pillar","Fear","Tiger"),8:("Ren","Life","Nine Heaven"),9:("Hero","Scenery","Serpent")}

def get_branch(h): return "Zi" if h==23 else BRANCHES[((h+1)//2)%12]

def main():
    st.title("⭐ QMDJ Destiny Analysis")
    
    with st.sidebar:
        st.header("🎂 Birth Info")
        bazi = st.session_state.get("bazi_birth_info", {})
        if bazi:
            st.success("🔗 From BaZi")
            bd, bh = bazi.get("date", date(1978,6,27)), bazi.get("hour", 20)
        else:
            bd = st.date_input("Date", date(1978,6,27))
            bh = st.selectbox("Hour", range(24), 20)
        reveal = st.button("🔮 Reveal Destiny", type="primary", use_container_width=True)
    
    if reveal:
        p_num = BRANCH_PALACE.get(get_branch(bh), 6)
        star, door, deity = PALACE_COMP.get(p_num, ("Heart","Open","Chief"))
        p, s, d, de = PALACE_INFO[p_num], STAR_INFO[star], DOOR_INFO[door], DEITY_INFO[deity]
        
        # Header
        st.header("2️⃣ QI MEN DESTINY PALACE 奇门命宫")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"## P{p_num} {p['trigram']}\n### {p['name']}\n**{p['dir']} • {p['elem']}**")
            for row in [[4,9,2],[3,5,7],[8,1,6]]:
                cols = st.columns(3)
                for i,px in enumerate(row):
                    with cols[i]:
                        if px==p_num: st.success(f"**P{px}** ⭐")
                        else: st.info(f"P{px}")
        with c2:
            st.markdown(f"### {p['meaning']}\n\n{p['life_theme']}\n\n**Career:** {p['career']}\n\n**Challenge:** {p['challenge']}")
        
        st.divider()
        
        # Star
        st.header(f"⭐ NATAL STAR: {star} {s['cn']}")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"## {s['arch']}\n**{s['elem']}**")
            st.markdown("**Strengths:**")
            for x in s['str']: st.markdown(f"✅ {x}")
            st.markdown("**Challenges:**")
            for x in s['ch']: st.markdown(f"⚡ {x}")
        with c2:
            st.markdown(s['desc'])
            st.info(f"**Career:** {s['career']}")
        
        st.divider()
        
        # Door
        st.header(f"🚪 NATAL DOOR: {door} {d['cn']}")
        c1, c2 = st.columns([1,2])
        with c1:
            st.markdown(f"## {d['theme']}\n**{d['elem']}**")
            st.markdown("**Life Gifts:**")
            for x in d['gifts']: st.markdown(f"🎯 {x}")
        with c2:
            st.success(f"**Advice:** {d['advice']}")
        
        st.divider()
        
        # Deity
        st.header(f"👑 NATAL DEITY: {deity} {de['cn']}")
        st.info(f"**Spiritual Gift:** {de['gift']}")
        
        st.divider()
        
        # 2025 Annual
        st.header("9️⃣ 2025 LIFE PALACE 流年命宫")
        annual_p = 4  # Snake year
        st.markdown(f"**2025 activates Palace {annual_p} ({PALACE_INFO[annual_p]['name']})**")
        if p_num == annual_p:
            st.success("✅ Double Activation! Significant year for you!")
        else:
            st.info(f"Annual energy supports your natal palace P{p_num}")
        
        st.divider()
        
        # Summary
        st.header("🔮 SYNTHESIS")
        st.markdown(f"""
**Your Destiny Blueprint:**
- **Palace {p_num}** ({p['elem']}) = Your life arena
- **{star}** = Your personality archetype
- **{door}** = Your opportunity theme
- **{deity}** = Your spiritual backing

**Key Recommendations:**
1. Career: {s['career']}
2. Focus: {', '.join(d['gifts'])}
3. Direction: {p['dir']}
4. Element: {p['elem']}
""")
        
        if st.button("🤖 AI Prompt"):
            st.code(f"""QMDJ Destiny: {bd} at {bh}:00
Palace {p_num} - {p['name']} ({p['dir']}, {p['elem']})
Star: {star} {s['cn']} - {s['arch']}
Door: {door} {d['cn']} - {d['theme']}
Deity: {deity} {de['cn']}

Analyze destiny, life path, career, relationships, 2025 guidance.""")
    else:
        st.info("👈 Enter birth info and click **Reveal Destiny**")

if __name__ == "__main__":
    main()
