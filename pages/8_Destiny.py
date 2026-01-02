# pages/8_Destiny.py - Ming QiMenDunJia v10.1 FIXED
import streamlit as st
from datetime import date

st.set_page_config(page_title="Destiny", page_icon="⭐", layout="wide")

PALACE = {1:("Kan","N","Water"),2:("Kun","SW","Earth"),3:("Zhen","E","Wood"),4:("Xun","SE","Wood"),
          5:("Center","C","Earth"),6:("Qian","NW","Metal"),7:("Dui","W","Metal"),8:("Gen","NE","Earth"),9:("Li","S","Fire")}

STARS = {"Canopy":("天蓬","Water","The Strategist"), "Grass":("天芮","Earth","The Healer"),
         "Impulse":("天冲","Wood","The Pioneer"), "Assistant":("天辅","Wood","The Scholar"),
         "Connect":("天禽","Earth","The Connector"), "Heart":("天心","Metal","The Authority"),
         "Pillar":("天柱","Metal","The Critic"), "Ren":("天任","Earth","The Diplomat"), "Hero":("天英","Fire","The Performer")}

DOORS = {"Open":("开门","Metal","Leadership"), "Rest":("休门","Water","Prosperity"), "Life":("生门","Earth","Growth"),
         "Harm":("伤门","Wood","Competition"), "Delusion":("杜门","Wood","Strategy"), "Scenery":("景门","Fire","Recognition"),
         "Death":("死门","Earth","Transformation"), "Fear":("惊门","Metal","Awareness")}

DEITIES = {"Chief":("值符","Authority backing"), "Serpent":("腾蛇","Strong intuition"), "Moon":("太阴","Hidden support"),
           "Six Harmony":("六合","Relationship blessing"), "Hook":("勾陈","Grounding force"), "Tiger":("白虎","Fierce protection"),
           "Emptiness":("玄武","Hidden wisdom"), "Nine Earth":("九地","Deep patience"), "Nine Heaven":("九天","Upward ambition")}

COMP = {1:("Canopy","Rest","Emptiness"),2:("Connect","Death","Nine Earth"),3:("Impulse","Harm","Six Harmony"),
        4:("Assistant","Delusion","Moon"),5:("Connect","Life","Hook"),6:("Heart","Open","Chief"),
        7:("Pillar","Fear","Tiger"),8:("Ren","Life","Nine Heaven"),9:("Hero","Scenery","Serpent")}

BRANCH_P = {"Zi":1,"Chou":8,"Yin":8,"Mao":3,"Chen":4,"Si":4,"Wu":9,"Wei":2,"Shen":2,"You":7,"Xu":6,"Hai":6}
BRANCHES = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]

def get_branch(h): return "Zi" if h==23 else BRANCHES[((h+1)//2)%12]

st.title("⭐ QMDJ Destiny")

with st.sidebar:
    st.header("🎂 Birth Info")
    bazi = st.session_state.get("bazi_birth_info",{})
    if bazi:
        st.success("🔗 From BaZi")
        bd = bazi.get("date", date(1990,1,1))
        bh = bazi.get("hour", 12)
    else:
        bd = st.date_input("Date", date(1990,1,1))
        bh = st.selectbox("Hour", range(24), 12)
    
    go = st.button("🔮 Reveal", type="primary", use_container_width=True)

if go:
    branch = get_branch(bh)
    p = BRANCH_P.get(branch, 6)
    star,door,deity = COMP.get(p, ("Heart","Open","Chief"))
    pn,pd,pe = PALACE[p]
    
    st.markdown(f"### 🏯 Birth: {bd} at {bh:02d}:00")
    c1,c2,c3 = st.columns(3)
    c1.metric("Palace", f"P{p}")
    c2.metric("Direction", pd)
    c3.metric("Element", pe)
    
    st.divider()
    st.subheader("🏯 Your Birth Palace")
    for row in [[4,9,2],[3,5,7],[8,1,6]]:
        cols = st.columns(3)
        for i,px in enumerate(row):
            with cols[i]:
                if px==p: st.success(f"**P{px}** ⭐ YOU")
                else: st.info(f"**P{px}**")
    
    st.divider()
    st.subheader("🌟 Your Components")
    
    st.markdown("---")
    scn,selem,sarch = STARS.get(star, ("?","?","?"))
    st.markdown(f"### ⭐ NATAL STAR: {star} {scn}")
    st.markdown(f"**\"{sarch}\"** • Element: {selem}")
    
    st.markdown("---")
    dcn,delem,dtheme = DOORS.get(door, ("?","?","?"))
    st.markdown(f"### 🚪 NATAL DOOR: {door} {dcn}")
    st.markdown(f"**\"{dtheme}\"** • Element: {delem}")
    
    st.markdown("---")
    decn,debrief = DEITIES.get(deity, ("?","?"))
    st.markdown(f"### 👑 NATAL DEITY: {deity} {decn}")
    st.info(debrief)
    
    st.divider()
    if st.button("🤖 AI Prompt"):
        st.code(f"""QMDJ Destiny: Birth {bd} at {bh:02d}:00
Palace {p} - {pn} ({pd}, {pe})
Star: {star} {scn} ({selem}) - {sarch}
Door: {door} {dcn} ({delem}) - {dtheme}  
Deity: {deity} {decn} - {debrief}

Analyze personality, life path, and advice.""")
else:
    st.info("👈 Enter birth info and click Reveal")
