# Ming QiMenDunJia 明奇门遁甲 - Project State

## Current Version: v8.0 (Hybrid Architecture)

**Repository:** github.com/Espivc/ming-qimendunjia  
**Live URL:** ming-qimendunjia-3mhmafdxmktvzckeugjm9b.streamlit.app  
**Last Update:** 2025-12-30

---

## 🏗️ TWO-PROJECT ARCHITECTURE (HYBRID)

```
┌─────────────────────────────────────────────────────────────┐
│              PROJECT 2: MING QIMENDUNJIA (App)              │
│                    "Developer Engine"                        │
├─────────────────────────────────────────────────────────────┤
│  HYBRID - Useful Quick Insights                             │
│  • Chart calculations & data generation                     │
│  • Scores with BRIEF explanations (why this score)          │
│  • Formation detection + names shown                        │
│  • Component archetypes + strengths/challenges              │
│  • Door meanings, indicator insights                        │
│  • "Analyze with AI" button for deep analysis               │
└──────────────────────────┬──────────────────────────────────┘
                           │ Copy Prompt / Export
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              PROJECT 1: CLAUDE AI ANALYST                   │
│                    "Analyst Engine"                          │
├─────────────────────────────────────────────────────────────┤
│  DEEP - Full Personalized Analysis                          │
│  • Complete archetype interpretation                        │
│  • Life path guidance & career insights                     │
│  • Personalized strategy based on BaZi                      │
│  • Book cross-references (#64, #71, #73)                    │
│  • Formation meanings & synthesis                           │
│  • Actionable recommendations                               │
└─────────────────────────────────────────────────────────────┘
```

### Design Principle (Option C - Hybrid)

> **App shows WHAT + brief WHY** (useful standalone insights)  
> **Claude provides DEEP WHY** (personalized, contextual, book references)

App is useful on its own for quick decisions. 
AI analysis adds depth for important decisions.

---

## v8.0 Features

### 1. Formation Database (core/formations.py) ✅
- **53 formations** with detection logic
- Categories: Auspicious (21), Inauspicious (20), Neutral (7), Special (5)
- Auto-detection from palace components
- Scoring system (-3 to +3)
- Schema v2.0 export format
- **Note:** Detection logic only, interpretation in Project 1

### 2. Strategic Execution (pages/7_Strategic.py) ✅ HYBRID
**App provides:**
- Hour scores with brief explanations (why good/bad)
- Door meanings shown (e.g., "Open Door favors business")
- Formation names displayed (not just counts)
- Direction compass with insights
- Indicator explanations (Horse Star, Nobleman, D&E)

**AI provides (via prompt):**
- Full strategic interpretation
- Formation meanings & synthesis
- Personalized BaZi recommendations
- #71 Sun Tzu QMDJ principles
- Detailed timing strategy

### 3. QMDJ Destiny (pages/8_Destiny.py) ✅ HYBRID
**App provides:**
- Natal Star with archetype + strengths/challenges
- Natal Door with life theme + gifts
- Natal Deity with brief blessing description
- Birth palace position in 9 Palace grid
- Formation names if present

**AI provides (via prompt):**
- Complete archetype deep-dive
- Life path and career guidance
- Component interaction analysis
- Challenges to navigate
- BaZi comparison (if profile set)

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

## User Workflow (Hybrid)

### Quick Decisions (App Standalone)
1. Open Strategic/Destiny mode
2. Enter parameters
3. Get scores + brief explanations
4. See archetypes, strengths, challenges
5. Make informed quick decision

### Important Decisions (App + AI)
1. Complete analysis in app
2. Click "Copy Analysis Prompt" / "Copy Full Reading Prompt"
3. Paste to Claude (Project 1)
4. Receive deep personalized interpretation
5. Get book references, detailed strategy, BaZi synthesis

---

## Version History

### v8.0 (Current - Hybrid Architecture)
- [x] Formation database (53 formations)
- [x] Strategic Execution mode (hybrid - useful + AI prompt)
- [x] QMDJ Destiny mode (hybrid - insights + AI prompt)
- [x] "Analyze with AI" button workflow
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
