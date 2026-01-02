# pages/1_Chart.py - Ming QiMenDunJia v10.1 FIXED
import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(page_title="QMDJ Chart", page_icon="🎯", layout="wide")

# Constants
PALACE_INFO = {
    1: ("Kan 坎", "N", "Water"), 2: ("Kun 坤", "SW", "Earth"), 3: ("Zhen 震", "E", "Wood"),
    4: ("Xun 巽", "SE", "Wood"), 5: ("Center 中", "C", "Earth"), 6: ("Qian 乾", "NW", "Metal"),
    7: ("Dui 兑", "W", "Metal"), 8: ("Gen 艮", "NE", "Earth"), 9: ("Li 离", "S", "Fire")
}

STARS = {"Canopy": "天蓬", "Grass": "天芮", "Impulse": "天冲", "Assistant": "天辅", "Connect": "天禽",
         "Heart": "天心", "Pillar": "天柱", "Ren": "天任", "Hero": "天英"}

DOORS = {"Open": "开门", "Rest": "休门", "Life": "生门", "Harm": "伤门", "Delusion": "杜门",
         "Scenery": "景门", "Death": "死门", "Fear": "惊门"}

DEITIES = {"Chief": "值符", "Serpent": "腾蛇", "Moon": "太阴", "Six Harmony": "六合", "Hook": "勾陈",
           "Tiger": "白虎", "Emptiness": "玄武", "Nine Earth": "九地", "Nine Heaven": "九天"}

# Chart data by Ju number
JU_DATA = {
    1: {1:("Canopy","Rest","Emptiness"),2:("Connect","Death","Nine Earth"),3:("Heart","Harm","Six Harmony"),
        4:("Pillar","Delusion","Moon"),5:("Ren","Life","Hook"),6:("Hero","Open","Chief"),
        7:("Grass","Fear","Serpent"),8:("Impulse","Scenery","Nine Heaven"),9:("Assistant","Rest","Tiger")},
    2: {1:("Grass","Death","Nine Earth"),2:("Heart","Fear","Serpent"),3:("Pillar","Harm","Moon"),
        4:("Hero","Delusion","Six Harmony"),5:("Connect","Life","Hook"),6:("Impulse","Open","Tiger"),
        7:("Assistant","Rest","Chief"),8:("Canopy","Scenery","Emptiness"),9:("Ren","Rest","Nine Heaven")},
    3: {1:("Assistant","Open","Chief"),2:("Connect","Fear","Serpent"),3:("Heart","Life","Moon"),
        4:("Pillar","Rest","Six Harmony"),5:("Ren","Death","Hook"),6:("Hero","Harm","Tiger"),
        7:("Canopy","Delusion","Emptiness"),8:("Grass","Scenery","Nine Earth"),9:("Impulse","Open","Nine Heaven")},
    4: {1:("Heart","Life","Moon"),2:("Pillar","Death","Tiger"),3:("Hero","Harm","Serpent"),
        4:("Canopy","Delusion","Emptiness"),5:("Connect","Rest","Hook"),6:("Impulse","Open","Nine Heaven"),
        7:("Grass","Fear","Nine Earth"),8:("Ren","Scenery","Six Harmony"),9:("Assistant","Rest","Chief")},
    5: {1:("Pillar","Death","Tiger"),2:("Hero","Fear","Serpent"),3:("Canopy","Harm","Emptiness"),
        4:("Grass","Delusion","Nine Earth"),5:("Connect","Life","Hook"),6:("Ren","Open","Six Harmony"),
        7:("Assistant","Rest","Chief"),8:("Impulse","Scenery","Nine Heaven"),9:("Heart","Rest","Moon")},
    6: {1:("Hero","Harm","Serpent"),2:("Canopy","Death","Emptiness"),3:("Grass","Fear","Nine Earth"),
        4:("Ren","Delusion","Six Harmony"),5:("Connect","Life","Hook"),6:("Assistant","Open","Chief"),
        7:("Impulse","Rest","Nine Heaven"),8:("Heart","Scenery","Moon"),9:("Pillar","Rest","Tiger")},
    7: {1:("Canopy","Rest","Emptiness"),2:("Grass","Death","Nine Earth"),3:("Ren","Harm","Six Harmony"),
        4:("Assistant","Delusion","Chief"),5:("Connect","Life","Hook"),6:("Impulse","Open","Nine Heaven"),
        7:("Heart","Fear","Moon"),8:("Pillar","Scenery","Tiger"),9:("Hero","Rest","Serpent")},
    8: {1:("Grass","Death","Nine Earth"),2:("Ren","Fear","Six Harmony"),3:("Assistant","Harm","Chief"),
        4:("Impulse","Delusion","Nine Heaven"),5:("Connect","Life","Hook"),6:("Heart","Open","Moon"),
        7:("Pillar","Rest","Tiger"),8:("Hero","Scenery","Serpent"),9:("Canopy","Rest","Emptiness")},
    9: {1:("Ren","Harm","Six Harmony"),2:("Assistant","Death","Chief"),3:("Impulse","Fear","Nine Heaven"),
        4:("Heart","Delusion","Moon"),5:("Connect","Life","Hook"),6:("Pillar","Open","Tiger"),
        7:("Hero","Rest","Serpent"),8:("Canopy","Scenery","Emptiness"),9:("Grass","Rest","Nine Earth")}
}

