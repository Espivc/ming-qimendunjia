"""
Ming Qimen 明奇门 - Help & Guide v6.0
Learn QMDJ and BaZi fundamentals
"""

import streamlit as st

st.set_page_config(page_title="Help | Ming Qimen", page_icon="❓", layout="wide")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    .page-header {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 2rem;
        letter-spacing: 2px;
    }
    
    .guide-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #12121e 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .guide-title {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .term-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #444;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .term-name {
        font-family: 'Cinzel', serif;
        color: #FFD700;
        font-size: 1rem;
    }
    
    .term-chinese {
        font-family: 'Noto Sans SC', sans-serif;
        color: #9B59B6;
        font-size: 1.2rem;
        margin-left: 0.5rem;
    }
    
    .element-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    .wood { background: #228B22; color: white; }
    .fire { background: #DC143C; color: white; }
    .earth { background: #DAA520; color: black; }
    .metal { background: #C0C0C0; color: black; }
    .water { background: #4169E1; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-header">❓ HELP & GUIDE</h1>', unsafe_allow_html=True)
st.markdown("*Learn the fundamentals of Qi Men Dun Jia and BaZi*")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔮 QMDJ Basics", "🎂 BaZi Basics", "📖 How to Use", "📚 Glossary"])

# TAB 1: QMDJ Basics
with tab1:
    st.subheader("🔮 Qi Men Dun Jia Fundamentals")
    
    st.markdown("""
    **Qi Men Dun Jia** (奇门遁甲) is an ancient Chinese metaphysical system used for:
    - Strategic decision-making
    - Timing selection
    - Forecasting outcomes
    - Understanding energy patterns
    """)
    
    st.markdown("---")
    
    # 9 Palaces
    st.markdown("### 🏛️ The 9 Palaces (九宫)")
    
    st.markdown("""
    The QMDJ chart uses the **Luo Shu** (洛书) magic square arrangement:
    
    | SE (4) | S (9) | SW (2) |
    |--------|-------|--------|
    | E (3)  | Center (5) | W (7) |
    | NE (8) | N (1) | NW (6) |
    
    Each palace has a **fixed element**:
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🌊 **Palace 1 (Kan)** - Water")
        st.markdown("🌿 **Palace 3 (Zhen)** - Wood")
        st.markdown("🌿 **Palace 4 (Xun)** - Wood")
    with col2:
        st.markdown("🏔️ **Palace 2 (Kun)** - Earth")
        st.markdown("🏔️ **Palace 5 (Center)** - Earth")
        st.markdown("🏔️ **Palace 8 (Gen)** - Earth")
    with col3:
        st.markdown("⚔️ **Palace 6 (Qian)** - Metal")
        st.markdown("⚔️ **Palace 7 (Dui)** - Metal")
        st.markdown("🔥 **Palace 9 (Li)** - Fire")
    
    st.markdown("---")
    
    # Components
    st.markdown("### ⭐ Chart Components")
    
    st.markdown("""
    Each palace contains **4 components** that interact:
    
    1. **Star (星)** - The heavenly influence (9 Stars)
    2. **Door (门)** - The gateway/approach (8 Doors)
    3. **Deity (神)** - The spiritual influence (8 Deities)
    4. **Stem (干)** - The energy carrier (10 Stems)
    """)
    
    # 9 Stars
    st.markdown("#### ⭐ Nine Stars (九星)")
    stars_data = [
        ("Canopy", "天蓬", "Water", "Inauspicious", "Obstacles, hidden dangers"),
        ("Grass", "天芮", "Earth", "Inauspicious", "Illness, stagnation"),
        ("Impulse", "天冲", "Wood", "Auspicious", "Action, breakthrough"),
        ("Assistant", "天辅", "Wood", "Auspicious", "Help, support"),
        ("Connect", "天禽", "Earth", "Neutral", "Connection, linking"),
        ("Heart", "天心", "Metal", "Auspicious", "Intelligence, strategy"),
        ("Pillar", "天柱", "Metal", "Neutral", "Stability, support"),
        ("Ren", "天任", "Earth", "Auspicious", "Achievement, responsibility"),
        ("Hero", "天英", "Fire", "Neutral", "Recognition, fame"),
    ]
    
    for name, chinese, element, nature, meaning in stars_data:
        element_class = element.lower()
        st.markdown(f"""
        <div class="term-card">
            <span class="term-name">{name}</span>
            <span class="term-chinese">{chinese}</span>
            <span class="element-badge {element_class}">{element}</span>
            <span style="color: {'#2ecc71' if nature == 'Auspicious' else '#e74c3c' if nature == 'Inauspicious' else '#f39c12'}">
                {nature}
            </span>
            <div style="color: #888; margin-top: 0.3rem;">{meaning}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 8 Doors
    st.markdown("#### 🚪 Eight Doors (八门)")
    doors_data = [
        ("Open", "开门", "Metal", "Auspicious", "New beginnings, opportunities"),
        ("Rest", "休门", "Water", "Auspicious", "Recovery, planning, rest"),
        ("Life", "生门", "Earth", "Auspicious", "Growth, wealth, expansion"),
        ("Harm", "伤门", "Wood", "Inauspicious", "Conflict, injury, competition"),
        ("Delusion", "杜门", "Wood", "Neutral", "Secrets, hiding, blocked"),
        ("Scenery", "景门", "Fire", "Neutral", "Fame, documentation, clarity"),
        ("Death", "死门", "Earth", "Inauspicious", "Endings, blockage, avoid"),
        ("Fear", "惊门", "Metal", "Inauspicious", "Surprises, anxiety, unexpected"),
    ]
    
    for name, chinese, element, nature, meaning in doors_data:
        element_class = element.lower()
        st.markdown(f"""
        <div class="term-card">
            <span class="term-name">{name}</span>
            <span class="term-chinese">{chinese}</span>
            <span class="element-badge {element_class}">{element}</span>
            <span style="color: {'#2ecc71' if nature == 'Auspicious' else '#e74c3c' if nature == 'Inauspicious' else '#f39c12'}">
                {nature}
            </span>
            <div style="color: #888; margin-top: 0.3rem;">{meaning}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # v6.0 Indicators
    st.markdown("### 🎯 Special Indicators (v6.0)")
    
    st.markdown("""
    <div class="guide-card">
        <div class="guide-title">⭐ Lead Palace (值符宫)</div>
        <p>The command center of the chart. Where Jia (甲) is hidden. Actions here have maximum authority.</p>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">🐴 Horse Star (驿马)</div>
        <p>Indicates travel, mobility, and fast results. Good for movement and change.</p>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">👑 Nobleman (贵人)</div>
        <p>Helpful people will appear. Excellent for seeking assistance and making connections.</p>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">💀 Death & Emptiness (空亡)</div>
        <p>Energy is diminished in these palaces. Results may be reduced or delayed.</p>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: BaZi Basics
with tab2:
    st.subheader("🎂 BaZi (Four Pillars) Fundamentals")
    
    st.markdown("""
    **BaZi** (八字), also known as Four Pillars of Destiny, analyzes your birth chart to understand:
    - Your elemental makeup
    - Personality and tendencies
    - Favorable and unfavorable elements
    - Life patterns and timing
    """)
    
    st.markdown("---")
    
    # 5 Elements
    st.markdown("### 🌊 The Five Elements (五行)")
    
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0;">
        <span class="element-badge wood" style="padding: 0.5rem 1rem; font-size: 1rem;">🌿 Wood 木</span>
        <span class="element-badge fire" style="padding: 0.5rem 1rem; font-size: 1rem;">🔥 Fire 火</span>
        <span class="element-badge earth" style="padding: 0.5rem 1rem; font-size: 1rem;">🏔️ Earth 土</span>
        <span class="element-badge metal" style="padding: 0.5rem 1rem; font-size: 1rem;">⚔️ Metal 金</span>
        <span class="element-badge water" style="padding: 0.5rem 1rem; font-size: 1rem;">🌊 Water 水</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Production Cycle (相生)")
        st.markdown("""
        - Wood feeds Fire 🌿→🔥
        - Fire creates Earth 🔥→🏔️
        - Earth produces Metal 🏔️→⚔️
        - Metal carries Water ⚔️→🌊
        - Water nourishes Wood 🌊→🌿
        """)
    
    with col2:
        st.markdown("#### Control Cycle (相克)")
        st.markdown("""
        - Wood breaks Earth 🌿→🏔️
        - Fire melts Metal 🔥→⚔️
        - Earth dams Water 🏔️→🌊
        - Metal chops Wood ⚔️→🌿
        - Water extinguishes Fire 🌊→🔥
        """)
    
    st.markdown("---")
    
    # Day Master
    st.markdown("### 👤 Day Master (日主)")
    
    st.markdown("""
    Your **Day Master** is the Heavenly Stem of your Day Pillar. It represents YOU.
    
    The 10 Day Masters:
    """)
    
    dm_data = [
        ("Jia 甲", "Yang Wood", "Leader, pioneer, growth-oriented"),
        ("Yi 乙", "Yin Wood", "Flexible, artistic, adaptable"),
        ("Bing 丙", "Yang Fire", "Radiant, generous, optimistic"),
        ("Ding 丁", "Yin Fire", "Warm, nurturing, detail-oriented"),
        ("Wu 戊", "Yang Earth", "Stable, reliable, protective"),
        ("Ji 己", "Yin Earth", "Nurturing, practical, resourceful"),
        ("Geng 庚", "Yang Metal", "Direct, decisive, justice-focused"),
        ("Xin 辛", "Yin Metal", "Refined, perfectionist, aesthetic"),
        ("Ren 壬", "Yang Water", "Wise, flowing, philosophical"),
        ("Gui 癸", "Yin Water", "Intuitive, sensitive, adaptive"),
    ]
    
    for name, element, traits in dm_data:
        element_word = element.split()[1].lower()
        st.markdown(f"""
        <div class="term-card">
            <span class="term-name">{name}</span>
            <span class="element-badge {element_word}">{element}</span>
            <div style="color: #888; margin-top: 0.3rem;">{traits}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Useful Gods
    st.markdown("### 💎 Useful Gods (用神)")
    
    st.markdown("""
    Based on your Day Master's strength, certain elements become **favorable** (Useful Gods) 
    and others become **unfavorable** (忌神).
    
    **General Rules:**
    - **Weak Day Master** → Needs elements that support/produce it
    - **Strong Day Master** → Needs elements that drain/control it
    
    In QMDJ, palaces with your Useful God element are more favorable for you!
    """)

# TAB 3: How to Use
with tab3:
    st.subheader("📖 How to Use Ming Qimen")
    
    st.markdown("### 🚀 Quick Start Guide")
    
    st.markdown("""
    <div class="guide-card">
        <div class="guide-title">Step 1: Set Up Your BaZi Profile</div>
        <ol>
            <li>Go to <strong>BaZi Calculator</strong> page</li>
            <li>Enter your birth date and time</li>
            <li>Click "Calculate My BaZi"</li>
            <li>Click "Save to Profile"</li>
        </ol>
        <p style="color: #888;">This helps personalize your QMDJ readings based on your Useful Gods.</p>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">Step 2: Generate a QMDJ Chart</div>
        <ol>
            <li>Go to <strong>Chart Generator</strong> page</li>
            <li>Select date and time for your question</li>
            <li>Click "Generate Chart"</li>
            <li>Review the 9-palace grid and indicators</li>
        </ol>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">Step 3: Analyze a Palace</div>
        <ol>
            <li>Click on any palace in the grid</li>
            <li>Review the Star, Door, and Deity</li>
            <li>Check special indicators (Lead, Horse, Noble, Empty)</li>
            <li>See BaZi alignment if profile is set</li>
        </ol>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">Step 4: Export for AI Analysis</div>
        <ol>
            <li>Go to <strong>Export Center</strong></li>
            <li>Copy the JSON or Analysis Prompt</li>
            <li>Paste into Claude (Project 1) for deep analysis</li>
            <li>Receive detailed interpretation and recommendations</li>
        </ol>
    </div>
    
    <div class="guide-card">
        <div class="guide-title">Step 5: Track Outcomes</div>
        <ol>
            <li>Save the DB Row to your database</li>
            <li>After taking action, update the Outcome</li>
            <li>Review patterns in History page</li>
            <li>Learn from successes and failures</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Reading Tips")
    
    st.markdown("""
    **For General Questions:**
    - Use the **Center Palace (5)** as your focus
    
    **For Career/Business:**
    - Use **Palace 1 (Kan)** - Career sector
    
    **For Wealth/Money:**
    - Use **Palace 4 (Xun)** - Wealth sector
    
    **For Relationships:**
    - Use **Palace 2 (Kun)** - Relationship sector
    
    **Always Check:**
    - ⭐ Lead Palace for authority
    - 💀 Empty palaces for reduced energy
    - 👑 Nobleman for helpful people
    - 🐴 Horse Star for fast results
    """)

# TAB 4: Glossary
with tab4:
    st.subheader("📚 Glossary of Terms")
    
    terms = [
        ("Qi Men Dun Jia", "奇门遁甲", "Ancient Chinese metaphysical system for strategic forecasting"),
        ("BaZi", "八字", "Four Pillars of Destiny - Chinese astrology based on birth time"),
        ("Day Master", "日主", "The Heavenly Stem of your Day Pillar - represents you"),
        ("Useful God", "用神", "Elements that are favorable for your chart"),
        ("Luo Shu", "洛书", "The magic square arrangement of 9 palaces"),
        ("Yang Dun", "阳遁", "Yang structure - used Winter Solstice to Summer Solstice"),
        ("Yin Dun", "阴遁", "Yin structure - used Summer Solstice to Winter Solstice"),
        ("Ju", "局", "Structure number (1-9) determining palace rotations"),
        ("Chai Bu", "拆补", "The calculation method used (most accurate)"),
        ("Lead Stem", "值符", "The palace where Jia is hidden - command center"),
        ("Lead Door", "直使", "The envoy door governing the hour"),
        ("Death & Emptiness", "空亡", "Empty branches with diminished energy"),
        ("Horse Star", "驿马", "Travel and mobility indicator"),
        ("Nobleman", "贵人", "Helpful people indicator"),
        ("Ten Gods", "十神", "The 10 relationship types between elements in BaZi"),
        ("Hidden Stems", "藏干", "Stems hidden within Earthly Branches"),
        ("Wealth Vault", "财库", "Special structure indicating wealth potential"),
    ]
    
    search = st.text_input("🔍 Search terms...")
    
    for english, chinese, definition in terms:
        if search.lower() in english.lower() or search in chinese or search.lower() in definition.lower() or not search:
            st.markdown(f"""
            <div class="term-card">
                <span class="term-name">{english}</span>
                <span class="term-chinese">{chinese}</span>
                <div style="color: #888; margin-top: 0.3rem;">{definition}</div>
            </div>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ❓ Help")
    st.markdown("Learn the fundamentals of Chinese metaphysics")
    
    st.markdown("---")
    st.markdown("### 📖 Quick Links")
    
    if st.button("📊 Chart Generator", use_container_width=True):
        st.switch_page("pages/1_Chart.py")
    
    if st.button("🎂 BaZi Calculator", use_container_width=True):
        st.switch_page("pages/6_BaZi.py")
    
    st.markdown("---")
    st.markdown("### 📚 External Resources")
    st.markdown("""
    - Joey Yap Academy
    - Qi Men Dun Jia books
    - BaZi reference materials
    """)

st.markdown("---")
st.caption("🌟 Ming Qimen 明奇门 | Help & Guide v6.0")
