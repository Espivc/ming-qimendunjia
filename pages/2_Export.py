"""
Ming Qimen 明奇门 - Export Center v6.0
Export chart data in Universal Schema v3.0 format
"""

import streamlit as st
import json
from datetime import datetime, timezone, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.qmdj_engine import PALACE_INFO, NINE_STARS, EIGHT_DOORS, EIGHT_DEITIES

# Page config
st.set_page_config(page_title="Export | Ming Qimen", page_icon="📤", layout="wide")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
    .page-header {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 2rem;
        letter-spacing: 2px;
    }
    
    .export-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .export-card.ready {
        border-color: #2ecc71;
    }
    
    .export-card.missing {
        border-color: #e74c3c;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    .status-ready { background: #2ecc71; color: white; }
    .status-missing { background: #e74c3c; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-header">📤 EXPORT CENTER</h1>', unsafe_allow_html=True)
st.markdown("*Export chart data for Project 1 (Analyst Engine) • Universal Schema v3.0*")

st.divider()

# Check data availability
has_chart = st.session_state.get("current_chart") is not None
has_profile = st.session_state.get("user_profile") is not None

# Status cards
col1, col2 = st.columns(2)

with col1:
    status_class = "ready" if has_chart else "missing"
    badge_class = "status-ready" if has_chart else "status-missing"
    badge_text = "✅ Ready" if has_chart else "❌ Missing"
    
    st.markdown(f"""
    <div class="export-card {status_class}">
        <h3>📊 QMDJ Chart</h3>
        <span class="status-badge {badge_class}">{badge_text}</span>
        <p style="color: #888; margin-top: 0.5rem;">
            {'Chart generated and ready for export' if has_chart else 'Generate a chart first'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not has_chart:
        if st.button("📊 Generate Chart", use_container_width=True):
            st.switch_page("pages/1_Chart.py")

with col2:
    status_class = "ready" if has_profile else "missing"
    badge_class = "status-ready" if has_profile else "status-missing"
    badge_text = "✅ Ready" if has_profile else "⚠️ Optional"
    
    st.markdown(f"""
    <div class="export-card {status_class}">
        <h3>🎂 BaZi Profile</h3>
        <span class="status-badge {badge_class}">{badge_text}</span>
        <p style="color: #888; margin-top: 0.5rem;">
            {'Profile will be included in export' if has_profile else 'Add profile for personalized analysis'}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not has_profile:
        if st.button("🎂 Set Up Profile", use_container_width=True):
            st.switch_page("pages/6_BaZi.py")

st.divider()

# Export section
if has_chart:
    chart = st.session_state.current_chart
    profile = st.session_state.get("user_profile", {})
    
    # Build Universal Schema v3.0
    def build_universal_schema():
        """Build export data in Universal Schema v3.0 format"""
        
        # Get selected palace or default to 5
        palace_num = st.session_state.get("selected_palace", 5)
        # Ensure palace_num is int
        if palace_num is None:
            palace_num = 5
        palace_num = int(palace_num)
        
        # Get palace data - handle both int and string keys
        if palace_num in chart["palaces"]:
            palace = chart["palaces"][palace_num]
        elif str(palace_num) in chart["palaces"]:
            palace = chart["palaces"][str(palace_num)]
        else:
            palace = chart["palaces"][list(chart["palaces"].keys())[0]]
        
        schema = {
            "schema_version": "3.0",
            "schema_name": "QMDJ_BaZi_Integrated_Data_Schema",
            
            "metadata": {
                "date_time": chart["metadata"]["datetime"],
                "date_display": chart["metadata"]["date_display"],
                "time_display": chart["metadata"]["time_display"],
                "chinese_hour": chart["metadata"]["chinese_hour"]["name"],
                "timezone": "UTC+8",
                "method": "Chai Bu",
                "purpose": "Forecasting",
                "analysis_type": "QMDJ_BAZI_INTEGRATED" if has_profile else "QMDJ_ONLY",
                "generated_by": "Ming Qimen v6.0"
            },
            
            "qmdj_data": {
                "chart_type": "Hour",
                "structure": chart["structure"]["structure"],
                "structure_chinese": chart["structure"]["structure_chinese"],
                "ju_number": chart["structure"]["ju_number"],
                
                "qmdj_pillars": chart["qmdj_pillars"],
                
                "lead_indicators": {
                    "lead_stem_palace": chart["lead_indicators"]["lead_stem_palace"],
                    "lead_stem_palace_name": chart["lead_indicators"]["lead_stem_palace_name"],
                    "lead_star": {
                        "name": chart["lead_indicators"]["lead_star"]["name"],
                        "chinese": chart["lead_indicators"]["lead_star"]["chinese"]
                    },
                    "lead_door": {
                        "name": chart["lead_indicators"]["lead_door"]["name"],
                        "chinese": chart["lead_indicators"]["lead_door"]["chinese"]
                    }
                },
                
                "death_emptiness": {
                    "cycle": chart["death_emptiness"]["cycle"],
                    "empty_branches": chart["death_emptiness"]["empty_branches"],
                    "affected_palaces": chart["death_emptiness"]["affected_palaces"]
                },
                
                "horse_star": {
                    "branch": chart["horse_star"].get("horse_branch"),
                    "palace": chart["horse_star"].get("horse_palace")
                },
                
                "nobleman": {
                    "day_nobleman_branches": chart["nobleman"].get("day_nobleman_branches", []),
                    "day_nobleman_palaces": chart["nobleman"].get("day_nobleman_palaces", [])
                },
                
                "palace_analyzed": {
                    "number": palace_num,
                    "name": palace["palace_info"]["name"],
                    "chinese": palace["palace_info"]["chinese"],
                    "direction": palace["palace_info"]["direction"],
                    "element": palace["palace_info"]["element"],
                    "indicators": palace["indicators"]
                },
                
                "components": {
                    "star": {
                        "name": palace["star"]["name"],
                        "chinese": palace["star"]["chinese"],
                        "element": palace["star"]["element"],
                        "nature": palace["star"]["nature"],
                        "strength": palace["star"].get("strength", "N/A"),
                        "strength_score": palace["star"].get("strength_score", 0)
                    },
                    "door": {
                        "name": palace["door"]["name"],
                        "chinese": palace["door"]["chinese"],
                        "element": palace["door"]["element"],
                        "nature": palace["door"]["nature"],
                        "strength": palace["door"].get("strength", "N/A"),
                        "strength_score": palace["door"].get("strength_score", 0)
                    },
                    "deity": {
                        "name": palace["deity"]["name"],
                        "chinese": palace["deity"]["chinese"],
                        "nature": palace["deity"]["nature"],
                        "function": palace["deity"].get("function", "")
                    }
                },
                
                "all_palaces_summary": {
                    p: {
                        "star": chart["palaces"][p]["star"]["name"],
                        "door": chart["palaces"][p]["door"]["name"],
                        "deity": chart["palaces"][p]["deity"]["name"],
                        "is_lead": chart["palaces"][p]["indicators"]["is_lead_palace"],
                        "has_horse": chart["palaces"][p]["indicators"]["has_horse_star"],
                        "has_noble": chart["palaces"][p]["indicators"]["has_nobleman"],
                        "is_empty": chart["palaces"][p]["indicators"]["is_empty"]
                    } for p in range(1, 10)
                }
            },
            
            "bazi_data": None,
            
            "synthesis": {
                "qmdj_score": calculate_qmdj_score(palace),
                "bazi_alignment_score": None,
                "combined_verdict_score": None,
                "verdict": calculate_verdict(palace),
                "confidence": "MEDIUM",
                "primary_action": generate_action(palace),
                "special_notes": generate_special_notes(chart, palace_num)
            },
            
            "tracking": {
                "db_row": generate_db_row(chart, palace_num, profile),
                "outcome_status": "PENDING",
                "outcome_notes": "",
                "feedback_date": None
            }
        }
        
        # Add BaZi data if available
        if has_profile:
            schema["bazi_data"] = {
                "chart_source": "User Profile",
                "day_master": {
                    "stem": profile.get("day_master", "Unknown"),
                    "element": profile.get("element", "Unknown"),
                    "polarity": profile.get("polarity", "Unknown"),
                    "strength": profile.get("strength", "Unknown"),
                    "strength_score": profile.get("strength_score", 5)
                },
                "useful_gods": {
                    "primary": profile.get("useful_gods", ["Unknown"])[0] if profile.get("useful_gods") else "Unknown",
                    "secondary": profile.get("useful_gods", ["Unknown", "Unknown"])[1] if len(profile.get("useful_gods", [])) > 1 else None,
                    "list": profile.get("useful_gods", [])
                },
                "unfavorable_elements": {
                    "list": profile.get("unfavorable", [])
                },
                "ten_god_profile": {
                    "profile_name": profile.get("profile", "Unknown")
                },
                "special_structures": {
                    "wealth_vault": profile.get("wealth_vault", False),
                    "nobleman_present": profile.get("nobleman", False)
                }
            }
            
            # Calculate BaZi alignment
            schema["synthesis"]["bazi_alignment_score"] = calculate_bazi_alignment(profile, palace)
            schema["synthesis"]["combined_verdict_score"] = (
                schema["synthesis"]["qmdj_score"] + schema["synthesis"]["bazi_alignment_score"]
            ) // 2
        
        return schema
    
    def calculate_qmdj_score(palace):
        """Calculate QMDJ score based on component strengths"""
        score = 5  # Base
        
        star_score = palace["star"].get("strength_score", 0)
        door_score = palace["door"].get("strength_score", 0)
        
        score += (star_score + door_score) // 2
        
        # Nature bonus
        if palace["star"]["nature"] == "Auspicious":
            score += 1
        if palace["door"]["nature"] == "Auspicious":
            score += 1
        if palace["deity"]["nature"] == "Auspicious":
            score += 1
        
        # Penalty for inauspicious
        if palace["star"]["nature"] == "Inauspicious":
            score -= 1
        if palace["door"]["nature"] == "Inauspicious":
            score -= 1
        if palace["deity"]["nature"] == "Inauspicious":
            score -= 1
        
        # Empty palace penalty
        if palace["indicators"]["is_empty"]:
            score -= 2
        
        # Lead palace bonus
        if palace["indicators"]["is_lead_palace"]:
            score += 1
        
        return max(1, min(10, score))
    
    def calculate_verdict(palace):
        """Calculate verdict based on score"""
        score = calculate_qmdj_score(palace)
        if score >= 8:
            return "HIGHLY AUSPICIOUS"
        elif score >= 6:
            return "AUSPICIOUS"
        elif score >= 4:
            return "NEUTRAL"
        elif score >= 2:
            return "INAUSPICIOUS"
        else:
            return "HIGHLY INAUSPICIOUS"
    
    def generate_action(palace):
        """Generate primary action recommendation"""
        door = palace["door"]["name"]
        nature = palace["door"]["nature"]
        
        actions = {
            "Open": "Proceed with plans - excellent for new beginnings",
            "Rest": "Good time for rest, recuperation, and planning",
            "Life": "Excellent for growth, wealth, and expansion",
            "Harm": "Be cautious - potential for conflict or injury",
            "Delusion": "Hidden matters - good for secrecy, bad for clarity",
            "Scenery": "Good for documentation, fame, and publicity",
            "Death": "Avoid major decisions - energy is blocked",
            "Fear": "Unexpected events possible - stay alert"
        }
        
        return actions.get(door, "Analyze components carefully before acting")
    
    def generate_special_notes(chart, palace_num):
        """Generate special notes based on indicators"""
        notes = []
        palace = chart["palaces"][palace_num]
        
        if palace["indicators"]["is_lead_palace"]:
            notes.append("Lead Palace: Maximum authority and command energy")
        if palace["indicators"]["has_horse_star"]:
            notes.append("Horse Star active: Fast results, travel favored")
        if palace["indicators"]["has_nobleman"]:
            notes.append("Nobleman present: Helpful people will appear")
        if palace["indicators"]["is_empty"]:
            notes.append("Death & Emptiness: Results may be diminished")
        
        return notes
    
    def calculate_bazi_alignment(profile, palace):
        """Calculate BaZi alignment score"""
        score = 5
        useful = profile.get("useful_gods", [])
        unfavorable = profile.get("unfavorable", [])
        palace_element = palace["palace_info"]["element"]
        
        if palace_element in useful:
            score += 3
        if palace_element in unfavorable:
            score -= 3
        
        # Component elements
        if palace["star"]["element"] in useful:
            score += 1
        if palace["door"]["element"] in useful:
            score += 1
        
        return max(1, min(10, score))
    
    def generate_db_row(chart, palace_num, profile):
        """Generate DB row for ML tracking"""
        palace = chart["palaces"][palace_num]
        
        parts = [
            chart["metadata"]["date_display"],
            chart["metadata"]["time_display"],
            f"P{palace_num}",
            f"{palace['star']['name']}+{palace['door']['name']}",
            str(calculate_qmdj_score(palace)),
            str(calculate_bazi_alignment(profile, palace)) if profile else "N/A",
            calculate_verdict(palace),
            generate_action(palace)[:50],
            "PENDING"
        ]
        
        return ",".join(parts)
    
    # Build schema
    export_data = build_universal_schema()
    
    # Export tabs
    tab1, tab2, tab3 = st.tabs(["📄 JSON Export", "📋 Analysis Prompt", "💾 DB Row"])
    
    with tab1:
        st.subheader("Universal Schema v3.0 JSON")
        
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        st.code(json_str, language="json", line_numbers=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download JSON",
                json_str,
                file_name=f"ming_qimen_{export_data['metadata']['date_display']}_{export_data['metadata']['time_display'].replace(':', '')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col2:
            if st.button("📋 Copy to Clipboard Info", use_container_width=True):
                st.info("Select the JSON above and use Ctrl+C / Cmd+C to copy")
    
    with tab2:
        st.subheader("Analysis Prompt for Project 1")
        
        prompt = f"""Analyze this Qi Men Dun Jia chart and provide strategic recommendations:

**Chart Data (Universal Schema v3.0):**
```json
{json.dumps(export_data, indent=2, ensure_ascii=False)}
```

**Please provide:**
1. Formation identification (check #64/#73 reference books)
2. Component relationship analysis (Star-Door-Deity interaction)
3. Special indicator interpretation (Lead Palace, Horse Star, Nobleman, Empty)
4. Strategic recommendations based on the query purpose
5. Timing advice (optimal hours to act)
6. Risk assessment and mitigation strategies

**Output as bilingual report (English + Chinese) in structured format.**
"""
        
        st.text_area("Copy this prompt to Claude (Project 1):", prompt, height=400)
        
        st.info("💡 Paste this entire prompt into Claude to get a detailed analysis report")
    
    with tab3:
        st.subheader("ML Database Row")
        
        db_row = export_data["tracking"]["db_row"]
        
        st.code(db_row)
        
        st.markdown("""
        **Format:** `Date,Time,Palace,Formation,QMDJ_Score,BaZi_Score,Verdict,Action,Outcome`
        
        After you receive analysis and take action, update the Outcome field:
        - `SUCCESS` - Action worked as predicted
        - `PARTIAL` - Partially successful
        - `FAILURE` - Did not work
        - `NOT_APPLICABLE` - Could not verify
        """)
        
        st.info("💡 Save this to your CSV database for ML pattern recognition")

else:
    st.warning("⚠️ No chart data available. Please generate a chart first.")
    
    if st.button("📊 Go to Chart Generator", type="primary", use_container_width=True):
        st.switch_page("pages/1_Chart.py")

# Sidebar
with st.sidebar:
    st.markdown("### 📤 Export Info")
    st.markdown(f"**Schema:** v3.0")
    st.markdown(f"**QMDJ Data:** {'✅ Ready' if has_chart else '❌ Missing'}")
    st.markdown(f"**BaZi Data:** {'✅ Ready' if has_profile else '⚠️ Optional'}")
    
    if has_chart:
        st.markdown("---")
        st.markdown("**Chart Details:**")
        st.markdown(f"Date: {chart['metadata']['date_display']}")
        st.markdown(f"Time: {chart['metadata']['time_display']}")
        st.markdown(f"Ju: {chart['structure']['ju_number']}")

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Export Center v6.0 | Universal Schema v3.0")
