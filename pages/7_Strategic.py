# Ming QiMenDunJia v8.0 - Strategic Execution Mode (Hybrid)
# pages/7_Strategic.py
"""
STRATEGIC EXECUTION MODE (战略执行) - HYBRID

Find optimal timing and direction for your actions.
- Shows useful quick insights (WHAT + brief WHY)
- "Analyze with AI" button for deep personalized analysis
"""

import streamlit as st
from datetime import datetime, timedelta
import pytz
import json

# Import from core modules
import sys
sys.path.insert(0, '..')

try:
    from core.qmdj_engine import (
        generate_qmdj_chart, calculate_qmdj_pillars,
        calculate_death_emptiness, calculate_horse_star,
        calculate_nobleman, calculate_lead_indicators,
        PALACE_INFO, SGT
    )
    from core.formations import (
        detect_formations, get_formation_score,
        format_formation_display, FormationCategory
    )
    IMPORTS_OK = True
except ImportError:
    IMPORTS_OK = False


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Strategic Execution | Ming Qimen",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0a1628; }
    .golden-card {
        background: linear-gradient(135deg, #1a2744 0%, #0d1829 100%);
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    .hour-card {
        background: #1a2744;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #4a5568;
    }
    .hour-good { border-left-color: #48bb78 !important; }
    .hour-bad { border-left-color: #f56565 !important; }
    .hour-golden { 
        border-left-color: #FFD700 !important;
        border: 2px solid #FFD700;
        background: linear-gradient(135deg, #1a2744 0%, #2d3748 100%);
    }
    .dir-cell {
        background: #1a2744;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        border: 1px solid #2d3748;
    }
    .dir-good { border-color: #48bb78; background: #1a3728; }
    .dir-bad { border-color: #f56565; background: #371a1a; }
    .insight-box {
        background: #1a2744;
        border-left: 3px solid #4299e1;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9em;
    }
    .ai-button {
        background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%);
        border: none;
        border-radius: 8px;
        padding: 15px 25px;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CONSTANTS & BRIEF INSIGHTS
# =============================================================================

CHINESE_HOURS = [
    ("Zi", "子", "23:00-01:00", "Rat"),
    ("Chou", "丑", "01:00-03:00", "Ox"),
    ("Yin", "寅", "03:00-05:00", "Tiger"),
    ("Mao", "卯", "05:00-07:00", "Rabbit"),
    ("Chen", "辰", "07:00-09:00", "Dragon"),
    ("Si", "巳", "09:00-11:00", "Snake"),
    ("Wu", "午", "11:00-13:00", "Horse"),
    ("Wei", "未", "13:00-15:00", "Goat"),
    ("Shen", "申", "15:00-17:00", "Monkey"),
    ("You", "酉", "17:00-19:00", "Rooster"),
    ("Xu", "戌", "19:00-21:00", "Dog"),
    ("Hai", "亥", "21:00-23:00", "Pig")
]

ACTIVITY_TYPES = {
    "💼 Business Meeting": {"palace": 6, "doors": ["Open", "Rest"], "desc": "Authority, negotiations"},
    "📝 Sign Contract": {"palace": 6, "doors": ["Open", "Life"], "desc": "Binding agreements"},
    "💰 Investment": {"palace": 4, "doors": ["Life", "Open"], "desc": "Wealth growth"},
    "💕 Dating/Romance": {"palace": 2, "doors": ["Rest", "Scenery"], "desc": "Relationships, connection"},
    "📚 Study/Exam": {"palace": 8, "doors": ["Scenery", "Life"], "desc": "Learning, recognition"},
    "✈️ Travel": {"palace": 1, "doors": ["Open", "Rest"], "desc": "Movement, journeys"},
    "🏥 Medical Visit": {"palace": 3, "doors": ["Life", "Rest"], "desc": "Health matters"},
    "🏠 Property Deal": {"palace": 8, "doors": ["Life", "Open"], "desc": "Real estate, stability"},
    "⚖️ Legal Matter": {"palace": 6, "doors": ["Open"], "desc": "Official processes"},
    "🎯 General Action": {"palace": 5, "doors": ["Open", "Life", "Rest"], "desc": "Any activity"}
}

# Brief door meanings (not full interpretations)
DOOR_INSIGHTS = {
    "Open": ("✨", "Opens opportunities, authority support"),
    "Rest": ("💤", "Ease, networking, passive gains"),
    "Life": ("🌱", "Growth, creation, wealth building"),
    "Harm": ("⚔️", "Competition, conflict, breakthroughs"),
    "Delusion": ("🌫️", "Hidden matters, strategy, secrecy"),
    "Scenery": ("🎭", "Recognition, expression, visibility"),
    "Death": ("💀", "Endings, stagnation - avoid new starts"),
    "Fear": ("⚡", "Surprises, legal issues, alertness")
}

DIRECTIONS = [
    ("N", "North", 1), ("NE", "Northeast", 8), ("E", "East", 3),
    ("SE", "Southeast", 4), ("S", "South", 9), ("SW", "Southwest", 2),
    ("W", "West", 7), ("NW", "Northwest", 6)
]


# =============================================================================
# SCORING WITH INSIGHTS
# =============================================================================

def score_hour(hour_dt: datetime, activity: str, user_profile: dict = None) -> dict:
    """Score an hour with brief insights explaining why."""
    if not IMPORTS_OK:
        import random
        return {
            "score": random.randint(3, 8),
            "door": "Open", "star": "Heart", "deity": "Chief",
            "formations": [], "insights": ["Demo mode - install core modules"],
            "verdict": "neutral"
        }
    
    try:
        chart = generate_qmdj_chart(hour_dt)
        activity_info = ACTIVITY_TYPES.get(activity, ACTIVITY_TYPES["🎯 General Action"])
        target_palace = activity_info["palace"]
        palace_data = chart.get("palaces", {}).get(str(target_palace), {})
        
        score = 5
        insights = []
        
        # Door analysis with insight
        door = palace_data.get("door", "")
        door_emoji, door_meaning = DOOR_INSIGHTS.get(door, ("", ""))
        
        if door in activity_info["doors"]:
            score += 2
            insights.append(f"{door_emoji} {door} Door favors this activity")
        elif door in ["Death", "Harm", "Fear"]:
            score -= 2
            insights.append(f"{door_emoji} {door} Door: {door_meaning}")
        else:
            insights.append(f"{door_emoji} {door} Door: {door_meaning}")
        
        # Formation detection with names
        formations = detect_formations(palace_data)
        f_score, _ = get_formation_score(formations)
        score += f_score
        
        formation_names = []
        for f in formations:
            if f.category == FormationCategory.AUSPICIOUS:
                formation_names.append(f"✨ {f.name_en}")
            elif f.category == FormationCategory.INAUSPICIOUS:
                formation_names.append(f"⚠️ {f.name_en}")
            else:
                formation_names.append(f"📜 {f.name_en}")
        
        if formation_names:
            insights.append(f"Formations: {', '.join(formation_names[:3])}")
        
        # Death & Emptiness
        if palace_data.get("death_emptiness", False):
            score -= 2
            insights.append("💀 Palace in Death & Emptiness - energy blocked")
        
        # Horse Star
        if palace_data.get("has_horse", False):
            if "Travel" in activity:
                score += 1
                insights.append("🐴 Horse Star activates - good for movement")
            else:
                insights.append("🐴 Horse Star present - things move fast")
        
        # Nobleman
        if palace_data.get("has_nobleman", False):
            score += 1
            insights.append("👑 Nobleman arrives - helpful people appear")
        
        # BaZi alignment
        if user_profile:
            useful_gods = user_profile.get("useful_gods", [])
            palace_element = palace_data.get("palace_element", "")
            if palace_element in useful_gods:
                score += 1
                insights.append(f"🎴 Palace {palace_element} aligns with your BaZi")
        
        score = max(1, min(10, score))
        
        # Determine verdict
        if score >= 7:
            verdict = "good"
        elif score <= 3:
            verdict = "bad"
        else:
            verdict = "neutral"
        
        return {
            "score": score,
            "door": door,
            "star": palace_data.get("star", ""),
            "deity": palace_data.get("deity", ""),
            "heaven_stem": palace_data.get("heaven_stem", ""),
            "formations": [f.name_en for f in formations],
            "formation_categories": [f.category.value for f in formations],
            "insights": insights,
            "verdict": verdict,
            "palace_data": palace_data
        }
    except Exception as e:
        return {"score": 5, "door": "?", "star": "?", "deity": "?", "insights": [str(e)[:50]], "verdict": "neutral"}


def score_direction(chart: dict, direction: str, palace_num: int) -> dict:
    """Score a direction with brief insight."""
    if not chart:
        return {"score": 5, "verdict": "neutral", "door": "?", "insight": "No data"}
    
    palace_data = chart.get("palaces", {}).get(str(palace_num), {})
    door = palace_data.get("door", "")
    door_emoji, door_meaning = DOOR_INSIGHTS.get(door, ("", "Unknown"))
    
    score = 5
    if door in ["Open", "Life", "Rest"]:
        score = 7
        verdict = "good"
    elif door in ["Death", "Harm", "Fear"]:
        score = 3
        verdict = "bad"
    else:
        verdict = "neutral"
    
    if palace_data.get("death_emptiness", False):
        score -= 2
        verdict = "bad"
    
    # Check for formations
    formations = detect_formations(palace_data) if IMPORTS_OK else []
    if formations:
        auspicious = sum(1 for f in formations if f.category == FormationCategory.AUSPICIOUS)
        if auspicious > 0:
            score += 1
    
    return {
        "score": max(1, min(10, score)), 
        "verdict": verdict, 
        "door": door,
        "insight": f"{door_emoji} {door_meaning}"
    }


# =============================================================================
# AI ANALYSIS PROMPT GENERATOR
# =============================================================================

def generate_ai_prompt(date_str: str, activity: str, hour_results: list, direction_scores: dict, user_profile: dict, golden_hour: dict) -> str:
    """Generate a ready-to-paste prompt for Claude."""
    
    # Build hour summary
    top_hours = sorted(hour_results, key=lambda x: x["score"], reverse=True)[:3]
    worst_hours = sorted(hour_results, key=lambda x: x["score"])[:2]
    
    top_hours_text = "\n".join([
        f"  - {h['hour_name']} ({h['time_range']}): Score {h['score']}/10, {h['door']} Door, {h['star']} Star"
        for h in top_hours
    ])
    
    worst_hours_text = "\n".join([
        f"  - {h['hour_name']} ({h['time_range']}): Score {h['score']}/10, {h['door']} Door"
        for h in worst_hours
    ])
    
    # Build direction summary
    good_dirs = [f"{d} ({v['door']})" for d, v in direction_scores.items() if v["verdict"] == "good"]
    bad_dirs = [f"{d} ({v['door']})" for d, v in direction_scores.items() if v["verdict"] == "bad"]
    
    # Build BaZi context
    bazi_text = ""
    if user_profile:
        bazi_text = f"""
User's BaZi Profile:
- Day Master: {user_profile.get('day_master', 'Unknown')} ({user_profile.get('element', '?')})
- Strength: {user_profile.get('strength', 'Unknown')}
- Useful Gods: {', '.join(user_profile.get('useful_gods', []))}
- Profile: {user_profile.get('profile', 'Unknown')}
"""
    
    # Build formations found
    all_formations = []
    for h in hour_results:
        all_formations.extend(h.get("formations", []))
    unique_formations = list(set(all_formations))
    
    prompt = f"""Analyze this Qi Men Dun Jia strategic execution scan:

**Date:** {date_str}
**Activity:** {activity}
**Target Palace:** P{ACTIVITY_TYPES.get(activity, {}).get('palace', 5)}

**Golden Hour:** {golden_hour['hour_name']} ({golden_hour['time_range']})
- Score: {golden_hour['score']}/10
- Door: {golden_hour['door']} | Star: {golden_hour['star']} | Deity: {golden_hour['deity']}
- Formations: {', '.join(golden_hour.get('formations', [])) or 'None'}

**Top 3 Hours:**
{top_hours_text}

**Hours to Avoid:**
{worst_hours_text}

**Directions (from Golden Hour chart):**
- Go: {', '.join(good_dirs) if good_dirs else 'None outstanding'}
- Avoid: {', '.join(bad_dirs) if bad_dirs else 'None critical'}

**Formations Detected:** {', '.join(unique_formations[:5]) if unique_formations else 'None'}
{bazi_text}
---

Please provide:
1. **Why** the Golden Hour is optimal for this activity (explain the door/star/deity combination)
2. **Formation analysis** if any formations are present
3. **Direction recommendation** with reasoning
4. **Timing strategy** - what to do/avoid during the recommended hour
5. **BaZi personalization** if profile is provided

Reference #71 Sun Tzu's Art of War QMDJ principles where applicable."""

    return prompt


# =============================================================================
# MAIN PAGE
# =============================================================================

def main():
    st.title("🎯 Strategic Execution")
    st.caption("Find optimal timing • Get AI-powered deep analysis")
    
    # Sidebar
    with st.sidebar:
        st.header("📅 Parameters")
        
        selected_date = st.date_input(
            "Date",
            value=datetime.now(pytz.timezone('Asia/Singapore')).date()
        )
        
        activity = st.selectbox("Activity", options=list(ACTIVITY_TYPES.keys()))
        activity_desc = ACTIVITY_TYPES[activity]["desc"]
        st.caption(f"*{activity_desc}*")
        
        st.divider()
        
        # BaZi profile
        profile = st.session_state.get("user_profile", None)
        if profile:
            st.success(f"✓ {profile.get('day_master', '?')} Day Master")
            st.caption(f"Useful: {', '.join(profile.get('useful_gods', []))}")
            use_bazi = st.checkbox("Apply BaZi alignment", value=True)
        else:
            st.caption("No BaZi profile • Go to Settings")
            use_bazi = False
            profile = None
        
        st.divider()
        scan_btn = st.button("🔍 Scan Day", type="primary", use_container_width=True)
    
    # Initialize session state
    if "scan_results" not in st.session_state:
        st.session_state.scan_results = None
    
    # Main content
    if scan_btn:
        tz = pytz.timezone('Asia/Singapore')
        
        # Scan hours
        hour_results = []
        for hour_name, hour_cn, time_range, animal in CHINESE_HOURS:
            start_hour = int(time_range.split(":")[0])
            if start_hour == 23:
                hour_dt = tz.localize(datetime.combine(selected_date - timedelta(days=1), datetime.min.time().replace(hour=23)))
            else:
                hour_dt = tz.localize(datetime.combine(selected_date, datetime.min.time().replace(hour=start_hour)))
            
            result = score_hour(hour_dt, activity, profile if use_bazi else None)
            result["hour_name"] = f"{hour_name} {hour_cn}"
            result["time_range"] = time_range
            result["hour_dt"] = hour_dt
            hour_results.append(result)
        
        # Sort and find golden hour
        sorted_hours = sorted(hour_results, key=lambda x: x["score"], reverse=True)
        golden = sorted_hours[0]
        
        # Get direction scores for golden hour
        if IMPORTS_OK:
            chart = generate_qmdj_chart(golden["hour_dt"])
        else:
            chart = None
        
        direction_scores = {}
        for d, name, palace in DIRECTIONS:
            direction_scores[d] = score_direction(chart, d, palace)
        
        # Store results
        st.session_state.scan_results = {
            "date": selected_date,
            "activity": activity,
            "hour_results": hour_results,
            "sorted_hours": sorted_hours,
            "golden": golden,
            "direction_scores": direction_scores,
            "profile": profile if use_bazi else None
        }
    
    # Display results if available
    if st.session_state.scan_results:
        results = st.session_state.scan_results
        golden = results["golden"]
        sorted_hours = results["sorted_hours"]
        direction_scores = results["direction_scores"]
        
        st.markdown(f"### 📊 Results for {results['date'].strftime('%B %d, %Y')}")
        st.caption(f"Activity: {results['activity']}")
        
        # Golden Hour Card
        st.markdown(f"""
        <div class="golden-card">
            <div style="color: #FFD700; font-size: 1.3em; font-weight: bold;">
                ⭐ Golden Hour: {golden['hour_name']} ({golden['time_range']})
            </div>
            <div style="color: #48bb78; font-size: 2em; margin: 10px 0;">{golden['score']}/10</div>
            <div style="color: #a0aec0; margin-bottom: 10px;">
                {golden['door']} Door • {golden['star']} Star • {golden['deity']} Deity
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Insights for Golden Hour
        if golden.get("insights"):
            st.markdown("**Quick Insights:**")
            for insight in golden["insights"][:4]:
                st.markdown(f"""<div class="insight-box">{insight}</div>""", unsafe_allow_html=True)
        
        st.divider()
        
        # Hour Rankings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Best Hours**")
            for h in sorted_hours[:4]:
                cls = "hour-golden" if h == golden else "hour-good" if h["score"] >= 6 else ""
                formations_str = f" • 📜 {len(h.get('formations', []))}" if h.get('formations') else ""
                
                st.markdown(f"""
                <div class="hour-card {cls}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><b>{h['hour_name']}</b> <span style="color: #718096;">({h['time_range']})</span></span>
                        <span style="color: #48bb78; font-size: 1.3em; font-weight: bold;">{h['score']}/10</span>
                    </div>
                    <div style="color: #a0aec0; font-size: 0.9em; margin-top: 5px;">
                        {h['door']} • {h['star']}{formations_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**⚠️ Avoid Hours**")
            for h in sorted_hours[-4:]:
                st.markdown(f"""
                <div class="hour-card hour-bad">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span><b>{h['hour_name']}</b> <span style="color: #718096;">({h['time_range']})</span></span>
                        <span style="color: #f56565; font-size: 1.3em; font-weight: bold;">{h['score']}/10</span>
                    </div>
                    <div style="color: #a0aec0; font-size: 0.9em; margin-top: 5px;">
                        {h['door']} Door - {DOOR_INSIGHTS.get(h['door'], ('',''))[1][:30]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Direction Compass
        st.subheader("🧭 Direction Analysis")
        st.caption(f"Based on Golden Hour ({golden['hour_name']}) chart")
        
        grid = [
            [("SE", 4), ("S", 9), ("SW", 2)],
            [("E", 3), ("CENTER", 5), ("W", 7)],
            [("NE", 8), ("N", 1), ("NW", 6)]
        ]
        
        for row in grid:
            cols = st.columns(3)
            for idx, (d, p) in enumerate(row):
                with cols[idx]:
                    if d == "CENTER":
                        st.markdown("""
                        <div class="dir-cell" style="background: #2d3748;">
                            <div style="color: #FFD700;">🏠 YOU</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        data = direction_scores[d]
                        cls = "dir-good" if data["verdict"] == "good" else "dir-bad" if data["verdict"] == "bad" else ""
                        emoji = "✅" if data["verdict"] == "good" else "⚠️" if data["verdict"] == "bad" else "⚖️"
                        st.markdown(f"""
                        <div class="dir-cell {cls}">
                            <div style="color: #FFD700; font-weight: bold;">{d}</div>
                            <div>{emoji} {data['score']}/10</div>
                            <div style="color: #718096; font-size: 0.75em;">{data['door']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Direction Summary
        good_dirs = [d for d, v in direction_scores.items() if v["verdict"] == "good"]
        bad_dirs = [d for d, v in direction_scores.items() if v["verdict"] == "bad"]
        
        col1, col2 = st.columns(2)
        with col1:
            if good_dirs:
                st.success(f"✅ Go: {', '.join(good_dirs)}")
                for d in good_dirs[:2]:
                    st.caption(f"  {d}: {direction_scores[d]['insight']}")
        with col2:
            if bad_dirs:
                st.error(f"⚠️ Avoid: {', '.join(bad_dirs)}")
                for d in bad_dirs[:2]:
                    st.caption(f"  {d}: {direction_scores[d]['insight']}")
        
        # =================================================================
        # AI ANALYSIS BUTTON
        # =================================================================
        st.divider()
        st.subheader("🤖 Get Deep Analysis")
        
        ai_prompt = generate_ai_prompt(
            results['date'].strftime("%Y-%m-%d"),
            results['activity'],
            results['hour_results'],
            direction_scores,
            results['profile'],
            golden
        )
        
        st.markdown("""
        Get personalized interpretation explaining **WHY** these hours and directions 
        are optimal for your activity, with formation analysis and BaZi alignment.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("📋 Copy Analysis Prompt", type="primary", use_container_width=True):
                st.session_state.show_prompt = True
        
        with col2:
            st.download_button(
                "💾 Save as TXT",
                ai_prompt,
                file_name=f"strategic_{results['date'].strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        if st.session_state.get("show_prompt", False):
            st.code(ai_prompt, language="markdown")
            st.info("👆 Copy this prompt and paste it to Claude for deep analysis")
        
        # Also offer JSON export
        with st.expander("📊 Export Raw Data (JSON)"):
            export_data = {
                "date": results['date'].strftime("%Y-%m-%d"),
                "activity": results['activity'],
                "golden_hour": {
                    "name": golden['hour_name'],
                    "time": golden['time_range'],
                    "score": golden['score'],
                    "door": golden['door'],
                    "star": golden['star'],
                    "deity": golden['deity'],
                    "formations": golden.get('formations', [])
                },
                "all_hours": [
                    {"hour": h['hour_name'], "score": h['score'], "door": h['door']}
                    for h in sorted_hours
                ],
                "directions": {d: {"score": v['score'], "verdict": v['verdict'], "door": v['door']} 
                              for d, v in direction_scores.items()},
                "user_bazi": results['profile']
            }
            st.json(export_data)
    
    else:
        # Placeholder
        st.info("👈 Select date and activity, then click **Scan Day**")
        
        st.markdown("""
        ### What You'll Get
        
        **Quick Insights (App):**
        - Hour scores with brief explanations
        - Formation detection
        - Direction recommendations
        - BaZi alignment indicators
        
        **Deep Analysis (AI):**
        - Full explanation of WHY hours are optimal
        - Formation meanings and implications
        - Personalized strategy based on your BaZi
        - Book references (#71 Sun Tzu principles)
        """)


if __name__ == "__main__":
    main()
