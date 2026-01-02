"""
Ming QiMenDunJia - BaZi Analysis Page v10.3
Enhanced with improved Luck Pillar visualization
"""

import streamlit as st
from datetime import datetime, date
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.bazi_engine import (
    calculate_bazi,
    calculate_day_master_strength,
    determine_useful_gods,
    calculate_ten_god_profiles,
    calculate_five_structures,
    calculate_luck_pillars
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="BaZi Pro - Ming QiMenDunJia",
    page_icon="🧬",
    layout="wide"
)

# ============================================================================
# ENHANCED LUCK PILLAR VISUALIZATION v10.3
# ============================================================================

def render_luck_pillar_timeline(luck_pillars, current_age, day_master_element, useful_gods):
    """
    Renders an enhanced visual timeline for Luck Pillars
    
    Args:
        luck_pillars: List of luck pillar dictionaries
        current_age: User's current age
        day_master_element: Day Master element (for favorability check)
        useful_gods: List of useful god elements
    """
    st.markdown("#### 🔮 10-Year Luck Pillar Timeline")
    
    if not luck_pillars or len(luck_pillars) == 0:
        st.warning("⚠️ No Luck Pillars available. Please check birth time is provided.")
        return
    
    # Find current pillar index
    current_index = 0
    for i, pillar in enumerate(luck_pillars):
        if pillar.get('start_age', 0) <= current_age < pillar.get('end_age', 999):
            current_index = i
            break
    
    # Visual timeline HTML
    timeline_html = """
    <style>
    .timeline-container {
        width: 100%;
        overflow-x: auto;
        padding: 20px 0;
        margin: 20px 0;
    }
    .timeline {
        display: flex;
        gap: 10px;
        min-width: max-content;
        padding: 10px;
    }
    .pillar-block {
        flex: 0 0 120px;
        min-width: 120px;
        padding: 15px 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #444;
        transition: all 0.3s ease;
        background: #1a1a2e;
    }
    .pillar-current {
        border: 3px solid #FFD700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        transform: scale(1.05);
    }
    .pillar-favorable {
        background: linear-gradient(135deg, #1a4d2e 0%, #2d5f3f 100%);
    }
    .pillar-unfavorable {
        background: linear-gradient(135deg, #4d1a1a 0%, #5f2d2d 100%);
    }
    .pillar-neutral {
        background: linear-gradient(135deg, #2a2a4d 0%, #3f3f5f 100%);
    }
    .pillar-age {
        font-size: 11px;
        color: #999;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .pillar-stems {
        font-size: 18px;
        font-weight: bold;
        color: #FFD700;
        margin: 8px 0;
        letter-spacing: 2px;
    }
    .pillar-element {
        font-size: 12px;
        color: #ccc;
        margin-top: 5px;
    }
    .pillar-god {
        font-size: 10px;
        color: #aaa;
        margin-top: 3px;
        font-style: italic;
    }
    .pillar-status {
        font-size: 10px;
        margin-top: 8px;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        font-weight: 600;
    }
    .status-favorable {
        background: #2d5f3f;
        color: #90EE90;
    }
    .status-unfavorable {
        background: #5f2d2d;
        color: #FFB6C6;
    }
    .status-neutral {
        background: #3f3f5f;
        color: #B0B0FF;
    }
    </style>
    <div class="timeline-container">
        <div class="timeline">
    """
    
    # Generate pillar blocks
    display_pillars = luck_pillars[:10]  # Show max 10 pillars
    
    for i, pillar in enumerate(display_pillars):
        stem = pillar.get('stem', '?')
        branch = pillar.get('branch', '?')
        start_age = pillar.get('start_age', 0)
        end_age = pillar.get('end_age', start_age + 10)
        element = pillar.get('element', 'Unknown')
        ten_god = pillar.get('ten_god', '')
        
        # Determine if favorable
        is_favorable = element in useful_gods
        is_current = (i == current_index)
        
        # Determine unfavorable elements for Day Master
        unfavorable_elements = []
        if day_master_element == 'Metal':
            unfavorable_elements = ['Fire', 'Water']
        elif day_master_element == 'Wood':
            unfavorable_elements = ['Metal', 'Earth']
        elif day_master_element == 'Water':
            unfavorable_elements = ['Earth', 'Fire']
        elif day_master_element == 'Fire':
            unfavorable_elements = ['Water', 'Metal']
        elif day_master_element == 'Earth':
            unfavorable_elements = ['Wood', 'Water']
        
        is_unfavorable = element in unfavorable_elements
        
        # Choose class
        if is_favorable:
            pillar_class = "pillar-favorable"
            status_class = "status-favorable"
            status_text = "✓ Favorable"
        elif is_unfavorable:
            pillar_class = "pillar-unfavorable"
            status_class = "status-unfavorable"
            status_text = "✗ Unfavorable"
        else:
            pillar_class = "pillar-neutral"
            status_class = "status-neutral"
            status_text = "○ Neutral"
        
        current_class = " pillar-current" if is_current else ""
        
        timeline_html += f"""
        <div class="pillar-block {pillar_class}{current_class}">
            <div class="pillar-age">Age {start_age}-{end_age-1}</div>
            <div class="pillar-stems">{stem}{branch}</div>
            <div class="pillar-element">{element}</div>
            <div class="pillar-god">{ten_god}</div>
            <div class="pillar-status {status_class}">{status_text}</div>
        </div>
        """
    
    timeline_html += """
        </div>
    </div>
    """
    
    st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Current period highlight
    if current_index < len(luck_pillars):
        current_pillar = luck_pillars[current_index]
        favorability = "✓ Favorable" if current_pillar.get('element') in useful_gods else "⚠️ Neutral/Unfavorable"
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a2332 0%, #2a3f5f 100%); 
                    padding: 20px; border-radius: 10px; border-left: 4px solid #FFD700; margin-top: 20px;'>
            <strong style='color: #FFD700; font-size: 16px;'>📍 Current Period ({favorability}):</strong><br/>
            <span style='color: #fff; font-size: 14px;'>
                Age {current_pillar.get('start_age', 0)}-{current_pillar.get('end_age', 0)-1} • 
                {current_pillar.get('stem', '?')}{current_pillar.get('branch', '?')} • 
                {current_pillar.get('element', 'Unknown')} • 
                {current_pillar.get('ten_god', '')}
            </span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# MAIN PAGE CONTENT
