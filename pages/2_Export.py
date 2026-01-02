# pages/2_Export.py - Ming QiMenDunJia v10.3 PRO
# Export Center - Fixed session state sync
import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Export | Ming Qimen", page_icon="📦", layout="wide")

def main():
    st.title("📦 EXPORT CENTER")
    st.caption("Export chart data for Project 1 (Analyst Engine) • Universal Schema v3.0")
    
    st.divider()
    
    # Check data availability
    has_qmdj = st.session_state.get("qmdj_chart") is not None
    has_bazi = st.session_state.get("bazi_data") is not None or st.session_state.get("user_profile") is not None
    
    # Sidebar status
    with st.sidebar:
        st.header("📋 Export Info")
        st.markdown(f"**Schema:** v3.0")
        
        if has_qmdj:
            st.success("QMDJ Data: ✅ Ready")
        else:
            st.error("QMDJ Data: ❌ Missing")
        
        if has_bazi:
            st.success("BaZi Data: ✅ Ready")
        else:
            st.error("BaZi Data: ❌ Missing")
        
        st.divider()
        
        # Debug info
        with st.expander("🔧 Debug"):
            st.write("Session keys:", list(st.session_state.keys()))
    
    # Data Status Cards
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🎯 QMDJ Chart")
            if has_qmdj:
                st.success("✅ Ready")
                chart = st.session_state.qmdj_chart
                st.markdown(f"**Time:** {chart.get('datetime', 'Unknown')}")
                st.markdown(f"**Structure:** {chart.get('structure', 'Unknown')} | **Ju:** {chart.get('ju', '?')}")
            else:
                st.error("❌ Missing")
                st.caption("Generate a chart first")
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🎴 BaZi Profile")
            if has_bazi:
                st.success("✅ Ready")
                profile = st.session_state.get("user_profile", st.session_state.get("bazi_data", {}))
                st.markdown(f"**Day Master:** {profile.get('day_master', profile.get('dm', 'Unknown'))}")
                st.markdown(f"**Strength:** {profile.get('strength', profile.get('strength_cat', 'Unknown'))}")
            else:
                st.error("❌ Missing")
                st.caption("Calculate BaZi first")
    
    # Quick navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Generate Chart", use_container_width=True, disabled=has_qmdj):
            st.switch_page("pages/1_Chart.py")
    with col2:
        if st.button("🎴 Calculate BaZi", use_container_width=True, disabled=has_bazi):
            st.switch_page("pages/6_BaZi.py")
    
    st.divider()
    
    # Export Options
    if has_qmdj or has_bazi:
        st.subheader("📤 Export Options")
        
        # Build export data
        export_data = {
            "schema_version": "3.0",
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadata": {
                "timezone": "UTC+8",
                "method": "Chai Bu",
                "analysis_type": "INTEGRATED" if (has_qmdj and has_bazi) else ("QMDJ_ONLY" if has_qmdj else "BAZI_ONLY")
            }
        }
        
        # Add QMDJ data
        if has_qmdj:
            chart = st.session_state.qmdj_chart
            export_data["qmdj_data"] = {
                "datetime": chart.get("datetime"),
                "structure": chart.get("structure"),
                "structure_cn": chart.get("structure_cn"),
                "ju_number": chart.get("ju"),
                "palaces": chart.get("palaces", {})
            }
        
        # Add BaZi data
        if has_bazi:
            bazi = st.session_state.get("bazi_data", {})
            profile = st.session_state.get("user_profile", {})
            
            export_data["bazi_data"] = {
                "day_master": {
                    "stem": bazi.get("dm", profile.get("day_master")),
                    "element": bazi.get("dm_elem", profile.get("element")),
                    "strength": bazi.get("strength_cat", profile.get("strength")),
                    "strength_pct": bazi.get("strength_pct")
                },
                "useful_gods": bazi.get("useful", profile.get("useful_gods", [])),
                "unfavorable": bazi.get("unfav", profile.get("unfavorable", [])),
                "pillars": bazi.get("pillars", []),
                "ten_profiles": bazi.get("gods_dist", {}),
                "main_profile": bazi.get("main_profile", profile.get("profile"))
            }
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            st.download_button(
                "📥 Download JSON",
                json_str,
                file_name=f"ming_qimen_export_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(json_str, language="json")
                st.success("Copy the JSON above!")
        
        with col3:
            if st.button("🤖 AI Analysis Prompt", use_container_width=True):
                st.session_state.show_ai_prompt = True
        
        # Show AI prompt
        if st.session_state.get("show_ai_prompt"):
            st.divider()
            st.subheader("🤖 AI Analysis Prompt")
            
            prompt = f"""# Chinese Metaphysics Analysis Request

## Data (Universal Schema v3.0)
```json
{json.dumps(export_data, indent=2, ensure_ascii=False)}
```

## Analysis Required
Please provide comprehensive analysis covering:

### QMDJ Analysis (if data available):
1. Overall chart auspiciousness
2. Best palace/direction for action
3. Formation assessment
4. Timing recommendations

### BaZi Analysis (if data available):
1. Day Master personality and traits
2. Strength assessment implications
3. Useful gods and favorable elements
4. 10 Profiles interpretation
5. Current luck period

### Integrated Synthesis:
1. How QMDJ timing aligns with BaZi destiny
2. Strategic recommendations
3. What to pursue vs avoid
4. Key action items

Please use Joey Yap terminology and provide practical, actionable advice."""

            st.code(prompt, language="markdown")
            
            if st.button("❌ Hide Prompt"):
                st.session_state.show_ai_prompt = False
                st.rerun()
        
        st.divider()
        
        # Preview
        with st.expander("👁️ Preview Export Data"):
            st.json(export_data)
    
    else:
        st.warning("⚠️ No chart data available. Please generate a chart first.")
        
        if st.button("🎯 Go to Chart Generator", type="primary", use_container_width=True):
            st.switch_page("pages/1_Chart.py")
    
    # Footer
    st.divider()
    st.caption("🌟 Ming Qimen 明奇门 | Export Center v6.0 | Universal Schema v3.0")

if __name__ == "__main__":
    main()