def calc_ju(dt): return ((dt.timetuple().tm_yday + dt.hour) % 9) + 1
def get_structure(dt): return "Yang Dun" if (dt.month < 6 or (dt.month == 12 and dt.day >= 22)) else "Yin Dun"
def get_empty(dt): return [[3,8],[4,9],[2,7],[1,6],[3,4],[8,9],[2,3],[7,8],[1,2]][dt.timetuple().tm_yday % 9]
def get_horse(dt): return ((dt.hour // 2) % 9) + 1
def get_noble(dt): return [[2,8],[1,7],[3,9],[4,6],[2,8],[1,5],[3,7],[4,8],[5,9]][dt.day % 9]

# Main
st.title("🎯 QMDJ Chart")

with st.sidebar:
    st.header("⏰ Time")
    tz = pytz.timezone('Asia/Singapore')
    now = datetime.now(tz)
    use_now = st.checkbox("Use current time", True)
    if use_now:
        chart_date, chart_hour = now.date(), now.hour
        st.info(f"📍 {now.strftime('%Y-%m-%d %H:%M')}")
    else:
        chart_date = st.date_input("Date", now.date())
        chart_hour = st.selectbox("Hour", range(24), now.hour)
    gen = st.button("🔮 Generate", type="primary", use_container_width=True)

if gen or st.session_state.get("ok"):
    if gen:
        tz = pytz.timezone('Asia/Singapore')
        dt = tz.localize(datetime.combine(chart_date, datetime.min.time().replace(hour=chart_hour)))
        st.session_state.dt, st.session_state.ok = dt, True
    else:
        dt = st.session_state.dt
    
    ju = calc_ju(dt)
    data = JU_DATA.get(ju, JU_DATA[1])
    empty, horse, noble = get_empty(dt), get_horse(dt), get_noble(dt)
    
    st.markdown(f"### 📅 {dt.strftime('%Y-%m-%d %H:%M')}")
    c1,c2,c3 = st.columns(3)
    c1.metric("Structure", get_structure(dt))
    c2.metric("Ju", ju)
    c3.metric("Hour", f"{dt.hour:02d}:00")
    
    st.divider()
    if "sel" not in st.session_state: st.session_state.sel = 5
    
    st.subheader("🏯 Nine Palaces")
    for row in [[4,9,2],[3,5,7],[8,1,6]]:
        cols = st.columns(3)
        for i,p in enumerate(row):
            with cols[i]:
                name,dir,elem = PALACE_INFO[p]
                star,door,deity = data.get(p, ("?","?","?"))
                ind = ("🐴" if p==horse else "")+("👑" if p in noble else "")+("⭕" if p in empty else "")
                
                if st.button(f"P{p}"+(" ★" if p==st.session_state.sel else ""), key=f"p{p}", use_container_width=True):
                    st.session_state.sel = p
                
                if p==st.session_state.sel: st.success(f"**{name}**")
                elif p in empty: st.warning(f"**{name}**")
                else: st.info(f"**{name}**")
                st.caption(f"{elem} {ind}")
                st.caption(f"★{star} 🚪{door}")
    
    st.divider()
    sel = st.session_state.sel
    name,dir,elem = PALACE_INFO[sel]
    star,door,deity = data.get(sel, ("?","?","?"))
    
    st.subheader(f"🔍 Palace {sel}: {name}")
    if sel in empty: st.error("⭕ Death & Emptiness - delay if possible")
    if sel == horse: st.info("🐴 Horse Star - movement favored")
    if sel in noble: st.success("👑 Nobleman - helpful people appear")
    
    st.divider()
    st.subheader("📦 Components")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"#### ⭐ STAR")
        st.markdown(f"**{star}** {STARS.get(star,'')}")
    with c2:
        st.markdown(f"#### 🚪 DOOR")
        st.markdown(f"**{door}** {DOORS.get(door,'')}")
    with c3:
        st.markdown(f"#### 👑 DEITY")
        st.markdown(f"**{deity}** {DEITIES.get(deity,'')}")
else:
    st.info("👈 Click Generate")