# ============================================================================

st.title("🧬 BaZi Pro Analysis")
st.markdown("*Four Pillars of Destiny with Advanced Features*")

# Check if we have BaZi data in session state
if 'bazi_data' not in st.session_state or st.session_state.bazi_data is None:
    st.warning("⚠️ No BaZi data available. Please enter your birth information first.")
    
    # Quick input form
    with st.expander("📝 Enter Birth Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            birth_date = st.date_input(
                "Birth Date",
                value=date(1978, 6, 27),
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
        
        with col2:
            birth_hour = st.number_input(
                "Birth Hour (0-23)",
                min_value=0,
                max_value=23,
                value=20,
                step=1
            )
        
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        if st.button("Calculate BaZi", type="primary"):
            with st.spinner("Calculating BaZi..."):
                try:
                    # Calculate BaZi
                    bazi_result = calculate_bazi(birth_date, birth_hour, gender)
                    
                    # Store in session state
                    st.session_state.bazi_data = bazi_result
                    st.session_state.bazi_birth_info = {
                        'date': birth_date,
                        'hour': birth_hour,
                        'gender': gender
                    }
                    
                    st.success("✅ BaZi calculated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error calculating BaZi: {e}")
    
    st.stop()

# ============================================================================
# DISPLAY BAZI DATA
# ============================================================================

bazi_data = st.session_state.bazi_data

# Header with key info
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Day Master",
        f"{bazi_data['day_master']['stem']} ({bazi_data['day_master']['element']})",
        bazi_data['day_master']['polarity']
    )

with col2:
    st.metric(
        "Strength",
        bazi_data['day_master']['strength'],
        f"{bazi_data['day_master'].get('strength_pct', 50)}%"
    )

with col3:
    useful_primary = bazi_data.get('useful_gods', {}).get('primary', 'Unknown')
    st.metric(
        "Useful God",
        useful_primary,
        "Primary"
    )

with col4:
    main_profile = bazi_data.get('ten_profiles', {}).get('main_profile_name', 'Unknown')
    st.metric(
        "Profile",
        main_profile[:15],  # Truncate if too long
        "Main"
    )

st.divider()

# ============================================================================
# LUCK PILLARS SECTION
# ============================================================================

st.markdown("### 🔮 Luck Pillars (十年大运)")

