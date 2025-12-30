# Ming QiMenDunJia v8.0 - Strategic Execution Mode (Tiered)
# pages/7_Strategic.py
"""
STRATEGIC EXECUTION MODE (战略执行) - QUICK TIER

Find optimal timing and direction for your actions.
- Shows WHAT (scores, rankings, verdicts)
- For WHY (deep analysis), export to Project 1 (AI Analyst)
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
        padding: 12px;
        margin: 5px 0;
        border-left: 4px solid #4a5568;
    }
    .hour-good { border-left-color: #48bb78 !important; }
    .hour-bad { border-left-color: #f56565 !important; }
    .hour-golden { 
        border-left-color: #FFD700 !important;
        border: 2px solid #FFD700;
    }
    .direction-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin: 10px 0;
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
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CONSTANTS
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
    "💼 Business Meeting": {"palace": 6, "doors": ["Open", "Rest"]},
    "📝 Sign Contract": {"palace": 6, "doors": ["Open", "Life"]},
    "💰 Investment": {"palace": 4, "doors": ["Life", "Open"]},
    "💕 Dating/Romance": {"palace": 2, "doors": ["Rest", "Scenery"]},
    "📚 Study/Exam": {"palace": 8, "doors": ["Scenery", "Life"]},
    "✈️ Travel": {"palace": 1, "doors": ["Open", "Rest"]},
    "🏥 Medical Visit": {"palace": 3, "doors": ["Life", "Rest"]},
    "🏠 Property Deal": {"palace": 8, "doors": ["Life", "Open"]},
    "⚖️ Legal Matter": {"palace": 6, "doors": ["Open"]},
    "🎯 General Action": {"palace": 5, "doors": ["Open", "Life", "Rest"]}
}

DIRECTIONS = [
    ("N", "North", 1), ("NE", "Northeast", 8), ("E", "East", 3),
    ("SE", "Southeast", 4), ("S", "South", 9), ("SW", "Southwest", 2),
    ("W", "West", 7), ("NW", "Northwest", 6)
]


# =============================================================================
# SCORING FUNCTIONS (Simplified output)
# =============================================================================

def score_hour(hour_dt: datetime, activity: str, user_profile: dict = None) -> dict:
    """Score an hour - returns score + key indicators only."""
    if not IMPORTS_OK:
        import random
        return {
            "score": random.randint(3, 8),
            "door": "Open", "star": "Heart", "deity": "Chief",
            "formation_count": 0, "formation_type": "neutral",
            "flags": ["Demo mode"]
        }
    
    try:
        chart = generate_qmdj_chart(hour_dt)
        activity_info = ACTIVITY_TYPES.get(activity, ACTIVITY_TYPES["🎯 General Action"])
        target_palace = activity_info["palace"]
        palace_data = chart.get("palaces", {}).get(str(target_palace), {})
        
        score = 5
        flags = []
        
        # Door check
        door = palace_data.get("door", "")
        if door in activity_info["doors"]:
            score += 2
            flags.append(f"✓ {door}")
        elif door in ["Death", "Harm", "Fear"]:
            score -= 2
            flags.append(f"✗ {door}")
        
        # Formation check
        formations = detect_formations(palace_data)
        f_score, _ = get_formation_score(formations)
        score += f_score
        
        auspicious_count = sum(1 for f in formations if f.category == FormationCategory.AUSPICIOUS)
        inauspicious_count = sum(1 for f in formations if f.category == FormationCategory.INAUSPICIOUS)
        
        if auspicious_count > 0:
            flags.append(f"📜+{auspicious_count}")
        if inauspicious_count > 0:
            flags.append(f"📜-{inauspicious_count}")
        
        # Death & Emptiness
        if palace_data.get("death_emptiness", False):
            score -= 2
            flags.append("💀")
        
        # Horse Star
        if palace_data.get("has_horse", False) and "Travel" in activity:
            score += 1
            flags.append("🐴")
        
        # Nobleman
        if palace_data.get("has_nobleman", False):
            score += 1
            flags.append("👑")
        
        # BaZi alignment
        if user_profile:
            useful_gods = user_profile.get("useful_gods", [])
            palace_element = palace_data.get("palace_element", "")
            if palace_element in useful_gods:
                score += 1
                flags.append("🎴")
        
        score = max(1, min(10, score))
        
        return {
            "score": score,
            "door": door,
            "star": palace_data.get("star", ""),
            "deity": palace_data.get("deity", ""),
            "formation_count": len(formations),
            "formation_type": "good" if auspicious_count > inauspicious_count else "bad" if inauspicious_count > auspicious_count else "neutral",
            "flags": flags,
            "palace_data": palace_data
        }
    except Exception as e:
        return {"score": 5, "door": "?", "star": "?", "deity": "?", "flags": [str(e)[:20]]}


def score_direction(chart: dict, direction: str, palace_num: int) -> dict:
    """Score a direction - simple good/neutral/bad."""
    if not chart:
        return {"score": 5, "verdict": "neutral", "door": "?"}
    
    palace_data = chart.get("palaces", {}).get(str(palace_num), {})
    door = palace_data.get("door", "")
    
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
    
    return {"score": max(1, min(10, score)), "verdict": verdict, "door": door}


# =============================================================================
# EXPORT FOR PROJECT 1
# =============================================================================

def generate_export_data(date_str: str, activity: str, hour_results: list, direction_scores: dict, user_profile: dict) -> dict:
    """Generate JSON for Project 1 (AI Analyst) deep analysis."""
    return {
        "analysis_type": "STRATEGIC_EXECUTION",
        "request": {
            "date": date_str,
            "activity": activity,
            "user_bazi": user_profile
        },
        "hour_scan": [
            {
                "hour": r["hour_name"],
                "time": r["time_range"],
                "score": r["score"],
                "door": r["door"],
                "star": r["star"],
                "deity": r["deity"],
                "flags": r["flags"]
            }
            for r in hour_results
        ],
        "direction_scan": {
            d: {"score": v["score"], "verdict": v["verdict"], "door": v["door"]}
            for d, v in direction_scores.items()
        },
        "top_3_hours": [
            {"hour": h["hour_name"], "score": h["score"], "door": h["door"]}
            for h in sorted(hour_results, key=lambda x: x["score"], reverse=True)[:3]
        ],
        "instruction": "Analyze this strategic execution scan. Explain WHY each hour/direction scored as it did. Provide personalized recommendations based on user's BaZi profile. Reference #71 Sun Tzu principles where applicable."
    }


# =============================================================================
# MAIN PAGE
# =============================================================================

def main():
    st.title("🎯 Strategic Execution")
    st.caption("Quick scan for optimal timing • Export to AI for deep analysis")
    
    # Sidebar
    with st.sidebar:
        st.header("📅 Parameters")
        
        selected_date = st.date_input(
            "Date",
            value=datetime.now(pytz.timezone('Asia/Singapore')).date()
        )
        
        activity = st.selectbox("Activity", options=list(ACTIVITY_TYPES.keys()))
        
        st.divider()
        
        # BaZi profile
        profile = st.session_state.get("user_profile", None)
        if profile:
            st.success(f"✓ {profile.get('day_master', '?')} Day Master")
            use_bazi = st.checkbox("Apply BaZi", value=True)
        else:
            st.caption("No BaZi profile • Go to Settings")
            use_bazi = False
            profile = None
        
        st.divider()
        scan_btn = st.button("🔍 Scan Day", type="primary", use_container_width=True)
    
    # Main content
    if scan_btn:
        tz = pytz.timezone('Asia/Singapore')
        
        # Scan hours
        st.subheader(f"⏰ {selected_date.strftime('%b %d')} Hour Scan")
        
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
            hour_results.append(result)
        
        # Sort by score
        sorted_hours = sorted(hour_results, key=lambda x: x["score"], reverse=True)
        golden = sorted_hours[0]
        
        # Golden Hour Card
        st.markdown(f"""
        <div class="golden-card">
            <div style="color: #FFD700; font-size: 1.4em; font-weight: bold;">
                ⭐ Golden Hour: {golden['hour_name']} ({golden['time_range']})
            </div>
            <div style="color: #48bb78; font-size: 1.8em; margin: 10px 0;">{golden['score']}/10</div>
            <div style="color: #a0aec0;">{' '.join(golden['flags'])}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hour Rankings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Best Hours**")
            for h in sorted_hours[:4]:
                cls = "hour-golden" if h == golden else "hour-good" if h["score"] >= 6 else ""
                st.markdown(f"""
                <div class="hour-card {cls}">
                    <b>{h['hour_name']}</b> <span style="color: #718096;">({h['time_range']})</span><br/>
                    <span style="color: #48bb78; font-size: 1.2em;">{h['score']}/10</span>
                    <span style="color: #a0aec0; margin-left: 10px;">{' '.join(h['flags'])}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**⚠️ Avoid Hours**")
            for h in sorted_hours[-4:]:
                st.markdown(f"""
                <div class="hour-card hour-bad">
                    <b>{h['hour_name']}</b> <span style="color: #718096;">({h['time_range']})</span><br/>
                    <span style="color: #f56565; font-size: 1.2em;">{h['score']}/10</span>
                    <span style="color: #a0aec0; margin-left: 10px;">{' '.join(h['flags'])}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Direction Compass
        st.subheader("🧭 Direction Quick Scan")
        
        # Get chart for golden hour
        if IMPORTS_OK:
            start_hour = int(golden['time_range'].split(":")[0])
            if start_hour == 23:
                golden_dt = tz.localize(datetime.combine(selected_date - timedelta(days=1), datetime.min.time().replace(hour=23)))
            else:
                golden_dt = tz.localize(datetime.combine(selected_date, datetime.min.time().replace(hour=start_hour)))
            chart = generate_qmdj_chart(golden_dt)
        else:
            chart = None
        
        direction_scores = {}
        for d, name, palace in DIRECTIONS:
            direction_scores[d] = score_direction(chart, d, palace)
        
        # 3x3 Grid
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
                            <div style="color: #718096; font-size: 0.8em;">{data['door']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Summary
        good_dirs = [d for d, v in direction_scores.items() if v["verdict"] == "good"]
        bad_dirs = [d for d, v in direction_scores.items() if v["verdict"] == "bad"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ Go: {', '.join(good_dirs) if good_dirs else 'None outstanding'}")
        with col2:
            st.error(f"⚠️ Avoid: {', '.join(bad_dirs) if bad_dirs else 'None critical'}")
        
        # =================================================================
        # EXPORT FOR DEEP ANALYSIS
        # =================================================================
        st.divider()
        st.subheader("🤖 Get Deep Analysis")
        st.caption("Export to AI Analyst for detailed interpretation")
        
        export_data = generate_export_data(
            selected_date.strftime("%Y-%m-%d"),
            activity,
            hour_results,
            direction_scores,
            profile if use_bazi else None
        )
        
        export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        with st.expander("📋 View Export Data"):
            st.code(export_json, language="json")
        
        st.download_button(
            "💾 Download JSON for AI Analysis",
            export_json,
            file_name=f"strategic_{selected_date.strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        st.info("💡 **Paste JSON to Claude:** *'Analyze this strategic scan and explain why these hours/directions are recommended.'*")
    
    else:
        st.info("👈 Select date and activity, then click **Scan Day**")
        
        st.markdown("""
        ### Quick vs Deep Analysis
        
        | This App (Quick) | AI Analyst (Deep) |
        |------------------|-------------------|
        | Hour scores 1-10 | WHY each hour works |
        | Direction ratings | Formation meanings |
        | Best/Avoid lists | Personalized strategy |
        | Indicator flags | Book references (#71) |
        """)


if __name__ == "__main__":
    main()
