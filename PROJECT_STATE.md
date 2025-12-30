# Ming QiMenDunJia 明奇门遁甲 - Project State

## Current Version: v8.0 (Tiered Architecture)

**Repository:** github.com/Espivc/ming-qimendunjia  
**Live URL:** ming-qimendunjia-3mhmafdxmktvzckeugjm9b.streamlit.app  
**Last Update:** 2025-12-30

---

## 🏗️ TWO-PROJECT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│              PROJECT 2: MING QIMENDUNJIA (App)              │
│                    "Developer Engine"                        │
├─────────────────────────────────────────────────────────────┤
│  QUICK TIER - Shows WHAT                                    │
│  • Chart calculations & data generation                     │
│  • Scores, rankings, verdicts (1-10)                        │
│  • Indicator flags (formations, D&E, Horse, Nobleman)       │
│  • Component labels (Star/Door/Deity names + elements)      │
│  • JSON export for deep analysis                            │
└──────────────────────────┬──────────────────────────────────┘
                           │ Export JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              PROJECT 1: CLAUDE AI ANALYST                   │
│                    "Analyst Engine"                          │
├─────────────────────────────────────────────────────────────┤
│  DEEP TIER - Explains WHY                                   │
│  • Full interpretation & meaning                            │
│  • Personalized strategy based on BaZi                      │
│  • Book cross-references (#64, #71, #73)                    │
│  • Formation analysis & synthesis                           │
│  • Life guidance & recommendations                          │
└─────────────────────────────────────────────────────────────┘
```

### Design Principle

> **App answers WHAT** (quick, mobile, offline)  
> **Claude answers WHY** (deep, personalized, contextual)

This avoids duplication between Project 1 and Project 2.

---

## v8.0 Features

### 1. Formation Database (core/formations.py) ✅
- **53 formations** with detection logic
- Categories: Auspicious (21), Inauspicious (20), Neutral (7), Special (5)
- Auto-detection from palace components
- Scoring system (-3 to +3)
- Schema v2.0 export format
- **Note:** Detection logic only, interpretation in Project 1

### 2. Strategic Execution (pages/7_Strategic.py) ✅ TIERED
**Quick Tier (App):**
- Scan 12 hours, show scores 1-10
- Golden Hour highlight
- Best/Avoid hour rankings
- Direction compass with verdicts
- Indicator flags (📜 formations, 💀 D&E, 🐴 Horse, 👑 Nobleman, 🎴 BaZi)

**Deep Tier (Export to Claude):**
- WHY each hour scored as it did
- Formation meanings
- Personalized strategy
- #71 Sun Tzu references

### 3. QMDJ Destiny (pages/8_Destiny.py) ✅ TIERED
**Quick Tier (App):**
- Birth palace position in 9 Palace grid
- Natal Star, Door, Deity names
- Element and brief labels
- Formation names (if any)

**Deep Tier (Export to Claude):**
- Full archetype explanation
- Life path interpretation
- Strengths & challenges
- Personalized guidance
- BaZi comparison

### 4. Feng Shui Mode (pages/9_FengShui.py) ✅ PLACEHOLDER
- Coming soon page

---

## Project Structure

```
ming-qimendunjia/
├── app.py                    # Main entry point
├── requirements.txt          # Dependencies
├── PROJECT_STATE.md          # This file
├── .streamlit/
│   └── config.toml          # Theme config
├── core/
│   ├── __init__.py          # Module exports (v8.0)
│   ├── qmdj_engine.py       # QMDJ calculations
│   ├── bazi_calculator.py   # BaZi calculations
│   └── formations.py        # Formation database (v8.0)
└── pages/
    ├── 1_Chart.py           # Chart generator
    ├── 2_Export.py          # JSON/CSV export
    ├── 3_History.py         # Chart history
    ├── 4_Settings.py        # User profile/BaZi
    ├── 5_Help.py            # Help documentation
    ├── 6_BaZi.py            # BaZi calculator
    ├── 7_Strategic.py       # Strategic Execution (v8.0)
    ├── 8_Destiny.py         # QMDJ Destiny (v8.0)
    └── 9_FengShui.py        # Feng Shui placeholder (v8.0)
```

---

## User Workflow

### Quick Analysis (Mobile/Offline)
1. Open app → Select mode (Strategic/Destiny)
2. Enter parameters (date/birth info)
3. Get scores, rankings, indicators
4. Make quick decisions

### Deep Analysis (Full Interpretation)
1. Complete Quick Analysis
2. Click "Export JSON"
3. Paste JSON to Claude (Project 1)
4. Ask: "Analyze this and explain why..."
5. Receive personalized interpretation with book references

---

## Version History

### v8.0 (Current - Tiered Architecture)
- [x] Formation database (53 formations)
- [x] Strategic Execution mode (Quick tier)
- [x] QMDJ Destiny mode (Quick tier)
- [x] Export to AI Analyst workflow
- [x] Feng Shui placeholder
- [ ] Integration with Chart page
- [ ] Export with formation data

### v6.0 (Live)
- Complete QMDJ engine
- BaZi calculator integration
- Death & Emptiness, Horse Star, Nobleman
- Lead Stem/Door/Star indicators
- Chart history tracking
- JSON/CSV export

---

## Deployment

### Files to add for v8.0:
```
core/formations.py        # NEW
core/__init__.py         # UPDATE
pages/7_Strategic.py     # NEW
pages/8_Destiny.py       # NEW
pages/9_FengShui.py      # NEW
PROJECT_STATE.md         # UPDATE
```

### Deploy Steps:
1. Backup current live version
2. Copy files to repository
3. Push to GitHub
4. Reboot Streamlit Cloud if needed

---

## Integration Tasks (v8.1)

1. **Update 1_Chart.py:**
   - Add formation detection display
   - Show formation score in summary

2. **Update 2_Export.py:**
   - Include formation data in JSON
   - Add formation_score to DB_ROW

---

## Contact

Project: Ming QiMenDunJia  
Mission: "Helping people first" with Chinese metaphysics