if 'luck_pillars' in bazi_data and bazi_data['luck_pillars']:
    luck_pillar_data = bazi_data['luck_pillars']
    pillars = luck_pillar_data.get('pillars', [])
    
    if pillars and len(pillars) > 0:
        # Get birth info for age calculation
        birth_info = st.session_state.get('bazi_birth_info', {})
        birth_date_obj = birth_info.get('date', date(1978, 6, 27))
        current_age = datetime.now().year - birth_date_obj.year
        
        # Get Day Master element and useful gods
        day_master_element = bazi_data['day_master']['element']
        useful_gods = [
            bazi_data.get('useful_gods', {}).get('primary', ''),
            bazi_data.get('useful_gods', {}).get('secondary', '')
        ]
        useful_gods = [g for g in useful_gods if g]  # Remove empty strings
        
        # Render enhanced timeline
        render_luck_pillar_timeline(pillars, current_age, day_master_element, useful_gods)
        
        # Detailed table below timeline
        with st.expander("📊 Detailed Luck Pillar Table"):
            import pandas as pd
            
            pillar_rows = []
            for pillar in pillars[:10]:
                pillar_rows.append({
                    'Period': f"{pillar.get('start_age', 0)}-{pillar.get('end_age', 0)-1}",
                    'Pillar': f"{pillar.get('stem', '?')}{pillar.get('branch', '?')}",
                    'Element': pillar.get('element', 'Unknown'),
                    'Ten God': pillar.get('ten_god', ''),
                    'Favorability': '✓' if pillar.get('element') in useful_gods else '○'
                })
            
            df_pillars = pd.DataFrame(pillar_rows)
            st.dataframe(df_pillars, use_container_width=True)
    else:
        st.info("ℹ️ Luck Pillars not calculated. Start age may be pending.")
else:
    st.warning("⚠️ Luck Pillars not available. Ensure birth time is provided.")

st.divider()

# ============================================================================
# FOUR PILLARS DISPLAY
# ============================================================================

st.markdown("### 📊 Four Pillars")

if 'four_pillars' in bazi_data:
    pillars = bazi_data['four_pillars']
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, (pillar_name, pillar_data) in zip(
        [col1, col2, col3, col4],
        [('Year', pillars.get('year', {})), 
         ('Month', pillars.get('month', {})),
         ('Day', pillars.get('day', {})),
         ('Hour', pillars.get('hour', {}))]
    ):
        with col:
            st.markdown(f"**{pillar_name} Pillar**")
            st.markdown(f"🌟 {pillar_data.get('stem', '?')}{pillar_data.get('branch', '?')}")
            st.caption(f"Ten God: {pillar_data.get('ten_god', 'N/A')}")
            
            # Hidden stems
            hidden = pillar_data.get('hidden', [])
            if hidden:
                st.caption(f"Hidden: {', '.join(hidden)}")

st.divider()

# ============================================================================
# TEN PROFILES & FIVE STRUCTURES
# ============================================================================

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎭 Ten Profiles")
    if 'ten_profiles' in bazi_data:
        profiles = bazi_data['ten_profiles']
        
        # Display main profile
        st.info(f"**Main Profile:** {profiles.get('main_profile_name', 'Unknown')}")
        
        # Bar chart would go here (if you have the visualization)
        # For now, show as list
        profile_data = {k: v for k, v in profiles.items() 
                       if k not in ['main_profile', 'main_profile_name']}
        
        for profile, value in sorted(profile_data.items(), key=lambda x: x[1], reverse=True):
            if value > 0:
                st.progress(value / 10, text=f"{profile}: {value}")

with col2:
    st.markdown("### ⭐ Five Structures")
    if 'five_structures' in bazi_data:
        structures = bazi_data['five_structures']
        
        # Display main structure
        st.info(f"**Main Structure:** {structures.get('main_structure', 'Unknown')}")
        
        # Show structure scores
        structure_data = {k: v for k, v in structures.items() 
                         if k != 'main_structure'}
        
        for struct, value in sorted(structure_data.items(), key=lambda x: x[1], reverse=True):
            if value > 0:
                st.progress(value / 10, text=f"{struct}: {value}")

st.divider()

# ============================================================================
# USEFUL GODS
# ============================================================================

st.markdown("### 🎯 Useful Gods & Unfavorable Elements")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**✅ Useful Gods (Favorable)**")
    if 'useful_gods' in bazi_data:
        useful = bazi_data['useful_gods']
        st.success(f"Primary: **{useful.get('primary', 'Unknown')}**")
        if useful.get('secondary'):
            st.success(f"Secondary: **{useful.get('secondary', '')}**")
        
        # Directions, colors, numbers
        if 'directions' in useful:
            st.caption(f"Favorable Directions: {', '.join(useful['directions'])}")
        if 'colors' in useful:
            st.caption(f"Favorable Colors: {', '.join(useful['colors'])}")
        if 'numbers' in useful:
            st.caption(f"Favorable Numbers: {', '.join(map(str, useful['numbers']))}")

with col2:
    st.markdown("**❌ Unfavorable Elements**")
    if 'unfavorable' in bazi_data:
        unfav = bazi_data['unfavorable']
        st.error(f"Primary: **{unfav.get('primary', 'Unknown')}**")
        
        # Directions, colors
        if 'directions' in unfav:
            st.caption(f"Avoid Directions: {', '.join(unfav['directions'])}")
        if 'colors' in unfav:
            st.caption(f"Avoid Colors: {', '.join(unfav['colors'])}")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.caption("Ming QiMenDunJia v10.3 • Enhanced Luck Pillar Visualization")
